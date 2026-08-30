---
title: Working Effectively
nav_order: 10
---

# Working Effectively

Getting good results is mostly about how you frame the work, not how you word the prompt. The habits below matter far more than any phrasing, and several of them run against the instinct people arrive with.

## Ask for more than you think you want

The most common mistake is asking for too little. People start with something narrow and mechanical — *run this tool with these settings on this file* — and widen only once that works.

Try the opposite. **Start with the largest sensible version of the request, and narrow down if it cannot manage it.** Describe the goal rather than the step: what you are trying to find out, what you have, and what a good answer would look like.

Two things follow. The first is efficiency — if the broad request works, you have skipped a dozen narrow ones. The second matters more. **A narrow request can only give you what you already thought of.** Ask for a specific tool with specific flags and that is exactly what you get, including in the case where a better approach was one question away. Open-ended requests surface solutions you would not have specified: a different tool, a simpler formulation, an assumption in your framing that does not hold.

The cost of a broad request that misses is one conversation. The cost of a narrow request that succeeds is never finding out what you missed.

One exception worth naming. When you know precisely what you want and a wrong guess is expensive — a destructive operation, a long compute job, anything touching raw data — say precisely what you want.

## Ask scientific questions, not just technical ones

Related, and easy to miss: you do not have to restrict yourself to tasks you have already identified as technical problems.

Point it at your data and ask an open scientific question. *What does the distribution of this look like across samples, and is anything about it surprising?* *Are there patterns in this table worth following up?* *What would you check first if you were trying to break this result?*

You advance the project and learn something at the same time. This is also where these tools are least like a faster autocomplete and most like a colleague who has actually read the data — and precisely why [Using AI in Research](using-ai.md) insists that evaluating the answer remains your job.

## Treat the agent as a teacher, not just a doer

A common criticism of generative AI is that it weakens people's abilities by depriving them of the learning and practice that come from doing the work themselves. That has not been my experience, nor the experience of colleagues who now use AI extensively. The difference, I think, is not an intrinsic property of the technology but how we choose to use it.

I am learning many new things as I use AI because I treat the agent as a teacher as well as a doer. Broad tasks and open-ended questions give it room to suggest approaches you did not know about or might not have chosen yourself. When that happens — ideally during planning, before anything expensive depends on the choice — ask why it chose that approach.

Sometimes you were right to question it. The agent may be missing context or expertise that you have, and explaining why another approach is better makes both the plan and your own reasoning more explicit. Other times it will introduce a method, tool, or way of thinking that is new to you. Ask it to explain the idea, its tradeoffs, and why it fits the problem; you have just added something to your own toolbox rather than merely receiving an output.

Stay curious. Ask why, ask what the alternatives are, and ask what you should understand before accepting a choice. Used this way, an agent does not remove learning from the work. It puts a patient, on-demand teacher inside it.

## Separate planning from building

Split the work into a planning phase and an implementation phase, deliberately, rather than letting them run together.

The reason is not tidiness. **A plan is where mistakes are cheap.** Once the agent starts building, it builds on whatever you told it, including the parts you got wrong — and by the time a bad assumption is visible in code it has already propagated through everything downstream. Reviewing a plan is your chance to check the details you supplied before anything is constructed on top of them.

In practice, begin with editing disabled: use Claude Code's Plan mode or Codex's `read-only` sandbox, or explicitly ask either agent to produce a plan before implementation. Read the plan properly, argue with it, and only then let the agent work.

Most work settles into a rhythm of plan, execute, then back to plan for the next piece. The commands differ, but the workflow does not: change the harness boundary deliberately when moving from review to implementation.

## Commit the plan for anything large

For a project of any size, do not leave the plan in the conversation. **By “the plan,” this manual means a real file such as `PLAN.md` or `dev_docs/overview.md` inside the Git repository, not a passage that exists only in chat.** Have the agent write it, commit it, and iterate on it before building anything.

Ask for the plan rather than writing it yourself. Then refine it the same way — *this section assumes we already have aligned reads, which we do not*, or *say more about how the two pipelines share input* — and make small edits by hand where that is quicker than explaining. The document is the thing you are working on for a while; the code comes later.

What this buys you is that everything becomes explicit. An assumption held in the conversation is one you have to notice going past; the same assumption written into a document is one you can read, disagree with, and correct before anything is built on it. You are reviewing the model's understanding of the problem while it is still cheap to be wrong.

And it does more besides:

- **It flushes out design decisions early**, while changing them is still free. A plan someone has to write down is a plan whose gaps become visible.
- **It creates memory across sessions.** Conversations end, and `/clear` is something you should be doing often. A committed plan is what you point the next session at, and the one after that.
- **It keeps the ship pointed in the right direction.** Over days of work it is easy to drift a long way from what you set out to do. A document you revise deliberately makes drift visible.

