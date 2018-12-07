# -*- coding: utf-8 -*-

"""Module providing access to all known data set definitions."""

from __future__ import absolute_import, division, print_function

import hashlib
import os
import pkg_resources
import py
import yaml

_hashinfo_version = 1


def _load_yml_definitions():
    """
    Read dataset .yml files from definitions/ and hashinfo/ directories.
    This is done once during the module import stage.
    """
    global definition, fileinfo, fileinfo_dirty
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
            h_file = "hashinfo/" + definition_file
            if not pkg_resources.resource_exists("dials_data", h_file):
                fileinfo_dirty.add(dataset_name)
                continue
            fileinfo[dataset_name] = yaml.load(
                pkg_resources.resource_stream("dials_data", h_file)
            )
            if (
                fileinfo[dataset_name]["definition"] != definition[dataset_name]["hash"]
                or definition[dataset_name]["version"] < _hashinfo_version
            ):
                fileinfo_dirty.add(dataset_name)


_load_yml_definitions()


def repository_location():
    """
    Returns an appropriate location where the downloaded regression data should
    be stored.

    In order of evaluation:
    * If the environment variable DIALS_DATA is set and exists or can be
      created then use that location
    * If a Diamond Light Source specific path exists then use that location
    * If the environment variable LIBTBX_BUILD is set and the directory
      'dials_data' exists or can be created underneath that location then
      use that.
    * Use ~/.cache/dials_data if it exists or can be created
    * Otherwise fail with a RuntimeError
    """
    if os.getenv("DIALS_DATA"):
        try:
            repository = py.path.local(os.getenv("DIALS_DATA"))
            repository.ensure(dir=1)
            return repository
        except Exception:
            pass
    try:
        repository = py.path.local("/dls/science/groups/scisoft/DIALS/dials_data")
        if repository.check(dir=1):
            return repository
    except Exception:
        pass
    if os.getenv("LIBTBX_BUILD"):
        try:
            repository = py.path.local(os.getenv("LIBTBX_BUILD")).join("dials_data")
            repository.ensure(dir=1)
            return repository
        except Exception:
            pass
    repository = (
        py.path.local(os.path.expanduser("~")).join(".cache").join("dials_data")
    )
    try:
        repository.ensure(dir=1)
        return repository
    except Exception:
        raise RuntimeError(
            "Could not determine regression data location. Use environment variable DIALS_DATA"
        )


def show_known_definitions(ds_list, quiet=False):
    for ds in sorted(ds_list):
        if quiet:
            print(ds)
            continue
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


def cli_show(cmd_args):
    import argparse

    parser = argparse.ArgumentParser(description="Show dataset information")
    parser.add_argument(
        "--missing-fileinfo",
        action="store_true",
        help="only show datasets that do not have a bill of material",
    )
    parser.add_argument("--quiet", action="store_true", help="machine readable output")
    args = parser.parse_args(cmd_args)
    if args.missing_fileinfo:
        ds_list = fileinfo_dirty
    else:
        ds_list = definition
    show_known_definitions(ds_list, quiet=args.quiet)
