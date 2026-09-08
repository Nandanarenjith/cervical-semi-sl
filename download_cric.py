import requests
from pathlib import Path
import time

# ============================================================
# CRIC Cervix Figshare Collection
# ============================================================

COLLECTION_ID = 4960286

# Your project folder
BASE_DIR = Path.home() / "Documents" / "cervical-semi-sl" / "cric_cervix"

IMAGE_DIR = BASE_DIR / "images"
METADATA_DIR = BASE_DIR / "metadata"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. Get ALL articles from the Figshare collection
# ============================================================

print("=" * 70)
print("FETCHING CRIC CERVIX COLLECTION")
print("=" * 70)

all_articles = []

page = 1
page_size = 100

while True:

    url = f"https://api.figshare.com/v2/collections/{COLLECTION_ID}/articles"

    params = {
        "page": page,
        "page_size": page_size
    }

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()

    articles = response.json()

    print(f"Page {page}: found {len(articles)} articles")

    if not articles:
        break

    all_articles.extend(articles)

    if len(articles) < page_size:
        break

    page += 1


print()
print(f"TOTAL ARTICLES FOUND: {len(all_articles)}")


# ============================================================
# 2. Get the actual files belonging to every article
# ============================================================

print()
print("=" * 70)
print("GETTING FILE INFORMATION")
print("=" * 70)

all_files = []

for i, article in enumerate(all_articles, start=1):

    article_id = article["id"]
    title = article.get("title", "")

    print(f"[{i}/{len(all_articles)}] {title}")

    article_url = f"https://api.figshare.com/v2/articles/{article_id}"

    response = requests.get(article_url, timeout=60)
    response.raise_for_status()

    article_data = response.json()

    for file_info in article_data.get("files", []):

        all_files.append({
            "article_id": article_id,
            "article_title": title,
            "name": file_info["name"],
            "download_url": file_info["download_url"],
            "size": file_info["size"]
        })


print()
print(f"TOTAL FILES FOUND: {len(all_files)}")


# ============================================================
# 3. Separate metadata and image files
# ============================================================

metadata_files = []
image_files = []

for file_info in all_files:

    filename = file_info["name"].lower()

    if filename.endswith((".csv", ".json", ".md")):
        metadata_files.append(file_info)

    elif filename.endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff")):
        image_files.append(file_info)


print()
print("=" * 70)
print("FILE SUMMARY")
print("=" * 70)

print(f"Metadata files: {len(metadata_files)}")
print(f"Image files:    {len(image_files)}")


# ============================================================
# 4. Download function
# ============================================================

def download_file(file_info, destination):

    filename = file_info["name"]
    filepath = destination / filename

    # Don't download something that already exists
    if filepath.exists():

        existing_size = filepath.stat().st_size

        if existing_size == file_info["size"]:
            print(f"    Already exists: {filename}")
            return

        else:
            print(f"    Existing file has different size. Re-downloading.")


    print(f"    Downloading: {filename}")

    try:

        response = requests.get(
            file_info["download_url"],
            stream=True,
            timeout=120
        )

        response.raise_for_status()

        with open(filepath, "wb") as f:

            for chunk in response.iter_content(
                chunk_size=1024 * 1024
            ):

                if chunk:
                    f.write(chunk)

        print(f"    Done: {filename}")

    except Exception as e:

        print(f"    ERROR downloading {filename}")
        print(f"    {e}")


# ============================================================
# 5. Download metadata
# ============================================================

print()
print("=" * 70)
print("DOWNLOADING METADATA")
print("=" * 70)

for file_info in metadata_files:

    download_file(
        file_info,
        METADATA_DIR
    )

    time.sleep(0.5)


# ============================================================
# 6. Download images
# ============================================================

print()
print("=" * 70)
print("DOWNLOADING CRIC IMAGES")
print("=" * 70)

for i, file_info in enumerate(image_files, start=1):

    print()
    print(f"IMAGE {i}/{len(image_files)}")

    download_file(
        file_info,
        IMAGE_DIR
    )

    time.sleep(0.5)


# ============================================================
# 7. Final summary
# ============================================================

print()
print("=" * 70)
print("DOWNLOAD COMPLETE")
print("=" * 70)

print(f"CRIC folder:")
print(BASE_DIR)

print()
print(f"Images:")
print(IMAGE_DIR)

print()
print(f"Metadata:")
print(METADATA_DIR)

print()
print(f"Expected image files: {len(image_files)}")
print(f"Expected metadata files: {len(metadata_files)}")