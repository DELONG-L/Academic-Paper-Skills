"""Validate public documentation, skill identity, and self-contained brand assets."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('paper-writing', 'paper-figures-tables', 'paper-review', 'paper-policy')
PAIRS = (
    ('README.md', 'README.zh-CN.md'),
    ('CONTRIBUTING.md', 'CONTRIBUTING.zh-CN.md'),
    ('docs/getting-started.md', 'docs/getting-started.zh-CN.md'),
    ('docs/architecture.md', 'docs/architecture.zh-CN.md'),
)


class HTMLReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('href', 'src'):
            if attrs.get(key):
                self.targets.append(attrs[key])
        for key in ('id', 'name'):
            if attrs.get(key):
                self.ids.add(attrs[key])


def prose(text):
    """Exclude fenced examples so documentation checks do not follow sample paths."""
    return re.sub(r'(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$', '', text)


def references(text):
    text = prose(text)
    parser = HTMLReferences()
    parser.feed(text)
    targets = re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text)
    return parser.targets + [t.strip('<>') for t in targets]


def anchors(text):
    text = prose(text)
    parser = HTMLReferences()
    parser.feed(text)
    result = set(parser.ids)
    counts = {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$', text, re.M):
        heading = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', heading)
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        result.add(slug if n == 0 else f'{slug}-{n}')
    return result


def check_document(path, root):
    errors = []
    for target in references(path.read_text()):
        url = urlsplit(target)
        if url.scheme or url.netloc:
            continue
        resolved = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
        if not resolved.is_relative_to(root.resolve()):
            errors.append(f'{path.name}: link escapes repository: {target}')
        elif not resolved.exists():
            errors.append(f'{path.name}: missing link target: {target}')
        elif url.fragment and resolved.suffix == '.md':
            if unquote(url.fragment) not in anchors(resolved.read_text()):
                errors.append(f'{path.name}: missing anchor: {target}')
    return errors


def check_pair(first, second, root):
    errors = []
    for source, counterpart in ((first, second), (second, first)):
        if not source.is_file():
            errors.append(f'Missing language edition: {source.relative_to(root)}')
            continue
        local_targets = []
        for value in references(source.read_text()):
            url = urlsplit(value)
            if not url.scheme and not url.netloc:
                local_targets.append((source.parent / unquote(url.path)).resolve())
        if counterpart.resolve() not in local_targets:
            errors.append(f'{source.name}: missing language switch to {counterpart.name}')
    if first.name == 'README.md' and first.is_file() and second.is_file():
        a, b = HTMLReferences(), HTMLReferences()
        a.feed(first.read_text()); b.feed(second.read_text())
        if a.ids != b.ids:
            errors.append('README language editions have different navigation anchors')
    return errors


def check_svg(path):
    errors = []
    try:
        root = ET.fromstring(path.read_bytes())
    except ET.ParseError as exc:
        return [f'{path.name}: invalid SVG: {exc}']
    if root.tag.split('}')[-1] != 'svg' or not root.get('viewBox'):
        errors.append(f'{path.name}: expected SVG root with viewBox')
    if not any(e.tag.split('}')[-1] == 'title' and e.text for e in root.iter()):
        errors.append(f'{path.name}: missing accessible title')
    for e in root.iter():
        if e.tag.split('}')[-1] in {'script', 'foreignObject', 'image'}:
            errors.append(f'{path.name}: active or raster content is not allowed in brand SVGs')
        for key, value in e.attrib.items():
            key = key.split('}')[-1]
            if key.startswith('on') or (key == 'href' and not value.startswith('#')):
                errors.append(f'{path.name}: external or active attribute: {key}')
            if 'url(' in value and not re.fullmatch(r'url\(#[\w-]+\)', value):
                errors.append(f'{path.name}: nonlocal URL reference')
    return errors


def check_skill(path):
    errors = []
    try:
        text = (path / 'SKILL.md').read_text()
        header = re.match(r'^---\n(.*?)\n---', text, re.S)
        data = yaml.safe_load(header.group(1)) if header else {}
        if data.get('name') != path.name:
            errors.append(f'{path.name}: skill name must match directory')
        if not isinstance(data.get('description'), str) or not data['description'].strip():
            errors.append(f'{path.name}: missing skill description')
        interface = yaml.safe_load((path / 'agents/openai.yaml').read_text()).get('interface', {})
        for key in ('display_name', 'short_description', 'default_prompt'):
            if not interface.get(key):
                errors.append(f'{path.name}: missing interface {key}')
        if '$' + path.name not in interface.get('default_prompt', ''):
            errors.append(f'{path.name}: default prompt does not invoke its skill')
    except (OSError, ValueError, AttributeError, yaml.YAMLError) as exc:
        errors.append(f'{path.name}: invalid metadata: {exc}')
    return errors


def check(root):
    errors = []
    docs = sorted(root.glob('*.md')) + sorted((root / 'docs').rglob('*.md'))
    for path in docs:
        errors.extend(check_document(path, root))
    for first, second in PAIRS:
        errors.extend(check_pair(root / first, root / second, root))
    for name in SKILLS:
        errors.extend(check_skill(root / name))
    for name in ('logo.svg', 'hero-en.svg', 'hero-zh-CN.svg'):
        path = root / 'docs/assets' / name
        if path.is_file():
            errors.extend(check_svg(path))
        else:
            errors.append(f'Missing brand asset: {name}')
    return errors, len(docs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=ROOT)
    args = parser.parse_args()
    errors, count = check(args.root.resolve())
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors))
        return 1
    print(f'Repository checks passed: {count} public documents, 4 language pairs, 4 skills, 3 SVG assets.')
    print('Scope: local links/anchors, metadata and SVG structure; not visual or scientific validation.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
