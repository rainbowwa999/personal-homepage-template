#!/usr/bin/env python3
"""Generate demo.html or render content.json into a standalone index.html."""

import argparse
import base64
import json
import re
from html import escape
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlsplit

ASSETS = Path(__file__).resolve().parents[1] / "assets"
IMAGE_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif", ".avif": "image/avif",
}


def text(item, key, *, required=False):
    value = item.get(key, "")
    if not isinstance(value, str) or (required and not value.strip()):
        raise ValueError(f"{key} 需要有效的文字。")
    return value.strip()


def objects(value, field):
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"{field} 需要一个对象列表。")
    return value


def url_is_allowed(url, schemes):
    if any(character.isspace() or ord(character) < 32 for character in url):
        return False
    parts = urlsplit(url)
    return parts.scheme in schemes and bool(parts.path if parts.scheme == "mailto" else parts.hostname)


def image_tag(item, project, *, portrait=False):
    source = text(item, "src", required=True)
    if urlsplit(source).scheme:
        if not url_is_allowed(source, {"https"}):
            raise ValueError("图片需要 HTTPS 地址或项目内的相对路径。")
    else:
        relative = Path(source)
        path = (project / relative).resolve()
        if relative.is_absolute() or not path.is_relative_to(project):
            raise ValueError("图片路径必须位于当前主页项目目录。")
        mime = IMAGE_TYPES.get(path.suffix.lower())
        if mime is None:
            raise ValueError("图片支持 PNG、JPG、WebP、GIF 和 AVIF。")
        source = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()
    alt = text(item, "alt")
    priority = 'fetchpriority="high"' if portrait else 'loading="lazy"'
    return f'<img src="{escape(source)}" alt="{escape(alt)}" {priority} decoding="async">'


def render_blocks(items, project, *, allow_cards=True):
    blocks = []
    for item in objects(items, "blocks"):
        kind = item.get("type")
        if kind in ("text", "heading"):
            value = text(item, "text")
            tag = "p" if kind == "text" else "h3"
            if value:
                blocks.append(f"<{tag}>{escape(value)}</{tag}>")
        elif kind == "image":
            picture = image_tag(item, project)
            caption = text(item, "caption")
            note = f"<figcaption>{escape(caption)}</figcaption>" if caption else ""
            blocks.append(f"<figure>{picture}{note}</figure>")
        elif kind == "link":
            label = text(item, "label", required=True)
            url = text(item, "url", required=True)
            if not re.fullmatch(r"#[a-z][a-z0-9-]*", url) and not url_is_allowed(url, {"http", "https", "mailto"}):
                raise ValueError("链接需要 HTTP、HTTPS、邮箱或页内地址。")
            blocks.append(f'<a class="text-button" href="{escape(url)}">{escape(label)}</a>')
        elif kind == "card" and allow_cards:
            title = escape(text(item, "title", required=True))
            summary = escape(text(item, "summary"))
            if summary:
                summary = f'<span class="card-description">{summary}</span>'
            details = render_blocks(item.get("blocks", []), project, allow_cards=False)
            if not details:
                raise ValueError("展开卡片需要至少一项详情。")
            blocks.append(
                f'<details class="content-card"><summary><strong>{title}</strong>{summary}</summary>'
                f'<div class="content-flow">{details}</div></details>'
            )
        else:
            raise ValueError(f"不支持此处的内容类型：{kind!r}")
    return "\n".join(blocks)


def render(project):
    data = json.loads((project / "content.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("content.json 需要一个 JSON 对象。")

    raw_name = text(data, "name")
    name = escape(raw_name or "个人主页")
    subtitle = text(data, "subtitle")
    raw_portrait = data.get("portrait")
    if raw_portrait is not None and not isinstance(raw_portrait, dict):
        raise ValueError("portrait 需要一个对象。")
    portrait = image_tag(raw_portrait, project, portrait=True) if raw_portrait is not None else ""
    sections = []
    used_ids = {"top"}
    for item in objects(data.get("sections", []), "sections"):
        content = render_blocks(item.get("blocks", []), project)
        if not content:
            continue
        identifier = text(item, "id", required=True)
        if identifier in used_ids or not re.fullmatch(r"[a-z][a-z0-9-]*", identifier):
            raise ValueError(f"区块 ID 需为唯一的小写英文 ID：{identifier!r}")
        used_ids.add(identifier)
        sections.append((identifier, escape(text(item, "title", required=True)), content))

    if not any((raw_name, subtitle, portrait, sections)):
        raise ValueError("还没有主页资料。可先打开示例，或用 --demo 生成示例网页。")

    links = "".join(f'<a href="#{identifier}">{title}</a>' for identifier, title, _ in sections)
    introduction = ""
    hero_id = ""
    if sections and sections[0][0] == "about":
        hero_id, _, introduction = sections.pop(0)
        hero_id = f' id="{hero_id}"'
        introduction = f'<div class="content-flow">{introduction}</div>'

    role = f'<p class="profile-subtitle">{escape(subtitle)}</p>' if subtitle else ""
    visual = f'<div class="hero-visual"><div class="portrait">{portrait}</div></div>' if portrait else ""
    layout = "hero" if portrait else "hero hero--plain"
    hero = f'<section{hero_id} class="{layout}"><div class="hero-copy"><h1>{name}</h1>{role}{introduction}</div>{visual}</section>'
    body = [hero]
    for identifier, title, content in sections:
        body.append(f'<section id="{identifier}" class="section"><h2>{title}</h2><div class="content-flow">{content}</div></section>')

    template = (ASSETS / "page.html").read_text(encoding="utf-8")
    values = {
        "__TITLE__": f"{name} · 个人主页" if raw_name else "个人主页",
        "__NAME__": name,
        "__NAV__": f'<nav aria-label="主导航">{links}</nav>' if links else "",
        "__BODY__": "\n".join(body),
    }
    return re.sub(r"__TITLE__|__NAME__|__NAV__|__BODY__", lambda match: values[match[0]], template)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--demo", action="store_true", help="write demo.html instead of building a personal site")
    args = parser.parse_args()
    project = args.project.resolve()
    temporary = None
    try:
        page = (ASSETS / "demo.html").read_text(encoding="utf-8") if args.demo else render(project)
        project.mkdir(parents=True, exist_ok=True)
        output = project / ("demo.html" if args.demo else "index.html")
        with NamedTemporaryFile(mode="w", encoding="utf-8", dir=project, delete=False) as file:
            temporary = Path(file.name)
            file.write(page)
        temporary.replace(output)
    except (OSError, ValueError) as error:
        parser.exit(1, f"生成失败：{error}\n")
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(output)


if __name__ == "__main__":
    main()
