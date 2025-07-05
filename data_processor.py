import pandas as pd
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class DataProcessor:
    """
    Process and clean scraped GitHub data for analysis and visualization.
    """
    
    def __init__(self):
        pass
    
    def clean_trending_data(self, raw_data: List[Dict]) -> pd.DataFrame:
        """
        Clean and normalize trending repository data.
        
        Args:
            raw_data: List of raw repository dictionaries
            
        Returns:
            Cleaned pandas DataFrame
        """
        if not raw_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(raw_data)
        
        # Clean repository names
        if 'name' in df.columns:
            df['name'] = df['name'].str.strip().str.replace('\n', ' ')
        
        # Clean descriptions
        if 'description' in df.columns:
            df['description'] = df['description'].fillna('No description available')
            df['description'] = df['description'].str.strip()
        
        # Normalize language field
        if 'language' in df.columns:
            df['language'] = df['language'].fillna('Unknown')
            df['language'] = df['language'].str.strip()
        
        # Ensure numeric fields are properly formatted
        numeric_fields = ['stars', 'forks', 'stars_today']
        for field in numeric_fields:
            if field in df.columns:
                df[field] = pd.to_numeric(df[field], errors='coerce').fillna(0).astype(int)
        
        # Clean contributors field
        if 'contributors' in df.columns:
            df['contributors'] = df['contributors'].fillna('N/A')
        
        # Add calculated fields
        df['popularity_score'] = self._calculate_popularity_score(df)
        df['activity_level'] = self._categorize_activity_level(df)
        
        return df
    
    def _calculate_popularity_score(self, df: pd.DataFrame) -> pd.Series:
        """Calculate a popularity score based on stars, forks, and recent activity."""
        if 'stars' not in df.columns or 'forks' not in df.columns:
            return pd.Series([0] * len(df))
        
        # Weighted popularity score
        stars_weight = 0.7
        forks_weight = 0.2
        stars_today_weight = 0.1
        
        stars_normalized = df['stars'] / df['stars'].max() if df['stars'].max() > 0 else 0
        forks_normalized = df['forks'] / df['forks'].max() if df['forks'].max() > 0 else 0
        
        if 'stars_today' in df.columns:
            stars_today_normalized = df['stars_today'] / df['stars_today'].max() if df['stars_today'].max() > 0 else 0
        else:
            stars_today_normalized = 0
        
        popularity_score = (
            stars_normalized * stars_weight +
            forks_normalized * forks_weight +
            stars_today_normalized * stars_today_weight
        )
        
        return popularity_score * 100  # Scale to 0-100
    
    def _categorize_activity_level(self, df: pd.DataFrame) -> pd.Series:
        """Categorize repositories by activity level."""
        if 'stars_today' not in df.columns:
            return pd.Series(['Unknown'] * len(df))
        
        def categorize_activity(stars_today):
            if stars_today >= 100:
                return 'Very High'
            elif stars_today >= 50:
                return 'High'
            elif stars_today >= 20:
                return 'Medium'
            elif stars_today >= 5:
                return 'Low'
            else:
                return 'Very Low'
        
        return df['stars_today'].apply(categorize_activity)
    
    def filter_by_language(self, df: pd.DataFrame, language: str) -> pd.DataFrame:
        """Filter repositories by programming language."""
        if language.lower() == 'all' or not language:
            return df
        
        return df[df['language'].str.lower() == language.lower()]
    
    def filter_by_stars(self, df: pd.DataFrame, min_stars: int = 0, max_stars: int = None) -> pd.DataFrame:
        """Filter repositories by star count range."""
        filtered_df = df[df['stars'] >= min_stars]
        
        if max_stars is not None:
            filtered_df = filtered_df[filtered_df['stars'] <= max_stars]
        
        return filtered_df
    
    def get_top_repositories(self, df: pd.DataFrame, n: int = 10, sort_by: str = 'stars') -> pd.DataFrame:
        """Get top N repositories sorted by specified metric."""
        if sort_by not in df.columns:
            sort_by = 'stars'
        
        return df.nlargest(n, sort_by)
    
    def get_language_statistics(self, df: pd.DataFrame) -> Dict:
        """Get statistics about programming languages in the dataset."""
        if 'language' not in df.columns:
            return {}
        
        language_stats = {
            'total_languages': df['language'].nunique(),
            'language_distribution': df['language'].value_counts().to_dict(),
            'most_popular_language': df['language'].value_counts().index[0] if len(df) > 0 else 'Unknown',
            'languages_with_most_stars': df.groupby('language')['stars'].sum().sort_values(ascending=False).to_dict()
        }
        
        return language_stats
    
    def process_repository_analysis(self, repo_data: Dict) -> Dict:
        """
        Process and enhance repository analysis data.
        
        Args:
            repo_data: Raw repository analysis data
            
        Returns:
            Enhanced repository analysis data
        """
        if not repo_data:
            return {}
        
        processed_data = repo_data.copy()
        
        # Process commit data
        if 'recent_commits' in processed_data and processed_data['recent_commits']:
            processed_data['commit_analysis'] = self._analyze_commits(processed_data['recent_commits'])
        
        # Process contributor data
        if 'top_contributors' in processed_data and processed_data['top_contributors']:
            processed_data['contributor_analysis'] = self._analyze_contributors(processed_data['top_contributors'])
        
        # Calculate activity metrics
        processed_data['activity_metrics'] = self._calculate_activity_metrics(processed_data)
        
        return processed_data
    
    def _analyze_commits(self, commits: List[Dict]) -> Dict:
        """Analyze commit patterns and frequency."""
        if not commits:
            return {}
        
        commit_df = pd.DataFrame(commits)
        
        # Parse commit dates
        if 'date' in commit_df.columns:
            commit_df['parsed_date'] = pd.to_datetime(commit_df['date'], errors='coerce')
            commit_df = commit_df.dropna(subset=['parsed_date'])
            
            # Calculate commit frequency
            if len(commit_df) > 1:
                date_range = (commit_df['parsed_date'].max() - commit_df['parsed_date'].min()).days
                daily_commit_rate = len(commit_df) / max(date_range, 1)
            else:
                daily_commit_rate = 0
        else:
            daily_commit_rate = 0
        
        # Analyze commit messages
        commit_analysis = {
            'total_commits': len(commits),
            'daily_commit_rate': daily_commit_rate,
            'unique_authors': len(set(commit.get('author', '') for commit in commits)),
            'average_message_length': sum(len(commit.get('message', '')) for commit in commits) / len(commits),
            'commit_types': self._classify_commit_types(commits)
        }
        
        return commit_analysis
    
    def _classify_commit_types(self, commits: List[Dict]) -> Dict:
        """Classify commits by type based on commit messages."""
        commit_types = {
            'feature': 0,
            'fix': 0,
            'docs': 0,
            'style': 0,
            'refactor': 0,
            'test': 0,
            'other': 0
        }
        
        for commit in commits:
            message = commit.get('message', '').lower()
            
            if any(keyword in message for keyword in ['feat', 'feature', 'add', 'new']):
                commit_types['feature'] += 1
            elif any(keyword in message for keyword in ['fix', 'bug', 'patch']):
                commit_types['fix'] += 1
            elif any(keyword in message for keyword in ['doc', 'readme', 'comment']):
                commit_types['docs'] += 1
            elif any(keyword in message for keyword in ['style', 'format', 'lint']):
                commit_types['style'] += 1
            elif any(keyword in message for keyword in ['refactor', 'clean', 'optimize']):
                commit_types['refactor'] += 1
            elif any(keyword in message for keyword in ['test', 'spec', 'coverage']):
                commit_types['test'] += 1
            else:
                commit_types['other'] += 1
        
        return commit_types
    
    def _analyze_contributors(self, contributors: List[Dict]) -> Dict:
        """Analyze contributor data and patterns."""
        if not contributors:
            return {}
        
        contributor_df = pd.DataFrame(contributors)
        
        # Parse commit counts
        if 'commits' in contributor_df.columns:
            contributor_df['commit_count'] = contributor_df['commits'].apply(self._parse_commit_count)
        
        contributor_analysis = {
            'total_contributors': len(contributors),
            'top_contributor': contributors[0].get('username', 'Unknown') if contributors else 'Unknown',
            'total_commits_by_top_contributors': contributor_df['commit_count'].sum() if 'commit_count' in contributor_df.columns else 0,
            'average_commits_per_contributor': contributor_df['commit_count'].mean() if 'commit_count' in contributor_df.columns else 0,
            'contributor_diversity': self._calculate_contributor_diversity(contributor_df)
        }
        
        return contributor_analysis
    
    def _parse_commit_count(self, commit_text: str) -> int:
        """Parse commit count from contributor text."""
        if not commit_text:
            return 0
        
        # Extract number from text like "123 commits"
        match = re.search(r'(\d+)', str(commit_text))
        return int(match.group(1)) if match else 0
    
    def _calculate_contributor_diversity(self, contributor_df: pd.DataFrame) -> float:
        """Calculate contributor diversity index."""
        if 'commit_count' not in contributor_df.columns or len(contributor_df) == 0:
            return 0.0
        
        total_commits = contributor_df['commit_count'].sum()
        if total_commits == 0:
            return 0.0
        
        # Calculate Herfindahl-Hirschman Index (HHI) and convert to diversity
        proportions = contributor_df['commit_count'] / total_commits
        hhi = sum(p**2 for p in proportions)
        
        # Convert to diversity index (0 = monopoly, 1 = perfect diversity)
        diversity = 1 - hhi
        
        return diversity
    
    def _calculate_activity_metrics(self, repo_data: Dict) -> Dict:
        """Calculate overall activity metrics for a repository."""
        metrics = {
            'health_score': 0,
            'activity_level': 'Unknown',
            'community_engagement': 0,
            'development_velocity': 0
        }
        
        # Calculate health score based on various factors
        health_factors = []
        
        # Stars factor
        stars = repo_data.get('stars', 0)
        if stars > 10000:
            health_factors.append(1.0)
        elif stars > 1000:
            health_factors.append(0.8)
        elif stars > 100:
            health_factors.append(0.6)
        else:
            health_factors.append(0.3)
        
        # Forks factor
        forks = repo_data.get('forks', 0)
        if forks > 1000:
            health_factors.append(1.0)
        elif forks > 100:
            health_factors.append(0.8)
        elif forks > 10:
            health_factors.append(0.6)
        else:
            health_factors.append(0.3)
        
        # Recent activity factor
        commit_analysis = repo_data.get('commit_analysis', {})
        daily_commit_rate = commit_analysis.get('daily_commit_rate', 0)
        if daily_commit_rate > 1:
            health_factors.append(1.0)
        elif daily_commit_rate > 0.5:
            health_factors.append(0.8)
        elif daily_commit_rate > 0.1:
            health_factors.append(0.6)
        else:
            health_factors.append(0.3)
        
        # Calculate overall health score
        if health_factors:
            metrics['health_score'] = sum(health_factors) / len(health_factors) * 100
        
        # Determine activity level
        if metrics['health_score'] >= 80:
            metrics['activity_level'] = 'Very High'
        elif metrics['health_score'] >= 60:
            metrics['activity_level'] = 'High'
        elif metrics['health_score'] >= 40:
            metrics['activity_level'] = 'Medium'
        elif metrics['health_score'] >= 20:
            metrics['activity_level'] = 'Low'
        else:
            metrics['activity_level'] = 'Very Low'
        
        # Calculate community engagement
        contributor_analysis = repo_data.get('contributor_analysis', {})
        total_contributors = contributor_analysis.get('total_contributors', 0)
        diversity = contributor_analysis.get('contributor_diversity', 0)
        
        metrics['community_engagement'] = min(100, (total_contributors * 10) + (diversity * 50))
        
        # Calculate development velocity
        metrics['development_velocity'] = min(100, daily_commit_rate * 50)
        
        return metrics
    
    def export_to_csv(self, df: pd.DataFrame, filename: str) -> str:
        """Export DataFrame to CSV format."""
        return df.to_csv(filename, index=False)
    
    def export_to_json(self, data: Dict, filename: str) -> str:
        """Export data to JSON format."""
        import json
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return filename
