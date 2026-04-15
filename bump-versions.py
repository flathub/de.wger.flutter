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

import json
import sys

FLATPAK_FLUTTER_JSON = "flatpak-flutter.json"


def update_source_tag(filename: str, git_url: str, new_tag: str):
    """Updates the tag of a git source in the flatpak-flutter JSON file."""

    with open(filename, 'r', encoding="utf-8") as f:
        data = json.load(f)

    updated = False
    modules = data.get("modules", [])
    for source in modules[0].get("sources", []):
        if source.get("type") == "git" and source.get("url") == git_url:
            source["tag"] = new_tag
            updated = True
            break

    if not updated:
        raise ValueError(f"Source entry {git_url} not found")

    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python bump-versions.py <wger-version> [flutter-version]")
        sys.exit(1)

    wger_version = sys.argv[1]
    update_source_tag(FLATPAK_FLUTTER_JSON, "https://github.com/wger-project/flutter", wger_version)
    print(f"wger version updated to {wger_version}.")

    if len(sys.argv) == 3:
        flutter_version = sys.argv[2]
        update_source_tag(FLATPAK_FLUTTER_JSON, "https://github.com/flutter/flutter.git", flutter_version)
        print(f"Flutter SDK version updated to {flutter_version}.")