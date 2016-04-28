import csv
import json
import re
import pdb

names = csv.DictReader(open("pypinames.txt", "r"), delimiter="\t")
depinfo = json.load(open("pypi_dependencies.json", "r"))
summary = csv.writer(open("pypi_dep_summary.csv", "w"))


firstword = re.compile(r"""[a-zA-Z0-9_\.-]*""")

namelookup = dict()
for n in names:
    namelookup[n["pypiname"]] = n["full_name"]

summary.writerow(["pypiname", "project", "version", "python_version", "info_source", "dependencies"])
for d in depinfo:
    project = namelookup[d["package"]]
    deps = []
    for r in d["reqs"]:
        try:
            deps.append(re.search(firstword, r).group(0))
        except Exception, e:
            print "No match in req ", r
    summary.writerow([d["package"], project, d["version"], d["version_type"], d["error"], ";".join(deps)])
