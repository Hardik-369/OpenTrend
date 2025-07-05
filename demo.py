#!/usr/bin/env python3
"""
OpenTrend Demo Script
Demonstrates core functionality without the full Streamlit interface
"""

import sys
import time
from github_scraper import GitHubScraper
from data_processor import DataProcessor
from visualizations import TrendVisualizer

def demo_scraping():
    """Demonstrate GitHub scraping functionality."""
    print("🕷️  DEMO: GitHub Trending Scraper")
    print("=" * 50)
    
    scraper = GitHubScraper()
    
    print("📈 Scraping trending Python repositories (daily)...")
    try:
        # Scrape trending Python repositories
        trending_data = scraper.scrape_trending(language="python", time_range="daily")
        
        if trending_data:
            print(f"✅ Successfully scraped {len(trending_data)} repositories!")
            
            # Show first few repositories
            print("\n🔝 Top trending repositories:")
            for i, repo in enumerate(trending_data[:3], 1):
                print(f"{i}. {repo.get('name', 'Unknown')}")
                print(f"   ⭐ Stars: {repo.get('stars', 0):,}")
                print(f"   🍴 Forks: {repo.get('forks', 0):,}")
                print(f"   📝 Description: {repo.get('description', 'No description')[:80]}...")
                print()
            
            return trending_data
        else:
            print("❌ No data retrieved. This might be due to rate limiting or network issues.")
            return []
            
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return []

def demo_data_processing(trending_data):
    """Demonstrate data processing functionality."""
    print("\n🔧 DEMO: Data Processing")
    print("=" * 50)
    
    if not trending_data:
        print("❌ No real-time data available to process.")
        print("💡 This could be due to:")
        print("   - Network connectivity issues")
        print("   - GitHub rate limiting")
        print("   - Temporary scraping restrictions")
        print("\n🔄 Try running the demo again in a few minutes.")
        return None
    
    processor = DataProcessor()
    
    print("📊 Processing and cleaning data...")
    df = processor.clean_trending_data(trending_data)
    
    if not df.empty:
        print(f"✅ Processed {len(df)} repositories")
        print(f"📈 Average popularity score: {df['popularity_score'].mean():.1f}")
        print(f"🏆 Most popular language: {df['language'].value_counts().index[0]}")
        
        # Show language statistics
        lang_stats = processor.get_language_statistics(df)
        print(f"🔍 Total unique languages: {lang_stats.get('total_languages', 0)}")
        
        return df
    else:
        print("❌ Data processing failed")
        return None

def demo_visualizations(data):
    """Demonstrate visualization functionality."""
    print("\n📈 DEMO: Visualizations")
    print("=" * 50)
    
    if data is None or len(data) == 0:
        print("⚠️  No data available for visualization")
        return
    
    # Convert to list format for visualizer
    if hasattr(data, 'to_dict'):
        data_list = data.to_dict('records')
    else:
        data_list = data
    
    visualizer = TrendVisualizer(data_list)
    
    print("🎨 Creating visualizations...")
    
    try:
        # Create language chart
        lang_chart = visualizer.create_language_chart()
        print("✅ Language distribution chart created")
        
        # Create stars vs forks chart
        scatter_chart = visualizer.create_stars_forks_scatter()
        print("✅ Stars vs Forks scatter plot created")
        
        # Create top repositories chart
        top_repos_chart = visualizer.create_top_repos_chart(top_n=5)
        print("✅ Top repositories chart created")
        
        print("📊 All charts generated successfully!")
        print("💡 In the full Streamlit app, these would be interactive and exportable")
        
    except Exception as e:
        print(f"❌ Visualization error: {e}")

def demo_repository_analysis():
    """Demonstrate individual repository analysis."""
    print("\n🔍 DEMO: Repository Analysis")
    print("=" * 50)
    
    # Use a well-known repository for demonstration
    repo_url = "https://github.com/microsoft/vscode"
    
    print(f"🔎 Analyzing repository: {repo_url}")
    
    scraper = GitHubScraper()
    
    try:
        repo_data = scraper.analyze_repository(repo_url)
        
        if repo_data:
            print("✅ Repository analysis completed!")
            print(f"📦 Repository: {repo_data.get('name', 'Unknown')}")
            print(f"⭐ Stars: {repo_data.get('stars', 0):,}")
            print(f"🍴 Forks: {repo_data.get('forks', 0):,}")
            print(f"👥 Language: {repo_data.get('language', 'Unknown')}")
            
            # Show recent commits if available
            recent_commits = repo_data.get('recent_commits', [])
            if recent_commits:
                print(f"📝 Recent commits found: {len(recent_commits)}")
                print("Latest commit:", recent_commits[0].get('message', 'No message')[:50] + "...")
            
            # Show contributors if available
            contributors = repo_data.get('top_contributors', [])
            if contributors:
                print(f"👥 Top contributors found: {len(contributors)}")
                top_contributor = contributors[0].get('username', 'Unknown')
                print(f"Top contributor: {top_contributor}")
        else:
            print("❌ Repository analysis failed")
            
    except Exception as e:
        print(f"❌ Repository analysis error: {e}")
        print("💡 This might be due to rate limiting or network connectivity")

def main():
    """Run the complete demo."""
    print("🚀 OpenTrend Functionality Demo")
    print("=" * 60)
    print("This demo showcases the core features of OpenTrend")
    print("without running the full Streamlit interface.\n")
    
    # Demo 1: Scraping trending repositories
    trending_data = demo_scraping()
    time.sleep(1)  # Brief pause between demos
    
    # Demo 2: Data processing
    processed_data = demo_data_processing(trending_data)
    time.sleep(1)
    
    # Demo 3: Visualizations
    demo_visualizations(processed_data)
    time.sleep(1)
    
    # Demo 4: Individual repository analysis
    demo_repository_analysis()
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed!")
    print("\n💡 To see the full interactive experience:")
    print("   python run.py")
    print("   or")
    print("   streamlit run app.py")
    print("\n📚 Check README.md for detailed documentation")

if __name__ == "__main__":
    main()
