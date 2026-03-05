from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


SITE_TITLE = "short stories"
SITE_SUBTITLE = "by Naman Kumar"
SITE_HEAD_TITLE = "Naman Kumar | Short Stories"
SITE_DESCRIPTION = (
	"Short stories by Naman Kumar."
)
FOOTER_TEXT = "&copy; Naman Kumar. All rights reserved."

ROOT_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT_DIR / "content" / "stories"
STORIES_DIR = ROOT_DIR / "stories"
INDEX_FILE = ROOT_DIR / "index.html"


@dataclass
class Story:
	title: str
	slug: str
	excerpt: str
	order: int
	body_html: str
	is_draft: bool


def main() -> None:
	CONTENT_DIR.mkdir(parents=True, exist_ok=True)
	STORIES_DIR.mkdir(parents=True, exist_ok=True)

	markdown_files = sorted(CONTENT_DIR.glob("*.md"), key=lambda item: item.name.lower())
	stories: list[Story] = []

	for file_path in markdown_files:
		raw = file_path.read_text(encoding="utf-8")
		meta, body = parse_front_matter(raw)
		is_draft = is_truthy(meta.get("draft", ""))

		default_slug = slugify(file_path.stem)
		title = meta.get("title") or infer_title(body) or humanize_slug(default_slug)
		slug = slugify(meta.get("slug", default_slug))
		excerpt = meta.get("excerpt") or extract_excerpt(body)
		order = parse_order(meta.get("order"))

		stories.append(
			Story(
				title=title,
				slug=slug,
				excerpt=excerpt,
				order=order,
				body_html=markdown_to_html(body),
				is_draft=is_draft,
			)
		)

	validate_unique_slugs(stories)
	stories.sort(key=lambda story: (story.order, story.title.lower()))
	published_stories = [story for story in stories if not story.is_draft]
	draft_stories = [story for story in stories if story.is_draft]

	expected_html_files = {f"{story.slug}.html" for story in stories}
	for existing_file in STORIES_DIR.glob("*.html"):
		if existing_file.name not in expected_html_files:
			existing_file.unlink()

	for index, story in enumerate(stories):
		output_file = STORIES_DIR / f"{story.slug}.html"
		output_file.write_text(
			render_story_page(story),
			encoding="utf-8",
		)

	INDEX_FILE.write_text(render_index_page(published_stories, draft_stories), encoding="utf-8")

	count = len(stories)
	published_count = len(published_stories)
	draft_count = len(draft_stories)
	noun = "story" if count == 1 else "stories"
	print(f"Built {count} {noun} ({published_count} published, {draft_count} drafts).")


def parse_front_matter(raw_text: str) -> tuple[dict[str, str], str]:
	text = raw_text.replace("\r\n", "\n")
	match = re.match(r"^---\n([\s\S]*?)\n---\n?([\s\S]*)$", text)

	if not match:
		return {}, text.strip()

	front_matter, body = match.groups()
	meta: dict[str, str] = {}

	for line in front_matter.split("\n"):
		pair = re.match(r"^([a-zA-Z0-9_-]+)\s*:\s*(.*)$", line.strip())
		if not pair:
			continue

		key = pair.group(1).lower()
		value = strip_wrapping_quotes(pair.group(2).strip())
		meta[key] = value

	return meta, body.strip()


def strip_wrapping_quotes(value: str) -> str:
	if (value.startswith('"') and value.endswith('"')) or (
		value.startswith("'") and value.endswith("'")
	):
		return value[1:-1]

	return value


def is_truthy(value: str) -> bool:
	if not value:
		return False

	return value.lower() in {"1", "true", "yes", "y"}


def parse_order(value: str | None) -> int:
	if value is None:
		return 2_147_483_647

	try:
		return int(value)
	except ValueError:
		return 2_147_483_647


def validate_unique_slugs(stories: list[Story]) -> None:
	seen: set[str] = set()

	for story in stories:
		if story.slug in seen:
			raise ValueError(f"Duplicate slug found: {story.slug}")

		seen.add(story.slug)


def infer_title(markdown: str) -> str:
	match = re.search(r"^#\s+(.+)$", markdown, flags=re.MULTILINE)
	if not match:
		return ""

	return strip_markdown(match.group(1))


def extract_excerpt(markdown: str) -> str:
	for line in markdown.replace("\r\n", "\n").split("\n"):
		trimmed = line.strip()
		if not trimmed:
			continue

		if (
			re.match(r"^#{1,6}\s+", trimmed)
			or re.match(r"^[-*+]\s+", trimmed)
			or re.match(r"^\d+\.\s+", trimmed)
			or re.match(r"^>\s+", trimmed)
			or re.match(r"^```", trimmed)
		):
			continue

		plain = strip_markdown(trimmed)
		if plain:
			return truncate(plain, 150)

	return "Read story"


