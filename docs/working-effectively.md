---
title: Working Effectively
nav_order: 8
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

## Separate planning from building

Split the work into a planning phase and an implementation phase, deliberately, rather than letting them run together.

The reason is not tidiness. **A plan is where mistakes are cheap.** Once the agent starts building, it builds on whatever you told it, including the parts you got wrong — and by the time a bad assumption is visible in code it has already propagated through everything downstream. Reviewing a plan is your chance to check the details you supplied before anything is constructed on top of them.

In practice: start in plan mode, where Claude explores and proposes but does not edit. `Shift+Tab` cycles the permission modes, and the status bar shows where you are. Read the plan properly, argue with it, and only then let it work.

Most work settles into a rhythm of plan, execute, then back to plan for the next piece. The cycle is not symmetric — it runs Manual → Accept edits → Plan → Auto → Manual, so plan to auto is one press forward but auto back to plan is three. If you are starting a session anyway, `claude --permission-mode plan` puts you where you want to be.

## Commit the plan for anything large

For a project of any size, do not leave the plan in the conversation. **Have Claude write it as a markdown document, commit it, and iterate on it before building anything.**

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

When you cannot state a gate for a piece of work, that is worth noticing rather than working around. Sometimes it means the task is genuinely exploratory and you should be in [plan mode](#separate-planning-from-building) asking questions rather than building. Sometimes it means you have not actually decided what you want yet.

## Then work in small, verified steps

Once you are building:

**Keep tasks small, and gated.** A change too large to read carefully was too large to ask for in one go — and each one should end at a check you named in advance.

**Let Claude run the code.** Do not copy error messages into the chat. Ask it to run the thing — it sees the full output, has the surrounding context, and can diagnose directly. Relaying fragments of a stack trace by hand is slower and loses information.

**Commit after each verified step**, and let Claude write the message. It will document the reasoning behind the change, which you would probably not have bothered to do.

**Then `/clear` before the next task.** A conversation carrying three tasks' worth of dead ends makes everything after it worse.

**Know how to undo.** `/rewind` restores the conversation and the files to an earlier point in the session. Committing often is the more durable version of the same idea.
