#!/usr/bin/env python

from sys import argv, exit
import csv
import re
from pprint import pprint

def clean(s):
    return re.sub('["“”]', '', s).replace("N/A", "Unknown")

if len(argv) != 4:
    print("usage: %s edges nodes <target name>" % (argv[0]))
    exit(1)

graph = {}
rootName = argv[3]
rootNode = None

# edges format: src;goal1;goal2
for row in csv.reader(open(argv[1]), delimiter=";"):
    src = row[0]
    if row[1] == '-':
        dst = []
    else:
        dst = row[1:]
    if row[0] not in graph:
        graph[src] = { "dst": dst}
    else:
        graph[src]["dst"] += dst

# nodes format: id;name;uni;year;title;;;
for row in csv.reader(open(argv[2]), delimiter=";"):
    node, name, uni, year, title, _, _, _ = row
    if name == rootName: rootNode = node
    graph[node]["name"] = name
    #graph[node]["uni"] = clean(uni)
    #graph[node]["year"] = clean(year)
    #graph[node]["title"] = clean(title)
    unis = [x.strip() for x in clean(uni).split('/')]
    years = [x.strip() for x in clean(year).split('/')]
    titles = [x.strip() for x in clean(title).split('/')]
    graph[node]["zipped"] = zip(unis, years, titles)

print('digraph G {')
#print('  rankdir = BT') # upside down
#print('  size = "33.1,46.8"') # fits on A0
print('  size = "23.4,33.1"') # fits on A1
#print('  ratio = 0.7071067') # horizontal DIN
print('  ratio = 1.4142135') # vertical DIN
print('  ranksep = 1')
print('  node [fontname=helvetica shape=plain]')
#print('  edge [dir=back]')

for key, val in graph.items():
    print('  %s [label=< <TABLE BORDER="0">' % (key,))
    print('                <TR><TD><B>%s</B></TD></TR>' % (val["name"],))
    #print('                <TR><TD><I>%s %s</I></TD></TR>' % (val["uni"], val["year"]))
    for uni, year, _ in val["zipped"]:
        if uni == 'Unknown' and year == 'Unknown':
            print('                <TR><TD><I>Unknown University and Year</I></TD></TR>')
        elif uni == 'Unknown':
            print('                <TR><TD><I>Unknown University (%s)</I></TD></TR>' % (year))
        elif year == 'Unknown':
            print('                <TR><TD><I>%s (Unknown Year)</I></TD></TR>' % (uni))
        else:
            print('                <TR><TD><I>%s (%s)</I></TD></TR>' % (uni, year))
    print('              </TABLE> >]')

if rootNode != None:
    print('  %s [fontsize=36]' % (rootNode,))

print('')

for key, val in graph.items():
    print('  %s -> {%s}' % (key, " ".join(val["dst"])))

print('}')