Revise it as you learn — a plan is a working document, not a contract. What matters is that changing direction becomes an explicit edit rather than something that happens by accident across three sessions.

This is a different thing from the standing instructions in [Managing Context](managing-context.md). `AGENTS.md` says how work is done here, always. A plan document says what we are doing now, and gets archived when it is done. The `dunnlab-new-project` skill builds the pattern in: it writes `dev_docs/overview.md` before any code exists, and reviewing that document is a step in the workflow rather than an afterthought.

## Set gates you can check

An agent keeps going until something tells it to stop. If your stopping condition is *looks right*, it will stop at looks right — which is the failure mode this manual keeps returning to, because plausible-looking wrong output is exactly what these tools are good at producing.

So decide, before the work starts, how you will know each step succeeded and how you will know the whole thing is finished. **The clearer the verification loop, the better the results**, and the effect is larger than almost anything else you can change.

Three things make a gate worth having:

**State it before the work, not after.** A criterion you invent after seeing the output is a criterion you will bend to fit it. Written down in advance it is also something the agent can aim at and check itself against, which turns it from a review step into a target.

**Prefer something it can run.** A passing test, a script that completes, an expected row count, a figure that regenerates identically, a known-answer case that reproduces. Anything the agent can execute, it can iterate against without you in the loop — and it will, until the gate is green. A gate you have to eyeball only fires when you happen to look.

**Include a scientific check, not just a technical one.** A passing test suite means the code runs, not that the analysis is right. Add the checks you would apply to a colleague's result: does the row count survive the join, is the effect still there in a subsample, does the control behave as it should, does the number carry the units you expect.

Then apply gates at two scales. **Between steps**, a gate is what lets the next task start from something verified rather than something assumed — it is what makes small, testable steps more than an aspiration. **At the end**, an agreed definition of done is what stops the work drifting into indefinite polishing, or stopping three-quarters of the way with the last quarter uninspected.

