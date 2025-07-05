import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta
import time
import random
from typing import List, Dict, Optional
import requests.exceptions

class GitHubScraper:
    """
    A scraper for GitHub trending repositories and repository analysis.
    Uses requests_html and BeautifulSoup for web scraping.
    """
    
    def __init__(self):
        self.session = HTMLSession()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.base_url = "https://github.com"
        self.max_retries = 3
        self.retry_delay = 2
        
    def scrape_trending(self, language: Optional[str] = None, time_range: str = "daily") -> List[Dict]:
        """
        Scrape trending repositories from GitHub trending page with retry logic.
        
        Args:
            language: Programming language filter (e.g., 'python', 'javascript')
            time_range: Time range filter ('daily', 'weekly', 'monthly')
            
        Returns:
            List of dictionaries containing repository information
        """
        for attempt in range(self.max_retries):
            try:
                print(f"Attempting to scrape GitHub trending (attempt {attempt + 1}/{self.max_retries})...")
                
                # Construct URL
                url = f"{self.base_url}/trending"
                params = {"since": time_range}
                
                if language:
                    url += f"/{language}"
                
                print(f"Fetching: {url}")
                
                # Make request with timeout
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                print(f"Successfully fetched page (status: {response.status_code})")
                
                # Parse HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find repository containers
                repo_containers = soup.find_all('article', class_='Box-row')
                
                if not repo_containers:
                    # Try alternative selectors
                    repo_containers = soup.find_all('div', class_='Box-row')
                
                print(f"Found {len(repo_containers)} repository containers")
                
                if not repo_containers:
                    print("No repository containers found. Page structure may have changed.")
                    if attempt < self.max_retries - 1:
                        print(f"Retrying in {self.retry_delay} seconds...")
                        time.sleep(self.retry_delay)
                        continue
                    return []
                
                repositories = []
                
                for i, container in enumerate(repo_containers):
                    try:
                        repo_data = self._extract_repo_data(container)
                        if repo_data:
                            repositories.append(repo_data)
                            print(f"Extracted data for repository {i+1}: {repo_data.get('name', 'Unknown')}")
                        
                        # Add small delay to be respectful
                        time.sleep(random.uniform(0.1, 0.3))
                        
                    except Exception as e:
                        print(f"Error extracting data from container {i+1}: {e}")
                        continue
                
                print(f"Successfully extracted {len(repositories)} repositories")
                return repositories
                
            except requests.exceptions.RequestException as e:
                print(f"Network error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    print("Max retries reached. Network request failed.")
                    
            except Exception as e:
                print(f"Unexpected error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    print("Max retries reached. Scraping failed.")
        
        return []
    
    def _extract_repo_data(self, container) -> Optional[Dict]:
        """Extract repository data from a trending repository container with robust selectors."""
        try:
            repo_data = {}
            
            # Get repository name and URL - try multiple selectors
            title_elem = container.find('h2', class_='h3') or container.find('h1') or container.find('h2')
            if title_elem:
                link = title_elem.find('a')
                if link:
                    repo_name = link.get_text().strip().replace('\n', '').replace(' ', '')
                    # Clean up the repository name
                    repo_name = re.sub(r'\s+', '', repo_name)
                    repo_data['name'] = repo_name
                    
                    href = link.get('href', '')
                    if href.startswith('/'):
                        repo_data['url'] = f"{self.base_url}{href}"
                    else:
                        repo_data['url'] = href
            
            # Get description - try multiple selectors
            desc_elem = (container.find('p', class_='col-9') or 
                        container.find('p', class_='color-fg-muted') or
                        container.find('p'))
            if desc_elem:
                desc_text = desc_elem.get_text().strip()
                repo_data['description'] = desc_text if desc_text else "No description available"
            else:
                repo_data['description'] = "No description available"
            
            # Get language - try multiple selectors
            lang_elem = (container.find('span', {'itemprop': 'programmingLanguage'}) or
                        container.find('span', class_='color-fg-default'))
            if lang_elem:
                repo_data['language'] = lang_elem.get_text().strip()
            else:
                repo_data['language'] = "Unknown"
            
            # Get stars and forks - try multiple approaches
            repo_data['stars'] = 0
            repo_data['forks'] = 0
            
            # Method 1: Look for links with specific hrefs
            stats_links = container.find_all('a')
            for link in stats_links:
                href = link.get('href', '')
                text = link.get_text().strip()
                
                if '/stargazers' in href or 'star' in href.lower():
                    repo_data['stars'] = self._parse_number(text)
                elif '/forks' in href or 'fork' in href.lower():
                    repo_data['forks'] = self._parse_number(text)
            
            # Method 2: Look for spans with specific text patterns
            if repo_data['stars'] == 0:
                star_elements = container.find_all('span')
                for elem in star_elements:
                    text = elem.get_text().strip()
                    if any(indicator in text.lower() for indicator in ['star', '⭐']):
                        repo_data['stars'] = self._parse_number(text)
                        break
            
            if repo_data['forks'] == 0:
                fork_elements = container.find_all('span')
                for elem in fork_elements:
                    text = elem.get_text().strip()
                    if any(indicator in text.lower() for indicator in ['fork', '🍴']):
                        repo_data['forks'] = self._parse_number(text)
                        break
            
            # Get today's stars - try multiple selectors
            repo_data['stars_today'] = 0
            today_indicators = ['stars today', 'today', 'stars this week', 'this week']
            
            for elem in container.find_all(['span', 'div']):
                text = elem.get_text().strip().lower()
                if any(indicator in text for indicator in today_indicators):
                    repo_data['stars_today'] = self._parse_number(elem.get_text())
                    break
            
            # Get contributors - try multiple approaches
            contributors = []
            
            # Method 1: Look for "Built by" text
            built_by_elem = container.find('span', string=re.compile(r'Built by', re.I))
            if built_by_elem:
                # Look for avatar links after "Built by"
                parent = built_by_elem.parent
                if parent:
                    contributor_imgs = parent.find_all('img', alt=True)
                    for img in contributor_imgs[:5]:
                        alt_text = img.get('alt', '')
                        if alt_text.startswith('@'):
                            contributors.append(alt_text[1:])  # Remove @ symbol
            
            # Method 2: Look for avatar images in the container
            if not contributors:
                avatar_imgs = container.find_all('img', alt=lambda x: x and x.startswith('@'))
                for img in avatar_imgs[:5]:
                    alt_text = img.get('alt', '')
                    if alt_text.startswith('@'):
                        contributors.append(alt_text[1:])
            
            repo_data['contributors'] = ', '.join(contributors) if contributors else "N/A"
            
            # Validate that we have at least the basic required fields
            if not repo_data.get('name') or not repo_data.get('url'):
                print(f"Missing essential data for repository: {repo_data}")
                return None
            
            return repo_data
            
        except Exception as e:
            print(f"Error extracting repository data: {e}")
            return None
    
    def _parse_number(self, text: str) -> int:
        """Parse number from text, handling k/m suffixes."""
        try:
            # Remove commas and extra spaces
            text = text.replace(',', '').strip()
            
            # Handle k/m suffixes
            if text.endswith('k'):
                return int(float(text[:-1]) * 1000)
            elif text.endswith('m'):
                return int(float(text[:-1]) * 1000000)
            else:
                # Extract just the number part
                number_match = re.search(r'\d+', text)
                if number_match:
                    return int(number_match.group())
                return 0
        except:
            return 0
    
    def analyze_repository(self, repo_url: str) -> Dict:
        """
        Analyze a specific GitHub repository for detailed information.
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Dictionary containing detailed repository analysis
        """
        try:
            # Extract owner and repo name from URL
            parts = repo_url.rstrip('/').split('/')
            if len(parts) < 2:
                return {}
            
            owner = parts[-2]
            repo_name = parts[-1]
            
            # Get main repository page
            response = self.session.get(repo_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            repo_data = {
                'name': f"{owner}/{repo_name}",
                'url': repo_url,
                'owner': owner,
                'repo_name': repo_name
            }
            
            # Get basic stats
            self._extract_repo_stats(soup, repo_data)
            
            # Get recent commits
            repo_data['recent_commits'] = self._get_recent_commits(owner, repo_name)
            
            # Get top contributors
            repo_data['top_contributors'] = self._get_top_contributors(owner, repo_name)
            
            # Get issues count
            repo_data['open_issues'] = self._get_issues_count(owner, repo_name)
            
            return repo_data
            
        except Exception as e:
            print(f"Error analyzing repository: {e}")
            return {}
    
    def _extract_repo_stats(self, soup: BeautifulSoup, repo_data: Dict):
        """Extract basic repository statistics."""
        try:
            # Get stars, forks, watchers
            stats_links = soup.find_all('a', class_='Link--primary')
            
            for link in stats_links:
                href = link.get('href', '')
                text = link.get_text().strip()
                
                if '/stargazers' in href:
                    repo_data['stars'] = self._parse_number(text)
                elif '/forks' in href:
                    repo_data['forks'] = self._parse_number(text)
                elif '/watchers' in href:
                    repo_data['watchers'] = self._parse_number(text)
            
            # Get language
            lang_elem = soup.find('span', {'itemprop': 'programmingLanguage'})
            if lang_elem:
                repo_data['language'] = lang_elem.get_text().strip()
            
            # Get description
            desc_elem = soup.find('p', {'itemprop': 'about'})
            if desc_elem:
                repo_data['description'] = desc_elem.get_text().strip()
            
            # Get repository size (approximate)
            size_elem = soup.find('span', string=re.compile(r'MB|KB|GB'))
            if size_elem:
                size_text = size_elem.get_text().strip()
                repo_data['size'] = self._parse_size(size_text)
            
        except Exception as e:
            print(f"Error extracting repository stats: {e}")
    
    def _parse_size(self, size_text: str) -> int:
        """Parse repository size to KB."""
        try:
            size_match = re.search(r'(\d+\.?\d*)\s*(KB|MB|GB)', size_text)
            if size_match:
                number = float(size_match.group(1))
                unit = size_match.group(2)
                
                if unit == 'KB':
                    return int(number)
                elif unit == 'MB':
                    return int(number * 1024)
                elif unit == 'GB':
                    return int(number * 1024 * 1024)
            return 0
        except:
            return 0
    
    def _get_recent_commits(self, owner: str, repo_name: str) -> List[Dict]:
        """Get recent commits for the repository."""
        try:
            commits_url = f"{self.base_url}/{owner}/{repo_name}/commits"
            response = self.session.get(commits_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            commits = []
            commit_items = soup.find_all('div', class_='Box-row')[:10]  # Get last 10 commits
            
            for item in commit_items:
                commit_data = {}
                
                # Get commit message
                msg_elem = item.find('a', {'data-pjax': True})
                if msg_elem:
                    commit_data['message'] = msg_elem.get_text().strip()
                
                # Get author
                author_elem = item.find('a', class_='commit-author')
                if author_elem:
                    commit_data['author'] = author_elem.get_text().strip()
                
                # Get date
                time_elem = item.find('relative-time')
                if time_elem:
                    commit_data['date'] = time_elem.get('datetime', '')
                
                if commit_data:
                    commits.append(commit_data)
            
            return commits
            
        except Exception as e:
            print(f"Error getting recent commits: {e}")
            return []
    
    def _get_top_contributors(self, owner: str, repo_name: str) -> List[Dict]:
        """Get top contributors for the repository."""
        try:
            contributors_url = f"{self.base_url}/{owner}/{repo_name}/graphs/contributors"
            response = self.session.get(contributors_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            contributors = []
            contributor_items = soup.find_all('li', class_='contrib-person')[:10]  # Top 10
            
            for item in contributor_items:
                contributor_data = {}
                
                # Get username
                username_elem = item.find('a', class_='text-normal')
                if username_elem:
                    contributor_data['username'] = username_elem.get_text().strip()
                
                # Get commit count
                commits_elem = item.find('span', class_='num')
                if commits_elem:
                    contributor_data['commits'] = commits_elem.get_text().strip()
                
                if contributor_data:
                    contributors.append(contributor_data)
            
            return contributors
            
        except Exception as e:
            print(f"Error getting top contributors: {e}")
            return []
    
    def _get_issues_count(self, owner: str, repo_name: str) -> int:
        """Get open issues count for the repository."""
        try:
            issues_url = f"{self.base_url}/{owner}/{repo_name}/issues"
            response = self.session.get(issues_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for issues count
            issues_elem = soup.find('span', {'id': 'issues-repo-tab-count'})
            if issues_elem:
                return self._parse_number(issues_elem.get_text().strip())
            
            return 0
            
        except Exception as e:
            print(f"Error getting issues count: {e}")
            return 0
