import xmlrpclib
import os
import csv
import urllib

downlog = csv.writer(open("download.log", "w"))

client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')

packages = open("pypinames.txt","r").readlines()
for package in packages:
    package = package.split(" ")[1].strip()
    releases = client.package_releases(package)
    print package, len(releases), "releases"
    for release in releases:
        for url in client.release_urls(package, release):
            downlog.writerow([package, release, url["packagetype"], url["upload_time"], url["filename"], url["python_version"]])
            dirname = package + "/" + release + "/" + url["python_version"]
            try:
                os.makedirs(dirname)
            except:
                pass
            filename = dirname + "/" + url["filename"]
            print url["url"], filename
            urllib.urlretrieve(url["url"], filename)
            
                
