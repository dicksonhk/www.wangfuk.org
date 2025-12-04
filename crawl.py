#!/usr/bin/env python3
"""
Web Crawler for www.wangfuk.org

This script crawls the website www.wangfuk.org and outputs WARC files
suitable for uploading to the Internet Archive.

Requirements:
    pip install warcio requests beautifulsoup4 lxml

Usage:
    python crawl.py [--output-dir ./archive] [--max-depth 0]

Output:
    - WARC file: www.wangfuk.org-YYYYMMDDHHMMSS.warc.gz
    - CDX index: www.wangfuk.org-YYYYMMDDHHMMSS.cdx
"""

import argparse
import gzip
import hashlib
import os
import re
import sys
import time
import uuid
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse, urlunparse

try:
    import requests
    from bs4 import BeautifulSoup
    from warcio.statusandheaders import StatusAndHeaders
    from warcio.warcwriter import WARCWriter
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("Install requirements with: pip install warcio requests beautifulsoup4 lxml")
    sys.exit(1)


class WebCrawler:
    """Web crawler that outputs WARC files for Internet Archive."""

    # Base URL and domain configuration
    START_URL = "http://www.wangfuk.org:80/html/home/index.asp"
    ALLOWED_DOMAINS = {"www.wangfuk.org"}

    # User agent for polite crawling
    USER_AGENT = "Mozilla/5.0 (compatible; ArchiveBot/1.0; +https://archive.org)"

    def __init__(self, output_dir="./archive", max_depth=0, delay=1.0):
        """
        Initialize the crawler.

        Args:
            output_dir: Directory to save WARC files
            max_depth: Maximum crawl depth (0 = unlimited)
            delay: Delay between requests in seconds
        """
        self.output_dir = output_dir
        self.max_depth = max_depth
        self.delay = delay
        self.visited = set()
        self.to_visit = []  # Queue of (url, depth) tuples
        self.session = requests.Session()
        self.session.headers["User-Agent"] = self.USER_AGENT

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Generate output filenames
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.warc_filename = os.path.join(
            output_dir, f"www.wangfuk.org-{timestamp}.warc.gz"
        )
        self.cdx_filename = os.path.join(
            output_dir, f"www.wangfuk.org-{timestamp}.cdx"
        )

        print(f"Output WARC: {self.warc_filename}")
        print(f"Output CDX:  {self.cdx_filename}")

    def normalize_url(self, url):
        """Normalize URL for deduplication."""
        parsed = urlparse(url)
        # Normalize scheme and netloc to lowercase
        # Remove default port 80 for http
        netloc = parsed.netloc.lower()
        if netloc.endswith(":80") and parsed.scheme == "http":
            netloc = netloc[:-3]
        # Rebuild URL with normalized components
        normalized = urlunparse(
            (
                parsed.scheme.lower(),
                netloc,
                parsed.path or "/",
                parsed.params,
                parsed.query,
                "",  # Remove fragment
            )
        )
        return normalized

    def is_allowed_url(self, url):
        """Check if URL is within allowed domains."""
        try:
            parsed = urlparse(url)
            # Must be http or https
            if parsed.scheme not in ("http", "https"):
                return False
            # Must be in allowed domains
            domain = parsed.netloc.lower()
            if domain.endswith(":80"):
                domain = domain[:-3]
            return domain in self.ALLOWED_DOMAINS
        except Exception:
            return False

    def extract_links(self, html, base_url):
        """Extract all links from HTML content."""
        links = set()
        try:
            soup = BeautifulSoup(html, "lxml")

            # Extract href links
            for tag in soup.find_all(href=True):
                href = tag.get("href", "")
                if href and not href.startswith(("#", "javascript:", "mailto:")):
                    full_url = urljoin(base_url, href)
                    links.add(full_url)

            # Extract src links (images, scripts, etc.)
            for tag in soup.find_all(src=True):
                src = tag.get("src", "")
                if src:
                    full_url = urljoin(base_url, src)
                    links.add(full_url)

            # Extract CSS url() references
            for style in soup.find_all("style"):
                if style.string:
                    urls = re.findall(r"url\(['\"]?([^'\")\s]+)['\"]?\)", style.string)
                    for url in urls:
                        full_url = urljoin(base_url, url)
                        links.add(full_url)

            # Extract link href (stylesheets)
            for link in soup.find_all("link", href=True):
                href = link.get("href", "")
                if href:
                    full_url = urljoin(base_url, href)
                    links.add(full_url)

        except Exception as e:
            print(f"  Warning: Error parsing HTML: {e}")

        return links

    def fetch_url(self, url):
        """Fetch a URL and return the response."""
        try:
            response = self.session.get(url, timeout=30, allow_redirects=True)
            return response
        except requests.RequestException as e:
            print(f"  Error fetching {url}: {e}")
            return None

    def write_warc_record(self, warc_writer, cdx_file, url, response):
        """Write a WARC record for the response."""
        try:
            # Create WARC record
            warc_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

            # HTTP status line
            http_status = f"HTTP/1.1 {response.status_code} {response.reason}"

            # Build headers list
            headers_list = []
            for key, value in response.headers.items():
                headers_list.append((key, value))

            status_and_headers = StatusAndHeaders(
                statusline=http_status,
                headers=headers_list,
                protocol="HTTP/1.1",
            )

            # Generate record ID
            record_id = f"<urn:uuid:{uuid.uuid4()}>"

            # Write response record
            record = warc_writer.create_warc_record(
                uri=url,
                record_type="response",
                payload=response.content,
                http_headers=status_and_headers,
            )
            warc_writer.write_record(record)

            # Write CDX entry
            content_type = response.headers.get("Content-Type", "-")
            content_length = len(response.content)
            digest = hashlib.sha1(response.content).hexdigest()
            cdx_entry = f"{url} {warc_date} {response.status_code} {content_type} {content_length} {digest}\n"
            cdx_file.write(cdx_entry)

        except Exception as e:
            print(f"  Error writing WARC record for {url}: {e}")

    def crawl(self):
        """Run the crawler."""
        print("\n" + "=" * 60)
        print("Web Crawler for www.wangfuk.org")
        print("=" * 60)
        print(f"Start URL: {self.START_URL}")
        print(f"Max Depth: {'Unlimited' if self.max_depth == 0 else self.max_depth}")
        print(f"Delay: {self.delay}s between requests")
        print("=" * 60 + "\n")

        # Initialize queue with start URL
        self.to_visit.append((self.START_URL, 0))

        # Open WARC and CDX files
        with gzip.open(self.warc_filename, "wb") as warc_output:
            warc_writer = WARCWriter(warc_output, gzip=False)

            # Write WARC info record
            info_record = warc_writer.create_warcinfo_record(
                filename=os.path.basename(self.warc_filename),
                info={
                    "software": "www.wangfuk.org crawler/1.0",
                    "format": "WARC File Format 1.1",
                    "conformsTo": "https://iipc.github.io/warc-specifications/",
                },
            )
            warc_writer.write_record(info_record)

            with open(self.cdx_filename, "w") as cdx_file:
                # Write CDX header
                cdx_file.write(
                    "!url !date !status !content-type !length !digest\n"
                )

                # Process queue
                crawled_count = 0
                while self.to_visit:
                    url, depth = self.to_visit.pop(0)

                    # Normalize and check if already visited
                    normalized_url = self.normalize_url(url)
                    if normalized_url in self.visited:
                        continue

                    # Check depth limit
                    if self.max_depth > 0 and depth > self.max_depth:
                        continue

                    # Check if URL is allowed
                    if not self.is_allowed_url(url):
                        continue

                    # Mark as visited
                    self.visited.add(normalized_url)
                    crawled_count += 1

                    print(f"[{crawled_count}] Crawling: {url}")

                    # Fetch URL
                    response = self.fetch_url(url)
                    if response is None:
                        continue

                    # Write WARC record
                    self.write_warc_record(warc_writer, cdx_file, url, response)

                    # If HTML, extract links
                    content_type = response.headers.get("Content-Type", "")
                    if "text/html" in content_type:
                        try:
                            html = response.content.decode(
                                response.encoding or "utf-8", errors="replace"
                            )
                            links = self.extract_links(html, url)
                            for link in links:
                                normalized_link = self.normalize_url(link)
                                if (
                                    normalized_link not in self.visited
                                    and self.is_allowed_url(link)
                                ):
                                    self.to_visit.append((link, depth + 1))
                        except Exception as e:
                            print(f"  Warning: Error extracting links: {e}")

                    # Be polite - wait between requests
                    if self.to_visit:
                        time.sleep(self.delay)

        print("\n" + "=" * 60)
        print("Crawl completed!")
        print("=" * 60)
        print(f"Total URLs crawled: {crawled_count}")
        print(f"WARC file: {self.warc_filename}")
        print(f"CDX file:  {self.cdx_filename}")
        print("\nTo upload to Internet Archive:")
        print("  1. Create an account at https://archive.org")
        print("  2. Get API keys from https://archive.org/account/s3.php")
        print(
            f"  3. Use ia CLI: ia upload <identifier> {os.path.basename(self.warc_filename)}"
        )
        print("\nOr use the web interface:")
        print("  Upload WARC files at https://archive.org/upload/")
        print("=" * 60 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Crawl www.wangfuk.org and output WARC files for Internet Archive"
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="./archive",
        help="Output directory for WARC files (default: ./archive)",
    )
    parser.add_argument(
        "--max-depth",
        "-d",
        type=int,
        default=0,
        help="Maximum crawl depth, 0 for unlimited (default: 0)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds (default: 1.0)",
    )

    args = parser.parse_args()

    crawler = WebCrawler(
        output_dir=args.output_dir, max_depth=args.max_depth, delay=args.delay
    )
    crawler.crawl()


if __name__ == "__main__":
    main()
