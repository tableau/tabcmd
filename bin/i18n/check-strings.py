#!/usr/bin/env python3
"""
Check for missing localization strings in the tabcmd codebase.

This script scans all Python source files under ./tabcmd for strings using the _() 
localization pattern and checks if they're present in the locale files under 
./tabcmd/locales/en/*.properties.

Usage:
    python bin/i18n/check-strings.py

Returns:
    0 if no missing strings found
    1 if missing strings found
"""

import os
import re
import sys
from pathlib import Path
from typing import Set, List, Tuple


def find_python_files(root_dir: str) -> List[str]:
    """Find all Python files under the given directory."""
    python_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip __pycache__ and other common directories to ignore
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]

        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    return python_files


def extract_string_keys_from_file(file_path: str) -> Set[str]:
    """Extract all string keys used in _() calls from a Python file."""
    string_keys = set()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()
        except Exception as e:
            print(f"Warning: Could not read file {file_path}: {e}", file=sys.stderr)
            return string_keys

    # Pattern to match _("string_key") or _('string_key')
    # This handles both single and double quotes
    pattern = r'_\s*\(\s*["\']([^"\']+)["\']\s*\)'

    matches = re.findall(pattern, content)
    string_keys.update(matches)

    return string_keys


def load_properties_files(locale_dir: str) -> Set[str]:
    """Load all string keys from properties files in the locale directory."""
    string_keys = set()

    if not os.path.exists(locale_dir):
        print(f"Warning: Locale directory {locale_dir} does not exist", file=sys.stderr)
        return string_keys

    # Find all .properties files
    for root, dirs, files in os.walk(locale_dir):
        for file in files:
            if file.endswith(".properties"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line_num, line in enumerate(f, 1):
                            line = line.strip()

                            # Skip comments and empty lines
                            if not line or line.startswith("#"):
                                continue

                            # Parse key=value format
                            if "=" in line:
                                key = line.split("=", 1)[0].strip()
                                string_keys.add(key)

                except UnicodeDecodeError:
                    # Try with different encoding if UTF-8 fails
                    try:
                        with open(file_path, "r", encoding="latin-1") as f:
                            for line_num, line in enumerate(f, 1):
                                line = line.strip()

                                # Skip comments and empty lines
                                if not line or line.startswith("#"):
                                    continue

                                # Parse key=value format
                                if "=" in line:
                                    key = line.split("=", 1)[0].strip()
                                    string_keys.add(key)
                    except Exception as e:
                        print(f"Warning: Could not read properties file {file_path}: {e}", file=sys.stderr)
                except Exception as e:
                    print(f"Warning: Could not read properties file {file_path}: {e}", file=sys.stderr)

    return string_keys


def find_missing_strings(python_files: List[str], defined_keys: Set[str]) -> List[Tuple[str, str]]:
    """Find missing string keys and their source files."""
    missing_strings = []

    for file_path in python_files:
        file_keys = extract_string_keys_from_file(file_path)

        for key in file_keys:
            if key not in defined_keys:
                missing_strings.append((key, file_path))

    return missing_strings


def main():
    """Main function to check for missing localization strings."""
    # Get the project root directory (assuming script is in bin/i18n/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    tabcmd_dir = project_root / "tabcmd"
    locale_dir = project_root / "tabcmd" / "locales" / "en"

    print(f"Scanning Python files in: {tabcmd_dir}")
    print(f"Checking locale files in: {locale_dir}")
    print()

    # Find all Python files
    python_files = find_python_files(str(tabcmd_dir))
    print(f"Found {len(python_files)} Python files to scan")

    # Load all defined string keys from properties files
    defined_keys = load_properties_files(str(locale_dir))
    print(f"Found {len(defined_keys)} defined string keys in locale files")

    # Find missing strings
    missing_strings = find_missing_strings(python_files, defined_keys)

    if missing_strings:
        print(f"\nERROR: Found {len(missing_strings)} missing string keys:")
        print("=" * 80)

        # Group by file for better output
        missing_by_file = {}
        for key, file_path in missing_strings:
            if file_path not in missing_by_file:
                missing_by_file[file_path] = []
            missing_by_file[file_path].append(key)

        for file_path in sorted(missing_by_file.keys()):
            # Show relative path from project root
            rel_path = os.path.relpath(file_path, project_root)
            print(f"\nFile: {rel_path}")
            print("-" * 40)
            for key in sorted(missing_by_file[file_path]):
                print(f"  Missing: {key}")

        print("\n" + "=" * 80)
        print("Please add the missing string keys to the appropriate .properties files.")
        return 1
    else:
        print("\nSUCCESS: All string keys are properly defined in locale files.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
