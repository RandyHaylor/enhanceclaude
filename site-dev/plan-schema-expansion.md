# Plan: Expand Tool Schema & Detail View

## Goal
Add `promptSuggestions` and `applications` to tool-info.json schema and render them in the detail expansion panel.

---

## 1. Schema Changes (tool-schema.json)

Add two new optional fields:

```json
"promptSuggestions": {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["title", "prompt"],
    "properties": {
      "title": { "type": "string", "description": "Short label for the prompt (e.g. 'Generate a flowchart')" },
      "prompt": { "type": "string", "description": "The actual prompt text the user can copy/paste" },
      "description": { "type": "string", "description": "Optional context on when/why to use this prompt" }
    }
  },
  "description": "Example prompts that demonstrate how to use this tool effectively"
},
"applications": {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["title"],
    "properties": {
      "title": { "type": "string", "description": "Name of the use case (e.g. 'CI/CD pipeline visualization')" },
      "description": { "type": "string", "description": "How the tool applies to this use case" }
    }
  },
  "description": "Real-world applications and use cases for this tool"
}
```

---

## 2. Detail View Changes (index.html)

In `expandToolCard()`, after the readme section, render two new sections if data exists:

### Prompt Suggestions section
- Header: "Try These Prompts"
- Each prompt rendered as a card with:
  - Title (bold)
  - Description (muted, if present)
  - Prompt text in a code block with a copy button
- Compact, stacked layout inside the detail panel

### Applications section
- Header: "Applications"
- Simple list of application titles with descriptions
- Minimal styling — just title + description pairs

---

## 3. Regenerate tool-info.json Files

Use an agent team to review each tool's actual code/instructions and populate:
- 2-4 prompt suggestions per tool (practical, copy-paste-ready)
- 2-5 applications per tool (real use cases)

---

## 4. Implementation Order

1. Update `tool-schema.json` with new fields
2. Update `expandToolCard()` in index.html to render both sections
3. Add CSS for prompt cards and application list
4. Run agent team to populate all 12 tool-info.json files
5. Test in browser
