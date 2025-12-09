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

## Automated Crawling with GitHub Actions

This repository includes a GitHub Actions workflow that automatically crawls the website and uploads the archive as artifacts.

### Manual Execution

To manually trigger the crawler workflow:

1. Go to the **Actions** tab in the GitHub repository
2. Select the **Crawl and Archive Website** workflow
3. Click **Run workflow**
4. Optionally configure:
   - **Max depth**: Maximum crawl depth (0 for unlimited)
   - **Delay**: Delay between requests in seconds
5. Click **Run workflow** to start

### Scheduled Execution

The workflow automatically runs every Sunday at 2 AM UTC to create weekly archives.

### Workflow Outputs

The workflow generates three types of artifacts:

1. **WARC Archive** (`warc-archive-*`): The compressed WARC file containing all crawled content
2. **CDX Index** (`cdx-index-*`): Index file for the WARC archive
3. **Crawl Log** (`crawl-log-*`): Detailed log of the crawling process
4. **Complete Archive** (`complete-archive-*`): Bundle containing all files above

All artifacts are retained for 90 days (logs for 30 days) and can be downloaded from the workflow run page.

### Downloading Artifacts

1. Go to the **Actions** tab
2. Click on a completed workflow run
3. Scroll to the **Artifacts** section at the bottom
4. Click on an artifact to download it