def truncate(text: str, max_length: int) -> str:
	if len(text) <= max_length:
		return text

	return f"{text[: max_length - 3].rstrip()}..."


def strip_markdown(text: str) -> str:
	output = text
	output = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", output)
	output = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", output)
	output = re.sub(r"`([^`]+)`", r"\1", output)
	output = re.sub(r"\*\*([^*]+)\*\*", r"\1", output)
	output = re.sub(r"\*([^*]+)\*", r"\1", output)
	output = re.sub(r"^>\s+", "", output)
	output = re.sub(r"^#{1,6}\s+", "", output)
	return output.strip()


def slugify(input_value: str) -> str:
	base = str(input_value).lower().strip()
	base = re.sub(r"[\"']", "", base)
	base = re.sub(r"[^a-z0-9]+", "-", base)
	base = re.sub(r"^-+|-+$", "", base)
	return base or "story"


def humanize_slug(slug: str) -> str:
	words = [word for word in slug.split("-") if word]
	return " ".join(word[0].upper() + word[1:] for word in words)


def markdown_to_html(markdown: str) -> str:
	lines = markdown.replace("\r\n", "\n").split("\n")
	blocks: list[str] = []
	paragraph_lines: list[str] = []
	list_type: str | None = None
	list_items: list[str] = []

	def flush_paragraph() -> None:
		nonlocal paragraph_lines

		if not paragraph_lines:
			return

		paragraph = " ".join(paragraph_lines).strip()
		if paragraph:
			blocks.append(f"<p>{render_inline(paragraph)}</p>")

		paragraph_lines = []

	def flush_list() -> None:
		nonlocal list_type, list_items

		if not list_type or not list_items:
			return

		items = "\n".join(f"  <li>{render_inline(item)}</li>" for item in list_items)
		blocks.append(f"<{list_type}>\n{items}\n</{list_type}>")

		list_type = None
		list_items = []

	index = 0
	while index < len(lines):
		trimmed = lines[index].strip()

		if not trimmed:
			flush_paragraph()
			flush_list()
			index += 1
			continue

		if trimmed.startswith("```"):
			flush_paragraph()
			flush_list()

			language = trimmed[3:].strip()
			code_lines: list[str] = []
			index += 1

			while index < len(lines) and not lines[index].strip().startswith("```"):
				code_lines.append(lines[index])
				index += 1

			language_class = f' class="language-{escape_html_attribute(language)}"' if language else ""
			code_html = escape_html("\n".join(code_lines))
			blocks.append(f"<pre><code{language_class}>{code_html}</code></pre>")

			index += 1
			continue

		heading = re.match(r"^(#{1,6})\s+(.*)$", trimmed)
		if heading:
			flush_paragraph()
			flush_list()

			level = len(heading.group(1))
			blocks.append(f"<h{level}>{render_inline(heading.group(2))}</h{level}>")
			index += 1
			continue

		if re.match(r"^---+$", trimmed):
			flush_paragraph()
			flush_list()
			blocks.append("<hr />")
			index += 1
			continue

		block_quote = re.match(r"^>\s+(.*)$", trimmed)
		if block_quote:
			flush_paragraph()
			flush_list()
			blocks.append(f"<blockquote><p>{render_inline(block_quote.group(1))}</p></blockquote>")
			index += 1
			continue

		unordered_item = re.match(r"^[-*+]\s+(.*)$", trimmed)
		if unordered_item:
			flush_paragraph()

			if list_type and list_type != "ul":
				flush_list()

			list_type = "ul"
			list_items.append(unordered_item.group(1))
			index += 1
			continue

		ordered_item = re.match(r"^\d+\.\s+(.*)$", trimmed)
		if ordered_item:
			flush_paragraph()

			if list_type and list_type != "ol":
				flush_list()

			list_type = "ol"
			list_items.append(ordered_item.group(1))
			index += 1
			continue

		flush_list()
		paragraph_lines.append(trimmed)
		index += 1

	flush_paragraph()
	flush_list()
	return "\n".join(blocks)


def render_inline(text: str) -> str:
	output = escape_html(text)

	output = re.sub(r"`([^`]+)`", r"<code>\1</code>", output)
	output = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", output)
	output = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", output)

	def replace_link(match: re.Match[str]) -> str:
		label = match.group(1)
		href = sanitize_href(match.group(2))
		return f'<a href="{escape_html_attribute(href)}">{label}</a>'

	output = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, output)
	return output


