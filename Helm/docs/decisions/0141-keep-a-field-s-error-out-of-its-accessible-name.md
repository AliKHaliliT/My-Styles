# 0141. Keep a field's error out of its accessible name

Status: Accepted
Date: 2026-11-25

## Context

The kit's text field put its validation message inside the label that
wraps its input, so while the message showed it joined the input's
accessible name. A project built from this style reported it after
adding a field with a line of guidance under its label, where the
guidance would have joined the name the same way. A screen reader reads
a field's name each time the field takes focus, so the message was read
as if it were the label, and a suite that finds fields by their labels
lost a field once it showed an error.

## Evidence

Run on 2026-11-25 at 05a5f80. A test rendered the template's text field
with the label Name and the message "Name the search.", found its input
named "Name Name the search.", and found nothing by the label Name. The
template's kit has no select field, which the reporting project built
itself. The style's record that holds the demo's controls to the
contrast and motion floors says nothing of a field's name, and the
template's suites find a field by its label only while it shows no
message.

## Options considered

- Hiding the message from assistive technology. Refused, because the
  message is the reason a value was refused, and it belongs where a
  reader of the field meets it, after the name.
- Keeping the wrapping label and naming the input from the label's text
  by id. Refused, because a label tied to its input by the input's id is
  the plain form, and it leaves no message inside the name to work
  around.

## Decision

The label is tied to the input by the input's id, a caller's id where
one is given and a generated one otherwise, the message sits after the
input with an id of its own that the input names as its description, and
the input is marked invalid while the message shows. Four cases join a
suite of the field's own, and the ledger gains the claim. Seven breaks,
each one point, each failed a case, the message back inside the label,
the label untied from the input, the description dropped, the message's
own id dropped, the invalid mark dropped, the invalid mark kept with no
message showing, and the caller's id ignored.

## Consequences

A field's name stays its label in every state, a screen reader reads the
message as the field's description, and a suite finds a field by its
label whether or not it shows an error.
