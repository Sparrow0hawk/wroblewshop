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
1. Load a cupboard using cURL
   ```bash
   curl -X POST http://127.0.0.1:5000/cupboard \
        -H "Content-type: application/json" \
        -d '{"id": 1, "name": "My cupboard"}'
   ```
1. Load a user using cURL
   ```bash
   curl -X POST http://127.0.0.1:5000/user \
        -H "Content-type: application/json" \
        -d '{"email": "USER@gmail.com", "cupboard": "My cupboard"}'
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

## Docker compose

To spin up an instance of the project and use a PostgreSQL database you can use Docker compose.

1. Spin up services
   ```bash
   docker compose up --build
   ```
   You can stop running services with CTRL+C
1. To destroy stopped services
   ```bash
   docker compose down
   ```

## Fly.io

1. Launch new Fly.io app using fly.toml
   ```bash
   fly launch
   ```

1. Create fly postgres machine. Use development setting and let it go to sleep. 
```bash
fly postgres create --name wroblewshop-pg
```

1. Attach the container machine to main wroblewshop machine. Note this will set DATABASE_URL secret.
```bash
fly postgres attach wroblewshop-pg --app wroblewshop
```

1. Set database URI secret for Flask.
```bash
fly secrets set FLASK_SQLALCHEMY_DATABASE_URI=postgresql+psycopg://wroblewshop:password@wroblewshop-pg.flycast:5432/wroblewshop
```

1. Create psql session in database.

```bash
fly postgres connect --app wroblewshop-pg --database wroblewshop
```
