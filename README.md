# 📈 OpenTrend - GitHub Trending Analyzer

A comprehensive Streamlit application for analyzing **real-time** trending open-source projects on GitHub. Built with pure Python and designed for tech founders, developers, and talent scouts to understand live open-source trends and contributors.

**🚨 No Sample Data! 🚨** This application exclusively uses real-time data scraped directly from GitHub's trending pages.

## 🌟 Features

### 📊 Trending Projects Analysis
- **GitHub Trending Scraper**: Automatically scrapes trending repositories from GitHub
- **Multi-language Support**: Filter by programming languages (Python, JavaScript, TypeScript, etc.)
- **Time Range Filtering**: Daily, weekly, and monthly trending data
- **Comprehensive Metrics**: Stars, forks, contributors, and daily activity tracking

### 🔍 Repository Deep Dive
- **Individual Repository Analysis**: Detailed analysis of any GitHub repository
- **Commit Activity Tracking**: Recent commits timeline and frequency analysis
- **Contributor Insights**: Top contributors and their contribution patterns
- **Repository Health Metrics**: Community engagement and development velocity scoring

### 📈 Interactive Visualizations
- **Language Distribution**: Pie charts showing programming language popularity
- **Stars vs Forks Analysis**: Scatter plots revealing repository relationships
- **Activity Trends**: Histograms and time series of repository activity
- **Performance Comparisons**: Box plots comparing metrics across languages
- **Repository Health Dashboard**: Radar charts for comprehensive health metrics

### 💾 Data Export
- **JSON Export**: Complete data export in JSON format
- **CSV Export**: Tabular data export for further analysis
- **Chart Export**: Save visualizations as HTML, PNG, or PDF files

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Interactive web interface)
- **Web Scraping**: requests-html + BeautifulSoup4
- **Data Processing**: pandas + numpy
- **Visualizations**: plotly + matplotlib + seaborn
- **Data Formats**: JSON + CSV export capabilities

## 📋 Requirements

- Python 3.8+
- All dependencies listed in `requirements.txt`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

#### Option A: Using the run script (Recommended)
```bash
python run.py
```

#### Option B: Direct Streamlit command
```bash
streamlit run app.py
```

### 3. Access the Application
Open your web browser and navigate to: `http://localhost:8501`

## 📖 Usage Guide

### Getting Started
1. **Launch the app** using one of the methods above
2. **Select filters** in the sidebar:
   - Choose a programming language (or "All" for all languages)
   - Select time range (daily, weekly, monthly)
3. **Click "🚀 Scrape Trending"** to fetch data from GitHub

### Trending Projects Tab 📊
- View trending repositories in an interactive table
- See metrics including stars, forks, and contributors
- Filter and sort data by various criteria
- Export data in JSON or CSV format

### Repository Analysis Tab 🔍
- Enter any GitHub repository URL for detailed analysis
- View recent commit activity and patterns
- Analyze top contributors and their contributions
- Get repository health scores and metrics

### Visualizations Tab 📈
- Interactive charts showing:
  - Programming language distribution
  - Stars vs forks relationships
  - Top repositories by popularity
  - Activity distribution patterns
  - Language performance comparisons

### Export Data Tab 💾
- Download trending data in JSON or CSV format
- Export repository analysis results
- Save visualizations for presentations

## 🏗️ Architecture

```
OpenTrend/
├── app.py                 # Main Streamlit application
├── github_scraper.py      # GitHub scraping functionality
├── data_processor.py      # Data cleaning and processing
├── visualizations.py      # Chart and graph generation
├── requirements.txt       # Python dependencies
├── run.py                # Application launcher script
└── README.md             # This documentation
```

### Core Components

#### `GitHubScraper` (github_scraper.py)
- Handles web scraping of GitHub trending pages
- Extracts repository metadata (stars, forks, contributors)
- Analyzes individual repositories for detailed insights
- Implements respectful scraping with delays and user-agent headers

#### `DataProcessor` (data_processor.py)
- Cleans and normalizes scraped data
- Calculates derived metrics (popularity scores, activity levels)
- Processes commit and contributor data
- Handles data export functionality

