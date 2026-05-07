FROM python:3.10-slim

# Proxy IUT
ENV http_proxy http://cache-etu.univ-artois.fr:3128
ENV https_proxy http://cache-etu.univ-artois.fr:3128

WORKDIR /app

# Installation des dépendances système nécessaires pour compiler mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "prog/app.py"]