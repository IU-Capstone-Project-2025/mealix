FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install faiss-cpu

WORKDIR /app

COPY ./fastapi-app /app

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# docker build -t mealix-api .
# docker run -p 8000:8000 --env-file .env mealix-api

