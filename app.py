import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
import re
from github_scraper import GitHubScraper
from data_processor import DataProcessor
from visualizations import TrendVisualizer

# Page configuration
st.set_page_config(
    page_title="OpenTrend - GitHub Trending Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .trend-table {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'trending_data' not in st.session_state:
        st.session_state.trending_data = None
    if 'repo_analysis' not in st.session_state:
        st.session_state.repo_analysis = None
    
    # Header
    st.markdown('<div class="main-header">📈 OpenTrend</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Analyze trending open-source projects on GitHub</p>', unsafe_allow_html=True)
    
    # Sidebar for filters
    st.sidebar.markdown("### 🔍 Trending Filters")
    
    # Language selection
    languages = [
        "All", "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", 
        "Rust", "PHP", "Ruby", "Swift", "Kotlin", "Dart", "HTML", "CSS", "Shell"
    ]
    selected_language = st.sidebar.selectbox("Programming Language", languages)
    
    # Time range selection
    time_ranges = {
        "Daily": "daily",
        "Weekly": "weekly", 
        "Monthly": "monthly"
    }
    selected_time_range = st.sidebar.selectbox("Time Range", list(time_ranges.keys()))
    
    # Scrape trending button
    if st.sidebar.button("🚀 Scrape Trending", type="primary"):
        # Clear any existing data
        st.session_state.trending_data = None
        
        with st.spinner("Fetching real-time data from GitHub trending..."):
            scraper = GitHubScraper()
            lang_param = None if selected_language == "All" else selected_language.lower()
            
            # Show progress in sidebar
            progress_placeholder = st.sidebar.empty()
            progress_placeholder.info("🔍 Connecting to GitHub...")
            
            trending_data = scraper.scrape_trending(
                language=lang_param,
                time_range=time_ranges[selected_time_range]
            )
            
            if trending_data and len(trending_data) > 0:
                st.session_state.trending_data = trending_data
                progress_placeholder.success(f"✅ Successfully fetched {len(trending_data)} trending repositories!")
            else:
                progress_placeholder.error("❌ Failed to fetch trending data. Please try again.")
                st.error("""
                **Unable to fetch real-time data from GitHub.**
                
                This could be due to:
                - Network connectivity issues
                - GitHub rate limiting
                - Temporary server restrictions
                
                **Please try again in a few minutes.**
                """)
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Trending Projects", "🔍 Repository Analysis", "📈 Visualizations", "💾 Export Data"])
    
    with tab1:
        display_trending_projects()
    
    with tab2:
        display_repository_analysis()
    
    with tab3:
        display_visualizations()
    
    with tab4:
        display_export_options()

def display_trending_projects():
    st.markdown('<div class="section-header">Real-Time Trending Projects</div>', unsafe_allow_html=True)
    
    if st.session_state.trending_data:
        data = st.session_state.trending_data
        
        # Show last updated time
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.caption(f"📅 Data fetched at: {current_time} (Real-time from GitHub)")
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Projects", len(data))
        
        with col2:
            total_stars = sum(repo.get('stars', 0) for repo in data)
            st.metric("Total Stars", f"{total_stars:,}")
        
        with col3:
            total_forks = sum(repo.get('forks', 0) for repo in data)
            st.metric("Total Forks", f"{total_forks:,}")
        
        with col4:
            avg_stars = total_stars / len(data) if data else 0
            st.metric("Avg Stars", f"{avg_stars:.0f}")
        
        # Convert to DataFrame for display
        df = pd.DataFrame(data)
        
        # Format the data for better display
        if not df.empty:
            display_df = df.copy()
            display_df['Stars'] = display_df['stars'].apply(lambda x: f"{x:,}" if pd.notna(x) else "0")
            display_df['Forks'] = display_df['forks'].apply(lambda x: f"{x:,}" if pd.notna(x) else "0")
            
            # Create clickable links
            display_df['Repository'] = display_df.apply(
                lambda row: f"[{row['name']}]({row['url']})", axis=1
            )
            
            # Select columns for display
            columns_to_show = ['Repository', 'description', 'Stars', 'Forks', 'language', 'contributors']
            display_df = display_df[columns_to_show]
            
            # Display the table
            st.markdown('<div class="trend-table">', unsafe_allow_html=True)
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Repository": st.column_config.LinkColumn("Repository"),
                    "description": st.column_config.TextColumn("Description", width="large"),
                    "Stars": st.column_config.TextColumn("Stars", width="small"),
                    "Forks": st.column_config.TextColumn("Forks", width="small"),
                    "language": st.column_config.TextColumn("Language", width="medium"),
                    "contributors": st.column_config.TextColumn("Contributors", width="medium")
                }
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add refresh button
            if st.button("🔄 Refresh Data", help="Fetch the latest trending repositories"):
                st.rerun()
    else:
        st.info("""
        ### 🚀 Get Started with Real-Time GitHub Trending Data
        
        **No sample data here!** This app fetches live, real-time trending repositories directly from GitHub.
        
        **Steps to get started:**
        1. 👈 Select a programming language from the sidebar (or choose "All")
        2. 📅 Choose a time range (Daily, Weekly, or Monthly)
        3. 🚀 Click "Scrape Trending" to fetch live data
        
        **You'll get:**
        - Real-time trending repositories
        - Current star counts and forks
        - Active contributors
        - Project descriptions and languages
        
        **Ready to explore what's trending right now?** 👆
        """)

