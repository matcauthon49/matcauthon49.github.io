# Short Stories Site

This website is generated from Markdown files.

## Add a new story

1. Create a new file in `content/stories/` with a `.md` extension.
2. Add frontmatter at the top:

```md
---
title: Your Story Title
slug: your-story-title
order: 4
excerpt: One sentence used on the homepage list.
---
```

3. Write your story below the frontmatter in Markdown.
4. Run:

```bash
python3 scripts/build_site.py
```

Your story page will be generated at `stories/<slug>.html`, and the homepage list in `index.html` will update automatically.

## Draft stories

Set `draft: true` in frontmatter to skip publishing while you are writing.
