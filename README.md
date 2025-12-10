# www.wangfuk.org
Archive of www.wangfuk.org

## Basic info
Homepage: http://www.wangfuk.org:80/html/home/index.asp

## Web Archive Format Overview

This repository uses web archiving formats developed by the [Webrecorder](https://webrecorder.net) project. Understanding the structure and relationships between WARC, WACZ, and related files is essential for working with web archives.

### WARC (Web ARChive)

**WARC** is the foundational file format for web archives, standardized as [ISO 28500:2017](https://www.iso.org/standard/68004.html).

- **Purpose**: Stores the raw archived web content - HTTP requests, responses, headers, and payloads
- **Format**: Plain text container format with concatenated records
- **File Extension**: `.warc` or `.warc.gz` (compressed)
- **Structure**: Each WARC record contains:
  - WARC header (metadata like record type, URL, timestamp)
  - HTTP headers
  - HTTP response body (HTML, CSS, JavaScript, images, etc.)

**Example WARC Record:**
```
WARC/1.0
WARC-Type: response
WARC-Target-URI: http://www.example.com/
WARC-Date: 2020-10-07T21:22:36Z
Content-Type: application/http; msgtype=response
Content-Length: 1234

HTTP/1.1 200 OK
Content-Type: text/html

<html>...</html>
```

### WACZ (Web Archive Collection Zipped)

**WACZ** is a packaging format that bundles WARC files with metadata and indexes for efficient web-based replay.

- **Purpose**: Package web archives for distribution and browser-based replay
- **Format**: ZIP file with standardized directory structure
- **File Extension**: `.wacz`
- **Specification**: [WACZ Format Spec v1.2.0](https://specs.webrecorder.net/wacz/latest/)

**WACZ Directory Structure:**
```
myarchive.wacz (ZIP file)
├── archive/
│   └── data.warc.gz          # WARC files with archived content
├── indexes/
│   └── index.cdx.gz          # CDXJ index for URL lookup
├── pages/
│   └── pages.jsonl           # Page list with metadata
├── datapackage.json          # Manifest and metadata
└── datapackage-digest.json   # Verification hash
```

**Key Components:**

1. **`archive/`** - Contains one or more WARC files with the actual archived web content

2. **`indexes/`** - CDXJ (CDX JSON) index files that allow quick URL lookups without scanning entire WARC files
   - Format: JSON Lines with URL, timestamp, WARC file location, and byte offsets
   - Enables efficient random access to archived resources

3. **`pages/pages.jsonl`** - List of entry point pages in JSON Lines format
   - Each line represents a page with `url`, `ts` (timestamp), and optional `title`, `id`, `text`
   - Used by replay systems to show a navigation menu

4. **`datapackage.json`** - Frictionless Data Package manifest containing:
   - Collection metadata (title, description, creation date)
   - List of all files with their paths, sizes, and SHA-256 hashes
   - Optional `home` object specifying the initial page to display
   - Profile: `"wacz"` to identify WACZ format

5. **`datapackage-digest.json`** - Contains SHA-256 hash of `datapackage.json` for integrity verification

### Pages and Replay Configuration

**pages.jsonl** serves as the primary navigation index for replaying web archives:

**Format (JSON Lines):**
```json
{"format": "json-pages-1.0", "id": "pages", "title": "All Pages"}
{"id": "1db0ef709a", "url": "https://www.example.com/page", "ts": "2020-10-07T21:22:36Z", "title": "Example Domain"}
{"id": "12304e6ba9", "url": "https://www.example.com/another", "ts": "2020-10-07T21:23:36Z", "title": "Another Page"}
```

**Fields:**
- `url` - Page URL (required)
- `ts` - RFC3339 timestamp when page was archived (required)
- `title` - Human-readable page title
- `id` - Unique identifier
- `text` - Extracted text for search
- `size` - Total size in bytes including resources

### How They Work Together

1. **Archiving Flow:**
   ```
   Live Web → Browser Capture → WARC Files
   ```

2. **Packaging Flow:**
   ```
   WARC Files → Index Generation → Add Metadata → Create WACZ ZIP
   ```

3. **Replay Flow:**
   ```
   WACZ File → Read datapackage.json → Load pages.jsonl → 
   User selects page → Lookup in CDXJ index → 
   Read specific bytes from WARC → Render in browser
   ```

### Efficient Random Access

WACZ enables efficient browser-based replay without downloading entire archives:

1. Browser reads ZIP directory to locate files
2. Loads `datapackage.json` and `pages.jsonl` for metadata
3. Loads compressed CDXJ index
4. When user requests a page:
   - Binary search in CDXJ index for URL+timestamp
   - Uses byte offset to fetch only needed WARC records via HTTP Range requests
   - Decompresses and renders the specific content

This allows viewing large web archives (GBs) by downloading only KBs of index data and the specific pages being viewed.

### Tools and Ecosystem

- **[py-wacz](https://github.com/webrecorder/py-wacz)** - Create and validate WACZ files from WARC
- **[ReplayWeb.page](https://replayweb.page)** - Browser-based WACZ viewer (no server needed)
- **[ArchiveWeb.page](https://github.com/webrecorder/archiveweb.page)** - Browser extension for creating web archives
- **[Browsertrix Crawler](https://github.com/webrecorder/browsertrix-crawler)** - High-fidelity web crawler
- **[warcio](https://github.com/webrecorder/warcio)** - Python library for reading/writing WARC files
- **[wabac.js](https://github.com/webrecorder/wabac.js)** - JavaScript library for web archive replay

### References

- [WACZ Format Specification](https://specs.webrecorder.net/wacz/latest/)
- [CDXJ Format Specification](https://specs.webrecorder.net/cdxj/latest/)
- [WARC ISO Standard](https://www.iso.org/standard/68004.html)
- [Webrecorder Specifications](https://github.com/webrecorder/specs)
- [Frictionless Data Package](https://specs.frictionlessdata.io/data-package/)
