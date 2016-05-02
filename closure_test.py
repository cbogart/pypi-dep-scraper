import json
from collections import defaultdict
import re

# Input file is a list of these:
# reqs strings vary quite a lot in format however
#
#     {
#        "error": "METADATA",
#        "version": "0.11.0",
#        "reqs": [
#            "scipy (>=0.9)",
#            "numpy (>=1.7.1)",
#            "nose (>=0.10.1); extra == 'test'",
#            "nibabel (>=1.2.0)",
#            "Sphinx (>=1.0); extra == 'doc'"
#        ],
#        "version_type": "3.5",
#        "package": "dipy"
#    },


packages = json.load(open("pypi_dependencies.json","r"))
in_set = set()     #  packagename
upstream = defaultdict(set)  #  packagename -> set(packages used by)

firstword = re.compile(r"""[a-zA-Z0-9_\.-]*""")

for p in packages:
    in_set.add(p["package"])
    deps = set([re.search(firstword, r).group(0) for r in p["reqs"]])
    for d in deps:
        upstream[d].add(p["package"])

print "", len(in_set), "packages have", len(upstream), "dependencies"
print "intersection has", len(in_set & set(upstream.keys())), "packages"
print "Most popular non-included dependencies:"
leftovers = set(upstream.keys()) - in_set
ordered_leftovers = sorted(leftovers, key=lambda l: -len(upstream[l]))
for l in ordered_leftovers:
    print l,"\t", len(upstream[l]),"\t",list(upstream[l])[:5]
