import re

def to_markdown(markdown_string):
    text = re.sub(r'#+\s', '', markdown_string)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', text)
    return text