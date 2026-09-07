# 0019. Read a key in backticks as a mention and let plants build what they name

Status: Accepted
Date: 2026-09-07

## Context

A project built from this template, an inquiry with three arrows, reported
two things about the audit. The rulebook's bibliography rule and record 0010
both write the example key `[ieee754-2019]` inside backticks, and the
citation check read every living document and every record with a pattern
blind to code spans, so a child had to enter IEEE 754 in its bibliography to
make the check pass, an entry recording what the template's example sentence
consulted rather than what the inquiry did. The template never saw it,
because the demo cites the standard for a real reason. Second, two selftest
plants named the demo. The manifest-currency plant pinned a claim to
`arrows/coinwise` and needed that arrow and its manifest to exist, and the
well-formed review pass cited a key only the demo's bibliography holds. In a
child both plants were inert, and the selftest reported two rules not
working over an audit that was green.

## Decision

A key inside backticks is a mention of the form, not a citation. The audit
blanks code spans before reading citations, the rulebook's bibliography rule
says so, and a legal plant proves that a record explaining the form passes
while the bare unknown key still fires.

A plant builds whatever it names. The manifest-currency plant creates a
temporary arrow directory and manifest for its one run, the review plants
plant a bibliography entry and restore the file's bytes afterwards, and no
plant names anything the tree happens to carry, so the selftest proves every
rule in a project that carries none of the demo. The two advisory plants
that read history still skip with a printed notice where no arrow has moved,
because history cannot be planted without a commit.

## Options considered

- Excluding style-owned files from citation resolution was refused. The
  audit has no way to know which records a child inherited, and a real
  citation in those files would go unchecked.
- Changing the rulebook's example to a key no bibliography would hold was
  refused, because it fixes one sentence and leaves every future backticked
  mention counting as a citation.
- Deriving plant names from the tree, the first arrow found and the first
  key entered, was refused. A fresh child has neither, so the proof would
  skip exactly where it is needed most.

## Consequences

A child's bibliography records what the inquiry consulted and nothing else.
The selftest's closing line means the same thing in every tree. Both
findings were the template mistaking its demo for the world, the bias the
adopting section names, and each is now a mechanical negative rather than a
warning in prose.
