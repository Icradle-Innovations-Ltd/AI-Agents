# AI Concepts: Practice Worksheet & Exercises

## Exercise 1: Identify the Tool (LLM vs Workflow vs Agent)

For each scenario, identify which tool would be best suited and explain why.

### 1.1 Scheduling Assistant
**Scenario**: You want a system that:
- Looks at your calendar
- Checks attendees' availability
- Suggests best meeting time
- Books the meeting
- Sends confirmation emails

```
Best Tool: _______________

Why: _______________________________________________


Can LLM do it alone? Yes / No
  Reason: _______________________________________________

Can a Workflow do it? Yes / No
  Reason: _______________________________________________

Would an Agent be better? Yes / No
  Reason: _______________________________________________
```

---

### 1.2 Email Drafter
**Scenario**: You want to generate a professional email from a bullet-point outline.

```
Best Tool: _______________

Why: _______________________________________________


Explain your choice in one sentence: _______________________________________________
```

---

### 1.3 Customer Support Bot
**Scenario**: You want a system that:
- Understands customer questions
- Searches product documentation
- Generates appropriate responses
- Learns what questions customers ask most
- Improves responses over time

```
Best Tool: _______________

Why: _______________________________________________


Which ability requires an Agent (not Workflow)?
_______________________________________________
```

---

### 1.4 Daily News Digest
**Scenario**: You want a system that:
- Fetches news from 5 sources
- Summarizes each article (max 2 sentences)
- Creates a daily digest
- Emails it to you every morning at 8 AM
- Always follows the same format

```
Best Tool: _______________

Why: _______________________________________________


Could you switch this from a Workflow to an Agent? 
When would that be beneficial?
_______________________________________________
```

---

### 1.5 Code Debugger
**Scenario**: You want a system that:
- Reads your code
- Identifies bugs
- Suggests fixes
- Tests the fixes
- Iterates until all tests pass

```
Best Tool: _______________

Why: _______________________________________________


Why is iteration important for this task?
_______________________________________________
```

---

## Exercise 2: Workflow Design

Design a workflow for the following task:

**Goal**: Create a weekly social media content calendar from trending topics

### What You Know:
- Use Twitter API to find trending topics
- Use news API to get articles about trending topics
- Use Claude to generate tweet ideas
- Schedule using Buffer API
- Run every Monday at 8 AM

### Your Task:

**Step 1**: List all the steps in order
```
1. _______________________________
2. _______________________________
3. _______________________________
4. _______________________________
5. _______________________________
```

**Step 2**: Identify which tool does what
```
Step __ : Twitter API  (Get trending topics)
Step __ : News API     (Get related articles)
Step __ : Claude       (Generate content)
Step __ : Buffer API   (Schedule tweets)
Step __ : Scheduler    (Run at 8 AM Monday)
```

**Step 3**: What would break this workflow?
```
- If a trending topic has no relevant news
  How would workflow fail? _______________________________________________
  
- If you wanted to add Instagram posts too
  How would workflow fail? _______________________________________________
  
- If you wanted the system to evaluate if tweets are good
  How would workflow fail? _______________________________________________
```

**Step 4**: How would an Agent handle these better?
```
Problem 1 (No news): _______________________________________________
Problem 2 (Instagram): _______________________________________________
Problem 3 (Quality evaluation): _______________________________________________
```

---

## Exercise 3: ReAct Framework

Practice breaking down a goal using the ReAct framework.

### Goal: "Find and summarize the top 3 research papers on AI agents published this year"

#### Step 1: REASONING
What does the agent need to do?
```
Problem decomposition:
- Need to: Find papers on AI agents
- Need to: Filter by publication date (this year only)
- Need to: Rank them (top 3)
- Need to: Summarize each
- Need to: Combine into report

What tools would I need?
- _______________________________________________
- _______________________________________________
- _______________________________________________
```

#### Step 2: ACTING
What actions would the agent take?
```
Action 1: _______________________________________________
Action 2: _______________________________________________
Action 3: _______________________________________________
Action 4: _______________________________________________
Action 5: _______________________________________________
```

#### Step 3: OBSERVING
What would the agent check?
```
After gathering papers:
- Are they all from this year? Yes / No
- Are all summaries high quality? Yes / No
- Did I find enough papers (top 3)? Yes / No

Questions to ask:
- _______________________________________________
- _______________________________________________
```

