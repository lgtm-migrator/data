# -*- coding: utf-8 -*-

"""Module providing access to all known data set definitions."""

from __future__ import absolute_import, division, print_function

import hashlib
import pkg_resources
import yaml

_hashinfo_version = 1

definition = {}
fileinfo = {}
fileinfo_dirty = set()
for definition_file in pkg_resources.resource_listdir("dials_data", "definitions"):
    if definition_file.endswith(".yml"):
        dataset_definition = pkg_resources.resource_string(
            "dials_data", "definitions/" + definition_file
        )
        dataset_name = definition_file[:-4]
        definition[dataset_name] = yaml.load(dataset_definition)
        dhash = hashlib.sha256()
        dhash.update(dataset_definition)
        definition[dataset_name]["hash"] = dhash.hexdigest()
        try:
            fileinfo[dataset_name] = yaml.load(
                pkg_resources.resource_stream(
                    "dials_data", "definitions/hashinfo/" + definition_file
                )
            )
            if (
                fileinfo[dataset_name]["definition"] != definition[dataset_name]["hash"]
                or definition[dataset_name]["version"] < _hashinfo_version
            ):
                fileinfo_dirty.add(dataset_name)
        except IOError:
            fileinfo_dirty.add(dataset_name)
            continue


def show_known_definitions():
    for ds in sorted(definition):
        print(
            (
                "{dsname} - {fullname}:\n"
                + "    {author} ({license}) {url}\n"
                + "    {description}"
            ).format(
                dsname=ds,
                fullname=definition[ds]["name"],
                author=definition[ds].get("author", "unknown author"),
                license=definition[ds].get("license", "unknown license"),
                url=definition[ds].get("url", ""),
                description=definition[ds]["description"].strip(),
            )
        )
        if ds in fileinfo_dirty:
            print("(currently not available)")
        print()
