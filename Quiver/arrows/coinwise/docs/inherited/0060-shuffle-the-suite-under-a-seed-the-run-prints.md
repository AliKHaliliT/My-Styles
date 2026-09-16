# 0060. Shuffle the suite under a seed the run prints

Status: Accepted
Date: 2026-09-16

## Context

The delivery gate's test-honesty item has said since it was written that
time, randomness, and order are controlled in the suites, and no
configuration in any seat made the order part true. Every runner executed
the suites in collection order, which is the same order every run, so a test
that leaned on a neighbour's side effect, a module-level cache warmed by an
earlier case, a fixture left dirty, an environment variable set and never
unset, would pass on every machine until an unrelated test was added ahead
of it. Treasury study 0005 found the countermeasure stated in the published
agent-skills ecosystem as a debugging step, run the suite in random order
under a recorded seed, and the family disposition, treasury 0030, Take eight
rules from the skills study and refuse the rest, adopted it as configuration,
because a sentence the tree already carried was not being enforced by
anything.

## Evidence

The sentence is in every code seat's gate and the property tests already
run derandomized by their own record, so the suites' randomness was
controlled while their order was not. No pyproject and no vitest
configuration in the family named an order, a seed, or a shuffle. The
python runner has no shuffle of its own and the ecosystem's plugin for it
reseeds the standard library's generator before each test and prints the
seed at the top of every run; the client runner shuffles natively and
prints its seed the same way. Both replay a run from the printed seed.

## Options considered

- A fixed seed in configuration. Refused, because a fixed seed is one more
  fixed order, and the point is that the order changes between runs while
  any single run can be replayed.
- A hand-written collection hook that shuffles under an environment
  variable. Refused, because it is code the family would then have to test
  and carry in three seats, where the plugin is one dependency line.
- Leaving the sentence as review's work. Refused under the enforcement
  ladder, which puts an unenforced sentence below a check whenever a check
  can decide the question, and this one can.
- Making the host seat's inquiry shuffle. Nothing to shuffle; the host
  carries no suite and its arrows run under their own styles.

## Decision

Every code seat's suite runs in a shuffled order under a seed the run
prints. The python seats add the shuffle plugin to their development
dependencies, with a comment beside the runner's configuration naming the
replay flag; the client seat turns on its runner's shuffle in its test
configuration with the same comment. The gate's test-honesty item names the
shuffle beside the sentence it enforces, so the guide says what the
configuration does. The rule lands as configuration, the second rung of the
ladder, because no type can make a hidden order dependency impossible and a
shuffled run decides the question on its own.

## Consequences

A test that depends on its neighbour now fails on some run soon after it is
written, with a seed in the log that reproduces the failure, instead of
passing for months and failing when a stranger's test lands ahead of it.
Every run's header carries one more line. The arrow's suite shuffles with
Keel's configuration. A child re-aligning receives the dependency and the
setting with its manifest.
