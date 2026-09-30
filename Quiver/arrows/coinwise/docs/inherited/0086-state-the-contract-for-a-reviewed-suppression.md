# 0086. State the contract for a reviewed suppression

Status: Accepted
Date: 2026-09-30

## Context

The gating selection carries the security heuristics that fire at a call
site, the subprocess rules and the URL-opening rule among them, and the
configuration said only that a suppression names the exact code it
silences. The docs audit's own subprocess calls carry such a suppression
with the reason on the line above, which is the form, and nothing said so.
A project built from the host style with an arrow of this style asked
three times on 2026-09-18 what the contract was, whether the heuristic
should become advisory, whether a constructed argument list must be
rewritten as a literal, and whether a guarded URL opener may keep its
suppression, having read the records and found no ruling.

## Evidence

Measured on 2026-09-30 with ruff 0.16 under this seat's configuration. A
literal argument list to a subprocess call raises nothing; a list built
from a variable raises the subprocess rule and the partial-path rule at
the call, which is the shape the audit's git helper has and answers with
its suppression. The credential heuristics were moved to advice in record
0025's line because they read any suggestive string, everywhere; these
rules fire only where a process is started or a URL opened, a handful of
sites per project, each worth a written reason that outlives a commit
message.

## Options considered

- Making the rules advisory, as the credential heuristics are. Refused,
  because a suppression with its reason at the site is a stronger record
  than a dismissal in a commit message, and the sites are few.
- Requiring literal argument lists. Refused, since a helper that builds a
  command from fixed parts is the ordinary shape and the suppression at
  its one site is the review.
- Leaving the form to the exemplar. Refused, because a project read the
  bytes and still asked.

## Decision

The ruff configuration says, beside the selection, that the subprocess and
URL-opening heuristics stay in the gate, that a literal argument list
needs nothing, and that a call which builds its arguments or opens a
guarded URL earns a suppression naming the code with its reason beside it
at the reviewed site, the review written where the call is. The sentence
lands in the configuration because the tool configuration is law the
style carries, and the same sentence stands in the server seat and the
demo arrow.

## Consequences

A project meets the contract in the file that enforces it, and its
reviewed suppressions are the form rather than a question. A blanket
suppression stays refused by the rule already there.
