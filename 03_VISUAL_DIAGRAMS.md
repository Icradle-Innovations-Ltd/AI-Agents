# AI Concepts: Visual Diagrams & Illustrations

## 1. The Three Levels Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE THREE LEVELS OF AI                       │
└─────────────────────────────────────────────────────────────────┘

LEVEL 1: LARGE LANGUAGE MODELS (LLMs)
────────────────────────────────────────
        Input (Prompt)
              │
              ▼
        ┌──────────────┐
        │     LLM      │  ← ChatGPT, Claude
        │              │  ← Generates text
        │              │  ← Limited knowledge
        │              │  ← Passive
        └──────────────┘
              │
              ▼
        Output (Response)

Example:
   Input:  "Draft an email"
   Output: [Professional email] ✓
   
   Input:  "When is my meeting?"
   Output: [Cannot answer] ✗ (no calendar access)


LEVEL 2: AI WORKFLOWS
─────────────────────
    Input (Request)
          │
          ▼
    ┌──────────────────────────────────────────┐
    │        Human-Defined Workflow Path       │
    │                                          │
    │  Step 1 → Step 2 → Step 3 → Step 4      │
    │ (Gather) (Process) (Refine) (Output)    │
    │    ↓        ↓         ↓        ↓        │
    │  API 1    API 2     API 3    LLM      │
    │                                          │
    └──────────────────────────────────────────┘
          │
          ▼
    Output (Result)
    
Key: Human programs the path → LLM follows instructions → Limited flexibility

Example Workflow:
   Step 1: Search Google Calendar
   Step 2: Extract meeting time
   Step 3: Return result
   
   Works for: "When is my meeting?" ✓
   Fails for:  "What's the weather then?" ✗ (weather step not defined)


LEVEL 3: AI AGENTS
──────────────────
        Goal / Request
              │
              ▼
    ┌──────────────────────────────────────────┐
    │   LLM Makes All Decisions (Autonomous)   │
    │                                          │
    │  ┌──────────┐                           │
    │  │ Reasoning│  "What's the best way?"  │
    │  └────┬─────┘                           │
    │       ▼                                  │
    │  ┌──────────┐                           │
    │  │  Acting  │  "Use these tools"       │
    │  └────┬─────┘                           │
    │       ▼                                  │
    │  ┌──────────┐                           │
    │  │Observing │  "Is the result good?"   │
    │  └────┬─────┘                           │
    │       ▼                                  │
    │  ┌──────────┐                           │
    │  │Iterating?│  "Need to improve?"      │
    │  └──────────┘                           │
    │       │ Yes? Loop back to Reasoning    │
    │       │ No?  Continue                  │
    │       ▼                                  │
    └──────────────────────────────────────────┘
              │
              ▼
        Final Output
    
Key: LLM is decision-maker → Autonomous reasoning → Adapts to new scenarios

Example: Video Search Agent
   Goal: "Find videos of skiers"
   Reason: "Skier = person on skis in snow"
   Act: Search video library
   Observe: Found 5 clips
   Iterate: Tag each as "skier", "mountain", "snow"
   Output: Tagged video clips
```

---

## 2. The Critical Difference: Workflow vs Agent

```
┌──────────────────────────────────────────────────────────────────┐
│                 FROM WORKFLOW TO AGENT                           │
│                 What's the ONE Big Change?                       │
└──────────────────────────────────────────────────────────────────┘


WORKFLOW (Human Decision-Maker)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Goal: "Create social media posts from news"                   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ HUMAN decides the path:                                 │ │
│  │ • Should I use Google Sheets or Word? → Google Sheets   │ │
│  │ • How to compile links? → Direct insert                 │ │
│  │ • Which tools to use? → Perplexity + Claude             │ │
│  │ • How to structure post? → LinkedIn best practices      │ │
│  │ • Is output good? → No, needs to be funnier             │ │
│  │                                                          │ │
│  │ HUMAN ACTION: Manually rewrite Claude prompt             │ │
│  │              Regenerate → Evaluate → Repeat              │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  Result: Workflow follows predefined human path                │
│          Humans do ALL the thinking & iterating                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


     ║
     ║  THE BIG CHANGE
     ║  Replace Human Decision-Maker with LLM
     ║
     ▼