{: .note }
Codex can make a durable objective explicit with its [`/goal` command](https://learn.chatgpt.com/use-cases/follow-goals). In Claude Code, state the same objective and gates in the prompt or plan and use [Auto mode](managing-security.md#auto-mode) for the run. Neither mechanism replaces a verifiable stopping condition; that is what makes unattended work reliable in either harness.

When you cannot state a gate for a piece of work, that is worth noticing rather than working around. Sometimes it means the task is genuinely exploratory and you should be in [plan mode](#separate-planning-from-building) asking questions rather than building. Sometimes it means you have not actually decided what you want yet.

## Then work in small, verified steps

Once you are building:

**Keep tasks small, and gated.** A change too large to read carefully was too large to ask for in one go — and each one should end at a check you named in advance.

**Let the agent run the code.** Do not copy error messages into the chat. Ask it to run the thing—it sees the full output, has the surrounding context, and can diagnose directly. Relaying fragments of a stack trace by hand is slower and loses information.

**Commit after each verified step**, and let the agent write the message. It will document the reasoning behind the change, which you would probably not have bothered to do.

**Then start fresh before the next task.** In Claude Code, `/clear` resets the conversation; in either harness, a new session avoids carrying three tasks' worth of dead ends into the next one.

**Know how to undo.** Git commits are the durable, cross-agent recovery mechanism. Claude Code also offers `/rewind`; other harness-local recovery features differ.

## Keep asking as you go

Gates tell you whether the thing you built works. They cannot tell you whether it was the right thing to build. That question has to be asked out loud, and it is worth asking often.

Stop periodically — before a large step, after finishing one, whenever something is taking longer than it should — and ask something open:

- *Are we on the right track?*
- *Is there a better way to do this?*
- *What have we learned so far?*
- *Do you see any other interesting patterns?*

These cost a few seconds and occasionally redirect a project. The agent has been reading your data and your code closely, often more closely than you have in the last hour, and it is holding context you are not. Asking is how you get at it.

*What have we learned so far?* earns its place particularly before `/clear`. It produces a summary you can fold into the plan document, which is how a session's findings outlive the session.

*Do you see any other interesting patterns?* is the one most likely to pay for the whole habit. It is the question that finds the thing you were not looking for — and, as [asking scientific questions](#ask-scientific-questions-not-just-technical-ones) argues, the thing you were not looking for is sometimes the result.

One caution. An agent asked *are we on the right track?* has a pull toward answering yes. If you want a real answer, make disagreement the easy reply: *what is the strongest argument that this approach is wrong?*, or *if you were reviewing this, what would you object to first?* You will get better information, and you will get it earlier.

## Keep the agent working for you

The goal is not to spend all day supervising an agent. It is to make the agent as autonomous as the work safely allows. A run that is going well may need little or no input for hours or even days while it implements the plan, runs analyses, checks intermediate results, and interprets what it finds.

Your attention should be reserved for the things only you can contribute: information the agent cannot access, consequential design decisions, scientific judgment, and expertise it does not already have. Clicking through routine permission requests, fetching files for it, and repeatedly answering questions that could have been settled in advance are signs that the workflow needs attention.

If many of your prompts merely grant permissions, revisit the [permission settings](managing-security.md). Allow the agent to do more where that is appropriate, but do not weaken protections that the environment genuinely needs. Change the environment instead: use a machine with fewer security concerns, work inside a sandbox or virtual machine, give the agent read-only access to raw data, or use the model's own sandboxing features. Design the workspace so that routine work is safe to authorize broadly and consequential actions remain constrained.

Frequent interruptions can also mean that the work was not planned far enough ahead. If the agent keeps asking you to make design decisions during implementation, return to the plan and make those decisions explicit. Before launching a large analysis, ask it to run a small end-to-end pilot. A pilot exposes missing inputs, ambiguous choices, permission problems, and unrealistic resource estimates while they are still cheap to fix.

Finally, put clear [gates](#set-gates-you-can-check) between the steps of the plan. Have the agent verify each stage before proceeding, so a silent problem does not travel downstream and become a much larger complication. Good planning, a representative pilot, and executable gates are what turn autonomy from wishful thinking into a reliable way of working.

## Manage multiple agents as a portfolio

Once your agents can work for long periods without you, you will naturally start running several sessions on different projects at once. Getting this right becomes one of the hardest parts of adopting AI extensively. It is a different scale and mode of work from most pre-AI workflows, and a few months into adoption it is often the problem people most want to compare notes about.

Parallel agents multiply execution, not your capacity for attention. You still have to hold the big picture, keep every project pointed in the right direction, review the work carefully, and sometimes edit or redo it. The paradox is that you may end up with more on your plate than before you had the help: far more work can move at once, but the parts that remain yours still require judgment and concentration.

Be realistic about the number of projects you can tend. For many people the practical limit is somewhere around two to six active projects, depending on their complexity and how much intervention they need. Beyond your limit, projects cannibalize one another: reviews get shallow, decisions wait, and work that was supposed to save attention creates a backlog of things requiring it.

Keep a simple document or sheet that puts every project into one well-defined state:

| State | Meaning |
|---|---|
| **Active** | Running now and worth checking regularly. |
| **Blocked** | Ready to be active but waiting for something not yet available, such as data from a collaborator or a few focused hours from you. |
| **Parked** | Previously active, but deliberately put on ice because the active set is full. |
| **To initiate** | Not started yet; a candidate to activate when capacity opens. |
| **Done** | Finished and no longer competing for attention. |

For each project, record the context you will need when you return:

| Record | What to include |
|---|---|
| **Objective** | The question or outcome the project is meant to address. |
| **Current step** | Where the project is in its plan and what is happening now. |
| **Agent and session** | The agent being used and the session name, link, or identifier needed to reopen it. |
| **Run location** | The computer, cluster, virtual machine, container, or terminal session where the agent or analysis is running. |
| **Working directory** | The exact path containing the files the agent is acting on. |
| **Repository** | The associated GitHub repository, branch, pull request, or other version-control context. |
| **Related context** | Relevant Slack channels, documents, data locations, issue trackers, or collaborators. |
| **Dependencies and blockers** | Anything the project needs before it can advance, and who or what it is waiting for. |
| **Most recent result** | The last meaningful and verified thing the project produced. |
| **Next action** | What should happen next, whether the agent can do it, and what input it needs from you. |

This may sound excessive until the first time those details are spread across several windows and machines.

That context matters because switching projects is not free. Each switch means finding the right windows, reconstructing what the project is about, remembering where it stopped, reviewing recent progress, deciding whether it needs you, and then recovering enough context to act well. A good tracker reduces this reorientation cost; limiting the active set reduces how often you pay it.

The tool itself matters less than the structure. I use a Google Doc. Other people use a spreadsheet, Obsidian or another task manager, or an agent-built dashboard that monitors runs in real time. Start with the simplest thing you will actually maintain and automate it only when the manual version becomes a burden.

If parallel work leaves you feeling scattered and fried, do not treat that as a personal failure or a reason to add another agent. Reduce the number of active projects, move the rest to parked, and make the state of each one explicit. Autonomy increases how much work can happen; it does not remove the need to choose how much work deserves your attention.

**And do not forget to touch grass.**
