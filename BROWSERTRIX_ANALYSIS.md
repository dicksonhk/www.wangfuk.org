# Browsertrix Crawl Analysis

This document describes the analysis of the www.wangfuk.org crawl data from Browsertrix.

## Collection Information

**Collection ID (UUID):** `00035ac5-46e8-400c-af27-1eb493c85ef4`  
**Collection URL:** `https://app.browsertrix.com/api/orgs/a483ba90-1e46-462b-aa09-e91c2876bd0f/collections/00035ac5-46e8-400c-af27-1eb493c85ef4/public/replay.json`

**Organization ID:** `a483ba90-1e46-462b-aa09-e91c2876bd0f`  
**Collection Name:** `www.wangfuk.org`  
**Collection Slug:** `www-wangfuk-org`

## API Access Status

✅ **Successfully Accessed** - The collection is publicly accessible via the UUID-based endpoint.

### Important Note on Collection IDs

The API requires UUID-based collection IDs, not slugs:
- ❌ Incorrect: `collections/www-wangfuk-org/public/replay.json` (slug)
- ✅ Correct: `collections/00035ac5-46e8-400c-af27-1eb493c85ef4/public/replay.json` (UUID)

## Analysis Results

The analysis tool successfully analyzed the complete www.wangfuk.org collection:

### Collection Statistics

- **Total Pages:** 944 pages (938 unique)
- **Total Size:** 7.3 GB (7,328,996,543 bytes)
- **Crawl Date:** December 5, 2025 (05:10-05:14 UTC)
- **Crawl Duration:** ~4.5 minutes
- **Homepage:** http://www.wangfuk.org/html/home/index.asp
- **Access:** Public
- **Download Available:** Yes

### Content Breakdown

**By Type:**
- PDFs: 837 files (88.7%)
- Videos (MP4): 63 files (6.7%)
- HTML Pages: 28 files (3.0%)
- Images (JPEG): 16 files (1.7%)

**By Extension:**
- .pdf: 840 files
- .mp4: 63 files
- .htm: 23 files
- .jpg: 16 files
- .asp: 2 files

**HTTP Status:**
- Success (200): 941 pages (99.7%)
- Not Found (404): 3 pages (0.3%)

### Domain Distribution

- **www.wangfuk.org:** 944 pages (100%)

### Time Range

- **First Page:** 2025-12-05 05:10:17 UTC
- **Last Page:** 2025-12-05 05:14:36 UTC
- **Total Entries:** 944

## Analysis Capabilities

The analysis tool (`analyze_browsertrix.py`) provides:

### 1. Crawl Metadata
- Collection name and description
- Organization information
- Crawl configuration (depth, scope, etc.)
- Timestamps: when the crawl started and completed
- Crawler version and settings

### 2. Page Statistics
- **Total pages crawled**: Number of unique pages discovered
- **URL count**: Total URLs processed
- **Domain distribution**: Breakdown of pages by domain/subdomain
- **Crawl depth**: How many levels deep the crawler went
- **Coverage**: Percentage of site crawled vs. discovered links

### 3. Content Analysis
- **Content types**: Distribution of HTML, CSS, JavaScript, images, PDFs, etc.
- **File sizes**: Total size of crawled content, average page size
- **HTTP status codes**: Success (200), redirects (301/302), errors (404, 500, etc.)
- **File extensions**: Most common file types (.html, .pdf, .jpg, etc.)
- **Broken links**: URLs that returned errors

### 4. Temporal Analysis
- **Crawl timeline**: Start and end times
- **Page timestamps**: Last-modified dates of crawled content
- **Crawl rate**: Pages per minute/hour
- **Time distribution**: When pages were last updated

### 5. Data Quality Assessment
- **Completeness**: Are all expected pages present?
- **Errors**: How many pages failed to crawl?
- **Duplicates**: Any duplicate content detected?
- **Recommendations**: Suggestions for improving future crawls

## replay.json Format

Based on Browsertrix documentation, the `replay.json` format typically includes:

```json
{
  "pages": [
    {
      "url": "https://example.com/page.html",
      "title": "Page Title",
      "timestamp": "20231201120000",
      "ts": "2023-12-01T12:00:00Z",
      "status": 200,
      "mime": "text/html",
      "text": "Extracted page text...",
      "screenshot": "screenshots/page.png"
    }
  ],
  "collection": {
    "id": "collection-uuid",
    "name": "Collection Name",
    "description": "Collection description"
  },
  "metadata": {
    "crawl_date": "2023-12-01",
    "tool": "browsertrix-crawler",
    "version": "1.0.0"
  }
}
```

