FROM python:3.12-slim

WORKDIR /code

COPY . /code
RUN pip install .

EXPOSE 5000

CMD ["gunicorn", "--bind", ":5000", "wroblewshop:create_app()"]
