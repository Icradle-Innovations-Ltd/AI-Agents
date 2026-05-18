# AI Concepts: Quick Reference & Glossary

## Quick Reference Cards

### Card 1: What is an LLM?

**In One Sentence:**
Large Language Models are AI systems trained on vast amounts of text data to generate and edit text.

**Key Facts:**
- Name: ChatGPT, Claude, Llama, PaLM
- Strength: Generating, editing, explaining text
- Weakness: No real-time data, no calendar access, not autonomous
- Behavior: Passive (waits for prompts)

**When to Use:**
- Writing emails
- Brainstorming ideas
- Generating code
- Answering questions

**When NOT to Use:**
- Need to access personal data
- Require decision-making without human guidance
- Need to call external APIs autonomously


### Card 2: What is an AI Workflow?

**In One Sentence:**
A workflow is a human-defined sequence of steps that connects an LLM with external tools and data sources.

**Key Facts:**
- Human decides: What steps, what tools, what order
- LLM role: Execute the steps as programmed
- Control logic: The path is predetermined
- Flexibility: Low (can't adapt to unexpected requests)

**When to Use:**
- Daily tasks with the same steps (e.g., daily news digest)
- Clear, predetermined processes
- Repetitive automation
- You know all the steps needed

**When NOT to Use:**
- Unexpected tasks appear
- Need flexible decision-making
- Must adapt to new requirements
- Require autonomous improvement

**Examples:**
- Make.com automation
- Zapier workflows
- IFTTT applets


### Card 3: What is an AI Agent?

**In One Sentence:**
An AI Agent is an autonomous system where the LLM makes decisions about reasoning, acting, and iterating to achieve a goal.

**Key Facts:**
- LLM is the decision-maker (not the human)
- Can choose which tools to use
- Can adapt to unexpected situations
- Can iterate and improve autonomously
- Uses ReAct framework (Reason + Act)

**When to Use:**
- Complex goals without predetermined paths
- Need autonomous decision-making
- System must adapt to new situations
- Quality improvement through iteration needed

**When NOT to Use:**
- Simple, repetitive task
- Predefined workflow exists
- No need for autonomy
- Resource constraints (agents are expensive)

**Examples:**
- Customer support agents
- Research assistants
- Code generation + debugging
- Content creation + evaluation


---

## Side-by-Side Comparison

### Scenario: "Get my calendar event and tell me the weather that day"

```
LLM Approach:
─────────────
User: "When is my coffee meeting tomorrow and what's the weather?"
LLM: "I don't have access to your calendar or real-time weather data."
Result: ✗ FAIL


WORKFLOW Approach:
──────────────────
Step 1: Always check Google Calendar
        └─ Gets: Coffee meeting at 2 PM ✓
Step 2: Always check weather API
        └─ Gets: Sunny, 72°F ✓
Result: "Your coffee meeting is at 2 PM. Weather: Sunny, 72°F"
Result: ✓ SUCCESS

What if user asks: "Should I bring an umbrella?"
Result: ✗ FAIL (not in predefined workflow logic)


AGENT Approach:
───────────────
Goal: "Tell me about my coffee meeting tomorrow including weather advice"

Agent Reasons:
├─ "I need to check calendar → Google Calendar API"
├─ "I need weather → OpenWeather API"
├─ "I need to provide advice → My reasoning"
└─ "Are my results good? → Verify against criteria"

Agent Acts:
├─ Retrieves: Meeting at 2 PM ✓
├─ Retrieves: Sunny, 72°F ✓
├─ Generates: "Nice weather, no umbrella needed"

Agent Evaluates:
├─ "Is this helpful?"
├─ "Is temperature accurate?"
└─ "Decision: Good quality"

Result: "Your coffee is at 2 PM. Weather is sunny (72°F). 
         No umbrella needed. Great day for outdoor coffee!"
Result: ✓ SUCCESS

What if user asks: "Should I bring a jacket?"
Agent thinks: "Temperature is 72°F, perfect. I'll recommend no jacket.
              But let me check if wind makes it feel cooler..."
Result: ✓ SUCCESS (agent adapts)
```

---

## Common Misconceptions

### ❌ Misconception 1: "RAG is different from workflows"
**Reality**: RAG (Retrieval Augmented Generation) is just a type of workflow. It's the process of retrieving external data before generating a response.

---

### ❌ Misconception 2: "More steps = more complex tool"
**Reality**: 
- 10-step workflow = still a workflow
- 1000-step workflow = still a workflow
- It only becomes an agent when LLM makes the decisions, not the number of steps

---

### ❌ Misconception 3: "Agents are always better than workflows"
**Reality**:
- For simple, repetitive tasks → Workflows are better (simpler, cheaper)
- For complex, adaptive tasks → Agents are better
- Choose the right tool for the job

---

### ❌ Misconception 4: "LLMs understand the world"
**Reality**:
- LLMs are trained on text data
- They have knowledge cutoff dates
- They can't access real-time information
- They can't learn from conversations
- They make plausible-sounding but false statements sometimes

---

### ❌ Misconception 5: "An AI Agent can do anything"
**Reality**:
- Agents are limited to their available tools
- They can't do things outside their tool ecosystem
- They can fail if given impossible goals
- They still make mistakes and need oversight

---

## The Big Ideas to Remember

### Idea #1: It's All About Decision-Making
```
LLM:      Human decides → LLM executes
Workflow: Human decides → LLM executes (with tools)
Agent:    LLM decides   → LLM executes (with tools)
```

### Idea #2: LLMs Need Help to Be Useful
```
Raw LLM: Can only generate text from memory
LLM + Tools: Can access real data but needs human guidance (Workflow)
LLM + Tools + Autonomy: Can independently solve complex problems (Agent)
```

### Idea #3: Complexity Progression
```
Simple                          Complex
├─ LLM (Text only)
├─ Workflow (Guided with tools)
└─ Agent (Autonomous with tools)
```

### Idea #4: The Critical Change
```
Workflow → Agent happens when:

BEFORE: "You must follow this path: Step 1 → Step 2 → Step 3"
AFTER:  "Here's a goal. You decide the best path."

It's about AUTONOMY in DECISION-MAKING.
```

---

## Glossary: Essential Terms

| Term | Definition | Example |
|------|-----------|---------|
| **Autonomous** | Able to make decisions and act without human instruction | Agent decides which tool to use |
| **Control Logic** | The predetermined sequence of steps in a workflow | Step 1: Get data, Step 2: Process, Step 3: Send |
| **Decision-Maker** | The entity that chooses how to proceed | In workflows: human; In agents: LLM |
| **Iteration** | Repeating a process to improve results | Agent regenerates post, evaluates, regenerates again |
| **LLM** | Large Language Model; AI trained on text to generate text | ChatGPT, Claude, Llama |
| **Prompt** | Input instruction given to an LLM | "Write a formal email requesting a meeting" |
| **RAG** | Retrieval Augmented Generation; retrieving data before generating | Checking calendar before answering "When's my meeting?" |
| **ReAct** | Reasoning + Acting; the agent framework | Agent reasons about approach, then acts with tools |
| **Tool** | External system an LLM can access | Google Calendar, Weather API, Database |
| **Workflow** | Predefined sequence of steps + tools + LLM execution | Make.com automation with 5 steps |
| **Reasoning** | Process of analyzing a goal and deciding the best approach | Agent thinks: "I need to search news first, then analyze" |
| **Acting** | Process of using tools to execute decisions | Agent calls NewsAPI, analyzes results |

---

## Learning Path Timeline

### Week 1: Foundations (3-4 hours)
- [ ] Understand what LLMs are and their limitations
- [ ] Learn how LLMs work at a high level
- [ ] Complete "What is RAG?" section
- [ ] Answer Levels 1 Study Questions (1-9)

### Week 2: Workflows (3-4 hours)
- [ ] Deep dive into workflow structure
- [ ] Study RAG as a type of workflow
- [ ] Learn about workflow limitations
- [ ] Answer Level 2 Study Questions (10-22)
- [ ] Create a simple workflow diagram for a task you do

### Week 3: Agents (4-5 hours)
- [ ] Understand the critical shift from workflow to agent
- [ ] Study ReAct framework in detail
- [ ] Learn about reasoning, acting, and iteration
- [ ] Answer Level 3 Study Questions (23-35)
- [ ] Watch Andrew Ng's AI Agents demo (linked in transcript)

### Week 4: Integration (3-4 hours)
- [ ] Complete all study questions
- [ ] Answer all discussion questions
- [ ] Design your own example: LLM vs Workflow vs Agent
- [ ] Create a visual diagram for your example

---

## Testing Your Understanding

### The "Explain to a Friend" Test
Can you explain to someone who's never heard of these concepts:
1. What's the difference between LLM and Workflow?
2. What's the difference between Workflow and Agent?
3. Why would someone use a Workflow instead of an Agent?

If you can answer all three in 1-2 sentences each, you understand it!

---

### The "Choose the Right Tool" Test

For each scenario, identify LLM / Workflow / Agent:

1. Auto-generate captions for Instagram posts
   Answer: ___________

2. Check stock price and send daily summary email
   Answer: ___________

3. Research a question, gather sources, synthesize answer, evaluate quality
   Answer: ___________

4. Translate email from English to Spanish
   Answer: ___________

5. Analyze customer support tickets, draft responses, route to right department
   Answer: ___________

**Answers**: 1-LLM, 2-Workflow, 3-Agent, 4-LLM, 5-Agent

---

## Resources for Deeper Learning

### Official Sources
- OpenAI ChatGPT Documentation
- Anthropic Claude Documentation
- Andrew Ng's AI Agents Demo (mentioned in transcript)

### Framework References
- Make.com - Visual workflow builder
- n8n - Workflow automation (open source)
- Zapier - Workflow automation (no-code)
- LangChain - LLM application framework
- AutoGPT - Simple agent framework

### Key Concepts to Explore
- Prompt Engineering
- Few-shot Learning
- Chain of Thought Prompting
- ReAct Framework in detail
- Token Limits and Context Windows

---

## One-Page Summary

### Three Levels of AI

**Level 1: LLMs**
- What: Text generation AI
- How: Input → Output based on training data
- Limit: No external data, not autonomous
- Use when: Just need text generation

**Level 2: Workflows**
- What: LLM + Tools + Predefined path
- How: Human programs steps → LLM executes → Output
- Limit: Can't adapt, no autonomous improvement
- Use when: Repetitive task with known steps

**Level 3: Agents**
- What: LLM makes decisions + Uses tools + Iterates
- How: Goal → LLM reasons/acts/observes/iterates → Output
- Strength: Adaptive, autonomous, improves itself
- Use when: Complex goals, unknown path, need flexibility

### The Critical Insight
**Workflow → Agent happens when the human decision-maker is replaced by an LLM.**

It's not about the number of steps or tools.
It's about **who decides**: Human or AI?

---

## Next Steps

1. **Review** the summary documents
2. **Study** the visual diagrams
3. **Answer** all study guide questions
4. **Create** your own examples
5. **Explore** building a real workflow or agent
6. **Share** your learning with others
