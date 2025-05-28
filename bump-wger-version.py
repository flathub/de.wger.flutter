import json
import sys

def update_flutter_version(filename: str, new_version: str):
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
    update_flutter_version("flatpak-flutter.json", version)
    print(f"Version updated to {version}.")