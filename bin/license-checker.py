#!/usr/bin/env python
# https://git.soma.salesforce.com/python-at-sfdc/license_checker
# Modified version of https://stackoverflow.com/a/44090218
from __future__ import print_function
from collections import defaultdict
from pathlib import Path
from importlib.metadata import distributions

def get_pkg_license(dist):
    # Match original behavior: scan text lines for "License:" only
    try:
        lines = dist.read_text('METADATA').splitlines()
    except Exception:
        lines = (dist.read_text('PKG-INFO') or '').splitlines()
    for line in lines:
        if line.startswith('License:'):
            return line[9:].strip()
    return '(Licence not found)'

def print_table(table):
    column_index_to_max_width = defaultdict(int)
    for row_index, row in enumerate(table):
        for cell_index, cell in enumerate(row):
            cur_max = column_index_to_max_width[cell_index]
            cell_width = len(cell)
            if cell_width > cur_max:
                column_index_to_max_width[cell_index] = cell_width
    for row_index, row in enumerate(table):
        line = ''
        for cell_index, cell in enumerate(row):
            cell_width = column_index_to_max_width[cell_index]
            line += cell.ljust(cell_width)
            line += " - "
        line = line.ljust(25)
        line = line.rstrip(" -")
        print(line)
        if row_index == 0:
            print("-" * len(line))


def get_location(dist):
    # Try to locate the site-packages directory containing this distribution
    files = list(dist.files or [])
    # Prefer metadata files to infer the base
    meta_file = next((f for f in files if getattr(f, 'name', None) in ('METADATA', 'PKG-INFO')), None)
    if meta_file is not None:
        abs_path = Path(dist.locate_file(meta_file))
        # .../site-packages/<dist>.dist-info/METADATA -> site-packages
        return str(abs_path.parent.parent)
    if files:
        some_file = Path(dist.locate_file(files[0]))
        return str(some_file.parent)
    return '(Unknown)'


def print_packages_and_licenses():
    table = []
    table.append(['Package', 'License', 'Location'])
    # Sort by distribution name
    dists = []
    for dist in distributions():
        name = (dist.metadata.get('Name') or '').strip()
        dists.append((name.lower(), dist))
    for _, dist in sorted(dists, key=lambda t: t[0]):
        name = (dist.metadata.get('Name') or 'UNKNOWN').strip()
        version = getattr(dist, 'version', '')
        pkg_display = f"{name} {version}".strip()
        license_value = get_pkg_license(dist)[:25]
        location_value = get_location(dist)
        table.append([pkg_display.rjust(25)[:25], license_value, location_value])
    print_table(table)


if __name__ == "__main__":
    print_packages_and_licenses()
