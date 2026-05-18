# AI Concepts Study Guide: Learning Path & Key Questions

## Learning Path Structure

### Level 1: LLMs (Foundation)
**Duration**: 30 minutes
**Goal**: Understand what LLMs are and their limitations

### Level 2: Workflows (Integration)
**Duration**: 1-2 hours
**Goal**: Learn how to connect LLMs with external tools and data

### Level 3: Agents (Autonomy)
**Duration**: 2-3 hours
**Goal**: Understand autonomous AI decision-making

---

## Study Questions by Level

### LEVEL 1: Large Language Models

#### Basic Understanding
1. What is an LLM?
2. Name 2 popular LLMs mentioned in the transcript.
3. What are LLMs trained on?
4. What 2 tasks are LLMs fantastic at?

#### Limitations
5. Why can't ChatGPT tell you when your coffee chat is scheduled?
6. What are 2 key traits of LLMs?
7. Are LLMs active or passive? Explain.

#### Application
8. Give an example of a task LLMs can do well.
9. Give an example of a task LLMs cannot do alone.

---

### LEVEL 2: AI Workflows

#### Core Concepts
10. What is an AI workflow?
11. How do workflows extend LLM capabilities?
12. Who decides the workflow path? (Human or LLM?)
13. What is "control logic"?

#### RAG Concept
14. What does RAG stand for?
15. Explain RAG in simple terms.
16. Is RAG a type of workflow or a type of agent?

#### Limitations & Design
17. What happens in a workflow if you ask a question outside the predefined path?
18. Can a workflow with 1,000 steps be considered an agent? Why or why not?
19. How many steps did the Make.com workflow have? List them.

#### Real-World Application
20. In the Make.com example, which tools were used?
21. What was the human's role in the Make.com workflow?
22. What happened when the human wanted the LinkedIn post to be funnier?

---

### LEVEL 3: AI Agents

#### The Critical Shift
23. **This is the most important concept**: What ONE change transforms a workflow into an agent?
24. What does it mean for an LLM to be a "decision-maker"?

#### Core Agent Capabilities
25. What does "reasoning" mean for an AI agent?
26. What does "acting" mean for an AI agent?
27. What does "iterating" mean for an AI agent?
28. Why is iteration important? Give an example.

#### ReAct Framework
29. What does ReAct stand for?
30. Why is ReAct the most common configuration for AI agents?

#### Agent Behavior
31. In the video search agent example, what did the agent reason about?
32. What tools/actions did the agent take?
33. How did the agent handle quality control without human intervention?

#### Autonomy
34. If a human programs a 1,000-step workflow, is it an agent? Why or why not?
35. Can an AI agent decide which tools to use, or must it follow a predefined tool sequence?

---

## Comparison Tables for Study

### Fill in the Blanks

#### Table 1: LLM vs Workflow vs Agent

| Question | LLM | Workflow | Agent |
|----------|-----|----------|-------|
| Who decides the path? | | | |
| Can access external data? | | | |
| Can iterate autonomously? | | | |
| Makes its own tool choices? | | | |
| Requires human decision-maker? | | | |

**Answer Key**:
| Question | LLM | Workflow | Agent |
|----------|-----|----------|-------|
| Who decides the path? | No path | Human | LLM |
| Can access external data? | No | Yes (predefined) | Yes (autonomous) |
| Can iterate autonomously? | No | No | Yes |
| Makes its own tool choices? | N/A | No | Yes |
| Requires human decision-maker? | N/A | Yes | No |

---

## Deep Dive Questions

### Conceptual Understanding

**Q1: The Coffee Chat Problem**
You ask ChatGPT: "When is my coffee chat with Elon Musk tomorrow?"

a) Why does it fail?
b) How would a workflow solve this?
c) How would an agent approach this differently?

**Answer Guide**:
- a) ChatGPT has no access to your calendar data
- b) A workflow would have a predefined step: "Always check user's Google Calendar"
- c) An agent would reason: "The user is asking about a scheduled event → I need calendar access → Let me search for calendar tools → Fetch and return the data" (autonomously choosing the approach)

---

**Q2: The Flexibility Test**

You're using a workflow for social media posting that has these steps:
1. Search news
2. Summarize news
3. Draft Instagram posts

Then you ask it to also create TikTok videos. What happens?

a) What does the workflow do?
b) What does an agent do?

