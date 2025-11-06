import requests
import pandas as pd
import time

product_ids = [
    16736269,  # Galaxy S24 FE
    17464490,  # Galaxy A16
    18575577,  # Galaxy A56
    17918956,  # Galaxy S25 Ultra
    16552148,  # Galaxy A06
    18577783,  # Galaxy A36
]

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7"
}

all_comments = []

for product_id in product_ids:
    print(f"\n📦 Extracting comments for product_id={product_id} ...")

    url = f"https://api.digikala.com/v1/product/{product_id}/comments/"
    page = 1

    while True:
        response = requests.get(url, headers=headers, params={"page": page})
        data = response.json()

        comments = data.get("data", {}).get("comments", [])
        if not comments:
            break

        for c in comments:
            all_comments.append({
                "product_id": product_id,
                "comment_id": c.get("id"),
                "author_name": c.get("user_name"),
                "rating": c.get("rate"),
                "date": c.get("created_at"),
                "comment_text": c.get("body")
            })

        print(f"✅ Collected {len(comments)} comments from page {page}")
        page += 1

        time.sleep(0.8)

print(f"\n📊 Total comments collected: {len(all_comments)}")

df = pd.DataFrame(all_comments)
df.to_csv("digikala_samsung_comments.csv", index=False, encoding="utf-8-sig")

print("💾 Saved all comments to digikala_samsung_comments.csv")