AGENT (LLM Decision-Maker)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Goal: "Create social media posts from news"                   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ LLM REASONS & DECIDES:                                   │ │
│  │ • "I need to gather news → Use Google API"               │ │
│  │ • "Summarize them → Use Perplexity"                      │ │
│  │ • "Write posts → Use Claude"                             │ │
│  │ • "Evaluate quality → Check LinkedIn best practices"     │ │
│  │ • "Post needs humor → Adjust tone → Regenerate"          │ │
│  │ • "Repeat → Until quality threshold met"                 │ │
│  │                                                          │ │
│  │ LLM ACTION: Autonomously executes & iterates              │ │
│  │             No human intervention needed                  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  Result: Agent adapts to goal, makes all decisions,            │
│          Iterates autonomously without human prompting         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Capability Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│           CAPABILITY MATRIX: LLM vs WORKFLOW vs AGENT            │
└─────────────────────────────────────────────────────────────────┘

                        LLM      WORKFLOW    AGENT
                        ───      ────────    ─────

Can generate text?      ✓✓✓       ✓✓✓        ✓✓✓

Can access data?        ✗         ✓✓         ✓✓

Can access specific?    ✗         ✓ (set)    ✓ (autonomous)

Knows what tools use?   ✗         ✗          ✓

Can adapt to new?       ✗         ✗          ✓

Can iterate autonomously? ✗       ✗          ✓

Makes own decisions?    ✗         ✗          ✓

Requires human logic?   N/A       ✓✓✓        ✗

Flexible with goals?    Limited   Rigid      ✓✓✓


SUMMARY BY CAPABILITY:
─────────────────────

Task:          "Draft an email"
  LLM:  ✓ Works great
  WF:   ✓ Works (unnecessary)
  Agent: ✓ Works (overkill)

Task:          "Check my calendar then tell me meeting time"
  LLM:  ✗ Can't access calendar
  WF:   ✓ Works well (predefined calendar check)
  Agent: ✓ Works (less efficient than WF for this task)

Task:          "Create social posts from news + evaluate + iterate quality"
  LLM:  ✗ No news access, no iteration logic
  WF:   ✓ Works if human evaluates & rewrites
  Agent: ✓ Works best (fully autonomous, handles all steps)

Task:          "Do something we didn't program you for"
  LLM:  ? Depends on prompt cleverness
  WF:   ✗ Complete failure (path not defined)
  Agent: ✓ Adapts (reasons about approach, finds tools)
```

---

## 4. The ReAct Framework

```
┌──────────────────────────────────────────────────────────────────┐
│                    THE ReAct FRAMEWORK                           │
│           Most Common AI Agent Architecture                      │
└──────────────────────────────────────────────────────────────────┘


ReAct = Reasoning + Acting


         ┌─────────────────────────────────┐
         │     Agent Receives Goal          │
         │  "Find skier videos and tag"    │
         └────────────┬────────────────────┘
                      │
                      ▼
         ┌─────────────────────────────────┐
         │  1. REASONING                    │
         │  ─────────────                   │
         │  Analyze goal:                   │
         │  • Skier = person on skis       │
         │  • In snow/mountains            │
         │  • Going fast                    │
         │  What tools do I have?           │
         │  What's the best approach?       │
         └────────────┬────────────────────┘
                      │
                      ▼
         ┌─────────────────────────────────┐
         │  2. ACTING                       │
         │  ───────                         │
         │  Take action:                    │
         │  • Search video library          │
         │  • Analyze clips with vision AI  │
         │  • Identify potential matches    │
         └────────────┬────────────────────┘
                      │
                      ▼
         ┌─────────────────────────────────┐
         │  3. OBSERVING                    │
         │  ──────────────                  │
         │  Examine results:                │
         │  • Found 5 clips                 │
         │  • 3 are definitely skiers       │
         │  • 2 are questionable            │
         │  Did it work?                    │
         └────────────┬────────────────────┘
                      │
                      ▼
         ┌─────────────────────────────────┐
         │  4. DECISION POINT               │
         │  ──────────────────              │
         │  Is the goal complete?           │
         │                                  │
         │  ┌──────────┐   ┌──────────────┐ │
         │  │  NO      │   │   YES        │ │
         │  │ Need more│   │ Return output│ │
         │  │ iteration│   │ Done!        │ │
         │  └──────┬───┘   └──────────────┘ │
         │         │                         │
         └─────────┼─────────────────────────┘
                   │
                   └──→ Loop back to REASONING
                       ("Refine approach")
                       │
                       └──→ Continue ACTING, OBSERVING...


