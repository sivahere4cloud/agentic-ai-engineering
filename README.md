# agentic-ai-engineering
Hands-on projects and notes from my Agentic AI Engineering learning path, building AI agents with OpenAI Agents SDK, CrewAI, LangGraph and MCP.

# 1. Agentic Foundation

Hands-on foundations for building AI agents: calling LLM APIs, comparing providers, giving a model tools, and hand-building an agent loop without a framework. The week ends with a working chatbot that represents me and answers questions about my career.

## What I built

### 1. First LLM calls
- Loaded API keys from `.env` and verified them without printing secrets
- Called the OpenAI Chat Completions and Responses APIs
- Chained calls so one model's output becomes the next prompt (prompt chaining)
- Used a stronger model as a judge to evaluate an answer (LLM-as-judge)

### 2. Multi-model comparison
- Sent the same question to several providers: OpenAI, Anthropic, Gemini, Groq, and a local model through Ollama
- Reused the OpenAI client class for every provider by changing `base_url` and the API key
- Collected the answers, anonymised them, and had a judge model rank them and return JSON
- Parsed the JSON to map the ranking back to model names
- Extension: an evaluator-optimizer round (critique the best answer, then revise it)

### 3. Career digital twin
- A chatbot grounded in my CV (read from a PDF) and a short written summary
- Gradio chat interface
- A tool the model can call to record the email address of a visitor who wants to get in touch
- A hand-written agent loop: call the model, run any tools it asks for, return the results, repeat until it answers
- An evaluator call that checks each reply stays on topic, with one retry

## Patterns practised

| Pattern | Where |
|---|---|
| Prompt chaining | Question, answer, judge chain |
| Parallelization | Same task sent to many models, results aggregated |
| Evaluator / LLM-as-judge | Ranking model answers; checking twin replies |
| Evaluator-optimizer | Critique and revise; retry on a failed check |
| Tool use | Email recording function described to the model as JSON |
| Agent loop | `while` the model requests tools, run them and call again |

## Key ideas I can explain

- **LLM calls are stateless.** The model remembers nothing between calls. A chat only feels like it has memory because the full history is resent each time.
- **A tool is a normal function.** The model never runs code. It returns the tool name and JSON arguments, my code runs the function, and I send the result back.
- **System prompt as grounding.** The twin only knows what I put in its context, so the prompt also tells it to say "I don't know" instead of inventing answers.
- **Many providers, one client.** Several providers expose OpenAI-compatible endpoints, so one library can call all of them.
- **Trade-offs of evaluators.** An extra check improves reliability but adds cost and latency to every reply, and a judge model can still be wrong or biased.

## Project layout

```
1_agentic-foundation/
  first-llm-call.ipynb         first calls, chaining, LLM-as-judge
  multi-model-comparison.ipynb multi-provider calls, ranking, evaluator-optimizer
  career-twin.ipynb            digital twin, tool calling, agent loop, evaluator
  twin/                        my CV (PDF) and summary - not committed
  emails.txt                   emails recorded by the tool - not committed
```

Adjust the notebook names above to match the files in this folder.

## Setup

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```powershell
uv sync
copy .env.example .env   # then add your own keys
```

Keys used (only the ones you need): `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `GROQ_API_KEY`.

To run the digital twin, create a `twin` folder next to the notebook with your own `linkedin.pdf` (or CV as a PDF) and a `summary.txt`. Optional: install [Ollama](https://ollama.com) for the local-model section.

## Privacy and safety notes

- `.env`, `emails.txt` and the `twin` folder are kept out of git. They hold secrets and personal data.
- The email tool trusts whatever string the model passes in. A production version would validate the address, handle write errors and store it somewhere safer than a text file.
- The agent loop has no round limit. A production version should cap the number of tool rounds to avoid runaway cost.

## Next

Week 2: the OpenAI Agents SDK, replacing the hand-built loop with a framework.