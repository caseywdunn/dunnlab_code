---
title: Coding Agents
nav_order: 6
---

# Coding Agents

The concepts in the previous chapter are implemented differently by each coding-agent harness. This chapter maps [Agent Concepts](claude-intro.md) onto Claude Code and OpenAI Codex. We use both, so the goal is not to rank them; it is to make their similar capabilities and different names, controls, and configuration files legible.

## Claude Code and Codex at a glance

| Concept | Claude Code | Codex |
|---|---|---|
| **Model** | Claude models | OpenAI models, with model selection varying by surface and account |
| **Local harness** | Claude Code CLI and editor integrations | Codex CLI and IDE extension |
| **Cloud harness** | Claude Code on the web | Codex cloud |
| **Project instructions** | `CLAUDE.md` and `.claude/rules/` | Layered `AGENTS.md` files |
| **Remembered context** | Auto memory | Session history; durable project knowledge belongs in files |
| **Core tools** | File operations, search, shell commands, and web tools | File operations, search, shell commands, and web tools |
| **Extensions** | Skills, hooks, subagents, MCP servers, and plugins | Skills, subagents, MCP servers, and plugins; support varies by surface |
| **Permissions** | Permission modes and allow/ask/deny rules | Approval policy, sandbox policy, and newer permission profiles |
| **Unattended work** | Non-interactive CLI and web tasks | `codex exec` and cloud tasks |

Both are harnesses around a model. Both assemble context, follow repository instructions, inspect and edit files, run terminal tools, and iterate on results. Both have local and cloud forms, support MCP and skills, can delegate to subagents, and can be configured for more or less autonomy. Git remains the common record: whichever agent does the work, review its diff and preserve verified steps as commits.

The differences are mostly in how those ideas are packaged. A command, setting, or extension that exists in one should not be assumed to exist—or behave identically—in the other.

## Working directory and context

In the terminal, launch either agent from the root of the Git repository. That directory becomes the focus for file discovery, commands, Git operations, and project instructions. It is not automatically a security boundary; permissions and sandboxing determine what the harness can actually reach.

Claude Code assembles project context from `CLAUDE.md`, `.claude/rules/`, auto memory, installed skills and plugins, and configured MCP servers. `/context` shows what has loaded.

Codex reads `AGENTS.md` files from the repository root down to the current directory, with instructions closer to the working directory taking precedence. Its CLI, IDE extension, and desktop app share MCP configuration, while the exact context supplied by an editor or cloud task differs from a terminal session.

## Tools and extensions

Both harnesses can read and edit files, search code, and drive the shell. This makes ordinary command-line tools—Git, `gh`, test runners, package managers, analysis programs, and schedulers—the most portable way to extend what they can do.

The two products also support skills, subagents, MCP servers, and plugins, but their configuration and surface support differ. Claude Code additionally exposes hooks that run deterministic shell commands at lifecycle events. Treat matching feature names as a starting point for comparison, not proof of interchangeability.

## Permissions

