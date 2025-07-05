import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional
import numpy as np

class TrendVisualizer:
    """
    Create interactive visualizations for GitHub trending data analysis.
    """
    
    def __init__(self, data: List[Dict]):
        """
        Initialize the visualizer with trending data.
        
        Args:
            data: List of repository dictionaries
        """
        self.data = data
        self.df = pd.DataFrame(data) if data else pd.DataFrame()
        
        # Define color palette
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e', 
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff7f0e',
            'info': '#17a2b8',
            'dark': '#343a40'
        }
        
        # Define color scales
        self.color_scales = {
            'viridis': 'viridis',
            'plasma': 'plasma',
            'custom': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        }
    
    def create_language_chart(self) -> go.Figure:
        """Create a pie chart showing programming language distribution."""
        if self.df.empty or 'language' not in self.df.columns:
            return self._create_empty_chart("No language data available")
        
        # Count languages
        language_counts = self.df['language'].value_counts()
        
        # Create pie chart
        fig = px.pie(
            values=language_counts.values,
            names=language_counts.index,
            title="Programming Language Distribution in Trending Repositories",
            color_discrete_sequence=self.color_scales['custom']
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        
        fig.update_layout(
            font=dict(size=12),
            title_font_size=16,
            showlegend=True,
            height=500
        )
        
        return fig
    
    def create_stars_forks_scatter(self) -> go.Figure:
        """Create a scatter plot showing relationship between stars and forks."""
        if self.df.empty or 'stars' not in self.df.columns or 'forks' not in self.df.columns:
            return self._create_empty_chart("No stars/forks data available")
        
        # Prepare data
        hover_data = []
        for _, row in self.df.iterrows():
            hover_text = f"<b>{row.get('name', 'Unknown')}</b><br>"
            hover_text += f"Language: {row.get('language', 'Unknown')}<br>"
            hover_text += f"Stars: {row.get('stars', 0):,}<br>"
            hover_text += f"Forks: {row.get('forks', 0):,}<br>"
            if 'description' in row:
                desc = row['description'][:100] + "..." if len(str(row['description'])) > 100 else row['description']
                hover_text += f"Description: {desc}"
            hover_data.append(hover_text)
        
        # Create scatter plot
        fig = px.scatter(
            self.df,
            x='stars',
            y='forks',
            color='language',
            size='stars',
            size_max=50,
            title="Stars vs Forks Relationship",
            labels={'stars': 'Stars Count', 'forks': 'Forks Count'},
            color_discrete_sequence=self.color_scales['custom']
        )
        
        # Update traces with custom hover data
        for i, trace in enumerate(fig.data):
            trace.hovertemplate = hover_data[i] if i < len(hover_data) else trace.hovertemplate
        
        # Add trend line
        if len(self.df) > 1:
            z = np.polyfit(self.df['stars'], self.df['forks'], 1)
            p = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=self.df['stars'],
                y=p(self.df['stars']),
                mode='lines',
                name='Trend Line',
                line=dict(color='red', dash='dash'),
                hovertemplate='Trend Line<extra></extra>'
            ))
        
        fig.update_layout(
            font=dict(size=12),
            title_font_size=16,
            height=600,
            xaxis_title="Stars Count",
            yaxis_title="Forks Count"
        )
        
        return fig
    
    def create_top_repos_chart(self, top_n: int = 10) -> go.Figure:
        """Create a horizontal bar chart of top repositories by stars."""
        if self.df.empty or 'stars' not in self.df.columns:
            return self._create_empty_chart("No repository data available")
        
        # Get top N repositories
        top_repos = self.df.nlargest(top_n, 'stars')
        
        # Create horizontal bar chart
        fig = px.bar(
            top_repos,
            x='stars',
            y='name',
            orientation='h',
            title=f"Top {top_n} Repositories by Stars",
            labels={'stars': 'Stars Count', 'name': 'Repository'},
            color='stars',
            color_continuous_scale='viridis'
        )
        
        # Customize hover data
        hover_template = '<b>%{y}</b><br>Stars: %{x:,}<br><extra></extra>'
        fig.update_traces(hovertemplate=hover_template)
        
        # Update layout
        fig.update_layout(
            font=dict(size=12),
            title_font_size=16,
            height=600,
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Stars Count",
            yaxis_title="Repository",
            coloraxis_colorbar=dict(title="Stars")
        )
        
        return fig
    
    def create_activity_distribution(self) -> go.Figure:
        """Create a distribution chart of repository activity levels."""
        if self.df.empty or 'stars_today' not in self.df.columns:
            return self._create_empty_chart("No activity data available")
        
        # Create histogram
        fig = px.histogram(
            self.df,
            x='stars_today',
            nbins=20,
            title="Distribution of Daily Star Activity",
            labels={'stars_today': 'Stars Today', 'count': 'Number of Repositories'},
            color_discrete_sequence=[self.colors['primary']]
        )
        
        # Add statistics
        mean_stars = self.df['stars_today'].mean()
        median_stars = self.df['stars_today'].median()
        
        fig.add_vline(
            x=mean_stars,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {mean_stars:.1f}"
        )
        
        fig.add_vline(
            x=median_stars,
            line_dash="dot",
            line_color="green",
            annotation_text=f"Median: {median_stars:.1f}"
        )
        
        fig.update_layout(
            font=dict(size=12),
            title_font_size=16,
            height=500,
            xaxis_title="Stars Today",
            yaxis_title="Number of Repositories"
        )
        
        return fig
    
    def create_language_performance_chart(self) -> go.Figure:
        """Create a box plot showing performance metrics by language."""
        if self.df.empty or 'language' not in self.df.columns or 'stars' not in self.df.columns:
            return self._create_empty_chart("No language performance data available")
        
        # Filter to top languages only
        top_languages = self.df['language'].value_counts().head(8).index
        filtered_df = self.df[self.df['language'].isin(top_languages)]
        
        fig = px.box(
            filtered_df,
            x='language',
            y='stars',
            title="Repository Stars Distribution by Programming Language",
            labels={'language': 'Programming Language', 'stars': 'Stars Count'},
            color='language',
            color_discrete_sequence=self.color_scales['custom']
        )
        
        fig.update_layout(
            font=dict(size=12),
            title_font_size=16,
            height=600,
            xaxis_title="Programming Language",
            yaxis_title="Stars Count",
            showlegend=False
        )
        
        fig.update_xaxes(tickangle=45)
        
        return fig
    
    def create_repo_analysis_charts(self, repo_data: Dict) -> List[go.Figure]:
        """Create charts for individual repository analysis."""
        charts = []
        
        # Commit activity chart
        if 'recent_commits' in repo_data and repo_data['recent_commits']:
            commit_chart = self._create_commit_activity_chart(repo_data['recent_commits'])
            charts.append(commit_chart)
        
        # Contributors chart
        if 'top_contributors' in repo_data and repo_data['top_contributors']:
            contributor_chart = self._create_contributors_chart(repo_data['top_contributors'])
            charts.append(contributor_chart)
        
        # Activity metrics radar chart
        if 'activity_metrics' in repo_data:
            metrics_chart = self._create_metrics_radar_chart(repo_data['activity_metrics'])
            charts.append(metrics_chart)
        
        return charts
    
    def _create_commit_activity_chart(self, commits: List[Dict]) -> go.Figure:
        """Create a timeline chart of commit activity."""
        commit_df = pd.DataFrame(commits)
        
        if 'date' not in commit_df.columns:
            return self._create_empty_chart("No commit date data available")
        
        # Parse dates
        commit_df['parsed_date'] = pd.to_datetime(commit_df['date'], errors='coerce')
        commit_df = commit_df.dropna(subset=['parsed_date'])
        
        if commit_df.empty:
            return self._create_empty_chart("No valid commit dates")
        
        # Group by date
        daily_commits = commit_df.groupby(commit_df['parsed_date'].dt.date).size().reset_index()
        daily_commits.columns = ['date', 'commits']
        
        fig = px.line(
            daily_commits,
            x='date',
            y='commits',
            title="Daily Commit Activity",
            labels={'date': 'Date', 'commits': 'Number of Commits'},
            markers=True
        )
        
        fig.update_layout(
            font=dict(size=12),
            title_font_size=16,
            height=400,
            xaxis_title="Date",
            yaxis_title="Number of Commits"
        )
        
        return fig
    
    def _create_contributors_chart(self, contributors: List[Dict]) -> go.Figure:
        """Create a bar chart of top contributors."""
        contrib_df = pd.DataFrame(contributors)
        
        if 'username' not in contrib_df.columns:
            return self._create_empty_chart("No contributor data available")
        
        # Parse commit counts
        if 'commits' in contrib_df.columns:
            contrib_df['commit_count'] = contrib_df['commits'].apply(self._parse_commit_count)
        else:
            contrib_df['commit_count'] = 1
        
        # Take top 10 contributors
        top_contributors = contrib_df.head(10)
        
        fig = px.bar(
            top_contributors,
            x='username',
            y='commit_count',
            title="Top Contributors by Commit Count",
            labels={'username': 'Username', 'commit_count': 'Commits'},
            color='commit_count',
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            font=dict(size=12),
            title_font_size=16,
            height=400,
            xaxis_title="Username",
            yaxis_title="Number of Commits",
            coloraxis_colorbar=dict(title="Commits")
        )
        
        fig.update_xaxes(tickangle=45)
        
        return fig
    
    def _create_metrics_radar_chart(self, metrics: Dict) -> go.Figure:
        """Create a radar chart for repository activity metrics."""
        categories = ['Health Score', 'Community Engagement', 'Development Velocity']
        values = [
            metrics.get('health_score', 0),
            metrics.get('community_engagement', 0),
            metrics.get('development_velocity', 0)
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Repository Metrics',
            line_color='rgb(75, 192, 192)',
            fillcolor='rgba(75, 192, 192, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title="Repository Activity Metrics",
            font=dict(size=12),
            title_font_size=16,
            height=500
        )
        
        return fig
    
    def create_combined_dashboard(self) -> go.Figure:
        """Create a combined dashboard with multiple subplots."""
        if self.df.empty:
            return self._create_empty_chart("No data available for dashboard")
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Language Distribution', 'Stars vs Forks', 
                          'Top Repositories', 'Activity Distribution'),
            specs=[[{'type': 'domain'}, {'type': 'scatter'}],
                   [{'type': 'bar'}, {'type': 'histogram'}]]
        )
        
        # Language pie chart
        if 'language' in self.df.columns:
            language_counts = self.df['language'].value_counts()
            fig.add_trace(
                go.Pie(labels=language_counts.index, values=language_counts.values,
                      name="Languages", showlegend=False),
                row=1, col=1
            )
        
        # Stars vs Forks scatter
        if 'stars' in self.df.columns and 'forks' in self.df.columns:
            fig.add_trace(
                go.Scatter(x=self.df['stars'], y=self.df['forks'],
                          mode='markers', name="Repositories", showlegend=False,
                          marker=dict(color=self.colors['primary'])),
                row=1, col=2
            )
        
        # Top repositories
        if 'stars' in self.df.columns and 'name' in self.df.columns:
            top_repos = self.df.nlargest(5, 'stars')
            fig.add_trace(
                go.Bar(x=top_repos['stars'], y=top_repos['name'],
                      orientation='h', name="Top Repos", showlegend=False,
                      marker_color=self.colors['success']),
                row=2, col=1
            )
        
        # Activity distribution
        if 'stars_today' in self.df.columns:
            fig.add_trace(
                go.Histogram(x=self.df['stars_today'], name="Activity", showlegend=False,
                           marker_color=self.colors['warning']),
                row=2, col=2
            )
        
        fig.update_layout(
            title_text="GitHub Trending Repositories Dashboard",
            title_font_size=20,
            height=800,
            font=dict(size=10)
        )
        
        return fig
    
    def create_matplotlib_chart(self, chart_type: str = 'language_dist') -> plt.Figure:
        """Create matplotlib charts for export/display."""
        if self.df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=16)
            ax.set_title('No Data')
            return fig
        
        plt.style.use('seaborn-v0_8')
        
        if chart_type == 'language_dist':
            return self._create_matplotlib_language_chart()
        elif chart_type == 'stars_hist':
            return self._create_matplotlib_stars_histogram()
        elif chart_type == 'correlation':
            return self._create_matplotlib_correlation_matrix()
        else:
            return self._create_matplotlib_language_chart()
    
    def _create_matplotlib_language_chart(self) -> plt.Figure:
        """Create matplotlib language distribution chart."""
        if 'language' not in self.df.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No language data', ha='center', va='center')
            return fig
        
        language_counts = self.df['language'].value_counts().head(8)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        colors = plt.cm.Set3(np.arange(len(language_counts)))
        
        wedges, texts, autotexts = ax.pie(
            language_counts.values,
            labels=language_counts.index,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        ax.set_title('Programming Language Distribution', fontsize=16, fontweight='bold')
        
        # Improve text readability
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        return fig
    
    def _create_matplotlib_stars_histogram(self) -> plt.Figure:
        """Create matplotlib stars distribution histogram."""
        if 'stars' not in self.df.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No stars data', ha='center', va='center')
            return fig
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.hist(self.df['stars'], bins=20, color='skyblue', alpha=0.7, edgecolor='black')
        ax.set_xlabel('Stars Count', fontsize=12)
        ax.set_ylabel('Number of Repositories', fontsize=12)
        ax.set_title('Distribution of Repository Stars', fontsize=16, fontweight='bold')
        
        # Add statistics
        mean_stars = self.df['stars'].mean()
        ax.axvline(mean_stars, color='red', linestyle='--', label=f'Mean: {mean_stars:.0f}')
        ax.legend()
        
        plt.tight_layout()
        return fig
    
    def _create_matplotlib_correlation_matrix(self) -> plt.Figure:
        """Create correlation matrix heatmap."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'Insufficient numeric data', ha='center', va='center')
            return fig
        
        correlation_matrix = self.df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(
            correlation_matrix,
            annot=True,
            cmap='coolwarm',
            center=0,
            square=True,
            ax=ax,
            cbar_kws={'label': 'Correlation Coefficient'}
        )
        
        ax.set_title('Repository Metrics Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def _parse_commit_count(self, commit_text: str) -> int:
        """Parse commit count from text."""
        import re
        if not commit_text:
            return 0
        match = re.search(r'(\d+)', str(commit_text))
        return int(match.group(1)) if match else 0
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Create an empty chart with a message."""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            title=message,
            xaxis={'visible': False},
            yaxis={'visible': False},
            height=400
        )
        return fig
    
    def export_chart(self, fig: go.Figure, filename: str, format: str = 'html') -> str:
        """Export chart to file."""
        if format.lower() == 'html':
            fig.write_html(filename)
        elif format.lower() == 'png':
            fig.write_image(filename)
        elif format.lower() == 'pdf':
            fig.write_image(filename)
        elif format.lower() == 'svg':
            fig.write_image(filename)
        else:
            fig.write_html(filename)
        
        return filename
