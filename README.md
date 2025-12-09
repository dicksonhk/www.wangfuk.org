# www.wangfuk.org
Archive of www.wangfuk.org

## Basic info
Homepage: http://www.wangfuk.org:80/html/home/index.asp

## Browsertrix Crawl Analysis

This repository includes tools for analyzing web crawls from Browsertrix:

- **`analyze_browsertrix.py`** - Python script to fetch and analyze Browsertrix crawl data from replay.json endpoints
- **`BROWSERTRIX_ANALYSIS.md`** - Detailed documentation on the analysis approach and expected results
- **`sample_replay.json`** - Example replay.json data for testing
- **`requirements-analysis.txt`** - Python dependencies

### Quick Start

```bash
# Install dependencies
pip install -r requirements-analysis.txt

# Analyze a Browsertrix collection
python analyze_browsertrix.py "https://app.browsertrix.com/api/orgs/{org_id}/collections/{collection_id}/public/replay.json"

# Test with sample data
python analyze_browsertrix.py --help
```

For more information, see [BROWSERTRIX_ANALYSIS.md](BROWSERTRIX_ANALYSIS.md).
