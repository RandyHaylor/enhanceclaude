# Vanilla JS Patterns for Dynamic Single-Page Sites

Research for enhanceclaude.com single-file site that fetches JSON from GitHub and renders filterable cards.

---

## 1. Templating: Template Literals + innerHTML Wins

**Recommendation: Template literals with `innerHTML`** — cleanest and most common pattern.

- **Template literals + innerHTML**: Build HTML string in a loop, inject once. Readable, fast, minimal boilerplate.
  ```js
  let html = '';
  for (const item of items) {
    html += `<div class="card"><h3>${item.name}</h3><p>${item.desc}</p></div>`;
  }
  container.innerHTML = html;
  ```
- **`<template>` + cloneNode**: Native HTML element designed for reuse. Requires `cloneNode(true)` then multiple `querySelector()` calls to fill in data — verbose and cumbersome for dynamic lists. Better suited for static repeated structures.
- **DOM creation (createElement)**: Most control, avoids innerHTML XSS risks, but very verbose for card layouts. Not worth it for trusted data from your own GitHub repo.
- **XSS caveat**: If rendering user-supplied or third-party data, sanitize before innerHTML. For our case (our own JSON from GitHub), template literals are safe.

Sources: [Go Make Things - HTML Templates](https://gomakethings.com/html-templates-with-vanilla-javascript/), [John Papa - Vanilla JS and HTML](https://www.johnpapa.net/render-html-2/)

---

## 2. Web Components: Overkill for This Use Case

- Native custom elements (`class extends HTMLElement`) provide encapsulation via Shadow DOM and lifecycle callbacks (`connectedCallback`, `disconnectedCallback`).
- **Pros**: Reusable, framework-agnostic, standards-based, good for design systems.
- **Cons**: Verbose boilerplate for simple card rendering. Shadow DOM complicates global CSS styling. No SSR benefit for a client-rendered single file. Bundle overhead for small UI.
- **Verdict**: Skip for this project. Plain render functions with template literals are simpler and sufficient. Web Components shine in multi-page or multi-app contexts, not a single-file card renderer.

Sources: [MDN - Custom Elements](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements), [Smashing Magazine - Web Components vs Framework Components](https://www.smashingmagazine.com/2025/03/web-components-vs-framework-components/), [Zach Leat - Good Bad Web Components](https://www.zachleat.com/web/good-bad-web-components/)

---

## 3. Client-Side Filtering & Search

**Core pattern**: Query all cards, test text content against input, toggle visibility class.

```js
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', () => {
  const query = searchInput.value.toLowerCase();
  document.querySelectorAll('.card').forEach(card => {
    const match = card.textContent.toLowerCase().includes(query);
    card.classList.toggle('is-hidden', !match);
  });
});
```

**Category filtering** (buttons/tabs): Same pattern but check a data attribute.
```js
function filterByType(type) {
  document.querySelectorAll('.card').forEach(card => {
    const show = type === 'all' || card.dataset.type === type;
    card.classList.toggle('is-hidden', !show);
  });
}
```

**Combine both**: Run search filter AND type filter together. Keep state in simple variables, re-filter on either change.

**Performance**: Add debounce (200-300ms) on search input for large lists. For <100 cards, not needed.

```css
.is-hidden { display: none; }
```

Sources: [CSS-Tricks - In-Page Filtered Search](https://css-tricks.com/in-page-filtered-search-with-vanilla-javascript/), [Section.io - Filtered Search](https://www.section.io/engineering-education/in-page-filtered-search-with-vanilla-javascript/)

---

## 4. Modern Vanilla JS Patterns (2025-2026)

New browser APIs that reduce need for JS frameworks:

- **Popover API** (`popover` attribute): Native tooltips/modals with light-dismiss, focus trapping, top-layer rendering. No JS needed for basic use. Good for script detail pop-ups.
- **Declarative Shadow DOM** (`<template shadowrootmode="open">`): Server-renderable shadow DOM without JS. Works even with JS disabled. Useful if we ever want encapsulated components, but overkill for our current scope.
- **View Transitions API**: Smooth animated transitions between DOM states. Could enhance card filtering animations with minimal code.
- **CSS `:has()` selector**: Parent selection in CSS. Can drive filter UI states without JS (e.g., `form:has(input:checked) ~ .card`).
- **Dialog element**: Native modal with `showModal()` / `show()`. Better than custom modal divs.
- **`structuredClone()`**: Deep clone objects without JSON.parse/stringify hack. Useful for immutable state patterns.

Sources: [Chrome Blog - New in Web UI I/O 2025](https://developer.chrome.com/blog/new-in-web-ui-io-2025-recap), [OpenReplay - Trust Web Primitives](https://blog.openreplay.com/beneath-frameworks-trust-web-primitives/), [MDN - Popover API](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/popover)

---

## 5. Reference Examples

1. **[vanilla-js-single-page-app](https://github.com/managervcf/vanilla-js-single-page-app)** — Zero-dependency SPA using ES6 template literals, async fetch, client-side routing. Good architecture reference.
2. **[renderjson](https://github.com/caldwell/renderjson)** — Tiny lib that renders JSON into collapsible HTML. Shows clean DOM generation pattern from JSON input.
3. **[CSS-Tricks filtered search demo](https://css-tricks.com/in-page-filtered-search-with-vanilla-javascript/)** — Complete working example of card filtering with vanilla JS. Closest to our use case.

---

## Recommended Approach for enhanceclaude.com

1. **Fetch JSON** from GitHub raw URL with `fetch()` + `async/await`
2. **Render cards** using template literals + `innerHTML` (single render function)
3. **Filter by type** using `data-type` attributes + button click handlers
4. **Search by text** using `input` event + `textContent.includes()`
5. **Combine filters** by re-running both checks on any filter change
6. **Use native Popover API** if we need detail pop-ups
7. **Keep it in one file** — no build step, no modules, no dependencies