**Answer Guide**:
- a) The workflow fails because TikTok video creation wasn't in the predefined path. A human must manually add this step.
- b) The agent reasons: "User wants TikTok videos → That requires video generation tools → Let me identify and use appropriate video tools → Create content in TikTok format." Agent adapts without human reprogramming.

---

**Q3: The Iteration Problem**

You use an AI workflow to generate LinkedIn posts. The output isn't funny enough, so you:
- Manually rewrite the prompt to Claude
- Regenerate the output
- Check if it's better
- Repeat 3 times until satisfied

a) Why is this the human's job in a workflow?
b) How would an agent handle this differently?

**Answer Guide**:
- a) In a workflow, the human is the decision-maker. The workflow can't autonomously judge whether the post is "funny enough" because that judgment requires reasoning about what "funny" means and how to improve it.
- b) An agent would have built-in evaluation: "I've drafted V1 → Let me evaluate it against 'LinkedIn best practices & humor standards' → It needs more jokes → I'll adjust tone and regenerate → Evaluate again → Repeat until criteria met → Return final version"

---

## Vocabulary Builder

| Term | Definition | Example |
|------|-----------|---------|
| **LLM** | Large Language Model; AI trained on vast text data to generate text | ChatGPT, Claude |
| **Prompt** | Input instruction given to an LLM | "Draft a polite email" |
| **Workflow** | Predefined sequence of steps combining LLM with external tools | Make.com automation |
| **Control Logic** | The predetermined path a workflow follows | Step 1 → Step 2 → Step 3 |
| **RAG** | Retrieval Augmented Generation; accessing external data before responding | Checking calendar before answering "When's my meeting?" |
| **AI Agent** | Autonomous system where LLM makes decisions and takes actions | Video search agent that tags clips |
| **Reasoning** | Agent's process of deciding the best approach | "I'll use tool X before tool Y" |
| **Acting** | Agent's process of using tools to execute decisions | Calling APIs, accessing databases |
| **Iterating** | Agent's process of evaluating results and improving | Regenerating post until quality met |
| **ReAct** | Framework combining Reasoning + Acting in AI agents | Most common agent architecture |
| **Tool Integration** | Connecting LLM to external systems/APIs | Linking Claude to Google Sheets |

---

## Practice Scenarios

### Scenario 1: Email Drafting Assistant
**Setup**: You ask ChatGPT to draft an email AND include your recent meeting notes.

**Questions**:
- As LLM: Can it do this? Why?
- As Workflow: How would you set it up?
- As Agent: How would it approach this?

---

### Scenario 2: Customer Support Bot
**Setup**: You want a system that answers customer questions by:
1. Searching your product documentation
2. Checking customer's purchase history
3. Drafting a personalized response

**Questions**:
- Could an LLM alone handle this?
- Would a workflow work well?
- What advantages would an agent have?

---

### Scenario 3: Research Paper Compiler
**Setup**: You want a system that:
1. Finds papers on a topic
2. Summarizes them
3. Identifies conflicting findings
4. Decides which summaries are most relevant
5. Compiles a research report

**Questions**:
- Is this better as a workflow or agent?
- What decisions need to be made?
- Where would human vs. AI decision-making be?

---

## Self-Assessment Checklist

After studying all three levels, check if you can:

### Level 1 - LLMs
- [ ] Explain what an LLM is in simple terms
- [ ] Give 2 examples of LLM limitations
- [ ] Describe why LLMs are passive
- [ ] Name a task LLMs do well and one they can't do

### Level 2 - Workflows
- [ ] Explain how a workflow gives LLMs access to external data
- [ ] Draw or describe the flow of a 3-step workflow
- [ ] Define RAG and explain it's just a type of workflow
- [ ] Describe what happens when a workflow faces an unexpected question
- [ ] Explain why humans make all decisions in workflows

### Level 3 - Agents
- [ ] State THE critical change that makes an agent different from a workflow
- [ ] Explain reasoning, acting, and iterating with examples
- [ ] Describe the ReAct framework
- [ ] Explain how an agent handles tasks it wasn't explicitly programmed for
- [ ] Compare agent autonomy vs. workflow rigidity

---

## Discussion Questions

1. Is a chatbot that can search the internet an agent or a workflow? Explain.
2. Could an agent help you with a task that doesn't exist yet?
3. What would be harder to build: a workflow or an agent? Why?
4. In your daily life, what tasks would benefit from AI agents vs. workflows?
5. What are the risks of autonomous AI agents compared to workflows?

