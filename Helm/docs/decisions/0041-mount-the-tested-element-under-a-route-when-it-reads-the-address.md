# 0041. Mount the tested element under a route when it reads the address

Status: Accepted
Date: 2026-09-07

## Context

A project's pages read identifiers out of the address and validated what
they read before rendering, which is worth a test, and the render helper
wrapped the element under test in a bare memory router with no routes, so a
component reading route parameters saw nothing. The template's own vessel
detail page reads its id from the address and had no test at all. The
template shipped a page its own helper could not mount, and nothing showed
it.

## Decision

`renderWithProviders` takes optional `path` and `at`. With a path, the
element is mounted under a `Route` inside `Routes` and the router starts at
the given address, so the component reads its parameters the way the app's
router hands them over; without one, it renders bare as before, so every
existing call is unchanged and the router stays at the seam where it
belongs. The vessel detail page gains its suite, mounted at an address: a
real id renders the record, an address without an id is refused, and an
unknown id shows the backend's reason.

## Options considered

- Exporting the page's body as a prop-taking component and testing that was
  refused, because it moves a structural decision into a test's convenience
  and tests something other than the page.
- Mounting the whole application router in page tests was refused, because
  it drags the layout and the auth guard into every page suite.

## Consequences

Pages are tested as pages. The helper documents both of its modes, and
addresses are read in one place.
