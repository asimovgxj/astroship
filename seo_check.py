
import requests
import json
import time

def get_google_suggestions(keyword):
    """获取 Google 搜索自动联想词（代表真实搜索意图）"""
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={keyword}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data[1]
        return []
    except Exception as e:
        return [f"Error: {str(e)}"]

keywords_to_test = [
    "Xiaomi Auto lawsuit",
    "Chinese EV brands",
    "Maextro car",
    "criticize Chinese cars",
    "car brand reputation management",
    "NIO vs Xiaomi controversy",
    "Xiaomi vs Tesla China",
    "JAC Huawei car"
]

results = {}

for kw in keywords_to_test:
    print(f"Fetching suggestions for: {kw}")
    results[kw] = get_google_suggestions(kw)
    time.sleep(1) # 避免频率限制

print("\n--- GOOGLE AUTOCOMPLETE FINDINGS ---")
for kw, suggestions in results.items():
    print(f"\n[{kw}]")
    for s in suggestions:
        print(f"  - {s}")
