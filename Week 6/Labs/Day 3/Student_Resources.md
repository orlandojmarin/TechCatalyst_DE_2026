# Week 6 · Day 3 - Student Resources: LLM APIs, Function Calling, Agents, and MCP

> **AI coding tools note:** AI assistants are allowed from Week 5 onward, and you review everything they write. Today has one exception worth taking seriously: write the tool schemas, the agent loops, and the ReAct parser by hand. Understanding that machinery is the whole point of the day, and Friday is dedicated to using assistants well.

---

## Core Documentation

| Resource | Why It Helps |
| :--- | :--- |
| [OpenAI text generation guide](https://platform.openai.com/docs/guides/text) | The `messages` list, roles, and streaming. The reference for everything in Activity 1 |
| [OpenAI function calling guide](https://platform.openai.com/docs/guides/function-calling) | Tool schema format, `tool_calls`, and how to return results. Read alongside Activity 4 |
| [Gemini OpenAI compatibility](https://ai.google.dev/gemini-api/docs/openai) | The exact `base_url` that lets the `openai` client talk to Gemini, plus what is and is not supported |
| [tiktoken](https://github.com/openai/tiktoken) | OpenAI's BPE tokenizer. Count tokens locally, before you spend anything, used in Activity 2 |
| [OpenAI embeddings guide](https://platform.openai.com/docs/guides/embeddings) | What an embedding is, the current models, and their dimensions |
| [Ollama](https://ollama.com/) | Installing and running open models locally, with an OpenAI-compatible endpoint on port 11434 |
| [Transformers pipelines](https://huggingface.co/docs/transformers/main/en/pipeline_tutorial) | The shortest path from a model name to running inference, used in Activity 3 |
| [Model Context Protocol](https://modelcontextprotocol.io/) | What MCP is, why it exists, and the concepts behind servers, clients, and tools |
| [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | The `mcp` package used in Activity 6, including server and client examples |
| [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629) | The original paper behind the Thought, Action, Observation loop you build in Activity 5 |

---

## One client, three backends

The only things that change between providers are `api_key` and `base_url`.

```python
from openai import OpenAI

# OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Gemini, through the same client
gemini_client = OpenAI(
    api_key=os.environ["GOOGLE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# A model running on your own machine
ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```

Every one of them then uses the identical call:

```python
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a claims operations assistant."},
        {"role": "user", "content": "Summarize this claim note in one sentence."},
    ],
)
print(completion.choices[0].message.content)
```

---

## Tokens

Text is chopped into tokens before a model sees it. Count them locally, for free, before sending anything.

```python
import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o-mini")
ids = encoder.encode("The insured filed a claim.")

print(len(ids))                                  # how many tokens
print([encoder.decode([i]) for i in ids])        # where the cuts landed
```

Rough rule: one token is about three quarters of an English word. But not all text costs the same.

| Text | Tokens | Why |
| :--- | :--- | :--- |
| `cat` | 1 | Common enough to earn its own token |
| `deductible` | 3 | `ded` + `uct` + `ible` |
| `CLM_101` | 4 | Not a word at all |
| Spanish vs the same English sentence | roughly 2x | The vocabulary was built mostly from English |

This is also why models miscount letters. `strawberry` arrives as `['st', 'raw', 'berry']`, so the letters were never visible.

---

## Embeddings

An embedding turns text into a list of numbers positioned so that similar meanings land near each other. Compare them with cosine similarity, which runs from 1.0 (same direction) to 0.0 (unrelated).

```python
response = client.embeddings.create(model="text-embedding-3-small", input=SENTENCES)
vectors = [item.embedding for item in response.data]

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
```

A local model needs no API and no GPU:

```python
from model2vec import StaticModel

embedder = StaticModel.from_pretrained("minishlab/potion-base-8M")
vectors = embedder.encode(SENTENCES)
```

Cosine scores are **not** comparable across models. Only the ranking transfers, and ranking is usually all you need.

| Embeddings are right for | Embeddings are wrong for |
| :--- | :--- |
| Semantic search, RAG | Exact lookups (`WHERE claim_id = 'CLM_101'`) |
| Deduplication, clustering | Structured filters (amount, state, date) |
| Classification against examples | Generating any text at all |
| Recommendation | Explaining a decision to a human |

---

## Reading the whole response

The text is one field on a larger object. `finish_reason` is the one to watch.

```python
print(completion.model)                          # which model actually answered
print(completion.usage.prompt_tokens)            # what you paid to send
print(completion.usage.completion_tokens)        # what you paid to receive
print(completion.choices[0].finish_reason)       # why it stopped
```

| `finish_reason` | Meaning |
| :--- | :--- |
| `stop` | The model finished its answer on its own |
| `length` | It hit `max_tokens` mid-thought, the answer is cut off |
| `tool_calls` | It stopped on purpose, it wants a function run before it continues |

---

## The function calling cycle

```
1. You send      question + tool descriptions
2. Model replies "run get_claim_status(claim_id='CLM_101')"   <- stops here
3. You run       the actual Python function
4. You send      the whole conversation + the result
5. Model replies the final answer in plain language
```

A tool description is what the model reads. It never sees your code.

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_claim_status",
        "description": "Look up an insurance claim's status, amount, and type by claim ID.",
        "parameters": {
            "type": "object",
            "properties": {"claim_id": {"type": "string", "description": "e.g. CLM_101"}},
            "required": ["claim_id"],
        },
    },
}]
```

Returning a result needs both the assistant's original request and a `tool` message tagged with the matching `tool_call_id`:

```python
messages.append(reply)                       # the assistant's tool-call request, unchanged
messages.append({
    "role": "tool",
    "tool_call_id": call.id,
    "content": json.dumps(result),
})
```

---

## Prompting levers

| Lever | Fixes | Cost |
| :--- | :--- | :--- |
| System prompt | Output format, tone, role | One line, essentially free |
| Few-shot examples | Patterns easier to show than to describe | A few extra messages per call |
| Chain of thought | Multi-step reasoning and arithmetic errors | More output tokens, slower |

The highest-leverage move is telling the model exactly what shape the answer must be in:

```python
{"role": "system", "content": "Respond with exactly one word: LOW, MEDIUM, or HIGH. No explanation."}
```

---

## The ReAct loop

```
Question: Claim CLM_101 is on policy POL_991. What is the net payout?
  Thought:     I need the claim amount first.
  Action:      get_claim_status: CLM_101
  PAUSE
  Observation: CLM_101: status=Approved, amount=3400.0
  Thought:     Now I need the deductible.
  Action:      get_policy_deductible: POL_991
  PAUSE
  Observation: POL_991: deductible=500.0
  Thought:     I can calculate the payout.
  Action:      calculate_net_payout: 3400 - 500
  PAUSE
  Observation: 2900.0
  Answer:      The net payout on claim CLM_101 is $2,900.00.
```

| | Native function calling | ReAct |
| :--- | :--- | :--- |
| Model signals a tool need by | `finish_reason == "tool_calls"`, structured JSON | A text line, `Action: name: input` |
| You detect it by | Checking a field | A regular expression |
| Reasoning visible? | No | Yes, the `Thought` lines |
| Breaks if the model reformats? | No, the API enforces it | Yes |
| Works on any chat model? | Only ones with a tool API | Yes |

---

## MCP in three pieces

**A server** is a normal Python program. No hand-written schemas, the decorator reads your type hints and docstring.

```python
from mcp.server import MCPServer

mcp = MCPServer("claims-tools")

@mcp.tool()
def get_claim_status(claim_id: str) -> dict:
    """Look up an insurance claim's status, amount, and type by claim ID."""
    return CLAIMS_DB.get(claim_id, {"error": f"{claim_id} not found"})

if __name__ == "__main__":
    mcp.run()
```

**A client** launches it and asks what it can do. Note that each connection is opened and closed inside a single `async with` block.

```python
from mcp import Client, StdioServerParameters, stdio_client

server_params = StdioServerParameters(command=sys.executable, args=["claims_mcp_server.py"])

async with Client(stdio_client(server_params)) as session:
    listed = await session.list_tools()
    result = await session.call_tool("get_claim_status", {"claim_id": "CLM_101"})

print(result.content[0].text)
```

**The bridge** into a function-calling loop is three keys moved to three other keys:

```python
def mcp_to_openai(tool):
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.input_schema,
        },
    }
```

MCP standardizes discovery and transport. The loop underneath is unchanged.

---

## Lab Deliverable Checklist

| Requirement | Description | Status |
| :--- | :--- | :--- |
| **Environment** | `openai`, `python-dotenv`, and `mcp` installed from the repo root; keys in `.env`; starters copied to `student-work/week6/day3/` | ☐ |
| **Multi-backend calls** | `compare_providers` runs the same prompt against at least two backends | ☐ |
| **Token counting** | `count_tokens` written, and you can explain why one of your examples had an unusually high token-to-word ratio | ☐ |
| **Embeddings** | Extended the sentence set and printed all pairwise similarities, from both the API and the local model | ☐ |
| **Local model** | Ran the sentiment classifier and a local chat model in Colab, and compared quality against the API | ☐ |
| **Function calling by hand** | Completed one full round trip manually before using the loop | ☐ |
| **Tool loop** | `run_conversation` answers a question needing multiple dependent tool calls | ☐ |
| **Added tool** | Added `list_denied_claims` to the schema list and the function dictionary, and used it | ☐ |
| **Prompting levers** | Demonstrated a system prompt, few-shot examples, and chain of thought | ☐ |
| **ReAct agent** | Built the Thought, Action, Observation loop and added one action of your own | ☐ |
| **MCP server** | Server exposes four tools, discovered at runtime by the client | ☐ |
| **MCP loop** | `run_mcp_conversation` answers the multi-step question using MCP-backed tools | ☐ |
| **Decision worksheet** | Team worksheet completed and defended in the 3-minute readout | ☐ |
| **Exit ticket** | Completed `quiz/Day3_Quiz.md` | ☐ |
