#!/usr/bin/env python3
import io
import re

def parse_ruby(line):
    def repl(match):
        return r'<ruby>{}<rp>（</rp><rt>{}</rt><rp>）</rp></ruby>'.format(*match.group(1, 2))
    return re.sub(r'\[(.+?)\]\((.+?)\)', repl, line).replace(r'</ruby><ruby>', '')  # Eliminate redundant sibling tags

def parse_text(lyrics_text):
    title = ''
    paragraphs = []
    this_paragraph = []

    for line in lyrics_text.splitlines():
        line = line.strip()
        if line.startswith('#'):        # Title text
            title = line[1:].strip()
        elif line:                      # Regular lyrics
            this_paragraph.append(parse_ruby(line))
        elif this_paragraph:            # Blank line, check if we’re in paragraph
            paragraphs.append(this_paragraph)
            this_paragraph = []

    if this_paragraph:      # Dangling last paragraph
        paragraphs.append(this_paragraph)

    return title, paragraphs
