#!/usr/bin/python3
import sys
import os
import re
import hashlib

def convert_md_to_html(input_file, output_file):
    try:
        with open(input_file, 'r') as md, open(output_file, 'w') as html:
            in_ul = False
            in_ol = False
            for line in md:
                line = line.rstrip()

                # Handle Headings
                heading_match = re.match(r'^(#{1,6}) (.*)', line)
                if heading_match:
                    level = len(heading_match.group(1))
                    content = heading_match.group(2)
                    html.write(f'<h{level}>{content}</h{level}>\n')
                    continue

                # Handle Unordered Lists
                if line.startswith('- '):
                    if not in_ul:
                        html.write('<ul>\n')
                        in_ul = True
                    html.write(f'<li>{line[2:].strip()}</li>\n')
                    continue
                if in_ul:
                    html.write('</ul>\n')
                    in_ul = False

                # Handle Ordered Lists
                if line.startswith('* '):
                    if not in_ol:
                        html.write('<ol>\n')
                        in_ol = True
                    html.write(f'<li>{line[2:].strip()}</li>\n')
                    continue
                if in_ol:
                    html.write('</ol>\n')
                    in_ol = False

                # Handle Paragraphs
                if line:
                    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
                    line = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)
                    line = re.sub(r'\(\((.*?)\)\)', lambda m: re.sub(r'[cC]', '', m.group(2)), line)
                    line = line.replace('\n', '<br/>')
                    html.write(f'<p>{line}</p>\n')
    except Exception as e:
        sys.stderr.write(f'Error: {e}\n')
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: ./markdown2html.py README.md README.html\n')
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f'Missing {input_file}\n')
        sys.exit(1)

    convert_md_to_html(input_file, output_file)
    sys.exit(0)
