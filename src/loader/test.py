import re

text="this is a test sentence"

print re.findall(r"\b[a-z]+\b", text, re.I)