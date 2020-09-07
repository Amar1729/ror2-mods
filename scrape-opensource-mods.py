#! /usr/bin/env python3

"""
Scrape all the mods from the thunderstore that include source code (on e.g. github, gitlab).

Usage:
$ ./scrape-opensource-mods.py > OPENSOURCE.md

Requires:
- `requests` (python module)
"""

from urllib.parse import urlparse

import requests


URL = "https://thunderstore.io/api/"


def display(result):
	full_name = result["full_name"]
	link_thunderstore = "[Thunderstore]({})".format(result["package_url"])
	link_url = "[Source]({})".format(result["latest"]["website_url"])
	print("| {} | {} | {} |".format(full_name, link_thunderstore, link_url))


def results():
	page = 1
	while True:
		r = requests.get(URL + "v2/package", params={"page":page})
		if r.status_code >= 400 or "results" not in r.json():
			break
		for result in r.json()["results"]:
			yield result
		page += 1


def main():
	print("| Name | Thunderstore | Source |")
	print("|----- | ------------ | -------|")
	for result in results():
		o = urlparse(result["latest"]["website_url"])
		if "git" in o.netloc:
			display(result)


if __name__ == "__main__":
	main()
