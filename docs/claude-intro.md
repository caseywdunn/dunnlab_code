---
title: Agent Concepts
nav_order: 5
---

# Agent Concepts

Coding agents differ in their interfaces and configuration, but they share the same basic architecture. This chapter provides a conceptual template for understanding any of them. The next chapter, [Coding Agents](other-agents.md), maps Claude Code and Codex onto these concepts.

[Managing Security](managing-security.md) is about constraining an agent, [Managing Context](managing-context.md) about giving it the right information, and [Working Effectively](working-effectively.md) about directing its work. All three build on the vocabulary introduced here.

## Model, harness, agent, and tool

The terms *model* and *agent* are often used interchangeably, but the distinction matters:

| Concept | What it is | Examples |
|---|---|---|
| **Model** | The system that interprets context and decides what to say or do next | Claude, GPT |
| **Harness** | The software around the model that assembles context, offers tools, executes approved actions, and manages sessions | Claude Code, Codex |
| **Agent** | A model operating through a harness in a loop toward a goal | A Claude Code or Codex session working on a project |
| **Tool** | A bounded action the harness makes available to the model | Read a file, edit text, run a command, search the web |

Vendors do not always use *harness* consistently, but it is useful language. A model by itself does not have a working directory, edit files, run shell commands, remember project instructions, or decide when approval is required. The harness supplies those capabilities and constraints. The same model can be used through different harnesses, and some harnesses can use more than one model.

## The agent loop

An agent repeatedly:

1. observes the request, current context, and results of earlier actions;
2. decides on a response or tool call;
3. asks the harness to execute that tool call;
4. receives the result in its context; and
5. continues until it considers the task complete, reaches a gate, or needs input.

This loop is what makes an agent different from a chatbot that only returns one answer. A single prompt can lead to many file reads, edits, commands, tests, and revisions. The harness enforces the actual boundary: a model can propose an action, but it is the harness and its surrounding operating system that determine whether the action happens.

## Working directory and project

A local coding agent normally starts in a **working directory**, usually the root of a Git repository. This tells the harness where to focus, where to find project instructions, and which files belong to the task. It is a default scope, not necessarily a security boundary: depending on the harness and its settings, an agent may be able to read or write elsewhere.

Start the agent from the project root unless you deliberately want narrower scope. This also gives it the complete Git history, project-level instructions, tests, and planning files.

## Context

The **context** is the information the model can use at a particular moment. A harness assembles it from some combination of:

- your request and the conversation;
- standing project and user instructions;
- files the agent reads or that an editor supplies;
- tool definitions and skill descriptions;
- tool results, such as command output and search results; and
- saved memory or session state.

The agent does not automatically hold the whole repository in its mind. Context is finite, and large files, verbose command output, and long conversations compete for space. Good harnesses load some information progressively and let the agent retrieve more when needed. [Managing Context](managing-context.md) explains how to make the right information easy to find.

## Instructions, memory, and skills

Harnesses usually load standing instructions from plain-text files in or above the project. These record commands, conventions, constraints, and other facts that should apply across sessions. The filenames and precedence rules vary by product.

Some harnesses can also retain **memory** from earlier sessions. Treat it as a convenience rather than the authoritative project record: durable decisions belong in version-controlled files.

A **skill** is a reusable package of instructions, sometimes accompanied by scripts, references, or assets. Skills provide task-specific methods without placing every detail in the startup context. Product support and packaging differ, even where agents use the same underlying open format.

## Tools and extensions

The harness exposes tools to the model. Most coding agents include tools for reading and editing files, searching a repository, and running terminal commands. The terminal is especially powerful because it gives the agent access to ordinary command-line programs such as Git, test runners, data-analysis software, cluster schedulers, and the GitHub CLI.

Common extension mechanisms include:

| Mechanism | Purpose |
|---|---|
| **Tools** | Perform bounded actions such as reading, editing, searching, or running a command |
| **Skills** | Supply reusable, task-specific instructions and supporting resources |
| **Hooks** | Run deterministic code at defined points in the harness lifecycle |
| **Subagents** | Delegate bounded work into a separate context, sometimes in parallel |
| **MCP servers** | Connect the harness to external tools and data through the Model Context Protocol |
| **Plugins** | Bundle one or more extensions for installation and distribution |

Not every harness supports every mechanism, and identical names do not guarantee identical behavior.

## Permissions and sandboxing

Two controls are easy to confuse:

- An **approval policy** determines when the harness pauses to ask a person before acting.
- A **sandbox** determines what an action can technically access even if the model or user approves it.

An approval prompt is a workflow gate, not a security boundary. A sandbox, container, virtual machine, dedicated computer, or restricted account supplies the boundary. The safest useful setup combines an appropriate boundary with an approval policy that does not interrupt routine work. See [Managing Security](managing-security.md) for the practical consequences.

## Sessions and surfaces

A **session** is a continuing run with its conversation and accumulated state. Sessions may be interactive or unattended, local or remote, and exposed through a terminal, editor, desktop application, or web interface. Some harnesses can resume sessions or hand work between surfaces, but the exact state that travels varies.

Local and cloud agents can implement the same loop while running in very different environments. A local harness acts through your machine and credentials. A cloud harness normally works in a provisioned environment and returns a patch, branch, or pull request. For long-running local and remote work, see [Working Across Computers](working-across-computers.md).

With this template in place, the meaningful questions about a coding agent become concrete: which model and context does its harness use, which tools can it call, where does it run, how is it constrained, and how does it preserve state? The next chapter answers those questions for Claude Code and Codex.
