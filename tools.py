"""
tools.py

The three required FitFindr tools. Each tool is a standalone function that
can be called and tested independently before being wired into the agent loop.

Complete and test each tool before moving to agent.py.

Tools:
    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)              → str
    create_fit_card(outfit, new_item)               → str
"""

import os

from dotenv import load_dotenv
from groq import Groq

from utils.data_loader import load_listings

load_dotenv()


# ── Groq client ───────────────────────────────────────────────────────────────

def _get_groq_client():
    """Initialize and return a Groq client using GROQ_API_KEY from .env."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to a .env file in the project root."
        )
    return Groq(api_key=api_key)


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(description: str, size: str | None = None, max_price: float | None = None, session: dict | None = None) -> list[dict]:
    """
    Search the mock listings dataset for items matching the description,
    optional size, and optional price ceiling.

    Args:
        description: Keywords describing what the user is looking for
                     (e.g., "vintage graphic tee").
        size:        Size string to filter by, or None to skip size filtering.
                     Matching is case-insensitive (e.g., "M" matches "S/M").
        max_price:   Maximum price (inclusive), or None to skip price filtering.

    Returns:
        A list of matching listing dicts, sorted by relevance (best match first).
        Returns an empty list if nothing matches — does NOT raise an exception.

    Each listing dict has the following fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand, platform

    TODO:
        1. Load all listings with load_listings().
        2. Filter by max_price and size (if provided).
        3. Score each remaining listing by keyword overlap with `description`.
        4. Drop any listings with a score of 0 (no relevant matches).
        5. Sort by score, highest first, and return the listing dicts.

    Before writing code, fill in the Tool 1 section of planning.md.
    """
    #  
    """
    Search thrift listings by description, optionally filtering by size and max price.

    Scoring is based on keyword overlap between the user's description and each
    listing's title, description, and style_tags. Listings with a score of 0 are
    dropped. Results are sorted highest score first.

    Returns an empty list and sets session["error"] if no listings match.
    Returns a sorted list of matching listing dicts on success.
    """
    # Load all listings from the data source
    all_listings = load_listings()

    # Step 1: Filter by size and max_price if provided
    filtered = []
    for listing in all_listings:
        if size is not None and listing.get("size", "").lower() != size.lower():
            continue
        if max_price is not None and listing.get("price", 0.0) > max_price:
            continue
        filtered.append(listing)

    # Step 2: Score each remaining listing by keyword overlap with description
    keywords = set(description.lower().split())

    def score(listing: dict) -> int:
        # Build a bag of words from title, description, and style_tags
        words = set()
        words.update(listing.get("title", "").lower().split())
        words.update(listing.get("description", "").lower().split())
        for tag in listing.get("style_tags", []):
            words.update(tag.lower().split())
        return len(keywords & words)

    # Step 3: Drop zero-score listings and sort highest first
    results = sorted(
        [l for l in filtered if score(l) > 0],
        key=score,
        reverse=True,
    )

    # Step 4: Handle empty results
    if not results:
        if session is not None:
            session["error"] = (
                f"No listings found matching '{description}'"
                + (f" under ${max_price}" if max_price is not None else "")
                + (f" in size {size}" if size is not None else "")
                + ". Try broadening your search."
            )
        return []

    return results


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict, client) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest 1–2 complete outfits.

    Args:
        new_item: A listing dict (the item the user is considering buying).
        wardrobe: A wardrobe dict with an 'items' key containing a list of
                  wardrobe item dicts. May be empty — handle this gracefully.

    Returns:
        A non-empty string with outfit suggestions.
        If the wardrobe is empty, offer general styling advice for the item
        rather than raising an exception or returning an empty string.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If empty: call the LLM with a prompt for general styling ideas
           (what kinds of items pair well, what vibe it suits, etc.).
        3. If not empty: format the wardrobe items into a prompt and ask
           the LLM to suggest specific outfit combinations using the new item
           and named pieces from the wardrobe.
        4. Return the LLM's response as a string.

    Before writing code, fill in the Tool 2 section of planning.md.
    """
    #
    """
    Suggest outfit combinations for a thrifted item using the user's wardrobe.

    If the wardrobe is empty, returns general styling advice for the item.
    If the wardrobe has items, returns up to 2 specific outfit combinations
    using named pieces from the wardrobe.

    Never returns an empty string. Never raises an exception.
    Returns a string containing the LLM's styling suggestion.
    """
    item_summary = (
        f"{new_item.get('title', 'this item')} "
        f"({new_item.get('category', '')} · {new_item.get('style_tags', [])} · "
        f"colors: {new_item.get('colors', [])})"
    )

    wardrobe_items = wardrobe.get("items", [])

    if not wardrobe_items:
        # Empty wardrobe — ask for general styling advice, no wardrobe references
        prompt = (
            f"A user is considering buying: {item_summary}.\n\n"
            "They haven't shared their wardrobe yet. Give them general styling advice "
            "for this item: describe the vibe it suits, what types of pieces pair well "
            "with it, and what occasions it works for. Be specific about silhouettes, "
            "colors, and aesthetics. Keep it to 3–5 sentences, casual and friendly."
        )
    else:
        # Build a readable list of wardrobe pieces
        wardrobe_lines = []
        for item in wardrobe_items:
            line = (
                f"- {item.get('title', 'unknown item')} "
                f"({item.get('category', '')} · colors: {item.get('colors', [])})"
            )
            wardrobe_lines.append(line)
        wardrobe_summary = "\n".join(wardrobe_lines)

        prompt = (
            f"A user is considering buying: {item_summary}.\n\n"
            f"Here is what they already own:\n{wardrobe_summary}\n\n"
            "Suggest up to 2 complete outfits using the new item and specific named pieces "
            "from the wardrobe above. For each outfit, name the exact wardrobe pieces used "
            "and briefly describe the vibe. Keep it casual and specific — like advice from "
            "a friend who knows fashion, not a product description."
        )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a personal stylist helping someone build outfits around "
                    "thrifted finds. Be specific, casual, and use the actual item names provided."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict, client) -> str:
    """
    Generate a short, shareable outfit caption for the thrifted find.

    Args:
        outfit:   The outfit suggestion string from suggest_outfit().
        new_item: The listing dict for the thrifted item.

    Returns:
        A 2–4 sentence string usable as an Instagram/TikTok caption.
        If outfit is empty or missing, return a descriptive error message
        string — do NOT raise an exception.

    The caption should:
    - Feel casual and authentic (like a real OOTD post, not a product description)
    - Mention the item name, price, and platform naturally (once each)
    - Capture the outfit vibe in specific terms
    - Sound different each time for different inputs (use higher LLM temperature)

    TODO:
        1. Guard against an empty or whitespace-only outfit string.
        2. Build a prompt that gives the LLM the item details and the outfit,
           and asks for a caption matching the style guidelines above.
        3. Call the LLM and return the response.

    Before writing code, fill in the Tool 3 section of planning.md.
    """
    #
    """
    Generate a short, shareable OOTD caption for a thrifted item and outfit suggestion.

    Validates the outfit string before prompting the LLM. If the outfit is empty
    or whitespace-only, returns a descriptive error string without raising an exception.

    Returns a 2–4 sentence caption string styled like a real Instagram/TikTok OOTD post.
    """
    # Validate outfit input
    if not outfit.strip():
        return (
            f"Could not generate a fit card: the outfit suggestion for "
            f"'{new_item.get('title', 'this item')}' was empty or incomplete. "
            "Try running suggest_outfit again."
        )

    # Pull the fields the caption needs to mention naturally
    item_name = new_item.get("title", "this piece")
    price = new_item.get("price", "unknown price")
    platform = new_item.get("platform", "a thrift platform")

    prompt = (
        f"Write a 2–4 sentence Instagram/TikTok OOTD caption for this thrifted fit.\n\n"
        f"The thrifted item: {item_name} — found for ${price} on {platform}.\n"
        f"The outfit: {outfit}\n\n"
        "Rules:\n"
        f"- Mention '{item_name}', '${price}', and '{platform}' each exactly once, woven in naturally\n"
        "- Sound like a real person posting their outfit, not a product description\n"
        "- Capture the specific vibe of this outfit (name the aesthetic, mood, or occasion)\n"
        "- Keep it 2–4 sentences, no hashtags, no emojis unless they feel totally natural\n"
        "- Make it feel fresh — avoid generic openers like 'Obsessed with' or 'Loving this'"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are writing captions for a thrift fashion account. "
                    "Every caption should feel like it was written by the person wearing "
                    "the outfit — specific, casual, and authentic to the vibe described."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.95,
    )

    return response.choices[0].message.content.strip()