#### `TrendVisualizer` (visualizations.py)
- Creates interactive Plotly charts
- Generates matplotlib charts for export
- Provides multiple visualization types
- Handles empty data scenarios gracefully

## 🎯 Use Cases

### For Tech Founders
- **Identify trending technologies** and emerging frameworks
- **Scout promising open-source projects** for potential collaboration
- **Track technology adoption** across different programming languages
- **Monitor competitor projects** and their community engagement

### For Developers
- **Discover new tools and libraries** in your tech stack
- **Find inspiration** from successful open-source projects
- **Identify learning opportunities** in trending technologies
- **Track project popularity** and community health

### For Talent Scouts
- **Find active contributors** in specific technology areas
- **Identify prolific open-source developers** for recruitment
- **Analyze developer activity patterns** and contribution quality
- **Discover emerging talent** in trending projects

## 🔧 Configuration

### Scraping Parameters
The application includes configurable scraping parameters:

- **Rate Limiting**: Built-in delays between requests (0.1-0.3 seconds)
- **User Agent**: Proper browser user-agent headers
- **Error Handling**: Graceful handling of failed requests
- **Data Validation**: Input validation and sanitization

### Visualization Settings
- **Color Schemes**: Customizable color palettes
- **Chart Types**: Multiple visualization options
- **Export Formats**: HTML, PNG, PDF, SVG support
- **Responsive Design**: Mobile-friendly layouts

## 📊 Sample Data Structure

### Trending Repository Data
```json
{
  "name": "owner/repository-name",
  "url": "https://github.com/owner/repository-name",
  "description": "Repository description",
  "language": "Python",
  "stars": 15420,
  "forks": 2891,
  "stars_today": 127,
  "contributors": "contributor1, contributor2, contributor3"
}
```

### Repository Analysis Data
```json
{
  "name": "owner/repository-name",
  "stars": 15420,
  "forks": 2891,
  "watchers": 892,
  "open_issues": 45,
  "recent_commits": [...],
  "top_contributors": [...],
  "activity_metrics": {
    "health_score": 85.7,
    "community_engagement": 78.2,
    "development_velocity": 92.1
  }
}
```

## 🚨 Important Notes

### Rate Limiting & Ethics
- The application implements respectful scraping practices
- Built-in delays prevent overwhelming GitHub's servers
- Use responsibly and in accordance with GitHub's Terms of Service
- Consider using GitHub's API for production applications

### Data Accuracy
- Data is scraped from GitHub's trending pages in real-time
- Results may vary based on GitHub's trending algorithm
- Some repositories may have incomplete data due to scraping limitations
- Cross-reference important data with GitHub directly

## 🛡️ Error Handling

The application includes comprehensive error handling:
- **Network Errors**: Graceful handling of connection issues
- **Parsing Errors**: Robust HTML parsing with fallbacks
- **Data Validation**: Input sanitization and validation
- **UI Feedback**: Clear error messages and loading indicators

## 🔄 Updates and Maintenance

### Regular Updates
- Monitor GitHub's HTML structure changes
- Update scraping selectors as needed
- Keep dependencies updated for security
- Add new visualization types based on user feedback

### Performance Optimization
- Efficient data processing with pandas
- Lazy loading of visualizations
- Caching of scraped data (session-based)
- Optimized chart rendering

## 📝 License

This project is open-source and available under the MIT License. See the LICENSE file for more details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Clone the repository
2. Install development dependencies
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

If you encounter any issues or have questions:
1. Check the error messages in the Streamlit interface
2. Ensure all dependencies are properly installed
3. Verify your internet connection for scraping functionality
4. Open an issue on the GitHub repository for bugs or feature requests

## 🚀 Future Enhancements

- **GitHub API Integration**: Replace scraping with official API calls
- **Database Storage**: Persistent data storage for historical analysis
- **Advanced Analytics**: Machine learning insights and predictions
- **Real-time Updates**: Live data streaming and notifications
- **Collaboration Features**: Team sharing and collaborative analysis
- **Mobile App**: Native mobile application for on-the-go analysis

---

**Happy analyzing! 📈✨**
