#!/bin/bash
# Crawl www.wangfuk.org into specified output directory
# Usage: ./crawl.sh [output_directory]

set -e

if ! command -v wget &> /dev/null; then
  echo "Error: wget is required but not installed." >&2
  exit 1
fi

OUTPUT_DIR="${1:-output}"

mkdir -p "$OUTPUT_DIR"

# Note: Using HTTP as the source site only supports HTTP on port 80
wget \
  --recursive \
  --no-parent \
  --page-requisites \
  --convert-links \
  --adjust-extension \
  --directory-prefix="$OUTPUT_DIR" \
  --no-host-directories \
  --wait=1 \
  --random-wait \
  http://www.wangfuk.org:80/html/home/index.asp
