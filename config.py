import os

DADDY_BASE_URL = "https://thedaddy.click"

FLASK_HOST = os.environ.get("FLASK_HOST", "0.0.0.0")

DEFAULT_GLOBAL_USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 "
    "EdgiOS/131.0.2903.42 Mobile/15E148 Safari/537.36"
)
APP_PY_STYLE_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "FxiOS/33.0 Mobile/15E148 Safari/605.1.15"
    ),
    "Referer": "https://google.com/",
    "Origin":  "https://google.com",
    "Accept":  "*/*",
}

M3U_FETCH_TIMEOUT = 12
KEY_FETCH_TIMEOUT = 10
TS_FETCH_TIMEOUT = (5, 5)

PYPPETEER_CHROME_PATH = os.environ.get("PYPPETEER_CHROME_PATH")
PYPPETEER_TIMEOUT_MS = 20_000

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