def display_repository_analysis():
    st.markdown('<div class="section-header">Real-Time Repository Deep Dive</div>', unsafe_allow_html=True)
    
    st.info("""
    🔍 **Live Repository Analysis** - Get real-time insights from any GitHub repository!
    
    Enter any public GitHub repository URL below to get:
    - Current stars, forks, and issues count
    - Recent commit activity and patterns
    - Top contributors and their activity
    - Repository health metrics
    """)
    
    # Repository URL input
    repo_url = st.text_input(
        "Enter GitHub Repository URL:",
        placeholder="https://github.com/microsoft/vscode",
        help="Enter any public GitHub repository URL for real-time detailed analysis"
    )
    
    if st.button("🔍 Analyze Repository", type="primary"):
        if repo_url:
            # Validate URL
            if not re.match(r'https://github\.com/[\w\-\.]+/[\w\-\.]+', repo_url):
                st.error("Please enter a valid GitHub repository URL")
                return
            
            with st.spinner("Analyzing repository..."):
                scraper = GitHubScraper()
                repo_data = scraper.analyze_repository(repo_url)
                st.session_state.repo_analysis = repo_data
                st.success("✅ Repository analysis completed!")
        else:
            st.warning("Please enter a repository URL")
    
    # Display repository analysis
    if st.session_state.repo_analysis:
        repo_data = st.session_state.repo_analysis
        
        # Repository overview
        st.markdown("#### Repository Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Stars", f"{repo_data.get('stars', 0):,}")
            st.metric("Forks", f"{repo_data.get('forks', 0):,}")
            st.metric("Open Issues", f"{repo_data.get('open_issues', 0):,}")
        
        with col2:
            st.metric("Watchers", f"{repo_data.get('watchers', 0):,}")
            st.metric("Language", repo_data.get('language', 'N/A'))
            st.metric("Size", f"{repo_data.get('size', 0):,} KB")
        
        # Recent commits
        if repo_data.get('recent_commits'):
            st.markdown("#### Recent Commits")
            commits_df = pd.DataFrame(repo_data['recent_commits'])
            st.dataframe(commits_df, use_container_width=True, hide_index=True)
        
        # Top contributors
        if repo_data.get('top_contributors'):
            st.markdown("#### Top Contributors")
            contributors_df = pd.DataFrame(repo_data['top_contributors'])
            st.dataframe(contributors_df, use_container_width=True, hide_index=True)

def display_visualizations():
    st.markdown('<div class="section-header">Real-Time Trend Visualizations</div>', unsafe_allow_html=True)
    
    if st.session_state.trending_data:
        st.success(f"📈 Visualizing {len(st.session_state.trending_data)} real-time trending repositories")
        
        visualizer = TrendVisualizer(st.session_state.trending_data)
        
        # Language distribution
        st.markdown("#### Programming Language Distribution")
        st.caption("Current trending languages on GitHub right now")
        lang_chart = visualizer.create_language_chart()
        st.plotly_chart(lang_chart, use_container_width=True)
        
        # Stars vs Forks scatter plot
        st.markdown("#### Stars vs Forks Analysis")
        st.caption("Real-time relationship between repository popularity metrics")
        scatter_chart = visualizer.create_stars_forks_scatter()
        st.plotly_chart(scatter_chart, use_container_width=True)
        
        # Top repositories bar chart
        st.markdown("#### Top Repositories by Stars")
        st.caption("Most starred repositories in current trending list")
        top_repos_chart = visualizer.create_top_repos_chart()
        st.plotly_chart(top_repos_chart, use_container_width=True)
        
        # Repository analysis visualizations
        if st.session_state.repo_analysis:
            st.markdown("#### Repository Analysis")
            st.caption("Real-time analysis of selected repository")
            repo_charts = visualizer.create_repo_analysis_charts(st.session_state.repo_analysis)
            for chart in repo_charts:
                st.plotly_chart(chart, use_container_width=True)
    
    else:
        st.info("""
        ### 📈 Interactive Real-Time Visualizations
        
        **No sample charts here!** All visualizations are generated from live GitHub data.
        
        **What you'll see after fetching data:**
        - 🌐 **Language Distribution**: Current trending programming languages
        - ⭐ **Stars vs Forks**: Real-time popularity relationships
        - 🏆 **Top Repositories**: Most popular projects right now
        - 📈 **Activity Trends**: Live repository metrics
        
        **Get started:** Fetch trending data from the sidebar first! 👆
        """)

def display_export_options():
    st.markdown('<div class="section-header">Export Real-Time Data</div>', unsafe_allow_html=True)
    
    st.info("""
    📁 **Export Live Data** - Download your real-time GitHub insights!
    
    All exported data represents the current state of GitHub trending repositories
    at the time of scraping. No sample or cached data included.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Real-Time Trending Data")
        if st.session_state.trending_data:
            from datetime import datetime
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            st.success(f"📈 Ready to export {len(st.session_state.trending_data)} live repositories")
            
            # Export trending data
            trending_json = json.dumps(st.session_state.trending_data, indent=2)
            st.download_button(
                label="📥 Download Live Trending Data (JSON)",
                data=trending_json,
                file_name=f"github_trending_realtime_{current_time}.json",
                mime="application/json",
                help="Download current trending repositories in JSON format"
            )
            
            # Export as CSV
            if st.session_state.trending_data:
                df = pd.DataFrame(st.session_state.trending_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Live Trending Data (CSV)",
                    data=csv,
                    file_name=f"github_trending_realtime_{current_time}.csv",
                    mime="text/csv",
                    help="Download current trending repositories in CSV format"
                )
        else:
            st.warning("""
            **No real-time data available to export**
            
            Fetch live trending data first using the sidebar controls.
            """)
    
    with col2:
        st.markdown("#### Repository Analysis")
        if st.session_state.repo_analysis:
            # Export repository analysis
            repo_json = json.dumps(st.session_state.repo_analysis, indent=2)
            st.download_button(
                label="📥 Download Repository Analysis (JSON)",
                data=repo_json,
                file_name=f"repo_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.info("No repository analysis to export")

if __name__ == "__main__":
    main()
