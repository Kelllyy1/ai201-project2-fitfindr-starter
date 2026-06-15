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
So the user provides a description of what they are looking for including their target price, size and style. This tool takes those 3 descriptions as input and finds the top 3 listing that match those descriptions most closely. It returns the 3 top matches in order of revelance.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): a brief explanation of the style of the clothing the user wishes to find
- `size` (str): the desired size of the clothing the user wishes to find
- `max_price` (float): the highest price the user is interested in spending on the clothing

**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->
This tool returns a list of 3 matching listings in order of relevance based on the provided description, size and max_price. The results contain the item's description, cost and condition.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->

---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
This tool takes an item and the wardrobe as input and returns another recommended item to pair it with from the listings. It also gives feedback on how to modify/style the items together.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): a list of items provided by the user to be evaluated so that a recommended item can be paired with them
- `wardrobe` (dict): this list tells the tool where to search for items to recommend to the user

**What it returns:**
<!-- Describe the return value -->
This tool returns the descriptions for items that would pair well with the list of items provided by the user as input. The recommended items are found from the lists of wardrobes provided as input to the tool. It also gives advice on how to modify all of the items to pair nicely with each other.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->

---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
This tool takes outfit suggestions and new item suggestions as input and returns ???
<!-- TODO: -->

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (dict): a list of suggested outfits that were output from the "search_listings" tool
- `new_item` (dict): same input as provided to the "suggest_outfit" tool

**What it returns:**
<!-- Describe the return value -->
<!-- TODO: ??? not sure tbh -->

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->

---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- Describe the logic your planning loop uses. What does it look at? What conditions change its behavior? How does it know when it's done? -->

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

**Step 2:**
<!-- What happens next? What was returned from step 1? What tool is called now? -->

**Step 3:**
<!-- Continue until the full interaction is complete -->

**Final output to user:**
<!-- What does the user actually see at the end? -->