def sanitize_href(href: str) -> str:
	cleaned = href.strip()
	if re.match(r"^(https?://|mailto:|\.{1,2}/|/|#)", cleaned, flags=re.IGNORECASE):
		return cleaned
	return "#"


def escape_html(value: str) -> str:
	return (
		str(value)
		.replace("&", "&amp;")
		.replace("<", "&lt;")
		.replace(">", "&gt;")
		.replace('"', "&quot;")
		.replace("'", "&#39;")
	)


def escape_html_attribute(value: str) -> str:
	return escape_html(value).replace("`", "&#96;")


def render_story_list_items(stories: list[Story], *, animate: bool, empty_text: str) -> str:
	if not stories:
		return f'            <li class="story-item"><p>{escape_html(empty_text)}</p></li>'

	list_items: list[str] = []

	for index, story in enumerate(stories):
		delay_class = f" delay-{index + 1}" if animate and index < 3 else ""
		item_html = "\n".join(
			[
				f'            <li class="story-item{delay_class}">',
				f'              <a class="story-link" href="stories/{escape_html_attribute(story.slug)}.html">{escape_html(story.title)}</a>',
				f"              <p>{escape_html(story.excerpt)}</p>",
				"            </li>",
			]
		)
		list_items.append(item_html)

	return "\n\n".join(list_items)


def render_index_page(published_stories: list[Story], draft_stories: list[Story]) -> str:
	published_list_html = render_story_list_items(
		published_stories,
		animate=True,
		empty_text="No stories published yet.",
	)
	draft_list_html = render_story_list_items(
		draft_stories,
		animate=False,
		empty_text="No drafts yet.",
	)

	return "\n".join(
		[
			"<!doctype html>",
			'<html lang="en">',
			"  <head>",
			"    <meta charset=\"UTF-8\" />",
			"    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />",
			f"    <title>{escape_html(SITE_HEAD_TITLE)}</title>",
			"    <meta",
			'      name="description"',
			f'      content="{escape_html_attribute(SITE_DESCRIPTION)}"',
			"    />",
			'    <link rel="stylesheet" href="styles.css" />',
			"  </head>",
			"  <body>",
			'    <div class="site-shell fade-in">',
			'      <header class="site-header">',
			f'        <a class="site-title" href="index.html">{escape_html(SITE_TITLE)}</a>',
			f'        <p class="site-subtitle">{escape_html(SITE_SUBTITLE)}</p>',
			"      </header>",
			"",
			"      <main>",
			'        <section class="story-section" aria-label="Stories">',
			'          <ul class="story-list">',
			published_list_html,
			"          </ul>",
			"        </section>",
			'        <section class="story-section" aria-labelledby="drafts-heading">',
			'          <h2 id="drafts-heading">Drafts</h2>',
			'          <ul class="story-list">',
			draft_list_html,
			"          </ul>",
			"        </section>",
			"      </main>",
			"",
			'      <footer class="site-footer">',
			f"        <p>{FOOTER_TEXT}</p>",
			"      </footer>",
			"    </div>",
			"  </body>",
			"</html>",
			"",
		]
	)


def render_story_page(story: Story) -> str:
	nav_html = "\n".join(
		[
			'      <nav class="story-nav story-nav-single" aria-label="Story navigation">',
			'        <a href="../index.html">Back</a>',
			"      </nav>",
		]
	)

	body_html = "\n".join(f"        {line}" for line in story.body_html.split("\n"))

	return "\n".join(
		[
			"<!doctype html>",
			'<html lang="en">',
			"  <head>",
			"    <meta charset=\"UTF-8\" />",
			"    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />",
			f"    <title>{escape_html(story.title)} | Naman Kumar</title>",
			'    <link rel="stylesheet" href="../styles.css" />',
			"  </head>",
			'  <body class="story-page">',
			'    <div class="site-shell fade-in">',
			'      <header class="site-header">',
			f'        <a class="site-title" href="../index.html">{escape_html(SITE_TITLE)}</a>',
			f'        <p class="site-subtitle">{escape_html(SITE_SUBTITLE)}</p>',
			"      </header>",
			"",
			'      <header class="story-header">',
			f"        <h1>{escape_html(story.title)}</h1>",
			"      </header>",
			"",
			'      <article class="story-body">',
			body_html,
			"      </article>",
			"",
			nav_html,
			"    </div>",
			"  </body>",
			"</html>",
			"",
		]
	)


if __name__ == "__main__":
	main()
