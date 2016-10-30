#!/usr/bin/env python3
import io
import re

RUBYTEXT_RE = re.compile(r'\[(.+?)\]\((.+?)\)')

def parse_ruby(line):
    def repl(match):
        return r'{}（{}）'.format(*match.group(1, 2))
    return RUBYTEXT_RE.sub(repl, line)

def render_ruby(line):
    def repl(match):
        return r'<ruby>{}<rp>（</rp><rt>{}</rt><rp>）</rp></ruby>'.format(*match.group(1, 2))
    return RUBYTEXT_RE.sub(repl, line).replace(r'</ruby><ruby>', '')  # Eliminate redundant sibling tags

def parse_text(lyrics_text):
    title = ''
    paragraphs = []
    this_paragraph = []

    for line in lyrics_text.splitlines():
        line = line.strip()
        if line.startswith('#'):        # Title text
            title = line[1:].strip()
        elif line:                      # Regular lyrics
            this_paragraph.append(line)
        elif this_paragraph:            # Blank line, check if we’re in paragraph
            paragraphs.append(this_paragraph)
            this_paragraph = []

    if this_paragraph:      # Dangling last paragraph
        paragraphs.append(this_paragraph)

    return title, paragraphs

def render(lyrics_text, buf=None):
    title, paragraphs = parse_text(lyrics_text)

    # Ensure buffer is created
    if not buf:
        buf = io.StringIO()

    buf.write("""<!DOCTYPE html>
<html lang="ja-jp">
<head>
    <meta charset="utf-8" />
    <title>""")
    buf.write(parse_ruby(title))
    buf.write("""</title>
    <link rel="stylesheet" href="../styles.css" />
</head>
<body>""")
    if title:
        buf.write("""
    <h1>""")
        buf.write(render_ruby(title))
        buf.write("</h1>")
    for paragraph in paragraphs:
        buf.write("""
    <p>""")
        first_line = True
        for line in paragraph:
            if first_line:
                first_line = False
            else:
                buf.write("<br>")
            buf.write("""
        """)
            buf.write(render_ruby(line))
        buf.write("""
    </p>""")
    buf.write("""
</body>
</html>
""")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print('Usage: cat lyrics.txt | ./convert.py > output.html')
    else:
        render(sys.stdin.read(), buf=sys.stdout)
