FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libgcc1 \
    libglib2.0-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    lsb-release \
    xdg-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN wget -O chromium.zip https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/linux64/chrome-headless-shell-linux64.zip \
    && unzip chromium.zip \
    && rm chromium.zip

COPY requirements.txt .
COPY dl.so .
COPY config.py .
COPY app.py .
COPY daddylive.m3u .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYPPETEER_CHROME_PATH=/app/chrome-headless-shell-linux64/chrome-headless-shell
ENV FLASK_HOST=0.0.0.0
ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["gunicorn", "--workers", "1", "--threads", "10", "--bind", "0.0.0.0:7860", "--timeout", "60", "app:app"] 