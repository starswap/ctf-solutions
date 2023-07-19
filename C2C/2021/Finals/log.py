import re

ops = set()
with open("access (2).log") as f:
    for line in f:
        try:
            match = re.search(".*? - - \[.*?\] \".*?\" [0-9]+ [0-9]+ \".*?\" \"(.*?)\"", line)
            ops.add(match.group(1))
        except:
            ops.add(line)
for item in ops:
    print(item)