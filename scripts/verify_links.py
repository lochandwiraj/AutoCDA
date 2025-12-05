import requests
from pathlib import Path
import re

def extract_links_from_readme():
    """Extract all URLs from README"""
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        print("❌ README.md not found")
        return []
    
    content = readme_path.read_text()
    
    # Extract markdown links and raw URLs
    md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    raw_urls = re.findall(r'https?://[^\s\)]+', content)
    
    all_urls = [url for _, url in md_links] + raw_urls
    return list(set(all_urls))

def verify_links(urls):
    """Check if all links are accessible"""
    print(f"🔗 Verifying {len(urls)} links...\n")
    
    failed = []
    
    for url in urls:
        # Skip localhost URLs
        if "localhost" in url or "127.0.0.1" in url:
            print(f"⏭️  SKIPPED (localhost): {url}")
            continue
        
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            
            if response.status_code < 400:
                print(f"✅ OK: {url}")
            else:
                print(f"❌ FAILED ({response.status_code}): {url}")
                failed.append((url, response.status_code))
            
        except requests.exceptions.RequestException as e:
            print(f"❌ ERROR: {url}")
            print(f"   {str(e)[:100]}")
            failed.append((url, "ERROR"))
    
    print("\n" + "="*60)
    if failed:
        print(f"❌ {len(failed)} links failed:")
        for url, status in failed:
            print(f"   - {url} ({status})")
        return False
    else:
        print("✅ All links are working!")
        return True

if __name__ == "__main__":
    urls = extract_links_from_readme()
    
    if not urls:
        print("⚠️  No links found in README")
    else:
        verify_links(urls)
