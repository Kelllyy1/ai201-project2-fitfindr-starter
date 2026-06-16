# tests/test_tools.py
import os
from groq import Groq
from dotenv import load_dotenv
from tools import search_listings, suggest_outfit, create_fit_card, _get_groq_client


# Set up the client once for all tests
client = _get_groq_client()



# search_listings()
def test_search_returns_results():
    results = search_listings("vinstage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0
    
def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []   # empty list, no exception

def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)



# suggest_outfit()
def test_suggest_outfit_empty_wardrobe():
    """Empty wardrobe should return general styling advice, not an empty string."""
    new_item = {
        "title": "Vintage Levi's Denim Jacket",
        "category": "jacket",
        "style_tags": ["vintage", "casual"],
        "colors": ["blue"]
    }
    wardrobe = {"items": []}
    result = suggest_outfit(new_item, wardrobe, client)
    assert isinstance(result, str)
    assert len(result.strip()) > 0

def test_suggest_outfit_with_wardrobe():
    """Non-empty wardrobe should return outfit using named wardrobe pieces."""
    new_item = {
        "title": "Floral Mini Skirt",
        "category": "skirt",
        "style_tags": ["feminine", "vintage"],
        "colors": ["pink", "white"]
    }
    wardrobe = {"items": [
        {"title": "White Crop Top", "category": "top", "colors": ["white"]},
        {"title": "Black Chunky Boots", "category": "shoes", "colors": ["black"]}
    ]}
    result = suggest_outfit(new_item, wardrobe, client)
    assert isinstance(result, str)
    assert len(result.strip()) > 0



# create_fit_card()
def test_create_fit_card_empty_outfit():
    """Empty outfit string should return an error string, not crash."""
    new_item = {"title": "Graphic Tee", "price": 12.0, "platform": "Depop"}
    result = create_fit_card("", new_item, client)
    assert isinstance(result, str)
    assert len(result.strip()) > 0  # returns error message, not empty

def test_create_fit_card_whitespace_outfit():
    """Whitespace-only outfit string should also return an error string."""
    new_item = {"title": "Graphic Tee", "price": 12.0, "platform": "Depop"}
    result = create_fit_card("   ", new_item, client)
    assert isinstance(result, str)
    assert len(result.strip()) > 0

def test_create_fit_card_returns_caption():
    """Valid inputs should return a non-empty caption string."""
    new_item = {"title": "Vintage Band Tee", "price": 18.0, "platform": "Poshmark"}
    outfit = "Pair with baggy jeans and chunky sneakers for a 90s grunge vibe."
    result = create_fit_card(outfit, new_item, client)
    assert isinstance(result, str)
    assert len(result.strip()) > 0