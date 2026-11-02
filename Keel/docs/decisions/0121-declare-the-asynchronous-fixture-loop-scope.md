# 0121. Declare the asynchronous fixture loop scope

Status: Accepted
Date: 2026-11-02

## Context

The suites run asynchronous tests in the plugin's automatic mode and
turn every warning into an error, so a warning a dependency adds is a
failure the day it ships. The plugin that runs them began warning at
configuration while the default loop scope of asynchronous fixtures is
left unset, and under the error setting that warning stops collection
before a single test runs. A fresh install from the development
requirements today brought that plugin, and both Python seats' suites
stopped at configuration, as a project built from the server style found
first.

## Options considered

- Let the warning through for that one option. Refused, because a filter
  that admits one warning is the start of a list, and the suite's rule
  is that a warning is an error.
- Pin the plugin below the warning. Refused, because a floor on a tool
  is named for a behavior the suite needs, and here the suite needs
  nothing the old version had.

## Decision

The test configuration of the two Python seats declares the default loop
scope of asynchronous fixtures as function, with the sentence that says
why. A fixture gets a loop of its own test, which is the isolation the
suites already assume. The arrow carries no asynchronous configuration
and stays as it is.

## Consequences

A fresh install runs the suites again, and the isolation the suites
assumed is written where the plugin reads it.
