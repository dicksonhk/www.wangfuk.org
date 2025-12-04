# www.wangfuk.org

Archive of www.wangfuk.org

## Basic info

Homepage: http://www.wangfuk.org:80/html/home/index.asp

## Web Crawler

This repository includes tools to crawl the website and create WARC files suitable for uploading to the Internet Archive.

### Quick Start (Shell Script)

The simplest way to crawl the website using `wget`:

```bash
# Make the script executable
chmod +x crawl.sh

# Run the crawler (output to ./archive directory)
./crawl.sh

# Or specify a custom output directory
./crawl.sh /path/to/output
```

**Requirements:** wget 1.14+ with WARC support

### Python Crawler

For more control and flexibility, use the Python crawler:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the crawler
python crawl.py

# With options
python crawl.py --output-dir ./my-archive --delay 2.0 --max-depth 5
```

**Options:**

- `--output-dir`, `-o`: Output directory for WARC files (default: `./archive`)
- `--max-depth`, `-d`: Maximum crawl depth, 0 for unlimited (default: 0)
- `--delay`: Delay between requests in seconds (default: 1.0)

### Output Files

Both crawlers output:

- **WARC file** (`www.wangfuk.org-YYYYMMDDHHMMSS.warc.gz`): Web ARChive format, the standard for web archiving
- **CDX file** (`www.wangfuk.org-YYYYMMDDHHMMSS.cdx`): Index file for the WARC

### Uploading to Internet Archive

1. Create an account at https://archive.org
2. Get your API keys from https://archive.org/account/s3.php
3. Install the Internet Archive CLI: `pip install internetarchive`
4. Configure your credentials: `ia configure`
5. Upload the WARC file:
   ```bash
   ia upload www-wangfuk-org-archive www.wangfuk.org-*.warc.gz \
       --metadata="collection:opensource" \
       --metadata="mediatype:web" \
       --metadata="title:www.wangfuk.org Archive"
   ```

Or use the web upload interface at https://archive.org/upload/

### WARC Format

The WARC (Web ARChive) format is an ISO standard (ISO 28500:2017) used by:

- Internet Archive's Wayback Machine
- Library of Congress
- National libraries worldwide
- Archive-It
- Common Crawl

WARC files preserve:
- Original HTTP headers
- Response bodies (HTML, images, CSS, JS, etc.)
- Request/response metadata
- Timestamps
