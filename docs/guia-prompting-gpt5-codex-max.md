# The definitive prompting guide for GPT-5.1-Codex-Max

GPT-5.1-Codex-Max is OpenAI's frontier agentic coding model, purpose-built for long-running autonomous software engineering tasks—and it demands a fundamentally different prompting approach than previous models. Released November 19, 2025, this model introduces **native compaction** (coherent work across millions of tokens), achieves **77.9% on SWE-bench Verified** with 30% fewer thinking tokens, and can work independently for **24+ hours**. The critical insight: less prompting is more. Remove instructions for upfront plans, preambles, and status updates—these cause the model to stop abruptly. Start with OpenAI's standard Codex-Max prompt and make only tactical additions.

---

## What makes GPT-5.1-Codex-Max fundamentally different

This model represents a paradigm shift from general-purpose LLMs to specialized agentic coding. Unlike GPT-5.2 (general purpose) or GPT-4o (multimodal), GPT-5.1-Codex-Max is optimized exclusively for software engineering tasks in Codex-like environments. Three capabilities set it apart:

**Native compaction** enables the model to work across multiple context windows by automatically compressing conversation state while preserving critical context. When sessions approach the **400,000 token** limit, the model prunes history while retaining architectural decisions, test failures, and file locations. This unlocks project-scale refactors and multi-hour agent loops previously impossible with standard context windows.

**First-class Windows support** makes this the first OpenAI model trained to operate natively in Windows/PowerShell environments, not just Unix-like systems.

**Extreme instruction adherence** distinguishes it from Claude and other models—GPT-5.1-Codex-Max follows instructions with literal precision that can be counterproductive if prompts contain throwaway sentences. One developer reported watching the model work for 30 minutes on a convoluted solution because of a forgotten instruction clause.

| Specification | Value |
|--------------|-------|
| Context window | 400,000 tokens |
| Max output tokens | 128,000 tokens |
| Knowledge cutoff | September 30, 2024 |
| Pricing (input/cached/output) | $1.25 / $0.125 / $10.00 per 1M tokens |
| API availability | **Responses API only** (not Chat Completions) |
| Reasoning effort levels | none, medium, high, xhigh |

---

## The official system prompt that OpenAI optimized

OpenAI's prompting guide explicitly states to start with their standard prompt as your base. This prompt was optimized against internal evals for answer correctness, completeness, tool usage, parallelism, and bias for action. The four critical sections that must be preserved:

### Autonomy and persistence block
```
You are autonomous senior engineer: once the user gives a direction, 
proactively gather context, plan, implement, test, and refine without 
waiting for additional prompts at each step.

Persist until the task is fully handled end-to-end within the current 
turn whenever feasible: do not stop at analysis or partial fixes; carry 
changes through implementation, verification, and a clear explanation of 
outcomes unless the user explicitly pauses or redirects you.

Bias to action: default to implementing with reasonable assumptions; do 
not end your turn with clarifications unless truly blocked.
```

### Codebase exploration with mandatory parallelization
```
# Exploration and reading files
- **Think first.** Before any tool call, decide ALL files/resources you will need.
- **Batch everything.** If you need multiple files, read them together.
- **multi_tool_use.parallel** Use `multi_tool_use.parallel` to parallelize.
- **Workflow:** (a) plan all needed reads → (b) issue one parallel batch → 
  (c) analyze results → (d) repeat if new, unpredictable reads arise.

Never read files one-by-one unless logically unavoidable. This concerns 
every read/list/search operation including cat, rg, sed, ls, git show.
```

### Tool preference hierarchy
```
If a tool exists for an action, prefer to use the tool instead of shell 
commands (e.g read_file over cat). Default to solver tools: git (all git), 
rg (search), read_file, list_dir, glob_file_search, apply_patch, 
todo_write/update_plan. Use cmd/run_terminal_cmd only when no listed 
tool can perform the action.
```

### Frontend quality standards
```
# Frontend tasks
When doing frontend design tasks, avoid collapsing into "AI slop":
- Typography: Use expressive fonts, avoid defaults (Inter, Roboto, Arial)
- Color: Choose clear visual direction; define CSS variables; no purple bias
- Motion: Use meaningful animations (page-load, staggered reveals)
- Background: Use gradients, shapes, or subtle patterns—not flat colors
- Ensure the page loads properly on both desktop and mobile
```

