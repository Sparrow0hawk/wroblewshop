# Wroblewshop

## Setup

To run this repository you will need:
- Python 3.12


1. Create virtual environment
   ```bash
   python3.12 -m venv --prompt . --upgrade-deps .venv
   ```
2. Install dependencies
   ```
   source .venv/bin/activate
   
   pip install -e .
   ```
3. Build prototype
   ```bash
   python prototype/build.py
   ```
4. View prototype locally
   ```bash
   python -m http.server 8081 -d prototype/_site
   # can also use the Makefile target
   make prototype 
   ```
