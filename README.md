# Spotify Testing with Selenium

This repository contains my learning journey with Selenium WebDriver and Python, focused on automating and scraping data from Spotify's web application.

## Project Overview

The goal of this project is to learn and implement various Selenium concepts and techniques in a real-world application. The tests are organized in a progressive manner, starting with basic navigation and advancing to more complex interactions and data extraction.

## Test Files and Concepts

### 1. Basic WebDriver Operations (test_01.py)
- WebDriver initialization
- Basic navigation to Spotify
- Retrieving page information (title, URL)
- Proper browser closure

### 2. Element Interaction and Wait Management (test_02.py)
- Locating elements using CSS selectors and IDs
- Implementing explicit waits with WebDriverWait
- Form submission and data input
- Taking screenshots
- Cookie management with pickle
- Environment variables for sensitive data

### 3. Session Management (test_03.py)
- Loading saved cookies to maintain session
- Verifying session state with element presence check

### 4. Advanced Scraping (test_04.py)
- Dynamic content search and navigation
- Complex data extraction from playlists
- Dynamic scrolling to load more content
- Advanced XPath for nested element location
- Exporting data to CSV and JSON formats

### 5. Multi-tab Navigation and Deep Analysis (test_05.py)
- Managing multiple browser tabs
- Dialog/popup interaction
- Conditional scrolling to find specific elements
- Working with dynamically loaded data
- Random selection for test variety

## Project Structure

```
spotify-testing/
├── cookies/           # Stored session cookies
├── files/             # Extracted data output
├── screenshots/       # Test screenshots
└── tests/
    └── beginnerTests/ # Progressive test examples
```

## Learning Progress

This project demonstrates a progressive approach to learning Selenium:

1. Starting with the fundamentals of browser automation
2. Advancing to more complex interactions and form handling
3. Implementing session management techniques
4. Developing comprehensive data scraping capabilities
5. Creating sophisticated multi-tab workflows

## Future Improvements

Potential areas for improvement include:
- Implementing Page Object Model design pattern
- Structuring tests with pytest or unittest frameworks
- Enhancing error handling and recovery
- Optimizing wait strategies
- Exploring parallel test execution
