# scratch_test.py
import os
from groq import Groq
from tools import search_listings, suggest_outfit, create_fit_card

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

print("--- search_listings: no results ---")
results = search_listings("designer ballgown", size="XXS", max_price=5)
print(results)

print("\n--- suggest_outfit: empty wardrobe ---")
item = {"title": "Vintage Band Tee", "category": "top", "style_tags": ["grunge"], "colors": ["black"]}
print(suggest_outfit(item, {"items": []}, client))

print("\n--- create_fit_card: empty outfit ---")
print(create_fit_card("", item, client))

print("\n--- full happy path ---")
results = search_listings("vintage graphic tee", max_price=50)
if results:
    outfit = suggest_outfit(results[0], {"items": []}, client)
    print(suggest_outfit(results[0], {"items": []}, client))
    print(create_fit_card(outfit, results[0], client))
