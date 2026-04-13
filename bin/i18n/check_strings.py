#!/usr/bin/env python3
"""
Check for missing localization strings in the tabcmd codebase.

This script scans all Python source files under ./tabcmd for strings using the _() 
localization pattern and checks if they're present in the locale files.

Usage:
    python bin/i18n/check_strings.py                    # Dev mode: check against en/*.properties
    python bin/i18n/check_strings.py --mode build       # Build mode: check against filtered.properties for all locales

Returns:
    0 if no missing strings found
    1 if missing strings found
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Set, List, Tuple

# Default locales (matches dodo.py)
DEFAULT_LOCALES = ["en", "de", "es", "fr", "ga", "it", "pt", "sv", "ja", "ko", "zh"]


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


def load_properties_file(file_path: str) -> Set[str]:
    """Load string keys from a single properties file."""
    string_keys = set()
    
    if not os.path.exists(file_path):
        return string_keys
        
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


def format_limited_list(items: List[str], prefix: str = "  Missing: ", limit: int = 5) -> List[str]:
    """Format a list of items with a limit, showing [+x more] if truncated."""
    sorted_items = sorted(items)
    if len(sorted_items) <= 10:
        # Show all items if 10 or fewer
        return [f"{prefix}{item}" for item in sorted_items]
    else:
        # Show first 5 items + summary for more than 10
        result = [f"{prefix}{item}" for item in sorted_items[:limit]]
        remaining = len(sorted_items) - limit
        result.append(f"  [+{remaining} more]")
        return result


def check_build_mode(project_root: Path, locales: List[str]) -> int:
    """Check all locales against filtered.properties files (build pipeline mode)."""
    tabcmd_dir = project_root / "tabcmd"
    
    # Setup output file
    output_file = project_root / "localization_check_results.txt"
    
    def print_and_write(message, file_handle=None):
        """Print to console and write to file"""
        print(message)
        if file_handle:
            file_handle.write(message + "\n")
    
    with open(output_file, "w", encoding="utf-8") as f:
        print_and_write(f"Build mode: Scanning Python files in: {tabcmd_dir}", f)
        print_and_write(f"Checking locales: {', '.join(locales)}", f)
        print_and_write("", f)
        
        # Find all Python files and extract string keys
        python_files = find_python_files(str(tabcmd_dir))
        print_and_write(f"Found {len(python_files)} Python files to scan", f)
        
        code_strings = set()
        for file_path in python_files:
            code_strings.update(extract_string_keys_from_file(file_path))
        
        print_and_write(f"Found {len(code_strings)} unique string keys in code", f)
    
        # Check each locale, starting with English as baseline
        english_success = True  # Only track English success for exit code
        english_missing_keys = set()
        english_output = ""  # Store English output to repeat at end
        locales_with_same_missing = []
        
        for locale in locales:
            filtered_file = project_root / "tabcmd" / "locales" / locale / "LC_MESSAGES" / "filtered.properties"
            
            if not filtered_file.exists():
                print_and_write(f"WARNING: No filtered.properties for locale '{locale}' at {filtered_file}", f)
                continue
                
            defined_keys = load_properties_file(str(filtered_file))
            missing_keys = code_strings - defined_keys
            
            if missing_keys:
                if locale == "en":
                    # English has missing keys - this affects exit code
                    english_success = False
                    english_missing_keys = missing_keys
                    english_output = f"\nERROR: Found {len(missing_keys)} missing string keys for locale '{locale}':\n"
                    english_output += "=" * 60 + "\n"
                    for line in format_limited_list(list(missing_keys)):
                        english_output += line + "\n"
                    print_and_write(english_output.rstrip(), f)  # Print now for baseline
                else:
                    # For other languages, only show if different from English
                    if missing_keys == english_missing_keys:
                        locales_with_same_missing.append(locale)
                    else:
                        print_and_write(f"\nERROR: Found {len(missing_keys)} missing string keys for locale '{locale}' (different from English):", f)
                        print_and_write("=" * 60, f)
                        
                        # Show keys unique to this locale
                        unique_to_locale = missing_keys - english_missing_keys
                        if unique_to_locale:
                            print_and_write(f"  Additional missing keys in {locale}:", f)
                            for line in format_limited_list(list(unique_to_locale), "    Missing: "):
                                print_and_write(line, f)
                        
                        # Show keys missing in English but present in this locale
                        present_in_locale = english_missing_keys - missing_keys
                        if present_in_locale:
                            print_and_write(f"  Keys present in {locale} but missing in English:", f)
                            for line in format_limited_list(list(present_in_locale), "    Present: "):
                                print_and_write(line, f)
                        
                        # Show common missing keys if both have missing keys
                        common_missing = missing_keys & english_missing_keys
                        if common_missing and (unique_to_locale or present_in_locale):
                            print_and_write(f"  Keys missing in both English and {locale}: {len(common_missing)}", f)
            else:
                if locale == "en":
                    english_output = f"[OK] Locale '{locale}': All {len(code_strings)} string keys found"
                    print_and_write(english_output, f)  # Print now for baseline
                else:
                    print_and_write(f"[OK] Locale '{locale}': All {len(code_strings)} string keys found", f)
        
        # Show summary for locales with same missing keys as English
        if locales_with_same_missing:
            print_and_write(f"\nNOTE: The following locales have the same missing keys as English:", f)
            print_and_write(f"      {', '.join(locales_with_same_missing)}", f)
            print_and_write(f"      Missing keys: {len(english_missing_keys)}", f)
        
        # Print English results again at the end for visibility
        if english_output and "en" in locales:
            print_and_write(f"\n--- English Results (repeated for visibility) ---", f)
            print_and_write(english_output.rstrip(), f)
        
        # Summary message about file output
        print_and_write(f"\nResults saved to: {output_file}", f)
        
        # Only fail if English has missing strings
        if english_success:
            print_and_write("\nSUCCESS: All required English strings are present", f)
        else:
            print_and_write("\nFAILED: English is missing required strings", f)
    
    return 0 if english_success else 1


def check_dev_mode(project_root: Path) -> int:
    """Check against English properties files (development mode - original behavior)."""
    tabcmd_dir = project_root / "tabcmd"
    locale_dir = project_root / "tabcmd" / "locales" / "en"
    
    print(f"Dev mode: Scanning Python files in: {tabcmd_dir}")
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
            for line in format_limited_list(missing_by_file[file_path]):
                print(line)
        
        print("\n" + "=" * 80)
        print("Please add the missing string keys to the appropriate .properties files.")
        return 1
    else:
        print("\nSUCCESS: All string keys are properly defined in locale files.")
        return 0


def main():
    """Main function to check for missing localization strings."""
    parser = argparse.ArgumentParser(
        description="Check for missing localization strings in tabcmd codebase"
    )
    parser.add_argument(
        "--mode", 
        choices=["dev", "build"], 
        default="dev",
        help="dev: check against en/*.properties (default), build: check against filtered.properties for all locales"
    )
    parser.add_argument(
        "--locales", 
        nargs="*", 
        default=DEFAULT_LOCALES,
        help="Locales to check in build mode (default: all supported locales)"
    )
    
    args = parser.parse_args()
    
    # Get the project root directory (assuming script is in bin/i18n/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    
    if args.mode == "dev":
        return check_dev_mode(project_root)
    else:  # build mode
        return check_build_mode(project_root, args.locales)


if __name__ == "__main__":
    sys.exit(main())
