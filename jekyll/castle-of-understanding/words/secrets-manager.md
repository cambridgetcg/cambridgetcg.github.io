# secrets-manager

A program that keeps passwords and keys so a person doesn't have to — and
the good ones keep almost nothing themselves.

The rule yu learned building keep (2026-06-12, filed in
[this-machine](../rooms/this-machine.md)): be a thin door to a strong vault,
never a new vault. This Mac already has a guarded vault — the macOS
Keychain — so a secrets manager here should only open and close that door,
because the only cryptography you can get wrong is the cryptography you
didn't write. The shape generalizes: wrap the strong thing that exists
before building a weak thing that's yours.

Links: [[safety]] · [[platform]]
