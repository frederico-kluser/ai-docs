# Aider CLI Architecture: A Builder's Technical Reference

**Aider's architecture reveals battle-tested patterns for CLI-based AI coding assistants.** The ~39k-star open-source tool processes 15+ billion tokens weekly, with 70-88% of its own codebase written by AI. For builders, three insights stand out: the **Strategy pattern** for edit formats enables model-specific optimization, the **PageRank-based repository map** solves context window efficiency at scale, and the **architect/editor split** separates reasoning from syntactic accuracy—achieving state-of-the-art benchmark results.

This report dissects Aider's internals to inform your own CLI coding assistant design, with specific code references, algorithms, and actionable implementation guidance.

---

## System architecture centers on a modular Coder class

Aider's architecture follows a **modular design with clear separation of concerns**, employing the Strategy pattern for edit formats and Factory pattern for coder instantiation. The central orchestrator is the `Coder` class in `aider/coders/base_coder.py`.

### Core module structure

```
aider/
├── main.py           # CLI entry point, initialization
├── args.py           # Argument parsing (configargparse)
├── commands.py       # Slash command processing (/add, /drop, etc.)
├── io.py             # Terminal I/O (Rich + prompt_toolkit)
├── models.py         # LLM abstraction via LiteLLM
├── repo.py           # Git operations via GitPython
├── repomap.py        # PageRank-based code context
├── sendchat.py       # LLM communication layer
├── coders/           # Edit format implementations
│   ├── base_coder.py         # Central orchestrator
│   ├── editblock_coder.py    # SEARCH/REPLACE blocks
│   ├── wholefile_coder.py    # Complete file replacement
│   ├── udiff_coder.py        # Unified diff format
│   └── architect_coder.py    # Two-model workflow
└── resources/
    └── model-settings.yml    # Model-specific configurations
```

### Class responsibilities form a clear hierarchy

| Class | File | Responsibility |
|-------|------|----------------|
| **Coder** | base_coder.py | Orchestrates AI interactions, file tracking, message history |
| **Commands** | commands.py | Dispatches slash commands via introspection |
| **InputOutput** | io.py | Terminal I/O with Rich formatting, prompt_toolkit sessions |
| **Model** | models.py | LLM abstraction supporting 100+ models via LiteLLM |
| **GitRepo** | repo.py | Git operations, auto-commits, attribution |
| **RepoMap** | repomap.py | Tree-sitter parsing, PageRank context ranking |

The **Factory pattern** in `Coder.create()` instantiates the appropriate coder subclass based on the selected edit format:

```python
# From Coder.create() - simplified
edit_format_map = {
    "diff": EditBlockCoder,
    "whole": WholeFileCoder, 
    "udiff": UnifiedDiffCoder,
    "architect": ArchitectCoder,
}
coder_class = edit_format_map[edit_format]
return coder_class(main_model=main_model, ...)
```

---

## Data flow traces user input through LLM to file modification

Understanding the complete request lifecycle is essential for replicating Aider's behavior.

### End-to-end processing pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│  1. USER INPUT                                                   │
│     InputOutput.get_input() → prompt_toolkit session             │
│     Features: history, autocompletion, multiline                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. ROUTING (Coder.preproc_user_input)                          │
│     /command → Commands.run() → cmd_*() method                   │
│     Regular text → LLM processing                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. CONTEXT ASSEMBLY (format_chat_chunks)                       │
│     • System prompt (edit-format specific)                       │
│     • Repository map (PageRank-ranked symbols)                   │
│     • File contents (explicitly added files)                     │
│     • Chat history (may be summarized)                           │
│     • User message                                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. LLM CALL (litellm.completion)                               │
│     Streaming enabled by default                                 │
│     Retry logic for rate limits                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. EDIT EXTRACTION (get_edits - subclass-specific)             │
│     EditBlockCoder: Parse SEARCH/REPLACE blocks                  │
│     WholeFileCoder: Extract complete file contents               │
│     UnifiedDiffCoder: Parse unified diff hunks                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  6. EDIT APPLICATION (apply_edits - layered matching)           │
│     1. Exact match                                               │
│     2. Whitespace-normalized match                               │
│     3. Fuzzy match (difflib.SequenceMatcher)                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  7. GIT COMMIT (GitRepo.commit)                                 │
│     AI-generated commit message via weak_model                   │
│     Attribution: "(aider)" appended to author                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  8. VALIDATION (optional)                                        │
│     --auto-lint: Run linters, send errors to LLM                 │
│     --auto-test: Run tests, send failures to LLM                 │
└─────────────────────────────────────────────────────────────────┘
```

### Decision points where Aider acts autonomously

| Decision | Heuristic Used |
|----------|----------------|
| Call LLM vs. handle locally | Commands starting with `/` are local; all else goes to LLM |
| Edit format selection | Model-specific defaults in `model-settings.yml` |
| Repo map token allocation | Base **1,024 tokens**, doubled when no files in chat |
| File relevance ranking | PageRank on symbol reference graph |
| Chat history management | Summarize when exceeding `max_chat_history_tokens` |

---

## LLM integration uses LiteLLM for unified multi-model support

Aider's model layer abstracts 100+ LLMs through LiteLLM, enabling consistent API calls across OpenAI, Anthropic, Google, and dozens of other providers.

### When Aider calls the LLM

**Triggers LLM call:**
- User sends message requesting code changes
- Architect mode's two-step workflow (architect → editor)
- Commit message generation (uses cheap "weak_model")
- Chat history summarization
- Lint/test failure auto-fix loops

**Handles locally:**
- All `/commands` (add, drop, commit, undo, etc.)
- File I/O and parsing
- Git operations
- Repository map generation

### Dynamic prompt construction

Aider assembles prompts as "ChatChunks" with this structure:

```
System Message
├── Base system prompt (edit-format instructions)
├── Model-specific prefix (e.g., "Formatting re-enabled.")
└── Optional conventions from user config

