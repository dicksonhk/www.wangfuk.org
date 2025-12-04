#!/bin/bash
#
# Web Crawler for www.wangfuk.org
# Outputs WARC files suitable for Internet Archive upload
#
# Usage: ./crawl.sh [output_directory]
#

set -e

# Configuration
START_URL="http://www.wangfuk.org:80/html/home/index.asp"
DOMAIN="www.wangfuk.org"
OUTPUT_DIR="${1:-./archive}"
WARC_PREFIX="www.wangfuk.org"
TIMESTAMP=$(date +%Y%m%d%H%M%S)

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "=============================================="
echo "Web Crawler for www.wangfuk.org"
echo "=============================================="
echo "Start URL: $START_URL"
echo "Domain: $DOMAIN"
echo "Output Directory: $OUTPUT_DIR"
echo "WARC Prefix: ${WARC_PREFIX}-${TIMESTAMP}"
echo "=============================================="
echo ""

# Check if wget is available
if ! command -v wget &> /dev/null; then
    echo "Error: wget is not installed. Please install wget first."
    echo "  On Ubuntu/Debian: sudo apt-get install wget"
    echo "  On macOS: brew install wget"
    exit 1
fi

# Check wget version supports WARC
if ! wget --help 2>&1 | grep -q "warc"; then
    echo "Warning: Your version of wget may not support WARC output."
    echo "Please install wget 1.14 or later for WARC support."
fi

echo "Starting crawl..."
echo ""

# Run wget with WARC output
# Options explained:
#   --warc-file: Output to WARC format (Internet Archive compatible)
#   --warc-cdx: Also generate CDX index file
#   --recursive: Follow links
#   --level=inf: Unlimited recursion depth
#   --page-requisites: Get all assets (images, CSS, JS)
#   --convert-links: Convert links for offline viewing
#   --adjust-extension: Add .html extension to HTML files
#   --domains: Limit to specified domain
#   --no-parent: Don't ascend to parent directory
#   --wait: Wait between requests (be polite)
#   --random-wait: Randomize wait time
#   --tries: Number of retries
#   --timeout: Connection timeout
#   --user-agent: Identify as archiving bot

cd "$OUTPUT_DIR"

wget \
    --warc-file="${WARC_PREFIX}-${TIMESTAMP}" \
    --warc-cdx \
    --recursive \
    --level=inf \
    --page-requisites \
    --html-extension \
    --convert-links \
    --domains="$DOMAIN" \
    --no-parent \
    --wait=1 \
    --random-wait \
    --tries=3 \
    --timeout=30 \
    --user-agent="Mozilla/5.0 (compatible; ArchiveBot/1.0; +https://archive.org)" \
    --no-verbose \
    --show-progress \
    "$START_URL"

echo ""
echo "=============================================="
echo "Crawl completed!"
echo "=============================================="
echo ""
echo "Output files in $OUTPUT_DIR:"
ls -lh "$OUTPUT_DIR"/*.warc* 2>/dev/null || echo "  (WARC files will be in current directory)"
echo ""
echo "To upload to Internet Archive:"
echo "  1. Create an account at https://archive.org"
echo "  2. Get API keys from https://archive.org/account/s3.php"
echo "  3. Use ia CLI tool: ia upload <identifier> ${WARC_PREFIX}-${TIMESTAMP}.warc.gz"
echo ""
echo "Or use the web interface:"
echo "  Upload WARC files at https://archive.org/upload/"
echo ""
