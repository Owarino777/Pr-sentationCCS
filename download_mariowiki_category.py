#!/usr/bin/env python3
"""
Download files from MediaWiki categories and pages.

This script supports:
- MediaWiki categories
- MediaWiki article pages
- retry/backoff
- Windows-safe filenames
- extension filtering
- resume-safe downloads

Usage:
    python download_mariowiki_category.py
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


API_URL = "https://www.mariowiki.com/api.php"

CATEGORY_TITLES = [
    "Category:Super Mario Bros. assets",
]

PAGE_TITLES = [
    "New Super Mario Bros. 2",
    "New Super Mario Bros.",
]

OUTPUT_DIR = Path("mariowiki_assets")

REQUEST_TIMEOUT_SECONDS = 12
CATEGORY_PAGE_SIZE = 50
PAGE_IMAGE_LIMIT = 50
IMAGEINFO_BATCH_SIZE = 25
DOWNLOAD_DELAY_SECONDS = 0.75

ALLOWED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    ),
    "Accept": "application/json,text/plain,*/*",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Referer": "https://www.mariowiki.com/",
    "Connection": "close",
}


def sanitize_filename(filename: str) -> str:
    """Return a Windows-safe filename."""
    filename = unquote(filename)
    filename = filename.replace("/", "_").replace("\\", "_")
    filename = re.sub(r'[<>:"|?*]', "_", filename)
    filename = re.sub(r"\s+", " ", filename).strip()
    return filename


def create_session() -> requests.Session:
    """Create an HTTP session with retries."""
    retry = Retry(
        total=8,
        connect=8,
        read=8,
        status=8,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )

    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=1,
        pool_maxsize=1,
    )

    session = requests.Session()
    session.headers.update(HEADERS)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


def get_json_with_retry(
    session: requests.Session,
    params: dict[str, Any],
) -> dict[str, Any]:
    """Fetch JSON with explicit retry for blocked or unstable networks."""
    last_error: Exception | None = None

    for attempt in range(1, 9):
        try:
            response = session.get(
                API_URL,
                params=params,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            return response.json()

        except requests.RequestException as error:
            last_error = error
            wait_seconds = min(2 ** attempt, 30)
            print(f"[RETRY {attempt}/8] API indisponible, nouvel essai dans {wait_seconds}s")
            time.sleep(wait_seconds)

    raise RuntimeError(f"API request failed after retries: {last_error}") from last_error


def get_category_file_titles(
    session: requests.Session,
    category_title: str,
) -> list[str]:
    """Fetch every file title from a MediaWiki category."""
    titles: list[str] = []
    continuation: dict[str, str] = {}

    while True:
        params: dict[str, Any] = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": category_title,
            "cmtype": "file",
            "cmlimit": CATEGORY_PAGE_SIZE,
            **continuation,
        }

        payload = get_json_with_retry(session, params)
        members = payload.get("query", {}).get("categorymembers", [])

        for member in members:
            title = member.get("title")
            if title:
                titles.append(title)

        if "continue" not in payload:
            break

        continuation = payload["continue"]
        time.sleep(0.5)

    return titles


def get_page_file_titles(
    session: requests.Session,
    page_title: str,
) -> list[str]:
    """Fetch every image/file title used directly by a MediaWiki page."""
    titles: list[str] = []
    continuation: dict[str, str] = {}

    while True:
        params: dict[str, Any] = {
            "action": "query",
            "format": "json",
            "generator": "images",
            "titles": page_title,
            "gimlimit": PAGE_IMAGE_LIMIT,
            "prop": "imageinfo",
            "iiprop": "url",
            **continuation,
        }

        payload = get_json_with_retry(session, params)
        pages = payload.get("query", {}).get("pages", {})

        for page in pages.values():
            title = page.get("title")
            if title and title.startswith("File:"):
                titles.append(title)

        if "continue" not in payload:
            break

        continuation = payload["continue"]
        time.sleep(0.5)

    return titles


def chunked(values: list[str], size: int) -> list[list[str]]:
    """Split a list into fixed-size chunks."""
    return [values[index:index + size] for index in range(0, len(values), size)]


def get_file_urls(
    session: requests.Session,
    titles: list[str],
) -> dict[str, str]:
    """Fetch original file URLs by batches."""
    urls: dict[str, str] = {}

    for batch_index, batch in enumerate(chunked(titles, IMAGEINFO_BATCH_SIZE), start=1):
        params = {
            "action": "query",
            "format": "json",
            "prop": "imageinfo",
            "iiprop": "url",
            "titles": "|".join(batch),
        }

        payload = get_json_with_retry(session, params)
        pages = payload.get("query", {}).get("pages", {})

        for page in pages.values():
            title = page.get("title")
            imageinfo = page.get("imageinfo", [])

            if not title or not imageinfo:
                continue

            url = imageinfo[0].get("url")
            if url:
                urls[title] = url

        print(f"[INFO] URLs récupérées : batch {batch_index}")
        time.sleep(0.75)

    return urls


def get_extension_from_title(title: str) -> str:
    """Return the file extension from a MediaWiki file title."""
    filename = title.removeprefix("File:")
    return Path(filename).suffix.lower()


def is_allowed_file(title: str) -> bool:
    """Return whether the file extension is safe enough for this project."""
    return get_extension_from_title(title) in ALLOWED_EXTENSIONS


def download_file(
    session: requests.Session,
    url: str,
    output_path: Path,
) -> None:
    """Download one file atomically."""
    temporary_path = output_path.with_suffix(output_path.suffix + ".part")
    last_error: Exception | None = None

    for attempt in range(1, 7):
        try:
            with session.get(url, stream=True, timeout=60) as response:
                response.raise_for_status()

                with temporary_path.open("wb") as file:
                    for chunk in response.iter_content(chunk_size=1024 * 128):
                        if chunk:
                            file.write(chunk)

            temporary_path.replace(output_path)
            return

        except requests.RequestException as error:
            last_error = error
            wait_seconds = min(2 ** attempt, 20)
            print(f"[RETRY {attempt}/6] Téléchargement échoué, nouvel essai dans {wait_seconds}s")
            time.sleep(wait_seconds)

        finally:
            if temporary_path.exists() and not output_path.exists():
                temporary_path.unlink(missing_ok=True)

    raise RuntimeError(f"Download failed after retries: {url}") from last_error


def collect_all_titles(session: requests.Session) -> list[str]:
    """Collect unique file titles from configured categories and pages."""
    all_titles: list[str] = []

    for category_title in CATEGORY_TITLES:
        print(f"[INFO] Catégorie : {category_title}")
        category_titles = get_category_file_titles(session, category_title)
        print(f"[INFO] {len(category_titles)} fichier(s) trouvé(s) dans la catégorie.")
        all_titles.extend(category_titles)

    for page_title in PAGE_TITLES:
        print(f"[INFO] Page : {page_title}")
        page_titles = get_page_file_titles(session, page_title)
        print(f"[INFO] {len(page_titles)} fichier(s) trouvé(s) sur la page.")
        all_titles.extend(page_titles)

    unique_titles = sorted(set(all_titles))
    allowed_titles = [title for title in unique_titles if is_allowed_file(title)]

    skipped_count = len(unique_titles) - len(allowed_titles)

    print(f"[INFO] Total unique : {len(unique_titles)} fichier(s).")
    print(f"[INFO] Conservés : {len(allowed_titles)} fichier(s) image.")
    print(f"[INFO] Ignorés : {skipped_count} fichier(s) hors extensions autorisées.")

    return allowed_titles


def main() -> None:
    """Run the full download process."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    session = create_session()

    print("[INFO] Récupération de la liste des fichiers...")
    titles = collect_all_titles(session)

    print("[INFO] Récupération des URLs réelles...")
    urls = get_file_urls(session, titles)

    print(f"[INFO] {len(urls)} URL(s) récupérée(s).")

    for index, title in enumerate(titles, start=1):
        url = urls.get(title)

        if not url:
            print(f"[SKIP] URL introuvable : {title}")
            continue

        filename = sanitize_filename(title.removeprefix("File:"))
        output_path = OUTPUT_DIR / filename

        if output_path.exists():
            print(f"[{index}/{len(titles)}] Déjà présent : {filename}")
            continue

        try:
            print(f"[{index}/{len(titles)}] Téléchargement : {filename}")
            download_file(session, url, output_path)
            time.sleep(DOWNLOAD_DELAY_SECONDS)

        except RuntimeError as error:
            print(f"[ERROR] {filename} : {error}")

    print(f"[DONE] Dossier : {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()