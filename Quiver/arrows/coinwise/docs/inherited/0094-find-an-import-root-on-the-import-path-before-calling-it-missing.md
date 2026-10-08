# 0094. Find an import root on the import path before calling it missing

Status: Accepted
Date: 2026-10-08

## Context

The docs audit holds the import graph the Dependency Rule contract
runs over to the modules on disk, so a contract reporting KEPT over a
partial graph cannot pass as a verdict. To find the modules on disk it
takes each root the import-linter configuration names and looks for
its directory under `src/` or at the top of the tree, and a root found
in neither place fails as named as an import-linter root with no
directory matching it. A project that embeds an installed package and
wants a contract holding it to that package's public names must list
the package's portions as roots, because the graph squashes an
external package to one node, and the audit then refused every one of
those roots. A project built from a host style with an arrow of the
server seat, which carries this audit byte for byte, reported it on
2026-10-07. A forbidden contract naming the embedded engine as one root
had stayed green under a planted deep import, listing the engine's
five layers as roots made the contract catch the plant, and the audit
then failed the project with five findings.

## Evidence

Measured on 2026-10-08. The check reads each root's directory under
`src/` or the tree's top and nowhere else, and the graph it builds
first already stops on a root the import path cannot find, so the
finding named above fires only for a root the graph could build and
the tree does not hold, which is exactly an installed one. The selftest
had no plant for either case and said so on every run.

## Options considered

- Looking a root up with `importlib.util.find_spec`, as the project
  proposed. Refused in that form, because finding a dotted name imports
  its parents and the audit parses rather than executes; the path
  finder resolves the top package without importing anything, and the
  rest of the dotted path is a directory under it.
- Comparing coverage over in-tree roots alone, as the project also
  proposed. Refused, because the graph builds an installed root whole
  and its modules on disk are as countable as the tree's, so the
  comparison holds them to the same rule.
- Dropping the finding. Refused, because a root the graph could build
  with no directory anywhere is still a root the check cannot count,
  and saying so is what keeps the coverage honest.

## Decision

A root with no directory under `src/` or the tree's top is looked up
on the import path through the path finder on its top name, which
imports nothing, and its directory under the location found is read
like an in-tree root's, so its modules on disk join the coverage
comparison. A root found in neither place is reported as found
nowhere. The selftest plants the graph library itself as a root, which
must pass, beside a root found nowhere, which must stop the build.

## Consequences

A contract may hold an embedded package to its public names by naming
the package's portions as roots, and the audit reads those roots where
the interpreter would. The coverage rule is unchanged in what it
decides.
