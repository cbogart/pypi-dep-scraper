import os
import pdb
import json
import csv
import urllib
import subprocess

class FileAbsent(Exception):
    pass

def get_file_from(zipfile, filename):
    #unzip -p x.whl \*\*/METADATA
    if zipfile.endswith(".gz") or zipfile.endswith(".tar.gz") or zipfile.endswith("tgz"):
        tar = subprocess.Popen(["tar", "-zxf", zipfile, "--no-anchored", filename, "-O"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif zipfile.endswith(".whl") or zipfile.endswith(".zip") or zipfile.endswith(".egg"):
        tar = subprocess.Popen(["unzip", "-p", zipfile, "**/" + filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        raise FileAbsent("Unknown file format")
    tar_out = tar.communicate()
    if tar_out[1]  != '':
        raise FileAbsent(tar_out[1])
    return tar_out[0]

def parse_requires_txt(zipfile):
    raw = get_file_from(zipfile, "requires.txt")
    rets = []
    for req in raw.splitlines():
        if len(req) > 0:
            if req[0] != "[":
                rets.append(req.strip())
    return rets

def parse_PKG_INFO(zipfile):
    raw = get_file_from(zipfile, "PKG-INFO")
    try:
        return [req.split(":")[1].strip() for req in raw.splitlines() if req[:7] == "Require" and ":" in req]
    except:
        pdb.set_trace()

def parse_METADATA(zipfile):
    raw = get_file_from(zipfile, "METADATA")
    try:
        return [req.split(":")[1].strip() for req in raw.splitlines() if req[:7] == "Require" and ":" in req]
    except:
        pdb.set_trace()


dep_info = []

for (root, dirs, files) in os.walk("./pypi"):
    for fil in files:
         filename = root + "/" + fil
         error = ""
         reqs = []
         try:
             reqs = parse_requires_txt(filename)
             error= "requires.txt"
         except FileAbsent, e:
             try:
                 reqs = parse_PKG_INFO(filename)
                 error= "PKG-INFO"
             except FileAbsent, e:
                 try:
                     reqs = parse_METADATA(filename)
                     error= "METADATA"
                 except FileAbsent, e:
                     error = "NO deps found " + str(e)
         print filename, error
         pathparts = root.split("/")
         package = pathparts[2] #find /pypi/<package>/<version>/<version_type>
         version = pathparts[3]
         version_type = pathparts[4]
         dep_info += [{"package":  package, 
                       "version" : version,
                       "version_type" : version_type,
                       "reqs": list(set(reqs)), 
                       "error": error}]
         

pydep = open("pypi_dependencies.json", "w")
pydep.write(json.dumps(dep_info, indent=4))


#
#   notes on other metadata:
#     tar file (and probably zip) have a date associated with the requires or PKG-INFO or METADATA file; probably OK as release date
#     Author: and Author-email: in PKG-INFO and METADATA (but not requires.txt)
#     split version from constraints (pkgname == 3.4.1), etc.
#
