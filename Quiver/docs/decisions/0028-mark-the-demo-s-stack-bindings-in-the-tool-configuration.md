# 0028. Mark the demo's stack bindings in the tool configuration

Status: Accepted
Date: 2026-09-08

## Context

A project built from Keel had to delete three lines of the tool configuration
the adoption section calls law, the type checker's plugin for the demo's
validation library, the test runner's async mode, and the import contract's
ban on the demo's vendor SDK, because a child that uses none of them cannot
run the checks with them present, and it reported the deletions as a
departure it could not classify.

## Decision

Inside the tool configuration a line that binds the demo's own stack rather
than the style's rule is marked with a comment beginning Stack binding, and a
child re-adapts or removes such a line freely; everything unmarked is law.
The adoption section, shared by every style, says so. This host has no code
of its own, so the rule reaches it through the arrows, whose styles mark
their own bindings.

## Consequences

A child knows which configuration lines it may touch by reading them.
