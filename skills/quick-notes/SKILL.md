---
name: quick-notes
description: Create or append quick Markdown notes in a simple, consistent format. Use when the user asks to jot something down, capture a short note, save a thought, write a scratch note, or maintain lightweight notes without building a full document system.
---

# Quick Notes

Create short Markdown notes fast and keep formatting consistent.

## Workflow

1. Clarify the target note file if the user did not specify one.
2. Default to a workspace-local `.md` file with a simple descriptive name.
3. If the file does not exist, create it with a clear title heading.
4. Append new notes as bullet points or short dated sections.
5. Preserve existing content unless the user explicitly asks to rewrite or reorganize it.

## Format

Use a lightweight structure:

```markdown
# Note Title

## YYYY-MM-DD
- item one
- item two
```

Use bullets for short captures. Use a dated section when adding notes across multiple sessions.

## Style Rules

- Keep notes terse and scannable.
- Prefer plain Markdown.
- Do not add long introductions or summaries unless asked.
- Do not invent metadata fields.
- If the user gives raw text, preserve their wording as much as possible.

## File Handling

- Create files inside the current workspace unless the user specifies another path.
- Use descriptive lowercase hyphenated filenames when choosing a new file name.
- Append instead of overwrite by default.
- If restructuring a messy note, keep the original meaning and ordering unless the user asks for cleanup.

## References

Read `references/examples.md` when you need concrete note patterns.
