# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
So the user provides a description of what they are looking for including their target price, size and style. This tool searches through the listings to find items that match the provided inputs.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): a brief explanation of the style of the clothing the user wishes to find
- `size` (str): the desired size of clothing the user wishes to find or None to skip size filtering
- `max_price` (float): the highest price the user wants or None to skip price filtering

**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->
This tool returns a list of dictionaries matching the inputs provided. The list is sorted in order of relevance providing the best match first. An empty list is returned if nothing matches the input.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->
If no listings match the agent returns an empty list. It does not have to raise an exception.

---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
The user provides a thrifted item and their wardrobe and this tool provides a suggestion for up to 2 complete outfits.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): a dictionary of items provided by the user that they are considering buying.
- `wardrobe` (dict): a wardrobe dictionary with an "items" key. The "items" key contains a list of wardrobe item dictionaries. So a wardrobe dictionary with a key that contains a list of dictionaries describing the items.

**What it returns:**
<!-- Describe the return value -->
This tool returns a string containing a suggestion for items that would pair well with the list of items provided by the user as input.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->
If the wardrobe is empty it returns general styling advice for the item instead of returning an empty string. It does not return an empty string and it does not raise an exception.
---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
This tool takes outfit suggestions and generates a short, shareable outfit caption for the thrift that was found.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (str): the outfit suggestion string returned from the "suggest_outfit" tool
- `new_item` (dict): the listing dictionary for the thrifted item

**What it returns:**
<!-- Describe the return value -->
This tool returns a string that is 2-4 sentences in length that can be used as an Instagra/TikTok caption.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->
If the outfit is incomplete or empty, the tool should return a descriptive error message string. The tool should not raise an exception.

---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- Describe the logic your planning loop uses. What does it look at? What conditions change its behavior? How does it know when it's done? -->

### Tool: search_listings()
- create a blank list to store the `results[]`
- use the `description` provided as input
- load all the listings with the `load_listings()`. Each listing dict has the following fields:
     - id
     - title
     - description
     - category
     - style_tags (list)
     - size
     - condition
     - price (float)
     - colors (list)
     - brand
     - platform
- filter by `max_price` and `size` (if provided)
- score each remaining listing by keyword overlap with `description`
- drop any listings with a score of 0
- sort by score, highest first, and return the listing dictionary results
- before returning results, check if it is empty:
     - if not results: set an error message in the session, return early and cleanly and do not raise an exception
     - else, selected_item = results[0]
- proceed to the suggest_outfit tool

### Tool: suggest_outfit()
- check to see if wardrobe['items'] is empty, if not wardrobes['items']:
     - if empty, prompt the LLM to generate general styling ideas (for e.g. describe what items pair well together or what vybe it suits)
     - else, organize the wardrobe items into a prompt and ask the LLM to suggest specific outfit combinations using the new item and named pieces from the wardrobe.
- finally return `response`, which is a string containing the LLM's response
- proceed to the `create_fit_card` tool

### Tool: create_fit_card
- validate input against any empty or white-space only outfit strings; e.g using `if outfit.strip():` to remove leading whitespaces
<!-- (suggest_outfit should not be empty since I am prompting LLM to generate generic suggestion if the wardrobe is empty, but it it still returns an empty string generate a generic suggestion based on the `new_item` provided as input) -->
- build a prompt that gives the LLM the item details and the outfits, and asks for a caption matching the style guidelines below. The caption should:
     - feel casual and authentic, like a real OOTD post, not a product description
     - mention the item name, price, and platform naturall (one each)
     - capture the outfit vybe in specific terms
     - sound different each time for different inputs, using a higher LLM temperature
- call the LLM and return the `final_response`

---

## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->

---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | |
| suggest_outfit | Wardrobe is empty | |
| create_fit_card | Outfit input is missing or incomplete | |

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     ASCII art, a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html), or an embedded
     sketch are all fine. You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->

     ---
config:
  layout: elk
