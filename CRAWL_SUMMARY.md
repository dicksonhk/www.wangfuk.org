# Website Crawl Summary - www.wangfuk.org

**Date:** December 9, 2025  
**Source URL:** http://www.wangfuk.org:80/html/home/index.asp  
**Output Directory:** `output/`

## Crawl Statistics

### Overall Summary
- **Total Files Downloaded:** 357 files
- **Total Size:** 267 MB
- **Duration:** 7 minutes 18 seconds
- **Average Speed:** 31.2 MB/s

### Files by Content Type

| Content Type | Count | Total Size |
|-------------|-------|------------|
| PDF Documents | 319 files | 267 MB |
| JPEG Images | 31 files | ~200 KB |
| HTML Pages | 5 files | ~20 KB |
| GIF Images | 2 files | ~20 KB |

### Directory Structure

```
output/
└── html/
    ├── home/
    │   ├── doc/          (319 PDF files)
    │   └── images/       (31 JPEG files)
    └── images/           (2 GIF files)
```

### Content Breakdown

#### HTML Pages (5 files)
- index.asp.html (main homepage)
- index.htm
- index2.htm
- index3.htm
- inspection.asp.html

#### PDF Documents (319 files)
The crawl successfully downloaded 319 PDF documents from the `/html/home/doc/` directory, including:
- Building inspection notices
- Maintenance work schedules
- Repair engineering documents
- Window inspection records
- Air conditioning maintenance plans
- Property management documents
- Various official notices and reports

Documents range from 2024-06 to 2025-12, covering ongoing building maintenance and inspection activities.

#### Images (33 files)
- Navigation and UI images
- Property photos
- Icon files

## Technical Details

### wget Configuration Used
- `--recursive`: Followed all links recursively
- `--no-parent`: Prevented ascending to parent directories
- `--page-requisites`: Downloaded all CSS, images, and assets
- `--convert-links`: Converted links for local browsing
- `--adjust-extension`: Added appropriate file extensions
- `--wait=1 --random-wait`: Polite crawling with 1-second delays

### Crawl Notes
- One 404 error encountered: `2024-06-14 N001 拜神儀式1.pdf` (file not found on server)
- All links successfully converted for offline browsing
- Site structure preserved with proper directory hierarchy
- Chinese characters in filenames properly handled

## Browsing the Archive

To browse the archived site locally, open:
```
output/html/home/index.asp.html
```

All internal links have been converted to work offline.
