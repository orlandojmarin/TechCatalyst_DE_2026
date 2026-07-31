# Week 6 · Day 3 - Lab: LLM APIs, Function Calling, Agents, and MCP

Yesterday you built classical ML models on tabular data. Today you move into generative AI, and you do it from the inside out.

Most people meet this technology through a chat window and conclude that "AI" means typing into a text box. Today takes that apart. You will call models through their APIs instead of chatting with them, run one on hardware you control, watch a model stop mid-answer to request a function, write the loop that makes it an agent, and finish by exposing your own tools over the same protocol your AI coding assistant uses.

By the end you will have built, by hand, a small version of the product you thought you were using.

---

## Daily Sequence Arc

| Arc Block | Topic | Focus |
| :--- | :--- | :--- |
| Block 1 | One client, many models | Chat completions, streaming, and swapping backends by changing `base_url` |
| Block 2 | Tokens and embeddings | How text becomes numbers, what you actually pay for, and why two sentences with no shared words can match |
| Block 3 | Where models run | Loading open model weights yourself, and the cost, privacy, and quality trade-off |
| Block 4 | Function calling | Why a model stops mid-task, and the ask, run, hand back cycle |
| Block 5 | Prompting and agents | System prompts, few-shot, chain of thought, then a ReAct loop built from scratch |
| Block 6 | MCP | Exposing tools as a server any client can discover, and what Claude Code is really doing |
| Block 7 | Judgment | Deciding whether a problem needs AI at all, and which kind if it does |

---

## Core Learning Objectives

1. **Call models programmatically.** Send chat completion requests, stream responses, read the full response object, and point the same client at OpenAI, Gemini, or a local server.
2. **Explain how text becomes numbers.** Run BPE tokenization locally to count tokens and predict cost, then generate embeddings with both an API and a local model and explain what each representation is for.
3. **Reason about where a model runs.** Load open weights directly and defend the choice between a hosted API and local inference on cost, privacy, latency, and quality.
4. **Implement function calling from first principles.** Describe a function as a schema, detect `finish_reason == "tool_calls"`, execute the request yourself, and return the result correctly.
5. **Build an agent.** Generalize the by-hand tool cycle into a loop, then build the same behavior a second way with a from-scratch ReAct agent, and define "agentic" from the code rather than from marketing.
6. **Apply prompting deliberately.** Use system prompts, few-shot examples, and chain of thought as distinct tools with distinct costs.
7. **Standardize tools with MCP.** Expose Python functions as an MCP server, discover them from a client at runtime, and bridge them into a function-calling loop.
8. **Decide whether to use AI at all.** Run a real initiative through a five-gate decision framework and defend the outcome.

---

## Setup Instructions

Complete `Activity_0_Environment_and_API_Setup.md` first. In short, from the repository root:

```bash
uv sync
uv add openai python-dotenv tiktoken model2vec mcp
```

Then put `OPENAI_API_KEY` and `GOOGLE_API_KEY` in a `.env` file at the repository root, and copy today's notebooks into `student-work/week6/day3/` before opening anything.

---

## Lab Index

### Provided Files

| File | Purpose |
| :--- | :--- |
| `Reading_From_Chatbot_to_System.md` | Student reading: what a model actually is, and how the day's pieces fit together |
| `Student_Resources.md` | Documentation links, code patterns, and the deliverable checklist |
| `Activity_0_Environment_and_API_Setup.md` | Dependencies, API keys, and copying starters into `student-work/` |
| `Activity_1_OpenAI_Compatible_APIs.ipynb` | Chat completions, streaming, and one client pointed at OpenAI, Gemini, and Ollama |
| `Activity_2_Tokens_and_Embeddings.ipynb` | BPE tokenization with `tiktoken`, then embeddings from an API and from a local model |
| `Activity_3_Local_Models_with_HuggingFace.ipynb` | Runs in Colab. Loading open model weights directly, with no API or server |
| `Activity_4_Function_Calling_Internals.ipynb` | One tool-calling round trip by hand, then generalized into a loop |
| `Activity_5_Prompt_Engineering_and_ReAct.ipynb` | System prompts, few-shot, chain of thought, then a ReAct agent from scratch |
| `Activity_6_MCP_Standardizing_Tools.ipynb` | Building an MCP server, discovering tools at runtime, bridging them into the loop |
| `Group_Activity_AI_Decision_Hierarchy.md` | Five-gate decision framework applied to five proposed AI initiatives |
| `quiz/Day3_Quiz.md` | Knowledge check and exit ticket |

Activity 3 runs in Google Colab because it downloads real model weights and wants a GPU. Everything else runs locally against the repository-root `.venv`.

### Student Deliverables (Submit via PR)

| Deliverable File | Target Location | Purpose |
| :--- | :--- | :--- |
| Multi-backend comparison | `student-work/week6/day3/Activity_1_OpenAI_Compatible_APIs.ipynb` | `compare_providers` running against at least two backends |
| Tokens and embeddings | `student-work/week6/day3/Activity_2_Tokens_and_Embeddings.ipynb` | `count_tokens` plus your extended sentence set and its pairwise similarities |
| Local model notebook | `student-work/week6/day3/Activity_3_Local_Models_with_HuggingFace.ipynb` | Colab copy with your own test messages and the constrained-prompt comparison |
| Function calling loop | `student-work/week6/day3/Activity_4_Function_Calling_Internals.ipynb` | Working loop plus your added `list_denied_claims` tool |
| Prompting and ReAct | `student-work/week6/day3/Activity_5_Prompt_Engineering_and_ReAct.ipynb` | ReAct agent with your added action, plus the JSON output experiment |
| MCP server and client | `student-work/week6/day3/Activity_6_MCP_Standardizing_Tools.ipynb` and `claims_mcp_server.py` | Server with your fourth tool, discovered and called from the notebook |
| Decision worksheet | `student-work/week6/day3/AI_Decision_Hierarchy_<team>.md` | Your team's completed five-gate worksheet |
| PR Description | GitHub Pull Request | One paragraph: where your assigned initiative stopped, and why |

---

## A note on AI assistants

Weeks 1 through 4 were an AI-free zone. From Week 5 onward, AI coding assistants are allowed, with the standing rule that you review everything they produce.

Today has one specific exception worth stating: **write the tool schemas, the loops, and the ReAct parser yourself.** The entire point of the day is understanding the machinery, and letting an assistant generate the loop skips the only part that matters. Friday is dedicated to using those assistants well.
