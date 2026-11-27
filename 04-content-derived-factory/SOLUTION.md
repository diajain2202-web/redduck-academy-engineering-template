# Solution

## Language

<!-- Keep only the language you completed. Delete the others so a single value is left, e.g. language: "python" -->
language: "python"

## Why derive the identifier from content

The identifier is a SHA-256 digest of a canonical JSON encoding of the content: keys are sorted
and serialization separators are fixed, so the same fields and values produce the same bytes
regardless of dictionary insertion order. Anyone with the content can independently recompute
and compare the digest; no registry operator or mutable name-to-content mapping has to be trusted
to tell them which identifier belongs to the item. This provides a collision-resistant integrity
check, not proof of who created the content.

## What changes when the content changes

Changing a field changes the canonical bytes and, for practical purposes, produces a different
digest, so a recipient can detect that content was substituted by recomputing and comparing the
identifier. This is a feature for integrity, but it means an identifier names one particular
version of the content: edits create a new identifier instead of preserving the old one.
