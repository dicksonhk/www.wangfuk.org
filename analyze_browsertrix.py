#!/usr/bin/env python3
"""
Browsertrix Crawl Analyzer

This script fetches and analyzes crawl data from a Browsertrix collection.
It parses the replay.json endpoint to extract metadata about crawled pages
and generates a comprehensive analysis report.

Usage:
    python analyze_browsertrix.py <replay_json_url> [--output <file>]
    python analyze_browsertrix.py --org <org_id> --collection <collection_name> [--output <file>]

Example:
    python analyze_browsertrix.py "https://app.browsertrix.com/api/orgs/a483ba90-1e46-462b-aa09-e91c2876bd0f/collections/www-wangfuk-org/public/replay.json"
"""

import argparse
import json
import sys
from datetime import datetime
from urllib.parse import urlparse
from collections import Counter
import requests


class BrowsertrixAnalyzer:
    """Analyzes Browsertrix crawl data from replay.json endpoint."""

    def __init__(self, url, fetch_pages=False):
        """Initialize with replay.json URL."""
        self.url = url
        self.data = None
        self.analysis = {}
        self.fetch_pages = fetch_pages
        self.pages_data = []

    def fetch_data(self):
        """Fetch data from the Browsertrix replay.json endpoint."""
        print(f"Fetching data from: {self.url}")
        
        try:
            # Try direct API access
            response = requests.get(self.url, timeout=30)
            response.raise_for_status()
            
            # Check if we got JSON
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                self.data = response.json()
                print("✓ Successfully fetched JSON data")
                return True
            else:
                print(f"✗ Unexpected content type: {content_type}")
                print("Response appears to be HTML, not JSON API response")
                
                # Try to extract collection ID and suggest alternative
                parsed = urlparse(self.url)
                path_parts = parsed.path.split('/')
                if 'orgs' in path_parts and 'collections' in path_parts:
                    org_idx = path_parts.index('orgs')
                    coll_idx = path_parts.index('collections')
                    if org_idx + 1 < len(path_parts) and coll_idx + 1 < len(path_parts):
                        org_id = path_parts[org_idx + 1]
                        collection_name = path_parts[coll_idx + 1]
                        print(f"\nDetected:")
                        print(f"  Organization ID: {org_id}")
                        print(f"  Collection: {collection_name}")
                        print("\nNote: The provided URL may require authentication or may not be a public API endpoint.")
                        print("Consider accessing the Browsertrix web interface or using authenticated API calls.")
                
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching data: {e}")
            return False

    def fetch_all_pages(self):
        """Fetch all pages from the pagesQueryUrl if available."""
        # Return True if not requested - not an error condition
        if not self.fetch_pages:
            return True
        
        if not self.data:
            return False
        
        pages_url = self.data.get('pagesQueryUrl')
        if not pages_url:
            print("ℹ No pagesQueryUrl found in collection metadata")
            return False
        
        print(f"Fetching page list from: {pages_url}")
        all_pages = []
        page_num = 1
        page_size = 100
        max_pages = 1000  # Safety limit to prevent infinite loops
        
        try:
            while page_num <= max_pages:
                url = f"{pages_url}?page={page_num}&pageSize={page_size}"
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                items = data.get('items', [])
                
                # Stop if no items returned
                if not items:
                    break
                
                all_pages.extend(items)
                print(f"  Fetched page {page_num} ({len(items)} items, total so far: {len(all_pages)})")
                
                # If we got fewer items than page_size, we've reached the end
                if len(items) < page_size:
                    break
                
                page_num += 1
            
            if page_num > max_pages:
                print(f"⚠ Reached maximum page limit ({max_pages}), stopping pagination")
            
            self.pages_data = all_pages
            print(f"✓ Successfully fetched {len(all_pages)} pages")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching pages: {e}")
            return False

    def parse_pages(self):
        """Parse page data from the replay.json structure."""
        # If we fetched pages separately, use that data
        if self.pages_data:
            return self.pages_data
        
        if not self.data:
            return []
        
        # Browsertrix replay.json typically has a 'pages' array
        pages = self.data.get('pages', [])
        
        # Also check for other possible structures
        if not pages:
            # Sometimes data might be nested differently
            if 'resources' in self.data:
                pages = self.data['resources']
            elif isinstance(self.data, list):
                pages = self.data
        
        return pages

    def analyze(self):
        """Perform comprehensive analysis of the crawl data."""
        if not self.data:
            print("No data available to analyze.")
            return False
        
        pages = self.parse_pages()
        
        # Basic statistics
        self.analysis['total_pages'] = len(pages)
        self.analysis['crawl_metadata'] = {
            k: v for k, v in self.data.items() 
            if k not in ['pages', 'resources'] and not isinstance(v, list)
        }
        
        if not pages:
            print("Warning: No pages found in the data structure.")
            print("Data keys:", list(self.data.keys()))
            return True
        
        # Analyze URLs
        urls = []
        domains = []
        timestamps = []
        content_types = Counter()
        statuses = Counter()
        
        for page in pages:
            # Extract URL
            url = page.get('url', page.get('uri', ''))
            if url:
                urls.append(url)
                parsed = urlparse(url)
                domains.append(parsed.netloc)
            
            # Extract timestamp
            ts = page.get('timestamp', page.get('ts', ''))
            if ts:
                timestamps.append(ts)
            
            # Extract content type
            mime = page.get('mime', page.get('content-type', ''))
            if mime:
                content_types[mime] += 1
            
            # Extract status
            status = page.get('status', '')
            if status:
                statuses[status] += 1
        
        self.analysis['urls_crawled'] = len(urls)
        self.analysis['unique_domains'] = len(set(domains))
        self.analysis['domain_distribution'] = dict(Counter(domains).most_common(10))
        self.analysis['content_types'] = dict(content_types)
        self.analysis['http_statuses'] = dict(statuses)
        
        if timestamps:
            self.analysis['time_range'] = {
                'first': min(timestamps),
                'last': max(timestamps),
                'total_timestamps': len(timestamps)
            }
        
        # URL path analysis
        paths = [urlparse(url).path for url in urls]
        path_extensions = []
        for path in paths:
            if '.' in path:
                ext = path.split('.')[-1].lower()
                path_extensions.append(ext)
        
        if path_extensions:
            self.analysis['file_extensions'] = dict(Counter(path_extensions).most_common(10))
        
        return True

    def generate_report(self):
        """Generate a human-readable analysis report."""
        if not self.analysis:
            return "No analysis data available."
        
        lines = []
        lines.append("=" * 80)
        lines.append("BROWSERTRIX CRAWL ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Source: {self.url}")
        lines.append("")
        
        # Metadata
        if self.analysis.get('crawl_metadata'):
            lines.append("CRAWL METADATA")
            lines.append("-" * 80)
            for key, value in self.analysis['crawl_metadata'].items():
                lines.append(f"  {key}: {value}")
            lines.append("")
        
        # Overview
        lines.append("OVERVIEW")
        lines.append("-" * 80)
        lines.append(f"  Total Pages: {self.analysis.get('total_pages', 0)}")
        lines.append(f"  URLs Crawled: {self.analysis.get('urls_crawled', 0)}")
        lines.append(f"  Unique Domains: {self.analysis.get('unique_domains', 0)}")
        lines.append("")
        
        # Time range
        if 'time_range' in self.analysis:
            lines.append("TIME RANGE")
            lines.append("-" * 80)
            tr = self.analysis['time_range']
            lines.append(f"  First: {tr.get('first', 'N/A')}")
            lines.append(f"  Last: {tr.get('last', 'N/A')}")
            lines.append(f"  Entries with timestamps: {tr.get('total_timestamps', 0)}")
            lines.append("")
        
        # Domain distribution
        if 'domain_distribution' in self.analysis:
            lines.append("TOP DOMAINS")
            lines.append("-" * 80)
            for domain, count in self.analysis['domain_distribution'].items():
                lines.append(f"  {domain}: {count} pages")
            lines.append("")
        
        # Content types
        if 'content_types' in self.analysis:
            lines.append("CONTENT TYPES")
            lines.append("-" * 80)
            for ctype, count in sorted(self.analysis['content_types'].items(), 
                                       key=lambda x: x[1], reverse=True):
                lines.append(f"  {ctype}: {count}")
            lines.append("")
        
        # HTTP statuses
        if 'http_statuses' in self.analysis:
            lines.append("HTTP STATUS CODES")
            lines.append("-" * 80)
            for status, count in sorted(self.analysis['http_statuses'].items()):
                lines.append(f"  {status}: {count}")
            lines.append("")
        
        # File extensions
        if 'file_extensions' in self.analysis:
            lines.append("FILE EXTENSIONS")
            lines.append("-" * 80)
            for ext, count in self.analysis['file_extensions'].items():
                lines.append(f"  .{ext}: {count}")
            lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)

    def save_report(self, filename):
        """Save the analysis report to a file."""
        report = self.generate_report()
        with open(filename, 'w') as f:
            f.write(report)
        print(f"✓ Report saved to: {filename}")

    def save_json(self, filename):
        """Save the raw analysis data as JSON."""
        with open(filename, 'w') as f:
            json.dump(self.analysis, f, indent=2)
        print(f"✓ Analysis data saved to: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze Browsertrix crawl data from replay.json endpoint',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        'url',
        nargs='?',
        help='Direct URL to replay.json endpoint'
    )
    parser.add_argument(
        '--org',
        help='Organization ID (alternative to providing full URL)'
    )
    parser.add_argument(
        '--collection',
        help='Collection name or ID (alternative to providing full URL)'
    )
    parser.add_argument(
        '--output',
        '-o',
        default='browsertrix_analysis.txt',
        help='Output file for analysis report (default: browsertrix_analysis.txt)'
    )
    parser.add_argument(
        '--json',
        help='Save analysis data as JSON to specified file'
    )
    parser.add_argument(
        '--print',
        action='store_true',
        help='Print report to stdout instead of saving to file'
    )
    parser.add_argument(
        '--fetch-pages',
        action='store_true',
        help='Fetch complete page list from pagesQueryUrl for detailed analysis'
    )
    
    args = parser.parse_args()
    
    # Construct URL
    if args.url:
        url = args.url
    elif args.org and args.collection:
        # Construct URL from org and collection
        url = f"https://app.browsertrix.com/api/orgs/{args.org}/collections/{args.collection}/public/replay.json"
    else:
        parser.error("Either provide URL directly or use --org and --collection")
    
    # Create analyzer and fetch data
    analyzer = BrowsertrixAnalyzer(url, fetch_pages=args.fetch_pages)
    
    if not analyzer.fetch_data():
        print("\n" + "=" * 80)
        print("ALTERNATIVE: Analysis with Mock Data")
        print("=" * 80)
        print("\nSince the endpoint is not accessible, here's what the analysis would include:")
        print("\n1. CRAWL METADATA")
        print("   - Collection name and ID")
        print("   - Organization information")
        print("   - Crawl timestamp and duration")
        print("   - Crawler configuration")
        print("\n2. PAGE STATISTICS")
        print("   - Total pages crawled")
        print("   - Unique URLs discovered")
        print("   - Domain distribution")
        print("   - Crawl depth information")
        print("\n3. CONTENT ANALYSIS")
        print("   - Content types (HTML, CSS, JS, images, etc.)")
        print("   - File size distribution")
        print("   - HTTP status code summary")
        print("   - Error pages and broken links")
        print("\n4. TEMPORAL ANALYSIS")
        print("   - Crawl start and end times")
        print("   - Page modification timestamps")
        print("   - Crawl rate over time")
        print("\n5. RECOMMENDATIONS")
        print("   - Data quality assessment")
        print("   - Coverage analysis")
        print("   - Suggested improvements for future crawls")
        print("\nTo use this tool with actual data, ensure:")
        print("- The Browsertrix collection is set to public")
        print("- You have the correct API endpoint URL")
        print("- You have necessary authentication if required")
        sys.exit(1)
    
    # Fetch all pages if requested
    if args.fetch_pages:
        analyzer.fetch_all_pages()
    
    # Perform analysis
    if not analyzer.analyze():
        print("Analysis completed but no detailed data available.")
        sys.exit(1)
    
    # Output results
    if args.print:
        print("\n" + analyzer.generate_report())
    else:
        analyzer.save_report(args.output)
    
    if args.json:
        analyzer.save_json(args.json)
    
    print("\n✓ Analysis complete!")


if __name__ == '__main__':
    main()
