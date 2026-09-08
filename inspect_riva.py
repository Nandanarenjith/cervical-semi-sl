import json
from pathlib import Path

# ---------------------------------------------------------
# RIVA dataset location
# ---------------------------------------------------------

BASE_DIR = Path("riva_1.0")
ANNOTATION_FILE = BASE_DIR / "annotations" / "annotations.json"
IMAGE_DIR = BASE_DIR / "images"

# ---------------------------------------------------------
# Basic checks
# ---------------------------------------------------------

print("=" * 70)
print("RIVA DATASET INSPECTION")
print("=" * 70)

print(f"\nDataset folder:")
print(BASE_DIR.resolve())

print(f"\nAnnotation file:")
print(ANNOTATION_FILE.resolve())

print(f"\nImage folder:")
print(IMAGE_DIR.resolve())

if not ANNOTATION_FILE.exists():
    print("\nERROR: annotations.json was not found.")
    raise SystemExit

if not IMAGE_DIR.exists():
    print("\nERROR: images folder was not found.")
    raise SystemExit

# ---------------------------------------------------------
# Count images
# ---------------------------------------------------------

image_files = list(IMAGE_DIR.glob("*.png"))

print("\n" + "-" * 70)
print("IMAGE INFORMATION")
print("-" * 70)

print(f"PNG images found: {len(image_files)}")

# ---------------------------------------------------------
# Load annotations.json
# ---------------------------------------------------------

print("\n" + "-" * 70)
print("ANNOTATION FILE")
print("-" * 70)

with open(ANNOTATION_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Top-level Python type: {type(data).__name__}")

if isinstance(data, dict):
    print("Top-level keys:")
    for key in data.keys():
        print(f"  - {key}")

elif isinstance(data, list):
    print(f"Number of top-level entries: {len(data)}")

# ---------------------------------------------------------
# Inspect structure recursively
# ---------------------------------------------------------

def describe_structure(obj, level=0, max_level=3):
    indent = "  " * level

    if level > max_level:
        return

    if isinstance(obj, dict):
        print(f"{indent}dict with {len(obj)} keys")

        for key, value in list(obj.items())[:20]:
            print(f"{indent}  KEY: {key}")
            print(f"{indent}  TYPE: {type(value).__name__}")

            if isinstance(value, (dict, list)):
                describe_structure(value, level + 1, max_level)

    elif isinstance(obj, list):
        print(f"{indent}list with {len(obj)} items")

        if len(obj) > 0:
            print(f"{indent}first item:")
            describe_structure(obj[0], level + 1, max_level)

    else:
        print(f"{indent}{type(obj).__name__}: {repr(obj)[:200]}")


print("\n" + "-" * 70)
print("ANNOTATION STRUCTURE")
print("-" * 70)

describe_structure(data)

# ---------------------------------------------------------
# Print a small sample
# ---------------------------------------------------------

print("\n" + "-" * 70)
print("SAMPLE ANNOTATION DATA")
print("-" * 70)

if isinstance(data, dict):

    for key, value in list(data.items())[:5]:

        print(f"\nKEY: {key}")

        if isinstance(value, (dict, list)):
            print(json.dumps(value, indent=2)[:3000])
        else:
            print(repr(value))

elif isinstance(data, list):

    for i, item in enumerate(data[:3]):
        print(f"\nENTRY {i + 1}:")
        print(json.dumps(item, indent=2)[:3000])

# ---------------------------------------------------------
# Inspect filename class prefixes
# ---------------------------------------------------------

print("\n" + "-" * 70)
print("IMAGE FILENAME PREFIXES")
print("-" * 70)

prefixes = {}

for image in image_files:

    # Example:
    # HSIL_14_7.png
    # ASCUS_2_3.png
    #
    # The first part before "_" is extracted here.

    parts = image.stem.split("_")

    if parts:
        prefix = parts[0]
        prefixes[prefix] = prefixes.get(prefix, 0) + 1

print("\nCounts based ONLY on the first filename prefix:")

for prefix, count in sorted(prefixes.items()):
    print(f"  {prefix}: {count}")

print("\n" + "=" * 70)
print("INSPECTION COMPLETE")
print("=" * 70)