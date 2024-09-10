# Wroblewshop

## Setup

To run this repository you will need:
- Python 3.12
- Node 10

1. Create virtual environment
   ```bash
   python3.12 -m venv --prompt . --upgrade-deps .venv
   ```
1. Install dependencies
   ```
   source .venv/bin/activate
   
   pip install -e .
   ```
1. Build static assets
   ```bash
   npm install
   
   npm run build
   ```
1. Start app locally at http://127.0.0.1:5000
   ```bash
    flask --app wroblewshop run
   ```
   
## Prototype

To view the noddy prototype:
1. Build prototype
   ```bash
   python prototype/build.py
   ```
1. View prototype locally
   ```bash
   python -m http.server 8081 -d prototype/_site
   # can also use the Makefile target
   make prototype 
   ```

## Docker

To build the project with Docker, complete [project setup](#setup) and run:

1. Docker build
   ```bash
   docker build . -t wroblewshop
   ```
1. Run container and view at http://127.0.0.1:5000
   ```bash
   docker run --env-file .env --rm -p 5000:5000 wroblewshop:latest
   ```
