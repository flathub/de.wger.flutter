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

def update_wger_version(filename: str, new_version: str):
    """Updates the version of the wger flutter source in the flatpak-flutter JSON file."""

    with open(filename, 'r', encoding="utf-8") as f:
        data = json.load(f)

    updated = False
    modules = data.get("modules", [])
    for source in modules[0].get("sources", []):
        if (
            source.get("type") == "git"
            and source.get("url") == "https://github.com/wger-project/flutter"
        ):
            source["tag"] = new_version
            updated = True
            break

    if not updated:
        raise ValueError("Source entry https://github.com/wger-project/flutter not found")

    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bump-wger-version.py <x.y.z>")
        sys.exit(1)

    version = sys.argv[1]
    update_wger_version("flatpak-flutter.json", version)
    print(f"Version updated to {version}.")