Claude Code presents several [permission modes](https://code.claude.com/docs/en/permission-modes), including its normal interactive mode, a mode that accepts file edits while still reviewing other actions, plan mode, and `bypassPermissions`. Rules can allow, ask about, or deny particular tools and commands. Its sandbox can reduce approval prompts while restricting filesystem and network access.

Codex makes the two underlying controls especially explicit:

- The **sandbox policy** determines what a command can technically read, write, or reach. The three basic modes are `read-only`, `workspace-write`, and `danger-full-access`.
- The **approval policy** determines when Codex stops to ask you. The main choices are `on-request`, `untrusted`, and `never`; [Auto-review](https://developers.openai.com/codex/sandboxing/auto-review) can instead evaluate eligible approval requests automatically without removing the sandbox boundary.

Useful Codex starting points include:

| Setup | Behavior |
|---|---|
| **Read-only** — `--sandbox read-only --ask-for-approval on-request` | Inspects the project and answers questions; asks before edits, command execution, or network access. Good for planning and review. |
| **Auto** — `--sandbox workspace-write --ask-for-approval on-request` | Reads, edits, and runs commands inside the workspace automatically; asks before leaving it or using the network. This is the normal local default. |
| **Edit with command review** — `--sandbox workspace-write --ask-for-approval untrusted` | Can edit the workspace, but asks before running commands Codex does not classify as trusted. |
| **Auto-review** — `--approve-for-me` | Keeps the `workspace-write` boundary while routing eligible approval requests through automatic review instead of making you click through them. |
| **Unattended read-only** — `--sandbox read-only --ask-for-approval never` | Can inspect but not change the project and never interrupts for approval; useful in non-interactive checks. |
| **Full access** — `--dangerously-bypass-approvals-and-sandbox` | Removes both the sandbox and approval prompts. Use only inside a separate environment whose isolation you trust. |

Use `/permissions` to inspect or change permissions during an interactive Codex session. The CLI flags above are useful when launching a session, and the same values can be persistent in `~/.codex/config.toml`. Network access is separate and is off by default in `workspace-write`, which is why an otherwise autonomous session may still ask before downloading a dependency or contacting an API.

Newer Codex versions also have beta [permission profiles](https://developers.openai.com/codex/permissions), which combine filesystem and network rules into a named policy. The built-ins are `:read-only`, `:workspace`, and `:danger-full-access`, and narrower custom profiles can be defined for particular projects. This system replaces rather than layers on top of the older `sandbox_mode` settings, so consult the current documentation before adopting it in shared configuration.

Claude Code's `bypassPermissions` and Codex's full-access setting are deployment choices, not convenience toggles. In either case, make the surrounding computer, container, or virtual machine safe before removing the harness boundary. [Managing Security](managing-security.md) develops this principle in detail.

## Serving both from one file

The filenames for project instructions differ. Codex reads [`AGENTS.md`](https://agents.md/), a plain Markdown file at the repository root that can contain build commands, test commands, conventions, and warnings. It also discovers more specific `AGENTS.md` files deeper in the directory tree.

**Claude Code reads `CLAUDE.md`, not `AGENTS.md`.** A repository with only an `AGENTS.md` gives Claude Code no project instructions. Maintaining two copies invites them to drift, so put the real content in `AGENTS.md` and make `CLAUDE.md` a one-line import:

```markdown
@AGENTS.md
```

Claude Code expands the import at session start. Both harnesses then receive the same version-controlled instructions, while other agents that support `AGENTS.md` can use them too.

## What carries between agents

### Command-line tools and Git carry best

A script or command that works in the terminal usually works no matter which harness invokes it. Plain-text inputs, explicit commands, automated checks, and small Git commits therefore provide the strongest common foundation.

### MCP servers are portable

The [Model Context Protocol](https://modelcontextprotocol.io/) connects a harness to external tools and data, such as GitHub, a database, or an internal API. Claude Code and Codex both support MCP. A server can usually be reused, but each harness has its own configuration and authentication details.

### Skills share a core format

[Agent Skills](https://agentskills.io/) packages instructions in a `SKILL.md`, optionally with scripts and reference files. Claude Code and Codex both support skills and load their full instructions only when relevant. Product-specific frontmatter, variables, tool names, and invocation behavior may not transfer, so keep shared skills close to the core format and test them in every target harness.

### Plugin packaging may differ

Both Claude Code and Codex support plugins, but a plugin is more than the skills inside it: manifests, marketplaces, namespaces, and supported components can differ. Do not assume that a package built for one installs unchanged in the other. The Dunn Lab skills use ordinary `SKILL.md` files and are the portable core; the surrounding [plugin](plugin.md) may require product-specific packaging.

## Other coding agents

The same conceptual template can be used to evaluate other products. For now, this manual only notes the main categories:

| Tool | Useful distinction |
|---|---|
| **[GitHub Copilot](https://github.com/features/copilot)** | Editor, command-line, GitHub, review, and coding-agent surfaces integrated with GitHub workflows |
| **[Cursor](https://cursor.com/)** | An AI-focused editor built around an agentic coding workflow |
| **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** and **[Jules](https://jules.google/)** | Google's terminal and asynchronous cloud agents |
| **[Aider](https://aider.chat/)**, **[goose](https://block.github.io/goose/)**, and **[OpenCode](https://github.com/anomalyco/opencode)** | Terminal-oriented agents with varying model-provider support |
| **[Devin](https://devin.ai/)** and **[Windsurf](https://windsurf.com/)** | An asynchronous agent and an agent-oriented editor from Cognition |

Rather than asking which agent is best in the abstract, ask the harness questions from the previous chapter: Where does it run? What context and instructions does it load? Which tools can it call? What is the sandbox boundary? When does it ask permission? How are sessions resumed and work reviewed? Those answers determine whether it fits a particular project.
