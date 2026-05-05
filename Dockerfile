FROM python:3.10-slim

ENV http_proxy http://cache-etu.univ-artois.fr:3128
ENV https_proxy http://cache-etu.univ-artois.fr:3128

WORKDIR /app

COPY . .


RUN pip install --no-cache-dir requirements.txt

EXPOSE 5000


CMD ["python3", "prog/app.py"]