Repository Map (ranked code context)

File Contents (full content of /add-ed files)

Chat History (recent or summarized)

User Message (current request)
```

### Edit format selection matches model capabilities

| Model | Default Format | Rationale |
|-------|---------------|-----------|
| Claude 3.5/3.7 Sonnet | `diff` | Strong at search/replace |
| GPT-4o | `diff` | Reliable format conformance |
| GPT-4 Turbo | `udiff` | Reduces "lazy coding" tendency |
| Gemini | `diff-fenced` | Better fence compliance |
| o1/o3 models | `architect` | Strong reasoning, weak editing—use two-stage |
| Weaker models | `whole` | Simplest format, highest reliability |

### Streaming and error handling

Streaming is **enabled by default** (`--stream`), providing real-time feedback via Rich's `Live` context for markdown rendering. Error handling uses LiteLLM's unified exception hierarchy:

```python
# Exception types (all mapped to OpenAI-compatible)
- APITimeoutError → Retry with exponential backoff
- RateLimitError → Retry with backoff
- ContextWindowExceededError → Summarize history, retry
- ContentPolicyViolationError → Report to user
```

---

## File operations leverage tree-sitter for accurate code understanding

Aider uses **tree-sitter** for AST-based code parsing—not regex or simple pattern matching. This enables language-aware symbol extraction across 30+ languages.

### Code parsing architecture

```python
# From repomap.py - tag extraction
def get_tags_raw(self, fname, rel_fname):
    lang = filename_to_lang(fname)      # Map extension → language
    parser = get_parser(lang)           # Tree-sitter parser
    query_scm = get_scm_fname(lang)     # Load tags.scm query
    
    code = self.io.read_text(fname)
    tree = parser.parse(bytes(code, "utf-8"))
    
    query = language.query(query_scm)
    captures = query.captures(tree.root_node)  # Extract definitions
