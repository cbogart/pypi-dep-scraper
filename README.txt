

Files in this directory extract a dependency tree from a set of github pypi projects

extract_pypi_list.sh:     Query the database for the list of pypi names and github owner/project pairs to use
  pypinames.txt           Output of extract_pypi_list.sh
pypi_getter.py            Downloads all pypi distribution files into pypi directory
  pypi:                   Directory where pypi projects are cached
pypi_version_scanner.py   Reads pypi directory and creates pypi_dependencies.json
  pypi_dependencies.json  Dependency information extracted from each project
pypi_summarize.py         Reads pypi_depenencies.json and outputs pypi_dep_summary.csv
  pypi_dep_summary.csv    Summary of dependency information for each project
