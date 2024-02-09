# i18n Translator Automation

## Introduction
This project is my first attempt to automate the part of extraction of texts and translate it to a language from a relatively small-medium-sized codebase for internationalization

## Features
1. Extracts strings from '.html','.js','.astro','.jsx' files
2. Translates strings from english to specified languages
3. Stores the translated strings in a JSON file to be used in codebases

## Getting Started

### Prerequisites
- Python 3
- openai python library
- python-dotenv python library

### Installation
1. Clone the repository
2. Add your own API-Key for OpenAI API
3. Install the 3 prerequisite libraries

### Usage
Command to run the script:
```python
python main.py --folder /path/to/src --language Target_language_in_full
```


