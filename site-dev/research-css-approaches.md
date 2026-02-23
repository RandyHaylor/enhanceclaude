# CSS/Styling Approaches for a Single-File Static Site

## 1. Tailwind Play CDN — Production Viability

**Verdict: NOT suitable for production.**

- The Play CDN is explicitly "designed for development purposes only" per [Tailwind's own docs](https://tailwindcss.com/docs/installation/play-cdn).
- It ships the full Tailwind runtime as a JS file (~300KB+) and JIT-compiles CSS in the browser at runtime.
- This means: large download, CPU burn on every page load, no caching of a static CSS file, and a flash of unstyled content.
- A properly tree-shaken Tailwind build produces **<10KB of CSS** even for large projects ([source](https://medium.com/@sureshdotariya/tailwind-css-4-performance-checklist-for-2025-apps-build-fast-tiny-and-scalable-7fc14ea58c89)).
- **Bottom line**: Fine for prototyping. Must be replaced before shipping.

## 2. Tailwind Standalone CLI — Pre-built CSS

**Best path if we want to keep Tailwind utility classes.**

- Tailwind offers a [standalone CLI](https://tailwindcss.com/blog/standalone-cli) — a single binary, no Node.js/npm required.
- Workflow: write HTML with Tailwind classes, run `./tailwindcss -i input.css -o output.css --minify`, ship `output.css` alongside `index.html`.
- Output is a static, minified CSS file containing only the classes actually used.
- Result: tiny cacheable CSS file (~5-10KB typical), zero runtime JS, perfect Lighthouse scores.
- Tailwind v4 builds are [up to 5x faster](https://tailwindcss.com/blog/tailwindcss-v4) than v3.
- **Trade-off**: Requires a build step (even if trivial). Not truly "edit and deploy" without running a command.

## 3. Modern CSS — Can It Replace Tailwind?

**Yes, for a simple site like this. Modern CSS is very capable now.**

- **CSS Nesting**: Shipped in all major browsers. Eliminates need for Sass/preprocessors ([Builder.io overview](https://www.builder.io/blog/css-2024-nesting-layers-container-queries)).
- **`:has()` selector**: Parent selector, widely supported. Enables complex UI states without JS.
- **Container Queries**: Style based on parent size, not viewport. Great for component-level responsiveness.
- **`@layer`**: Controls cascade order explicitly — replaces the need for Tailwind's layer system.
- **CSS Custom Properties**: Native variables, theming, dark mode — all without a framework.
- For a single-page site with ~20 sections, hand-written modern CSS is arguably **simpler** than maintaining a Tailwind build pipeline. A well-structured `<style>` block in the HTML keeps everything in one file.
- **Trade-off**: No utility-class shorthand. More verbose for layout (e.g., writing `display: flex; gap: 1rem;` instead of `flex gap-4`). But for a single file, this is manageable.

## 4. Lightweight CSS Frameworks

### Pico CSS
- **Size**: ~10KB gzipped ([picocss.com](https://picocss.com)).
- **Approach**: Class-light / classless. Style semantic HTML directly (`<button>` looks good without classes).
- **Dark mode**: Built-in, auto-detects `prefers-color-scheme`. No JS needed.
- **Look**: Clean, modern, slightly opinionated. Good for forms, cards, typography.
- **Verdict**: Strong candidate. Drop a `<link>` tag, write semantic HTML, get a polished dark-mode site.

### Water.css
- **Size**: ~2KB gzipped ([Water.css GitHub](https://github.com/kognise/water.css)).
- **Approach**: Fully classless. Zero configuration.
- **Dark mode**: Built-in light/dark themes.
- **Look**: Minimal, clean. More suited to documentation or simple pages than a branded marketing site.
- **Verdict**: Too minimal for a branded site with custom sections, but excellent for docs pages.

### Open Props
- **Approach**: Not a framework — a set of CSS custom properties (colors, spacing, typography, animations).
- **Size**: Tree-shakeable, use only what you need.
- **Use case**: Pairs well with hand-written CSS. Gives you a design-token system without framework lock-in.
- **Verdict**: Good middle ground — provides consistent design tokens without imposing structure.

### Recommendation for This Project
**Pico CSS + custom overrides** or **hand-written modern CSS with Open Props tokens** are the two strongest options. Both avoid a build step and keep everything in a single file.

## 5. Google Fonts & Material Symbols — Performance

### Google Fonts CDN Issues
- Browser cache partitioning (since ~2020) eliminated the old "shared cache" benefit of Google Fonts CDN.
- Self-hosted fonts are consistently [200-300ms faster](https://medium.com/@ignatovich.dm/local-font-loading-vs-google-fonts-performance-comparison-with-real-data-021a62a763da) than CDN-loaded fonts.
- Privacy concern: Google Fonts CDN sends visitor IPs to Google.

### Self-Hosting Options
- **google-webfonts-helper**: Tool to download Google Fonts as WOFF2 files for self-hosting.
- **Fontsource**: npm packages for every Google Font, optimized for self-hosting.
- For a single-file site: download WOFF2 files, base64-encode them into the CSS `@font-face`, or serve them as separate files.

### Lighter Alternatives
- **Bunny Fonts** ([fonts.bunny.net](https://fonts.bunny.net)): Drop-in Google Fonts replacement, privacy-focused, fast CDN. Same API, just swap the domain.
- **System font stack**: `font-family: system-ui, -apple-system, sans-serif` — zero download, instant rendering. Looks native on every OS.
- **Material Symbols**: Consider replacing with inline SVG icons for the few icons needed. Avoids loading the full icon font (~100KB+). Alternatively, use a subset or the individual SVG downloads from Google.

### Recommendation
- **Body text**: Use system font stack. Zero cost, great readability.
- **Headings/brand font**: Self-host one WOFF2 file (e.g., Inter or Space Grotesk) — ~20KB.
- **Icons**: Inline SVG for the 5-10 icons needed. Skip the full Material Symbols font.

---

## Summary: Recommended Approach

| Option | Build step? | Size | Dark mode | Single-file friendly |
|--------|-------------|------|-----------|---------------------|
| Tailwind Play CDN | No | ~300KB JS | Manual | Yes (but slow) |
| Tailwind CLI build | Yes | ~5-10KB | Manual | Yes |
| Hand-written CSS | No | ~3-8KB | Native | Yes |
| Pico CSS | No | ~10KB | Auto | Yes |
| Pico + custom CSS | No | ~12-15KB | Auto | Yes |

**Top pick for production**: Hand-written modern CSS (with CSS nesting, custom properties, `@layer`) or Pico CSS as a base. Self-host one heading font as WOFF2, use system fonts for body, inline SVGs for icons. No build step, no runtime JS for styling, everything in one file.
