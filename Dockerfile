FROM python:3.11-slim-buster
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
WORKDIR /app/market_microservice
CMD ["python", "main.py"]
