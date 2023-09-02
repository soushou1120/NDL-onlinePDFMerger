import re

string =  "apple, banana,orange , grape"
print(string)
def string_splitter(string):
    Keywords_slicer = [m.start() for m in re.finditer(r'\S,\S', string)]
    parts = []
    start = 0
    for slicer in Keywords_slicer:
        part = string[start:slicer + 1]
        parts.append(part)
        start = slicer + 2
    parts.append(string[start:])
    print(parts)

string_splitter(string)