# www.wangfuk.org
Archive of www.wangfuk.org

## Basic info
Homepage: http://www.wangfuk.org:80/html/home/index.asp

## Browsertrix Crawl Analysis

This repository includes tools for analyzing web crawls from Browsertrix:

- **`analyze_browsertrix.py`** - Python script to fetch and analyze Browsertrix crawl data from replay.json endpoints
- **`BROWSERTRIX_ANALYSIS.md`** - Detailed documentation on the analysis approach and results
- **`sample_replay.json`** - Example replay.json data for testing
- **`requirements-analysis.txt`** - Python dependencies

### Quick Start

```bash
# Install dependencies
pip install -r requirements-analysis.txt

# Analyze collection metadata
python analyze_browsertrix.py "https://app.browsertrix.com/api/orgs/{org_id}/collections/{collection_id}/public/replay.json"

# Analyze with full page list (recommended)
python analyze_browsertrix.py {url} --fetch-pages --output report.txt --json data.json
```

### Real Collection Analysis

Successfully analyzed the www.wangfuk.org Browsertrix collection:
- **944 pages** crawled (7.3 GB total)
- **Content:** 837 PDFs, 63 videos, 28 HTML pages, 16 images
- **Success rate:** 99.7% (941/944 pages)

For detailed results and more information, see [BROWSERTRIX_ANALYSIS.md](BROWSERTRIX_ANALYSIS.md).