```

Tree-sitter query files (`aider/queries/*.scm`) define what to extract per language—function definitions, class declarations, method signatures.

### Edit formats and diff application

**SEARCH/REPLACE blocks** (most common format):
```
filename.py
<<<<<<< SEARCH
from flask import Flask
=======
import math
from flask import Flask
>>>>>>> REPLACE
```

**Multi-strategy matching algorithm** in `editblock_coder.py`:

1. **Exact match**: Direct string comparison
2. **Whitespace-normalized**: Strip/normalize whitespace
3. **Indentation-preserving**: Handle varying indent levels
4. **Fuzzy match**: `difflib.SequenceMatcher` for approximate matching

When edits fail, Aider provides **detailed feedback** including the actual file lines that might match, enabling LLM self-correction on retry.

### Git integration is deep and automatic

Every edit triggers a Git commit (unless `--no-auto-commits`):

1. Pre-edit: Commit any uncommitted changes (never lose user work)
2. Apply edits from LLM response
3. Post-edit: Commit with AI-generated message via weak_model
4. Attribution: Appends "(aider)" to git author name

Commands: `/diff`, `/undo` (git reset), `/commit`, `/git <args>`

---

## Context window management uses PageRank for intelligent prioritization

The **repository map** is Aider's key innovation for context efficiency—a compressed view of the codebase showing only the most relevant symbols.

### How the repository map works

```
1. SYMBOL EXTRACTION
   └── Tree-sitter parses all source files
   └── Extracts definitions (classes, functions) and references

2. GRAPH CONSTRUCTION
   └── Nodes = source files
   └── Edges = file A references symbol from file B
   └── Edge weights = reference frequency

3. PAGERANK RANKING
   └── Score propagates through graph
   └── Highly-referenced symbols rank higher
   └── Chat mentions boost ranking

4. TOKEN OPTIMIZATION
   └── Binary search to fit within --map-tokens budget
   └── Default: 1,024 tokens (doubles if no files in chat)
```

### Token budget allocation

| Component | Budget Strategy |
|-----------|-----------------|
| System prompts | Always included (first priority) |
| Files in chat | Full content, no chunking |
| Repository map | `--map-tokens` (default 1024), expands 2x when no files |
| Chat history | Summarized when exceeds `max_chat_history_tokens` |

The `/tokens` command shows current allocation:
```
$ 0.0034  1,133  system messages
$ 0.0493 16,419  repository map      use --map-tokens to resize
$ 0.0XXX  X,XXX  chat history        use /clear to clear
$ 0.0XXX  X,XXX  filename.py         /drop to remove
```

### Chat history summarization

When history exceeds budget, `ChatSummary` class uses the weak_model to compress older messages while preserving recent context and key identifiers. Persistent storage uses `.aider.chat.history.md` (human-readable log) and `.aider.input.history` (shell-style recall).

---

## CLI design combines prompt_toolkit and Rich for professional UX

### REPL implementation

The main loop in `Coder.run()` uses prompt_toolkit's `PromptSession`:

```python
session = PromptSession(
    history=FileHistory(".aider.input.history"),
    completer=AutoCompleter(commands, fnames),
    vi_mode=args.vim,
    multiline=False,  # Toggle with { } delimiters
)
```

### Command discovery via introspection

Commands are automatically discovered from `cmd_*` methods:

```python
def get_commands(self):
    return [name[4:].replace("_", "-") 
            for name in dir(self) 
            if name.startswith("cmd_")]

# cmd_add → /add, cmd_chat_mode → /chat-mode
```

### Streaming output with Rich

```python
from rich.live import Live
from rich.markdown import Markdown

with Live(console=console, refresh_per_second=10) as live:
    response = ""
    for chunk in llm_stream():
        response += chunk
        live.update(Markdown(response))
```

### Essential commands for users

| Category | Commands |
|----------|----------|
| **Files** | `/add`, `/drop`, `/read-only`, `/ls` |
| **Git** | `/commit`, `/undo`, `/diff`, `/git <cmd>` |
| **Mode** | `/model`, `/chat-mode`, `/architect`, `/ask` |
| **Session** | `/clear`, `/reset`, `/tokens`, `/settings` |
| **Execution** | `/run`, `/test`, `/lint` |

---

## Intelligence layer determines relevance through graph analysis

### File relevance determination

Rather than simple keyword matching, Aider uses **graph-based importance scoring**:

1. Build dependency graph from symbol references
2. Apply PageRank to identify hub files
3. Boost files mentioned in current chat
4. Rank symbols by cross-reference frequency
5. Select top-ranked items within token budget

### Edit localization strategies

**Standard mode**: LLM receives repo map + files → outputs SEARCH/REPLACE blocks

**Architect mode** (for reasoning models like o1/o3):
1. **Architect model** plans changes in plain English
2. **Editor model** translates plan into file edits
3. Achieves **83-85.7%** on polyglot benchmark (state-of-the-art)

This separation leverages reasoning model strengths while avoiding their formatting weaknesses.

### Validation feedback loops

```
LLM edits files
    ↓
--auto-lint runs linter
    ↓ (if errors)
Errors sent to LLM → "Fix these lint errors"
    ↓
--auto-test runs tests
    ↓ (if failures)
Failures sent to LLM → "Fix failing tests"
```

---

## Competitive tools take different architectural approaches

### Comparison matrix

| Tool | Interface | Context Strategy | Edit Method | Key Strength |
|------|-----------|------------------|-------------|--------------|
| **Aider** | CLI | Tree-sitter + PageRank | SEARCH/REPLACE | Transparency, Git-native |
| **Cursor** | IDE (VS Code fork) | Full project analysis | Sketch + Apply model | Flow-state development |
| **Continue** | IDE plugin | Embeddings + RAG | Real-time inline | Privacy, local LLMs |
| **Copilot CLI** | CLI | MCP servers | Agent workflows | GitHub ecosystem |
| **Mentat** | CLI | ctags + RAG | Multi-file coords | Simple setup |

### Architectural trade-offs

**CLI (Aider, Mentat, Copilot CLI)**
- ✓ Lightweight, scriptable, Git-native
- ✗ No visual feedback, steeper learning curve

**IDE-integrated (Cursor, Continue)**
- ✓ Visual diffs, autocomplete, familiar environment
- ✗ Resource-heavy, potential vendor lock-in

**Context strategies:**
- **Graph ranking** (Aider): High token efficiency, requires tree-sitter setup
- **RAG/embeddings** (Continue): Good for search, less structural awareness
- **Full analysis** (Cursor): Most context, highest cost

---

## Implementation checklist for your own CLI assistant

### Core components required

1. **Entry point & CLI parsing**
   - [ ] Argument parser (argparse/click/configargparse)
   - [ ] Configuration file hierarchy (home → project → CLI)
   - [ ] Environment variable support

2. **REPL & user interaction**
   - [ ] prompt_toolkit PromptSession with history
   - [ ] Command discovery via introspection
   - [ ] Tab completion for commands and files
   - [ ] Rich for styled output and streaming

3. **LLM integration**
   - [ ] Multi-provider abstraction (LiteLLM recommended)
   - [ ] Streaming response handling
   - [ ] Retry logic with exponential backoff
   - [ ] Token counting per model

4. **Context management**
   - [ ] Code parsing (tree-sitter for AST)
   - [ ] Symbol extraction and graph building
   - [ ] Relevance ranking algorithm
   - [ ] Token budget allocation

5. **Edit application**
   - [ ] Edit format parser (SEARCH/REPLACE or diff)
   - [ ] Multi-strategy matching (exact → fuzzy)
   - [ ] Error feedback for failed edits

6. **Git integration**
   - [ ] Auto-commits with AI-generated messages
   - [ ] Undo capability (git reset)
   - [ ] Attribution tracking

7. **Validation**
   - [ ] Linter integration
   - [ ] Test runner integration
   - [ ] Feedback loop for auto-fix

### Key libraries to use

| Purpose | Library |
|---------|---------|
| LLM API | LiteLLM |
| Code parsing | tree-sitter + tree-sitter-language-pack |
| Terminal I/O | prompt_toolkit + Rich |
| Git operations | GitPython |
| Graph algorithms | NetworkX (for PageRank) |

---

## Open questions and research gaps

**Not fully determined from available sources:**

1. **Exact PageRank parameters**: Edge weights (50.0 for chat files, 10.0 for mentioned identifiers, 0.1 for private names) are documented, but full algorithm details require source inspection

2. **Token limit handling**: Aider uses "soft limits" and relies on API errors—unclear if there's proactive context pruning

3. **Architect mode internals**: The two-model handoff mechanism between architect and editor models needs deeper code review

4. **Cache invalidation strategy**: `.aider.tags.cache.v3/` uses mtime, but full invalidation logic unclear

5. **Streaming chunk processing**: How partial SEARCH/REPLACE blocks are buffered during streaming

---

## Recommended resources for deeper study

### Aider source code (key files)
- `aider/coders/base_coder.py` - Central orchestration logic
- `aider/repomap.py` - Repository map and PageRank implementation  
- `aider/coders/editblock_coder.py` - SEARCH/REPLACE parsing
- `aider/commands.py` - All slash command implementations
- `aider/models.py` - LLM abstraction layer

### Documentation and discussions
- [aider.chat/docs](https://aider.chat/docs) - Official documentation
- [aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html) - Repo map explanation
- [aider.chat/2023/10/22/repomap.html](https://aider.chat/2023/10/22/repomap.html) - Paul Gauthier's blog on repo map design
- [aider.chat/docs/more/edit-formats.html](https://aider.chat/docs/more/edit-formats.html) - Edit format details

### Related tools to study
- **Continue** (github.com/continuedev/continue) - Open-source IDE plugin with different context approach
- **OpenHands** (formerly OpenDevin) - Agent-based coding with optional LLM editing
- **SWE-agent** - Research tool with novel ACI (Agent-Computer Interface)

### Paul Gauthier's writings
- Search for blog posts at aider.chat explaining design decisions
- GitHub discussions on paul-gauthier/aider for implementation rationale

---

## Conclusion

Aider's architecture demonstrates that **modular design with intelligent context management** is the key to effective CLI coding assistants. The Strategy pattern for edit formats allows model-specific optimization, the PageRank-based repository map provides efficient context within token budgets, and the architect/editor split achieves state-of-the-art accuracy on coding benchmarks.

For builders, the most transferable patterns are: (1) use tree-sitter for language-aware code understanding rather than regex, (2) implement graph-based relevance ranking rather than simple RAG, (3) design multiple edit formats to match different model capabilities, and (4) integrate validation loops that feed errors back to the LLM. The codebase itself—70-88% AI-written—is testament to these patterns' effectiveness.