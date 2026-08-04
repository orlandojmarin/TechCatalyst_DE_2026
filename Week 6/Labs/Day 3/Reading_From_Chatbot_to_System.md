# Reading: From Chatbot to System

**TechCatalyst Data Engineering 2026 · Week 6 Day 3**

Read this before class, or during the first break. It is the map for the day. The activities build each piece; this explains why the pieces exist.

---

## 1. The thing you have been using is not the thing you are learning

Almost everyone arrives at this topic having used ChatGPT or Claude, and reasonably concludes that "AI" means a text box you type into. That mental model is not wrong, it is just very small, and it hides everything a data engineer actually needs.

Here is the more useful version.

**ChatGPT is an application.** The model is one component inside it. Around that model sits a pile of engineering: a web interface, conversation storage, a search tool, a code interpreter, file upload handling, safety filters, and a loop that coordinates all of it. When you ask ChatGPT to look something up and it does, the model did not look anything up. The application ran a search tool on the model's behalf and pasted the results back into the conversation.

**The model itself is much simpler and much dumber than the product makes it look.** It takes text in and produces text out. It has no memory, no internet access, no file system, no ability to run anything. It cannot check the time.

Today you work with the model directly, through its API, and then build back up. By the end of the day you will have written the loop, the tool calls, and the coordination yourself, which is to say you will have built a small version of the thing you thought you were using all along.

That is the goal. Not "learn to use AI." Learn what is inside it, so you can decide what to build with it.

---

## 2. What the model actually does

A large language model predicts the next token, over and over. A token is a chunk of text, roughly three quarters of a word. Given everything so far, it produces a probability distribution over what comes next, picks one, appends it, and repeats until it produces a stop token.

That single mechanism, scaled up enormously, is responsible for everything you have seen a model do. Summarizing, translating, writing code, and answering questions are all the same operation with different text in front of it.

Three consequences matter to you:

**It is stateless.** The model does not remember your last message. Every API call sends the entire conversation again. When you see `messages=[...]` in the activities, that list *is* the memory, and you own it. A chat app feels like it remembers you because the application is storing and resending the history, not because the model retained anything.

**It generates plausible text, not verified text.** Nothing in the mechanism checks facts. A model asked for a claim status will happily invent one, because inventing a plausible-looking claim status is exactly what "predict the next token" produces when it has no claim data. This is the root of every hallucination story, and it is why tools exist.

**It costs money per token, in both directions.** You pay for what you send and what you get back. Sending an entire conversation history on every turn is why long chats get expensive, and why `usage.prompt_tokens` is worth watching.

There is also a hard limit called the **context window**, the maximum number of tokens the model can consider at once. Everything, system prompt, conversation history, retrieved documents, tool results, competes for that budget. Managing it is a real engineering constraint, not a footnote.

---

## 3. One protocol, many models

There are many model providers, and you might expect each to need its own library. In practice, OpenAI's request format became the de facto standard, and most providers now accept it.

That means a single Python client can talk to OpenAI, to Google's Gemini, or to a model running on your own laptop, and the only thing that changes is the address it sends the request to. Activity 1 has you do exactly that, three times, with the same six lines of code.

This is worth internalizing early, because it reframes the vendor question. "Which LLM should we use?" sounds like a giant architectural commitment. Structurally, it is often a configuration value. The real differences between providers show up in cost, latency, quality on your specific task, and data handling terms, which are business decisions you can revisit, not a rewrite.

---

## 4. Where the model runs, and why you would ever run it yourself

Calling an API is the default. But an API call means your text leaves your infrastructure and lands on somebody else's servers, and you pay per token forever.

The alternative is running the weights yourself. Open models can be downloaded and run on your own hardware, either through a small local server or by loading them directly in Python, which is what Activity 3 does.

The trade-off is honest and unglamorous:

| | Hosted API | Local model |
|---|---|---|
| Quality | Frontier models, very strong | Smaller models, noticeably weaker on nuance |
| Cost | Per token, forever | Hardware you already own |
| Data | Leaves your network | Never leaves |
| Offline | No | Yes |
| Ops burden | None | Yours |

The size gap explains most of it. A frontier model is far too large to hand out as a download, which is exactly why it is sold as a metered service. A model small enough to run on a free Colab GPU is measurably worse at reasoning and instruction-following.

But quality is not the only axis. If the job is one narrow task done ten million times, or the data is legally prohibited from leaving your network, a small local model is not a compromise, it is the only correct answer. Notice that the sentiment classifier in Activity 3 is not a chatbot at all. Most production uses of local models look like that: small, specialized, fast, boring, and cheap.

---

## 5. Function calling: giving the model hands

The model cannot query your database, look up a claim, or reliably do arithmetic. It has no hands.

What it *can* do is recognize that a question requires one of those things, stop, and tell you precisely what it wants run and with what arguments.

The sequence is worth memorizing, because everything else today is a variation on it:

