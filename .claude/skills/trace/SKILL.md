---
name: trace
description: Diagnose an ambiguous result or failure using competing explanations and evidence. Use when the cause is unclear; continue through correction when a fix was requested.
disable-model-invocation: true
argument-hint: "<observation, symptom, or why-question>"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Task"]
---

Apply `protocols/skills/trace.md` to `$ARGUMENTS`. When independent diagnosis
adds value, launch one `tracer` with a self-contained brief naming the
observation, relevant files, changes, and checks already run, without supplying
a conclusion. Have it read the shared protocol and return findings. The main
agent carries any requested fix through completion after the diagnosis.