---
flowchart TD
    UserInput[User Input<br/>description, max_price, size] -->|triggers| PlanningLoop[Planning Loop<br/>Agent Decision Logic]
    
    PlanningLoop -->|calls| SearchListings[search_listings]
    
    SearchListings -->|load_listings| ListingsDB[(Listings Database)]
    ListingsDB -->|returns| SearchListings
    
    SearchListings -->|filter & score| FilterScore[Filter by price/size<br/>Score by keyword overlap]
    
    FilterScore -->|check results| ResultsCheck{Results<br/>Empty?}
    
    ResultsCheck -->|yes| ErrorState[Set Error Message<br/>in Session]
    ErrorState -->|early return| SessionState[(Session State)]
    
    ResultsCheck -->|no| SelectItem[selected_item = results0]
    SelectItem -->|pass item| SuggestOutfit[suggest_outfit]
    
    SuggestOutfit -->|check| WardrobeCheck{Wardrobe<br/>Empty?}
    
    WardrobeCheck -->|yes| GenericSuggestion[Generate Generic<br/>Styling Ideas]
    WardrobeCheck -->|no| SpecificSuggestion[Suggest Outfit<br/>with Named Pieces]
    
    GenericSuggestion -->|LLM response| OutfitResponse[outfit string]
    SpecificSuggestion -->|LLM response| OutfitResponse
    
    OutfitResponse -->|store| SessionState
    OutfitResponse -->|pass outfit| CreateFitCard[create_fit_card]
    
    CreateFitCard -->|validate| ValidateOutfit{Outfit Valid<br/>& Non-empty?}
    
    ValidateOutfit -->|no| GenericCaption[Generate Generic<br/>Caption from Item]
    ValidateOutfit -->|yes| BuildPrompt[Build LLM Prompt<br/>with Item & Outfit]
    
    GenericCaption -->|LLM response| FinalCaption[final_response<br/>OOTD Caption]
    BuildPrompt -->|LLM response<br/>high temp| FinalCaption
    
    FinalCaption -->|store| SessionState
    SessionState -->|return to user| UserOutput[User Output<br/>Fit Card with Caption]
    
    classDef userNode stroke:#38bdf8,fill:#f0f9ff
    classDef toolNode stroke:#a78bfa,fill:#f5f3ff
    classDef decisionNode stroke:#fb923c,fill:#fff7ed
    classDef storageNode stroke:#4ade80,fill:#f0fdf4
    classDef outputNode stroke:#fb7185,fill:#fff1f2
    
    class UserInput,UserOutput userNode
    class PlanningLoop,SearchListings,SuggestOutfit,CreateFitCard toolNode
    class ResultsCheck,WardrobeCheck,ValidateOutfit decisionNode
    class ListingsDB,SessionState storageNode
    class ErrorState,GenericSuggestion,SpecificSuggestion,GenericCaption,BuildPrompt,FinalCaption outputNode

---

## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->

**Milestone 3 — Individual tool implementations:**

**Milestone 4 — Planning loop and state management:**

---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**
<!-- What does the agent do first? Which tool is called? With what input? -->
Agent calls "search_listings" tool -> search_listings("vintage graphic tee", max_price=30.0)

**Step 2:**
<!-- What happens next? What was returned from step 1? What tool is called now? -->
The search_listings tool searches through the listings.json and returns a list of (3) dictionaries that match the description and price provided by the input. The most relevant item is returned first.
Next, agent calls "suggest_outfit" -> suggest_outfit(new_item=<band tee>, wardrobe=<user's wardrobe>)

**Step 3:**
<!-- Continue until the full interaction is complete -->
The suggest_ouitfit tool returns a str with an outfit suggestion of items that can be paired well with the new item provided by user.
The str returned from suggest_outfit tool and new_item provided to suggest_outfit tool is input for the "create_fit_card" tool -> create_fit_card(outfit=<suggestion>, new_item=<band tee>)

**Final output to user:**
<!-- What does the user actually see at the end? -->
The create_fit_card tools returns a short (2-4 sentence), shareable suggestion str that can be used as an Instagram or TikTok caption
