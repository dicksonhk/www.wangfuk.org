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
LOG_FILE="${WARC_PREFIX}-${TIMESTAMP}.log"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Set up logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$OUTPUT_DIR/$LOG_FILE"
}

log "=============================================="
log "Web Crawler for www.wangfuk.org"
log "=============================================="
log "Start URL: $START_URL"
log "Domain: $DOMAIN"
log "Output Directory: $OUTPUT_DIR"
log "WARC Prefix: ${WARC_PREFIX}-${TIMESTAMP}"
log "Log File: $OUTPUT_DIR/$LOG_FILE"
log "=============================================="
log ""

# Check if wget is available
if ! command -v wget &> /dev/null; then
    log "ERROR: wget is not installed. Please install wget first."
    log "  On Ubuntu/Debian: sudo apt-get install wget"
    log "  On macOS: brew install wget"
    exit 1
fi

log "Checking wget version..."
WGET_VERSION=$(wget --version | head -n1)
log "Found: $WGET_VERSION"

# Check wget version supports WARC
if ! wget --help 2>&1 | grep -q "warc"; then
    log "WARNING: Your version of wget may not support WARC output."
    log "Please install wget 1.14 or later for WARC support."
fi

log "Starting crawl..."
log ""

# Run wget with WARC output
# Options explained:
#   --warc-file: Output to WARC format (Internet Archive compatible)
#   --warc-cdx: Also generate CDX index file
#   --recursive: Follow links
#   --level=inf: Unlimited recursion depth
#   --page-requisites: Get all assets (images, CSS, JS)
#   --convert-links: Convert links for offline viewing
#   --html-extension: Add .html extension to HTML files
#   --domains: Limit to specified domain
#   --no-parent: Don't ascend to parent directory
#   --wait: Wait between requests (be polite)
#   --random-wait: Randomize wait time
#   --tries: Number of retries
#   --timeout: Connection timeout
#   --user-agent: Identify as archiving bot

cd "$OUTPUT_DIR"

log "Running wget with the following parameters:"
log "  WARC file: ${WARC_PREFIX}-${TIMESTAMP}"
log "  Domain: $DOMAIN"
log "  Start URL: $START_URL"
log ""

# Run wget and capture its output to both screen and log
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
    --show-progress \
    "$START_URL" 2>&1 | tee -a "$LOG_FILE"

WGET_EXIT_CODE=${PIPESTATUS[0]}

log ""
log "Wget finished with exit code: $WGET_EXIT_CODE"
log ""
log "=============================================="
log "Crawl completed!"
log "=============================================="
log ""
log "Output files in $OUTPUT_DIR:"

# List and log the created files
if ls "$OUTPUT_DIR"/*.warc* 1> /dev/null 2>&1; then
    ls -lh "$OUTPUT_DIR"/*.warc* 2>/dev/null | tee -a "$LOG_FILE"
    
    # Count files created
    WARC_COUNT=$(ls -1 "$OUTPUT_DIR"/*.warc* 2>/dev/null | wc -l)
    log ""
    log "Total WARC files created: $WARC_COUNT"
else
    log "No WARC files found"
fi

if ls "$OUTPUT_DIR"/*.cdx 1> /dev/null 2>&1; then
    ls -lh "$OUTPUT_DIR"/*.cdx 2>/dev/null | tee -a "$LOG_FILE"
fi

log ""
log "To upload to Internet Archive:"
log "  1. Create an account at https://archive.org"
log "  2. Get API keys from https://archive.org/account/s3.php"
log "  3. Use ia CLI tool: ia upload <identifier> ${WARC_PREFIX}-${TIMESTAMP}.warc.gz"
log ""
log "Or use the web interface:"
log "  Upload WARC files at https://archive.org/upload/"
log ""

exit $WGET_EXIT_CODE