#### Step 4: ITERATING
Would the agent need to do more work?
```
If papers not from this year:
Action: _______________________________________________

If summaries are too long:
Action: _______________________________________________

If only found 1 paper:
Action: _______________________________________________
```

---

## Exercise 4: Compare Three Approaches

**Task**: "Generate a monthly sales report with insights"

### Approach A: Using Just LLM

**Process**:
```
1. User inputs: "Sales data for March"
2. LLM generates: Generic report from memory
3. Problem: _______________________________________________
4. Result Quality: Low / Medium / High
```

**Pros**: 
```
- _______________________________________________
```

**Cons**:
```
- No access to actual sales data
- _______________________________________________
```

---

### Approach B: Using Workflow

**Process**:
```
Step 1: Query database for sales figures
Step 2: Calculate growth percentages
Step 3: Claude creates report
Step 4: Email to stakeholders
Step 5: Run on first day of month
```

**Pros**:
```
- Uses real data
- _______________________________________________
```

**Cons**:
```
- Can't analyze unexpected trends
- _______________________________________________
```

---

### Approach C: Using Agent

**Process**:
```
Goal: "Create insightful monthly sales report with recommendations"

Agent Reasons:
- Need data from database
- Need to analyze trends
- Need to compare to last month
- Need to identify anomalies
- Need quality check

Agent Acts:
- Gets sales data
- Calculates metrics
- Analyzes patterns
- Compares to baseline
- Generates insights
- Creates report

Agent Observes:
- Are insights significant?
- Does report meet quality standards?
- Should I include special findings?

Agent Iterates:
- If insights weak: Analyze deeper
- If format wrong: Reformat
- If anything unclear: Clarify
```

**Pros**:
```
- Autonomous analysis
- _______________________________________________
- _______________________________________________
```

**Cons**:
```
- More expensive to run
- _______________________________________________
```

**Which approach would you recommend?** 
```
_______________________________________________
Why? _______________________________________________
```

---

## Exercise 5: The Iteration Challenge

**Scenario**: Building a system to generate marketing copy for products

### Version 1: LLM Only
```
Input: "Write marketing copy for wireless headphones"
Output: "Wireless headphones are great for listening to music..."

Problem: Generic, not optimized for conversions

Can it iterate and improve itself?  Yes / No
Why? _______________________________________________
```

### Version 2: Workflow
```
Step 1: Get product specs from database
Step 2: Claude generates copy
Step 3: Count words (must be 50-100)
Step 4: If too long/short, human rewrites prompt
Step 5: Claude regenerates
Step 6: Human checks quality
Step 7: If good, post; if not, repeat step 4
```

**How many times would a human need to rewrite the prompt to get good copy?**
```
Likely iterations: 1-3 times
Why? _______________________________________________
```

### Version 3: Agent
```
Goal: "Generate compelling marketing copy that maximizes conversions"

Agent Reasoning:
├─ I need product specs
├─ I need to understand target audience
├─ I need to write persuasive copy
├─ I need to A/B test elements
├─ I need to optimize for conversions

Agent Actions:
├─ Get specs and audience data
├─ Generate multiple copy variations
├─ Evaluate against best practices
├─ Test CTA button variations
├─ Measure simulated conversion impact
├─ Select best version

Agent Iteration:
├─ V1: "Generic but clear" (70% conversion potential)
├─ Observe: Missing urgency and social proof
├─ V2: "Add scarcity + testimonials" (85% potential)
├─ Observe: Still missing emotional appeal
├─ V3: "Add emotional hook" (94% potential)
├─ Observe: Met quality threshold
└─ Return V3
```

**How many iterations would the agent autonomously run?**
```
Likely iterations: 3-5 times
Why? _______________________________________________
```

**Which approach is better?**
```
Answer: _______________________________________________
Why? _______________________________________________
```

---

## Exercise 6: Tool Selection Decision Tree

You're an agent given this goal: "Help customers find the perfect product"

**Available Tools**:
- Product Database API
- Customer History API  
- Search Engine API
- Chat/Conversation API
- Recommendation Engine API
- Purchase API

### Decision Points

**Step 1**: Customer says "I need a laptop for coding"
```
Which tools would you use (and in what order)?
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

Why this order? _______________________________________________
```

**Step 2**: Customer says "Something like I bought before but better"
```
Which tools would you use?
1. _______________________________________________
2. _______________________________________________

Why? _______________________________________________
```

**Step 3**: Customer says "I don't know what I need"
```
What would you do differently?
_______________________________________________

Which additional tools might help?
_______________________________________________
```