```
1. You send:      the question, plus a description of the tools available
2. Model replies: "I need get_claim_status with claim_id='CLM_101'"  (it stops here)
3. You run:       get_claim_status("CLM_101") -> {"status": "Approved", ...}
4. You send:      the whole conversation, plus that result
5. Model replies: "Claim CLM_101 is approved for $3,400."
```

Step 2 is the part people misunderstand. **No code executes inside the model.** It does not run your function, it does not see your database, and it cannot reach your systems. It hands you a work order and waits. You decide whether to run it. That boundary is a security property, and it is entirely under your control: the model can only ever request tools you chose to describe to it.

How does it know which tool to pick? Only from the descriptions you write. The tool's name, its description, and its parameter descriptions are the complete set of information the model has. A vague description produces a tool the model uses at the wrong times or not at all. Writing good tool descriptions is a real skill, and it is closer to writing documentation than to writing code.

---

## 6. The loop, and what "agent" means

One request and one response handle a question needing one tool, once. Real questions are messier. "What is the net payout on this claim after the deductible?" needs the claim amount, then the policy deductible, then a calculation, and two of those depend on results you do not have yet.

You cannot know in advance how many rounds that takes. So you write a loop: call the model, check whether it stopped to request a tool, run whatever it asked for, append the results, call again. Stop when it finally answers in plain language.

That loop is the entire idea behind agents.

> An **agent** is a model wrapped in a loop that can observe its situation, decide whether it needs more information or a side effect before it can answer, take an action to get it, and repeat, without a human approving each individual step.

There is no additional magic. Frameworks with impressive names add planning, memory, multi-agent coordination, and retries, all of which are real and useful, but every one of them is built on the loop you will write by hand in Activity 4.

**ReAct** (Reason + Act), which you build in Activity 5, is the same loop with the reasoning made visible. Instead of the model silently deciding and emitting a structured request, you prompt it to narrate: a `Thought` line, then an `Action` line, then it pauses while you run the action and feed back an `Observation`. It predates native function calling, works on any model that can follow instructions, and is far easier to debug because you can read the model's reasoning. It is also more fragile, because you are parsing free text instead of a guaranteed structure. Both approaches are worth knowing, and knowing why the industry moved from one to the other tells you what problem the newer one solves.

---

## 7. Shaping behavior before the model acts

Tools are half of it. The other half is what you put in front of the model. Three levers do most of the work:

| Lever | What it fixes | What it costs |
|---|---|---|
| **System prompt** | Output format, tone, role, constraints | One line, essentially free |
| **Few-shot examples** | Patterns easier to demonstrate than describe | A few extra messages per call |
| **Chain of thought** | Multi-step reasoning errors | More output tokens, slower responses |

The system prompt is the highest-leverage line of code in most LLM applications. "Respond with exactly one word: LOW, MEDIUM, or HIGH" turns a paragraph a human has to read into a value your pipeline can branch on. Most "the model is unreliable" complaints are really "nobody told the model what shape the answer needed to be in."

Chain of thought is the one people over-apply. Asking the model to reason step by step genuinely improves multi-step logic and arithmetic, and genuinely wastes tokens and latency on a simple lookup. It is a trade, not an upgrade.

---

## 8. MCP: the standard plug

By the end of Activity 4 you have working tools, but look closely at where they live. The JSON schemas are hand-written in your notebook. The name-to-function mapping is a dictionary in your notebook. None of it can leave your notebook.

If a teammate wants the same tools, they copy your code. If you want those tools available inside Claude Code or another AI client, you cannot, because there is no shared way to describe "here are some tools, here is how to call them."

**Model Context Protocol (MCP)** is that shared way. You run your tools as a small standalone program that speaks an agreed-upon protocol. Any client that also speaks it can connect, ask what tools exist, and call them, with no integration code written on either side.

The comparison people reach for is USB, and it holds up. Before USB, every peripheral needed its own port and its own driver. After, one connector, and the device describes itself when you plug it in. MCP does the same for model tools: the client asks `list_tools()` at runtime and the server answers.

Two things are worth being precise about, because they are commonly confused:

**MCP does not replace function calling.** The model still stops, still asks for a tool by name with arguments, still needs you to run it and return the result. MCP standardizes *discovery and transport*. The engine underneath is the same loop.

**This is what your AI coding assistant is doing.** When Claude Code reads a file or searches your repo, it is launching a server, asking what tools it has, choosing one, calling it, and feeding the result back into its own loop. Its ability to talk to GitHub, or a database, or a server you wrote this afternoon, is not built in. Those are separate MCP servers.

---

## 9. What to take away

The day has one argument, made five times:

A chat assistant that appears to "just know how to do things" is a next-token predictor, wrapped in a loop, calling tools that somebody wrote and registered. There is no other ingredient.

Once you can see that clearly, the useful questions get much sharper. Not "can AI do this?" but: does this problem need a model at all, or does a SQL query answer it? If it needs one, does it need tools, or just a good prompt? Should it run on someone's API or on our own hardware? What happens when it is confidently wrong, and who notices?

Those are engineering questions with real answers, and they are what today's group activity is for.
