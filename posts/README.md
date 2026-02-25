# Blog Posts Directory

Store your blog posts as markdown files in this directory.

## File Naming Convention

Use the format: `YYYY-MM-DD-slug.md`

Example: `2026-02-24-my-first-post.md`

## Front Matter Format

Each post must have YAML front matter at the top:

```yaml
---
title: "Your Post Title"
slug: "url-friendly-slug"
date: 2026-02-24
tags: ["tag1", "tag2"]
excerpt: "A brief summary of your post"
published: true  # Set to false for drafts
---
```

## Writing Posts

After the front matter, write your content in standard Markdown:

```markdown
# Heading 1

Regular paragraph text.

## Heading 2

- List item 1
- List item 2

**Bold text** and *italic text*.

[Link text](https://example.com)

` + "```python\ncode block\n```" + `
```

## Publishing Workflow

1. Create a new `.md` file in `posts/` directory
2. Add front matter with `published: false` for drafts
3. Write your content
4. When ready, set `published: true`
5. The blog service will scan this directory and sync with the database

## Management

- **Drafts**: Set `published: false` in front matter
- **Editing**: Just edit the `.md` file directly
- **Deleting**: Remove the `.md` file (or set `published: false`)

The database stores metadata (title, slug, dates) but the actual content lives in these files.
