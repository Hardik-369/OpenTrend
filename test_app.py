#!/usr/bin/env python3
"""
Test script for OpenTrend application
Verifies that all components are working correctly
"""

import sys
import traceback

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ Matplotlib imported successfully")
    except ImportError as e:
        print(f"❌ Matplotlib import failed: {e}")
        return False
    
    try:
        import seaborn as sns
        print("✅ Seaborn imported successfully")
    except ImportError as e:
        print(f"❌ Seaborn import failed: {e}")
        return False
    
    try:
        from requests_html import HTMLSession
        print("✅ Requests-HTML imported successfully")
    except ImportError as e:
        print(f"❌ Requests-HTML import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported successfully")
    except ImportError as e:
        print(f"❌ BeautifulSoup import failed: {e}")
        return False
    
    return True

def test_custom_modules():
    """Test that custom modules can be imported and initialized."""
    print("\n🧪 Testing custom modules...")
    
    try:
        from github_scraper import GitHubScraper
        scraper = GitHubScraper()
        print("✅ GitHubScraper imported and initialized successfully")
    except Exception as e:
        print(f"❌ GitHubScraper failed: {e}")
        return False
    
    try:
        from data_processor import DataProcessor
        processor = DataProcessor()
        print("✅ DataProcessor imported and initialized successfully")
    except Exception as e:
        print(f"❌ DataProcessor failed: {e}")
        return False
    
    try:
        from visualizations import TrendVisualizer
        visualizer = TrendVisualizer([])
        print("✅ TrendVisualizer imported and initialized successfully")
    except Exception as e:
        print(f"❌ TrendVisualizer failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of core components."""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test data processor with sample data
        from data_processor import DataProcessor
        processor = DataProcessor()
        
        sample_data = [
            {
                'name': 'test/repo',
                'url': 'https://github.com/test/repo',
                'description': 'Test repository',
                'language': 'Python',
                'stars': 100,
                'forks': 20,
                'stars_today': 5,
                'contributors': 'user1, user2'
            }
        ]
        
        df = processor.clean_trending_data(sample_data)
        if not df.empty:
            print("✅ DataProcessor basic functionality working")
        else:
            print("❌ DataProcessor returned empty DataFrame")
            return False
            
    except Exception as e:
        print(f"❌ DataProcessor functionality test failed: {e}")
        return False
    
    try:
        # Test visualizer with sample data
        from visualizations import TrendVisualizer
        visualizer = TrendVisualizer(sample_data)
        
        # Test creating a chart
        chart = visualizer.create_language_chart()
        if chart:
            print("✅ TrendVisualizer basic functionality working")
        else:
            print("❌ TrendVisualizer chart creation failed")
            return False
            
    except Exception as e:
        print(f"❌ TrendVisualizer functionality test failed: {e}")
        return False
    
    return True

def test_app_structure():
    """Test that the main app structure is valid."""
    print("\n🧪 Testing app structure...")
    
    try:
        # Try to import the main app (this will validate syntax)
        import app
        print("✅ Main app.py structure is valid")
    except Exception as e:
        print(f"❌ Main app.py has issues: {e}")
        return False
    
    return True

def run_all_tests():
    """Run all tests and report results."""
    print("🚀 Running OpenTrend Application Tests\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("Custom Module Tests", test_custom_modules),
        ("Basic Functionality Tests", test_basic_functionality),
        ("App Structure Tests", test_app_structure)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
            traceback.print_exc()
    
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! OpenTrend is ready to run.")
        print("Run 'python run.py' or 'streamlit run app.py' to start the application.")
        return True
    else:
        print(f"\n❌ {total - passed} tests failed. Please check the errors above.")
        print("Install missing dependencies with: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
