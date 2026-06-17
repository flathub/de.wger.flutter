# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

import re
import sys

FLATPAK_FLUTTER_YAML = "flatpak-flutter.yml"


def update_source_tag(filename: str, url_markers: tuple, new_tag: str):
    """Updates the tag of a git source in the flatpak-flutter YAML file.

    Matches a source whose url contains any of the given substrings, so the
    local file:// dev URL works alongside the canonical GitHub URL.
    Edits line-based to preserve comments and formatting.
    """

    with open(filename, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    url_pattern = re.compile(r'^(\s*)url:\s*(\S+)\s*$')
    tag_pattern = re.compile(r'^(\s*)tag:\s*\S+\s*$')

    updated = False
    for i, line in enumerate(lines):
        url_match = url_pattern.match(line)
        if url_match and any(m in url_match.group(2) for m in url_markers):
            for j in range(i + 1, min(i + 5, len(lines))):
                tag_match = tag_pattern.match(lines[j])
                if tag_match:
                    indent = tag_match.group(1)
                    lines[j] = f"{indent}tag: {new_tag}\n"
                    updated = True
                    break
            if updated:
                break

    if not updated:
        raise ValueError(f"Source entry matching any of {url_markers!r} not found")

    with open(filename, 'w', encoding="utf-8") as f:
        f.writelines(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python bump-versions.py <wger-version> [flutter-version]")
        sys.exit(1)

    wger_version = sys.argv[1]
    update_source_tag(FLATPAK_FLUTTER_YAML, ("wger-project/flutter", "wger/flutter"), wger_version)
    print(f"wger version updated to {wger_version}.")

    if len(sys.argv) == 3:
        flutter_version = sys.argv[2]
        update_source_tag(FLATPAK_FLUTTER_YAML, ("flutter/flutter.git",), flutter_version)
        print(f"Flutter SDK version updated to {flutter_version}.")
