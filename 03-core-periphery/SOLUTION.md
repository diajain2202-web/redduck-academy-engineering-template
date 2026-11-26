# Solution

## Language

<!-- Keep only the language you completed. Delete the others so a single value is left, e.g. language: "python" -->
language: "typescript"

## What was the problem

The store held each user's password hash, but the original convenience lookup returned the
entire user record. The report used that lookup, so both a direct lookup caller and anyone who
could request a report received hashes alongside usernames and roles.

## The split

The core is `UserStore`: it retains the records in a JavaScript `#users` private field, verifies
passwords, lists usernames, and returns a fresh public profile containing only the username and
role. The report is periphery: `reportUsers` depends only on the `UserDirectory` interface and
builds its rows by looking up those hash-free profiles. It never receives or processes a user
record.

## Removal versus guarding

This removes the path to the hash rather than guarding it. No method returns a complete record,
and the periphery has no access to the private field; `#users` also prevents callers from
reaching it through the store instance at runtime. There is no report-specific permission check
or conditional to bypass: the hash is absent from every value the core exposes.
