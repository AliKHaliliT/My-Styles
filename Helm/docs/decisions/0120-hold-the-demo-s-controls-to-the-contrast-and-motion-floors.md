# 0120. Hold the demo's controls to the contrast and motion floors

Status: Accepted
Date: 2026-11-06

## Context

A design linter run over the demo at the desk on 2026-11-06, over the
source and in a browser at every width, found three defects on the
login screen and nothing else above its floor. The buttons' focus ring
stood at 1.16:1 against what lay behind it, because the button declared
no focus style and left the ring to the browser. The fields' edge stood
at 1.32:1 against the surface, because it was drawn with the line
token, which is tuned for dividers. The spinner kept turning for a
reader who had asked for reduced motion. The accessibility guideline
holds a control's edge and a focus indicator to 3:1 and text to 4.5:1.
Measured over the token file, every text token clears 4.5:1 against the
surface and the card in both themes, and the line token clears neither
floor, as a divider need not.

## Options considered

- Adopt the linter into the gate. Refused, because the tool is young
  and churning, retires and renumbers its gates, and its floor mixes
  the guideline with one studio's taste. It reopens when the tool has a
  stable release, or when an established checker covers the same
  defects.
- Darken the line token to the floor. Refused, because that token draws
  every divider and card edge, which the guideline holds to no floor,
  and the whole page would gain weight to fix one control.
- Hold the floors by review in the ledger. Refused, because the floors
  are arithmetic over the token file, which a test decides.

## Decision

The button declares its focus ring, two pixels of the ink token offset
from its edge, so the ring reads against the surface or the card at
13:1 or more in either theme. The token file gains an edge token for
the border of a control, cleared at 3.5:1 or more against the surface
and the card in both themes, and the field draws its border with it;
the line token keeps the dividers. The spinner stands still under
reduced motion, its ring still drawn.

A test over the token file holds the floors, text at 4.5:1 and the edge
at 3:1 against both backgrounds in both themes, with its expectation
taken from the guideline and not from the file, and proven by two
mutations, the edge set to the line's value and a text token set to it.
The ledger carries the row.

## Consequences

A control is found by keyboard in either theme, a field's edge is seen,
a reader who asked for stillness gets it, and a token that drifts below
a floor fails the suite before it ships. The linter that found the
defects stays outside the tree.
