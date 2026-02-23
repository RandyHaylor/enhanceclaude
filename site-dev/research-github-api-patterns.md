# GitHub API Patterns for Static HTML (file:// compatible)

Research for fetching public repo data from a static page with no server.

---

## 1. GitHub Contents API

**Endpoint:** `https://api.github.com/repos/{owner}/{repo}/contents/{path}`

- **Rate limits (unauthenticated):** 60 requests/hour per IP address ([docs](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api))
- **Authenticated:** 5,000 requests/hour (requires token, not suitable for public static pages)
- **CORS:** Returns `Access-Control-Allow-Origin: *` — works from any HTTP/HTTPS origin ([docs](https://docs.github.com/en/rest/using-the-rest-api/using-cors-and-jsonp-to-make-cross-origin-requests))
- **file:// origin:** Browsers send `Origin: null` for file:// pages. GitHub's `Access-Control-Allow-Origin: *` wildcard **does** permit `null` origins, so fetch requests work from file:// in most browsers
- **Response format:** JSON with `name`, `path`, `sha`, `size`, `type`, `content` (base64), `download_url`, etc. Directory listings return an array of file objects
- **Content encoding:** File contents are base64-encoded in the `content` field. Use `atob()` to decode. Alternatively, use the `download_url` field to fetch raw content directly

## 2. raw.githubusercontent.com

**URL pattern:** `https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}`

- **CORS:** Returns `Access-Control-Allow-Origin: *` — works from any origin including file:// ([discussion](https://github.com/orgs/community/discussions/69281))
- **Preflight (OPTIONS) requests:** Returns 403 — so only "simple" requests (GET with default headers) work. Do NOT set custom headers like `Authorization` or non-standard `Content-Type`
- **Caching:** `Cache-Control: max-age=300` (5 minutes). `Vary: Authorization,Accept-Encoding,Origin`
- **Content type:** Serves raw file content with appropriate MIME type
- **Reliability:** Highly reliable for public repos, backed by GitHub's CDN (Fastly)
- **Advantage over API:** No rate limit (or at least much more generous), no JSON wrapping, direct file content

## 3. Approaches Compared

### Option A: GitHub Contents API (live)
- **Pros:** Structured JSON, directory listings, file metadata (sha, size), enables dynamic discovery of repo contents
- **Cons:** 60 req/hr unauthenticated limit is very low for a public site, JSON overhead, base64 decoding needed

### Option B: raw.githubusercontent.com (live)
- **Pros:** Direct file content, no rate limit issues, simpler fetch code, works as-is from file://
- **Cons:** No directory listing (must know file paths), no metadata, 5-min cache means updates aren't instant

### Option C: Static JSON manifest (recommended for production)
- **Pros:** Zero API calls, no rate limits, instant loading, works offline, fully controlled content, works perfectly from file://
- **Cons:** Must regenerate manifest when content changes (can automate with GitHub Actions), not real-time
- **How it works:** A build step (GitHub Action or script) generates a `scripts-manifest.json` listing all scripts with metadata. The static page fetches this single file. The manifest is committed to the repo or deployed alongside the site.

### Recommended hybrid approach
1. **Primary:** Ship a static JSON manifest for zero-API-call loading
2. **Fallback:** Use raw.githubusercontent.com to fetch actual script content on demand
3. **Optional:** Use Contents API only for admin/preview tools, never for public-facing pages

## 4. Rate Limit Mitigation

### localStorage caching
```js
const CACHE_KEY = 'gh_scripts_cache';
const CACHE_TTL = 30 * 60 * 1000; // 30 minutes

function getCached(key) {
  const cached = localStorage.getItem(key);
  if (!cached) return null;
  const { data, timestamp } = JSON.parse(cached);
  if (Date.now() - timestamp > CACHE_TTL) {
    localStorage.removeItem(key);
    return null;
  }
  return data;
}

function setCache(key, data) {
  localStorage.setItem(key, JSON.stringify({ data, timestamp: Date.now() }));
}
```

### Conditional requests (ETag)
- GitHub responses include `ETag` header
- Send `If-None-Match: <etag>` on subsequent requests
- 304 responses do NOT count against rate limits **only when authenticated** ([docs](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api))
- For unauthenticated requests, conditional requests still count — so localStorage caching is more valuable
- Store ETags alongside cached data for optimal cache validation

### Rate limit headers
- `X-RateLimit-Remaining` — check before making requests
- `X-RateLimit-Reset` — Unix timestamp when limit resets
- Implement backoff: if remaining < 5, stop making API calls and use cached data

## 5. Error Handling & Fallbacks

| Scenario | HTTP Status | Handling |
|---|---|---|
| Rate limited | 403 + `X-RateLimit-Remaining: 0` | Fall back to cached data or static manifest |
| Repo not found | 404 | Show friendly error, check repo name |
| Server error | 500/502/503 | Retry once after 2s, then fall back to cache |
| Network offline | fetch throws | Serve from localStorage cache |
| CORS blocked | TypeError | Should not happen with `*` header, but fall back to manifest |

### Fallback chain pattern
```js
async function loadScripts() {
  // 1. Try localStorage cache first
  const cached = getCached('scripts');
  if (cached) return cached;

  // 2. Try static manifest (co-located JSON file)
  try {
    const manifest = await fetch('scripts-manifest.json');
    if (manifest.ok) return await manifest.json();
  } catch (e) { /* continue to fallback */ }

  // 3. Try GitHub API as last resort
  try {
    const resp = await fetch('https://api.github.com/repos/OWNER/REPO/contents/scripts');
    if (resp.ok) {
      const data = await resp.json();
      setCache('scripts', data);
      return data;
    }
  } catch (e) { /* all sources failed */ }

  return { error: 'Unable to load scripts. Please try again later.' };
}
```

---

**Bottom line:** For a public static site, avoid relying on the GitHub API at runtime. Use a static manifest as the primary data source, raw.githubusercontent.com for fetching file contents, and the API only as a fallback or for tooling.