---

## What you must NOT include in prompts

The most common cause of failed GPT-5.1-Codex-Max sessions is prompting for behaviors the model already handles automatically through its reasoning summary system—handled by a separate model that is **not promptable**.

| Anti-pattern | Why it breaks the model |
|--------------|------------------------|
| "First, outline your plan..." | Causes abrupt stopping before code completion |
| "Provide status updates as you work" | Interferes with reasoning summaries |
| "Start with a preamble explaining approach" | Model trained without preambles; requesting causes early termination |
| Instructions about intermediate messages | Reasoning summaries are separate and unpromptable |
| Single-step plans | Wastes overhead; skip planning for simple tasks |
| Promising tests/refactors without doing them | Mark as "optional Next steps" or exclude entirely |

**Critical**: The model also follows instructions with extreme literalness. One documented case: asked to "fix a test that asserts `1 + 1 === 3`," Claude would recognize the typo and fix the test. GPT-5.1-Codex-Max would attempt to rewrite arithmetic to make the assertion pass.

---

## Reasoning effort selection determines everything

The `reasoning.effort` parameter fundamentally changes model behavior and should be your primary tuning mechanism:

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5.1-codex-max",
    input="Refactor this codebase to use async I/O",
    reasoning={
        "effort": "medium"  # Options: none, medium, high, xhigh
    }
)
```

| Level | Thinking tokens | Use case |
|-------|----------------|----------|
| `none` | Zero | Fast, latency-sensitive tasks—formatting, simple queries |
| `medium` | Balanced | **Recommended default** for interactive coding |
| `high` | Thorough | Complex debugging, multi-file refactors |
| `xhigh` | Maximum | Hardest tasks—architectural changes, deep debugging sessions, 24-hour autonomous runs |

**Key insight**: `xhigh` achieved 77.9% on SWE-bench while using 30% fewer thinking tokens than GPT-5.1-Codex at `medium`. For difficult tasks, higher reasoning effort is both more accurate and more efficient.

---

## Structuring prompts for optimal code output

### The apply_patch tool is non-negotiable

GPT-5.1-Codex-Max was trained extensively on the apply_patch format. Using alternative diffing approaches degrades performance:

```python
# Built-in server-defined tool (simplest)
tools = [{"type": "apply_patch"}]

response = client.responses.create(
    model="gpt-5.1-codex-max",
    input=input_items,
    tools=tools,
    parallel_tool_calls=False,  # Recommended for file edits
)

# Response contains apply_patch_call items:
for item in response.output:
    if item.type == "apply_patch_call":
        # operation: {type: "update_file", path: "/app/page.tsx", diff: "..."}
        print(item.operation)