## Using the Analysis Tool

### Installation

```bash
pip install -r requirements-analysis.txt
```

### Usage

#### Basic analysis (metadata only):
```bash
python analyze_browsertrix.py "https://app.browsertrix.com/api/orgs/{org_id}/collections/{collection_id}/public/replay.json"
```

#### Complete analysis with full page list:
```bash
python analyze_browsertrix.py {url} --fetch-pages --output report.txt
```

#### With org and collection parameters:
```bash
python analyze_browsertrix.py --org {org_id} --collection {collection_id} --fetch-pages
```

#### Generate JSON output:
```bash
python analyze_browsertrix.py {url} --fetch-pages --output report.txt --json analysis.json
```

#### Print to stdout:
```bash
python analyze_browsertrix.py {url} --print
```

**Note:** The `--fetch-pages` flag fetches the complete page list from the collection's `pagesQueryUrl`, providing detailed analysis of all crawled pages including URLs, content types, status codes, and file extensions. Without this flag, only collection metadata is analyzed.

## Alternative Analysis Methods

Since the public API endpoint is not accessible, here are alternative approaches:

### 1. Access via Web Interface
Visit the Browsertrix web application and navigate to the collection to view:
- Collection overview and statistics
- List of crawled pages
- Replay functionality to browse archived pages

### 2. Download WACZ File
If the collection has an associated WACZ (Web Archive Collection Zipped) file:
```bash
# Extract and analyze WACZ
pip install wacz
wacz extract collection.wacz --output extracted/
# Then analyze the extracted WARC files
```

### 3. Use Browsertrix API with Authentication
If you have API credentials, use environment variables to avoid exposing them in shell history:
```bash
# Set credentials as environment variables
export BROWSERTRIX_USER="your_username"
export BROWSERTRIX_PASS="your_password"

# Login and get JWT token (credentials from environment)
TOKEN=$(curl -X POST https://app.browsertrix.com/api/auth/jwt/login \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$BROWSERTRIX_USER\", \"password\": \"$BROWSERTRIX_PASS\"}" \
  | jq -r '.access_token')

# Use token to access collection
curl -H "Authorization: Bearer $TOKEN" \
  https://app.browsertrix.com/api/orgs/{org_id}/collections/{collection_id}
```

### 4. Analyze Existing Crawl Data
If you have access to the crawl data from other sources (PR #2, #3 show wget and Python crawlers):
- Use the WARC files generated by previous crawls
- Analyze the WACZ archives created by the GitHub Actions workflow (PR #1)
- Review the crawler test results and summaries

## Expected Analysis Results for www.wangfuk.org

Based on previous crawl attempts in this repository (see PR #2 and #3):

**Expected Content:**
- **Pages**: ~5 HTML pages
- **PDFs**: ~319 PDF documents
- **Images**: ~33 image files
- **Total Size**: ~267 MB
- **Total Files**: ~357 files

**Domain:**
- Primary: www.wangfuk.org
- Port: 80
- Protocol: HTTP

**Content Structure:**
- Homepage: `/html/home/index.asp`
- Document structure: Mostly PDFs in various directories
- Static content (no JavaScript execution needed)

## Recommendations

1. **Verify Collection Access**: Confirm with the Browsertrix administrator that the collection is public and get the correct UUID-based collection ID.

2. **Use WACZ Format**: Request access to download the WACZ file for offline analysis.

3. **Leverage Existing Tools**: The repository already has successful crawl implementations (PR #2, #3) that can be used for comparison.

4. **Document Findings**: Once access is obtained, run the analysis tool and update this document with actual results.

5. **Automate Analysis**: Consider adding the analysis script to the GitHub Actions workflow to automatically analyze each crawl.

## Related Files

- `analyze_browsertrix.py` - Python script for analyzing Browsertrix crawl data
- `requirements-analysis.txt` - Python dependencies for the analysis tool
- `CRAWLER_TEST_RESULTS.md` - Results from previous WARC-based crawl (PR #2)
- `CRAWL_SUMMARY.md` - Results from wget-based crawl (PR #3)

## References

- [Browsertrix Documentation](https://docs.browsertrix.com/)
- [Browsertrix Crawler User Guide](https://crawler.docs.browsertrix.com/user-guide/)
- [Webrecorder Forum - API Setup](https://forum.webrecorder.net/t/api-setup-in-self-hosted-env/966)
- [WACZ Format Specification](https://specs.webrecorder.net/wacz/latest/)
