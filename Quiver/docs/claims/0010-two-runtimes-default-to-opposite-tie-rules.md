# 0010. Two runtimes default to opposite tie rules

Status: Supported
Date: 2026-09-29

## Claim

The Python decimal module's default context rounds a tie to the even
neighbour, the ECMAScript number formatter rounds a tie away from zero by
default, and Java's rounding-mode reference defaults to neither while naming
half even as the mode that minimizes cumulative error and half up as the one
taught at school. A ledger that inherits its runtime's default has therefore
chosen a tie rule without deciding one. It must convince a maintainer who
assumes the default is the same everywhere.

## Evidence

Read evidence, quoted from the works the pass of 2026-09-29 read in full,
with no pin, since no tree produced it.

The Python documentation states the default context [psf2026]: "The default
values are Context.prec = 28, Context.rounding = ROUND_HALF_EVEN, and
enabled traps for Overflow, InvalidOperation, and DivisionByZero." It
defines the two half modes as "ROUND_HALF_EVEN Round to nearest with ties
going to nearest even integer" and "ROUND_HALF_UP Round to nearest with ties
going away from zero".

The ECMA-402 specification reads the number formatter's option with a
default [ecma402-2026]: "Let roundingMode be ? GetOption(options,
"roundingMode", string, « "ceil", "floor", "expand", "trunc", "halfCeil",
"halfFloor", "halfExpand", "halfTrunc", "halfEven" », "halfExpand")", and
its table of modes glosses "halfExpand" as "Ties away from zero".

The Java reference defines HALF_UP as "Rounding mode to round towards
"nearest neighbor" unless both neighbors are equidistant, in which case
round up" and adds "Note that this is the rounding mode commonly taught at
school. This mode corresponds to the IEEE 754 rounding-direction attribute
roundTiesToAway"; it defines HALF_EVEN as "Rounding mode to round towards
the "nearest neighbor" unless both neighbors are equidistant, in which case,
round towards the even neighbor" and notes "This is the rounding mode that
statistically minimizes cumulative error when applied repeatedly over a
sequence of calculations. It is sometimes known as "Banker's rounding," and
is chiefly used in the USA" [oracle2023]. The reference names no default
among its modes.

## Threats

- Selection. Three runtimes chosen by the writer, not a census, so the
  disagreement is shown by example; a fourth runtime changes the count and
  not the claim, which rests on two defaults that differ.
- Category. The ECMAScript default governs a formatter for display, not an
  arithmetic type, so a reader may hold that display and ledger arithmetic
  are different questions; conceded, and the claim says formatter.
- Currency. Two of the works are living documentation and one is a draft
  specification, read on 2026-09-29; a later edition may move a default, and
  the pass record dates what was read.