```

The patch format uses a stripped-down diff grammar:

```
*** Begin Patch
*** Update File: src/utils.ts
@@ export function calculateTotal(
-  return items.reduce((sum, item) => sum + item.price, 0);
+  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
*** End Patch
```

### Multi-file code generation pattern

```python
MULTI_FILE_PROMPT = """
The user has the following files:
<BEGIN_FILES>
===== lib/auth.ts
export function validateToken(token: string): boolean {
    return token.length > 0;
}
===== api/routes.ts
import { validateToken } from '../lib/auth';
export function handleRequest(req: Request) {
    if (!validateToken(req.headers.authorization)) {
        return new Response('Unauthorized', { status: 401 });
    }
}
<END_FILES>

User query: Add JWT validation with expiry checking
"""

response = client.responses.create(
    model="gpt-5.1-codex-max",
    input=MULTI_FILE_PROMPT,
    tools=[{"type": "apply_patch"}],
    reasoning={"effort": "high"}
)
```

### File path reference format

When referencing files in prompts or expecting references in output:
- Use inline code paths: `src/app.ts`
- Include line numbers: `src/app.ts:42` or `src/app.ts:42:5` (line:column)
- Accept diff prefixes: `a/server/index.js`, `b/server/index.js#L10`
- **Never use** URIs like `file://`, `vscode://`, or `https://`

---

## JSON and structured output specifications

Structured outputs require explicit schema definition with strict constraints:

```python
response = client.responses.create(
    model="gpt-5.1-codex-max",
    input=[
        {"role": "user", "content": "Analyze this PR for issues..."}
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "code_review",
            "schema": {
                "type": "object",
                "properties": {
                    "issues": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                                "file": {"type": "string"},
                                "line": {"type": "integer"},
                                "description": {"type": "string"}
                            },
                            "required": ["severity", "file", "description"],
                            "additionalProperties": False
                        }
                    },
                    "summary": {"type": "string"}
                },
                "required": ["issues", "summary"],
                "additionalProperties": False
            },
            "strict": True  # Required for guaranteed schema adherence
        }
    }
)
```

**Constraints for structured outputs:**
- Root objects cannot be `anyOf` type
- All fields must appear in `required` array
- `additionalProperties` must be `false`
- `strict: true` is required for guaranteed adherence

For Pydantic users, the SDK provides native integration:

```python
from pydantic import BaseModel

class CodeReview(BaseModel):
    issues: list[dict]
    summary: str

response = client.responses.create(
    model="gpt-5.1-codex-max",
    input=[{"role": "user", "content": "Review this code..."}],
    text_format=CodeReview
)
parsed = response.output_parsed
```

---

## Compaction enables unlimited context sessions

Compaction is GPT-5.1-Codex-Max's breakthrough feature—automatic context compression that preserves critical information while freeing space for continued work.

### How to invoke compaction

```python
# When context grows large, call /compact endpoint
compacted = client.responses.compact(
    model="gpt-5.1-codex-max",
    input=conversation_history,  # Must fit within 400k context
    instructions="Optional system instructions"
)

# Response includes encrypted compaction item
# {"type": "compaction", "encrypted_content": "gAAAAABpM0Yj-...="}

# Pass compacted output to subsequent requests
next_response = client.responses.create(
    model="gpt-5.1-codex-max",
    input=compacted.output  # Includes encrypted_content
)
```

**Compaction preserves:**
- Architectural decisions and code choices
- Current goals and test failures
- Important file locations
- Salient interaction context in dense summary blocks

**Best practices:**
- Compact after major milestones or when context exceeds ~200k tokens
- Don't compact every turn (adds latency and cost)
- Treat `encrypted_content` as opaque—never parse it
- Note that aggressive summarization may blur subtle details over time

---

## Function calling and tool definitions

### Complete shell command tool

```typescript
const shellTool = {
    type: "function",
    name: "shell_command",
    description: "Runs a shell command. Always set workdir param.",
    strict: false,
    parameters: {
        type: "object",
        properties: {
            command: { type: "string", description: "Shell script to execute" },
            workdir: { type: "string", description: "Working directory" },
            timeout_ms: { type: "number", description: "Timeout in milliseconds" },
            with_escalated_permissions: { type: "boolean" },
            justification: { type: "string", description: "Required if escalated" }
        },
        required: ["command"],
        additionalProperties: false
    }
};
```

### Update plan tool for task tracking

```typescript
const updatePlanTool = {
    type: "function",
    name: "update_plan",
    description: "Updates task plan with steps and statuses.",
    parameters: {
        type: "object",
        properties: {
            explanation: { type: "string" },
            plan: {
                type: "array",
                items: {
                    type: "object",
                    properties: {
                        step: { type: "string" },
                        status: { type: "string", description: "pending, in_progress, completed" }
                    },
                    required: ["step", "status"]
                }
            }
        },
        required: ["plan"]
    }
};
```

### Built-in tools available
- `apply_patch` — Structured diff application (trained extensively on this)
- `web_search` — Internet search capability
- `file_search` — Vector store file search
- `code_interpreter` — Python code execution

### Tool response truncation rule
Limit all tool responses to **10k tokens** (approximate: `bytes / 4`). If truncation needed, use 50% budget for beginning, 50% for end, insert `…{N} tokens truncated…` in middle.

---

## AGENTS.md injects persistent instructions

The Codex CLI automatically discovers and injects AGENTS.md files from `~/.codex` plus each directory from repo root to CWD. Later directories override earlier ones.

```markdown
# AGENTS.md
## Repository expectations
- Run `npm run lint` before opening a pull request.
- Document public utilities in `docs/` when you change behavior.

## Safety rules (CRITICAL)
- NEVER delete files unless explicitly asked
- NEVER use `git checkout --` or `git reset --hard`
- NEVER revert existing changes you did not make
- If you notice unexpected changes, STOP and ask user
```

Each chunk is injected as a user-role message:
```
# AGENTS.md instructions for <directory>
<INSTRUCTIONS>
...file contents...
</INSTRUCTIONS>
```

---

## Production-ready TypeScript example

```typescript
import OpenAI from "openai";

const client = new OpenAI();

async function refactorCodebase(task: string) {
    const response = await client.responses.create({
        model: "gpt-5.1-codex-max",
        input: [
            {
                role: "system",
                content: `You are an autonomous senior engineer. 
                Persist until the task is fully handled end-to-end.
                Bias to action: implement with reasonable assumptions.
                Use apply_patch for all file modifications.
                Batch file reads with multi_tool_use.parallel.`
            },
            { role: "user", content: task }
        ],
        reasoning: { effort: "high" },
        tools: [
            { type: "apply_patch" },
            {
                type: "function",
                name: "shell_command",
                description: "Execute shell commands",
                parameters: {
                    type: "object",
                    properties: {
                        command: { type: "string" },
                        workdir: { type: "string" }
                    },
                    required: ["command"],
                    additionalProperties: false
                },
                strict: true
            }
        ],
        parallel_tool_calls: true
    });

    // Process apply_patch calls
    for (const item of response.output) {
        if (item.type === "apply_patch_call") {
            console.log(`Patching ${item.operation.path}`);
            // Apply the patch to filesystem
        }
    }

    return response.output_text;
}

// Usage
await refactorCodebase(
    "Refactor the authentication module to use OAuth 2.1 with refresh token rotation"
);
```

---

## Known failure modes and how to prevent them

### File deletion under stress
The model may delete entire files when it feels it has made "too many continuous edits." One GitHub issue documented the model deleting an almost-complete file after extended iteration.

**Prevention**: Add to AGENTS.md: `Never delete files unless explicitly asked`

### Excessive looping without progress
If the model re-reads or re-edits the same files without clear progress, it may give up destructively.

**Prevention**: The standard prompt includes: `Avoid excessive looping or repetition; if you find yourself re-reading or re-editing the same files without clear progress, stop and end the turn with a concise summary and any clarifying questions needed.`

### Premature completion
The model may return every 2 minutes even when tasks remain incomplete.

**Prevention**: Use `xhigh` reasoning effort for complex tasks; ensure autonomy instructions are preserved.

### Compaction context loss
Aggressive summarization during compaction may lose subtle details that become important later.

**Prevention**: Maintain versioned repo snapshots; don't rely solely on model's compacted memory.

---

## Security and sandbox recommendations

The model runs in a secure sandbox by default with file writes limited to workspace and network access disabled.

| Sandbox mode | Behavior |
|--------------|----------|
| `read-only` | Only file reading permitted |
| `workspace-write` | Read all files, edit only in cwd/writable_roots (recommended) |
| `danger-full-access` | No sandboxing (not recommended) |

**Critical security note**: Enabling internet access introduces prompt injection risks from untrusted content. OpenAI explicitly recommends keeping the model in restricted-access mode and reviewing all outputs before deployment.

The system card reports **100% refusal rate** on synthetic prompt injection benchmarks, though experts note this benchmark may not capture real-world attack vectors. The model is trained to ignore injected instructions and adhere to governing rules.

---

## Conclusion

GPT-5.1-Codex-Max requires a fundamentally different prompting philosophy than conversational models: minimize instruction, maximize autonomy, and trust the model's trained behaviors. The key principles that determine success:

**Start with OpenAI's standard prompt**—it was optimized against production evals. Make only tactical additions targeting specific project requirements.

**Never prompt for plans, preambles, or status updates**—these cause abrupt termination. Reasoning summaries are handled by a separate unpromptable system.

**Use `medium` reasoning effort as your default**, escalating to `high` or `xhigh` only for complex tasks where latency doesn't matter.

**Leverage compaction for long sessions** but maintain external backups—subtle context may blur over time.

**The model follows instructions with extreme literalness**—review AGENTS.md carefully and remove any throwaway clauses that could trigger counterproductive behavior.

For the most current reference implementation, clone [github.com/openai/codex](https://github.com/openai/codex) and explore the TypeScript SDK and the prompt file at `codex-rs/core/gpt-5.1-codex-max_prompt.md`.