**Step 4**: After recommendation, customer says "Too expensive"
```
Would you:
A) Recommend the same product again?
B) Ask what budget they have?
C) Search for alternatives?
D) Suggest financing options?

Answer: _______________________________________________
Why? _______________________________________________
```

---

## Exercise 7: Common Mistakes

### Mistake 1: "We built a 500-step automation, so it's an AI Agent"

**Why is this wrong?**
```
_______________________________________________
_______________________________________________
```

**The real question to ask:**
```
"Who makes the decisions?"
A) Human programs all decisions → Workflow
B) LLM makes decisions → Agent

This system has decision-maker: _______________
```

---

### Mistake 2: "Our system can access 10 different APIs, so it's an agent"

**Why is this not enough?**
```
_______________________________________________
```

**What else is needed for an agent?**
```
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________
```

---

### Mistake 3: "Our agent iterates once and delivers output"

**Why is this missing the point of an agent?**
```
_______________________________________________
```

**Iteration in agents means:**
```
A) Run the workflow once more
B) Evaluate quality, then decide if more work needed
C) Human evaluates and decides

Correct answer: _______________________________________________
```

---

## Scenario Analysis

### Scenario: Resume Screening System

**Current Workflow:**
```
Step 1: Receive resume (PDF)
Step 2: Claude extracts key info
Step 3: Score against job requirements (preset weights)
Step 4: Email hiring manager the score
Step 5: Manual review by human
```

**Problems with this workflow:**
```
Problem 1: _______________________________________________
Problem 2: _______________________________________________
Problem 3: _______________________________________________
```

**How would an agent improve this?**
```
Reasoning improvement:
"Instead of fixed weights, I would..."
_______________________________________________

Acting improvement:
"I would use additional tools like..."
_______________________________________________

Iteration improvement:
"Instead of one score, I would..."
_______________________________________________
```

**What tools would the agent need?**
```
- _______________________________________________
- _______________________________________________
- _______________________________________________
- _______________________________________________
```

---

## Reflection Questions

### Q1: When would you choose a Workflow over an Agent?
```
Answer: _______________________________________________
Example: _______________________________________________
```

### Q2: What's the most important trait of an AI Agent?
```
Answer: _______________________________________________
Why? _______________________________________________
```

### Q3: Can an agent work without access to external tools?
```
Answer: _______________________________________________
Explain: _______________________________________________
```

### Q4: In what way is building an Agent harder than a Workflow?
```
Answer: _______________________________________________
Example: _______________________________________________
```

### Q5: What would happen if an agent's goal is impossible?
```
Answer: _______________________________________________
How could we improve this? _______________________________________________
```

---

## Answer Key

### Exercise 1 Answers:
**1.1** Agent (needs autonomous decision-making about availability)
**1.2** LLM (simple text generation)
**1.3** Agent (learning and iteration required)
**1.4** Workflow (repetitive, same path daily)
**1.5** Agent (iteration to pass tests required)

### Exercise 2:
Should have 5 main steps:
1. Fetch trending topics
2. Get articles for each topic
3. Generate tweet ideas
4. Schedule tweets
5. Trigger daily at 8 AM

### Exercise 3:
ReAct breakdown for paper research would include:
- Tools: Research API, Academic Database, Summarization model
- Actions: Search, filter, rank, summarize
- Observations: Check year, quality, coverage
- Iterations: If insufficient papers, expand search

---

## Challenge Problems

### Challenge 1: Design an AI Agent for Content Moderation
```
Goal: Moderate user-generated social media content

Your task:
1. Define what the agent should reason about
2. List tools it would need
3. Explain how it would iterate

Reasoning: _______________________________________________
Tools: _______________________________________________
Iteration: _______________________________________________
```

### Challenge 2: Compare Three Eras of Building Apps
```
Era 1 (2020): Pure LLM chatbots
→ What could they do? _______________________________________________

Era 2 (2022): LLM + Fixed Workflows
→ What new capability? _______________________________________________

Era 3 (2024): AI Agents
→ What new capability? _______________________________________________

What will Era 4 (2026) bring?
→ Your prediction: _______________________________________________
```

### Challenge 3: The Impossible Task
```
An agent is given: "Create a viral TikTok video that's guaranteed to get 1M views"

Why is this impossible for an agent (or anything)?
_______________________________________________

How could the goal be reframed to be achievable?
_______________________________________________
```

