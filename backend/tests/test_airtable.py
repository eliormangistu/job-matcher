import re
import requests
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

with open(DATA_DIR / "airtable.html", encoding="utf-8") as f:
    html = f.read()

url_match = re.search(r'urlWithParams:\s*"([^"]+)"', html)

if not url_match:
    print("URL NOT FOUND")
    exit()

url = url_match.group(1)
url = url.replace(r"\u002F", "/")
url = url.replace(r"\u0026", "&")
url = "https://airtable.com" + url

headers_match = re.search(r'var headers = (\{.*?\});', html, re.S)

if not headers_match:
    print("HEADERS NOT FOUND")
    exit()

headers = json.loads(headers_match.group(1))
headers["x-time-zone"] = "Asia/Jerusalem"

response = requests.get(url, headers=headers)

print("STATUS:", response.status_code)
print("LENGTH:", len(response.content))

data = response.json()
table = data["data"]["table"]

print("\nTABLE KEYS:")
print(list(table.keys()))

print("\nCOLUMNS:")
for column in table.get("columns", []):
    print(
        column.get("id"),
        "=>",
        column.get("name"),
        "| type:",
        column.get("type")
    )

print("\nPOSSIBLE ROW/RECORD KEYS:")
for key, value in table.items():
    if isinstance(value, list):
        print(key, "=>", len(value), "items")