KEY INSIGHT:
───────────
The agent doesn't just execute once. It reasons about outcomes
and automatically repeats/refines until the goal is achieved.

A workflow would say:
  "Step 1: Search videos
   Step 2: Tag skiers
   Done."

An agent says:
  "Step 1: Search and tag
   Step 2: Evaluate results
   Step 3: Found 80% confident? Good enough!
           Found 60% confident? Need more searches
   Step 4: Refine search criteria and retry"
```

---

## 5. Example Journey: Social Media Post Creation

```
┌──────────────────────────────────────────────────────────────────┐
│          SOCIAL MEDIA POST CREATION: Three Approaches            │
└──────────────────────────────────────────────────────────────────┘


LLM APPROACH (No External Access)
──────────────────────────────────
  User: "Create a LinkedIn post about AI agents"
  
  Claude: "I'm unable to provide recent news articles..."
  
  Result: ✗ Generic post with outdated examples


WORKFLOW APPROACH (Predefined Path)
────────────────────────────────────
  User: "Create LinkedIn post from recent AI news"
  
  Step 1: Scrape news from TechCrunch
  Step 2: Summarize with Perplexity
  Step 3: Draft with Claude
  Step 4: Schedule with Make.com
  Step 5: Human checks → "Needs to be funnier"
  Step 6: Human rewrites Claude prompt
  Step 7: Regenerate → Human checks again
          ... repeat until satisfied
  
  Result: ✓ Good post, but requires human iteration
  
  If user later asks: "Also create TikTok version"
  Response: ✗ Cannot do it (workflow doesn't have TikTok step)
           Must manually add TikTok generation step


AGENT APPROACH (Autonomous & Adaptive)
───────────────────────────────────────
  User: "Create engaging LinkedIn post + TikTok version from recent AI news"
  
  Agent REASONING:
  ├─ Goal: Create 2 pieces of content
  ├─ Step 1: I need current news → Use news API
  ├─ Step 2: Need summaries → Use Perplexity
  ├─ Step 3: LinkedIn post → Use Claude with LinkedIn tone
  ├─ Step 4: TikTok version → Different tone/format
  ├─ Step 5: Evaluate quality → LinkedIn best practices?
  └─ Step 6: Funny enough? → If not, iterate
  
  Agent ACTING:
  ├─ Retrieves news from 5 sources
  ├─ Generates summaries
  ├─ Creates LinkedIn post (formal, informative)
  ├─ Creates TikTok script (casual, hooks, trending sounds)
  └─ Evaluates both against quality criteria
  
  Agent OBSERVING:
  ├─ LinkedIn post: 95% quality → Good!
  ├─ TikTok script: 70% quality → Too formal
  └─ Decision: Need iteration
  
  Agent ITERATING:
  ├─ Adjusts TikTok tone to be more casual
  ├─ Adds relevant emojis and trendy language
  ├─ Re-evaluates: 92% quality → Excellent!
  └─ Delivers both outputs
  
  Result: ✓ Both posts created, autonomously iterated to quality
          ✓ Adapted to new TikTok requirement without reprogramming
          ✓ No human intervention needed


COMPARISON:
───────────
  Effort:    Workflow >> Agent (human had to iterate)
  Flexibility: Agent >> Workflow (handles new TikTok request)
  Quality:   Agent ≥ Workflow (better after autonomous iteration)
  Time:      Agent < Workflow (no manual rewriting cycles)
```

---

## 6. Decision Tree: LLM vs Workflow vs Agent

```
┌─────────────────────────────────────────────────────────────────┐
│        DECISION TREE: Which Should I Use?                       │
└─────────────────────────────────────────────────────────────────┘


Start: What do you need to do?
│
├─ Just generate/edit text?
│  └─→ Use LLM ✓
│      (ChatGPT, Claude)
│
├─ Need to access external data + generate text?
│  │
│  └─ Do you know the exact steps/tools needed?
│     │
│     ├─ YES → Use WORKFLOW ✓
│     │        (Make.com, Zapier, n8n)
│     │        Good for: Repetitive tasks with clear paths
│     │
│     └─ NO or you want flexibility?
│        └─→ Use AGENT ✓
│            (Requires AI Agent framework)
│            Good for: Complex goals, unknown paths, iteration needed
│
└─ Need the system to make its own decisions autonomously?
   └─→ Use AGENT ✓
       Essential for agent use


DETAILED QUESTIONS TO ASK:
──────────────────────────

1. Can a human pre-define all steps?
   Yes → WORKFLOW or AGENT (either works)
   No  → AGENT (only option)

2. Will the requirements change after launch?
   Yes → AGENT (more flexible)
   No  → WORKFLOW (simpler, easier to build)

3. Does it need to iterate/improve autonomously?
   Yes → AGENT (must have)
   No  → WORKFLOW (not needed)

4. Does it need to choose which tools to use?
   Yes → AGENT (required)
   No  → WORKFLOW (you choose for it)

5. Is it a repetitive task with same path every time?
   Yes → WORKFLOW (ideal)
   No  → AGENT (better fit)


EXAMPLES BY USE CASE:
────────────────────

Use LLM:
  • Brainstorming ideas
  • Drafting copy
  • Answering questions
  • Code generation

Use WORKFLOW:
  • Daily email digest (news → summarize → send)
  • Content scheduling (write → format → post)
  • Invoice processing (extract → validate → file)
  • Data entry pipeline

Use AGENT:
  • Customer support (understand intent → find docs → draft answer)
  • Research assistant (gather → analyze → iterate → report)
  • Content optimization (generate → evaluate → refine)
  • Real estate property analysis (collect data → score → recommend)
```

---

## 7. The Iteration Difference

```
┌──────────────────────────────────────────────────────────────────┐
│                HOW ITERATION WORKS                               │
│            Workflow vs Agent                                     │
└──────────────────────────────────────────────────────────────────┘


WORKFLOW ITERATION (Manual, Human-Driven)
──────────────────────────────────────────

  First Draft:
  ┌──────────────────────────┐
  │ LinkedIn Post: "AI is    │
  │ cool. Check out agents." │
  └──────────────┬───────────┘
                 │
                 ▼
  Human Evaluation:
  ┌──────────────────────────┐
  │ "Not funny enough!        │
  │ User wants humor."        │
  └──────────────┬───────────┘
                 │
                 ▼
  Human Action (Manual):
  ┌──────────────────────────┐
  │ HUMAN rewrites prompt:   │
  │ "Add 3 jokes, use puns"  │
  │                           │
  │ Calls Claude again       │
  └──────────────┬───────────┘
                 │
                 ▼
  Second Draft:
  ┌──────────────────────────┐
  │ [New version with jokes] │
  └──────────────┬───────────┘
                 │
                 ▼
  Human Evaluation:
  ┌──────────────────────────┐
  │ "Better, but still       │
  │ missing edge."           │
  └──────────────┬───────────┘
                 │
                 ▼
  ... HUMAN REPEATS ...
  
  Result: Multiple manual cycles, slow, error-prone


AGENT ITERATION (Autonomous, Self-Driven)
──────────────────────────────────────────

  Goal Received:
  ┌──────────────────────────┐
  │ "Create hilarious        │
  │  LinkedIn post about AI" │
  └──────────────┬───────────┘
                 │
                 ▼
  Agent Reasoning:
  ┌──────────────────────────┐
  │ "I need to:              │
  │ 1. Draft post            │
  │ 2. Add humor             │
  │ 3. Check LinkedIn rules  │
  │ 4. Iterate until great"  │
  └──────────────┬───────────┘
                 │
                 ▼
  Draft V1:
  ┌──────────────────────────┐
  │ [Initial post with jokes]│
  └──────────────┬───────────┘
                 │
                 ▼
  Agent Evaluation (Built-in):
  ┌──────────────────────────┐
  │ Score: 7/10              │
  │ Issues:                  │
  │ • Not edgy enough        │
  │ • Timing awkward         │
  │ Decision: Iterate        │
  └──────────────┬───────────┘
                 │
                 ▼
  Draft V2:
  ┌──────────────────────────┐
  │ [Edgier, better timing]  │
  └──────────────┬───────────┘
                 │
                 ▼
  Agent Evaluation:
  ┌──────────────────────────┐
  │ Score: 9/10              │
  │ Good: Matches criteria   │
  │ Decision: Done!          │
  └──────────────┬───────────┘
                 │
                 ▼
  Return Final Output
  
  Result: Fast, consistent, autonomous improvement
```

---

## 8. Tool Access Visualization

```
┌──────────────────────────────────────────────────────────────────┐
│               TOOL ACCESS & DECISION MAKING                      │
└──────────────────────────────────────────────────────────────────┘


LLM: Limited Tool Access
─────────────────────────
  
  ┌──────────┐
  │   LLM    │
  │          │
  │ Can use: │
  │ • Text   │
  │ • Memory │
  └──────────┘
      │
      └─ Cannot reach: Calendar, APIs, Web, Files


WORKFLOW: Predefined Tool Access
─────────────────────────────────
  
  ┌──────────────────────────────────────┐
  │        HUMAN DECIDES PATH             │
  │  ┌──────────────────────────────────┐ │
  │  │ Workflow: IF calendar requested  │ │
  │  │ THEN call Google Calendar API    │ │
  │  │                                  │ │
  │  │ Workflow: IF news needed         │ │
  │  │ THEN call NewsAPI                │ │
  │  └──────────────────────────────────┘ │
  └──────────────────────────────────────┘
          │              │
          ▼              ▼
    Google Calendar    NewsAPI
    
  Tools Accessible: Only what human predefined
  Who Chooses: Human (before runtime)


AGENT: Autonomous Tool Discovery & Selection
─────────────────────────────────────────────
  
  ┌──────────────────────────────────────────────────┐
  │              LLM (Decision-Maker)                 │
  │                                                  │
  │  Available Tools Register:                       │
  │  • Calendar API (Google Calendar)                │
  │  • Weather API (OpenWeather)                     │
  │  • News API (NewsAPI)                            │
  │  • Search (Google Search)                        │
  │  • Vision (ImageAnalysis)                        │
  │  • Database (SQL)                                │
  │  ... [dozens more]                               │
  │                                                  │
  │  Agent Thinks:                                   │
  │  "Goal: Find and analyze recent tech news       │
  │   What tools do I need?                          │
  │   → NewsAPI to find articles                     │
  │   → Vision to analyze images in articles         │
  │   → Database to store findings"                  │
  │                                                  │
  │  Agent Acts:                                     │
  │  → Selects & calls appropriate tools            │
  │  → Chains results together                       │
  │  → Iterates if needed                            │
  └──────────────────────────────────────────────────┘
          │        │          │
          ▼        ▼          ▼
      NewsAPI   Vision API  Database
      
  Tools Accessible: All available tools
  Who Chooses: LLM (at runtime, dynamically)
```

