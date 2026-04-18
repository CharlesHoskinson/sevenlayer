---
title: "Compact's Disclosure Analysis"
slug: ch03-compact-s-disclosure-analysis
chapter: 3
chapter_title: "Choreographing the Act"
heading_level: 2
source_lines: [1108, 1161]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 576
---

## Compact's Disclosure Analysis

Compact, Midnight's smart contract language, takes a fundamentally different approach to the bug problem. Rather than giving developers direct access to constraints and hoping they get it right, Compact's compiler enforces a *disclosure rule*: witness values are private by default, and any attempt to use a private value in a public context without explicit consent is a compile-time error.

This is not a style guide. It is not a best practice recommendation. It is a hard compiler rejection.

Here is how it works. In Compact, private data enters the circuit through *witness* functions -- declared in Compact, implemented in TypeScript:

```typescript
witness get_secret(): Bytes<32>;
```

The implementation runs off-chain, in the user's browser or node:

```javascript
const witnesses = {
  get_secret: (ctx) => [ctx.privateState, hexToBytes("aabb...")]
};
```

The witness value is private. It exists only on the user's device. To use it inside a circuit -- where it will be constrained and proven -- the developer must explicitly call `disclose()`:

```typescript
export circuit verify(): [] {
  const sk = disclose(get_secret());
  const my_hash = persistentHash([pad(32, "auth:"), sk]);
  assert(my_hash == stored_hash, "not authorized");
}
```

Without `disclose()`, the compiler rejects the program. The error message traces the complete path from the witness value to the public surface:

```
potential witness-value disclosure must be declared but is not:
  witness value potentially disclosed:
    the return value of witness get_amount at line 8 char 1
  nature of the disclosure:
    ledger operation might disclose the witness value
  via this path through the program:
    the argument to increment at line 11 char 8
```

The compiler catches three categories of accidental leakage: witness values used in ledger operations (writing to on-chain state), witness values returned from circuits (visible in the proof's public outputs), and witness values passed to kernel operations (token transfers, balance queries).

The disclosure analysis pass runs as part of the 26-stage nanopass compilation pipeline, at the `Lnodisclose` intermediate language stage. The privacy boundary is verified before any code generation occurs. The compiler has already type-checked the program, analyzed data flow paths, and confirmed that every potential disclosure is explicitly marked -- or the compilation fails.

Consider a concrete case. The Midnight developer guide documents that the first attempt at implementing a private voting contract -- using naive if/else branching on witness values -- was rejected by the compiler with 11 disclosure errors. Each error traced the path from a witness value to a public surface. The compiler forced a fundamental redesign: Merkle trees replaced per-slot branching, nullifiers replaced voted-flags, and arithmetic tallying replaced conditional increments. The resulting design was not just compiler-compliant -- it was architecturally superior. The naive approach would have leaked which candidate each voter chose through the pattern of ledger writes. The compiler-forced redesign made this impossible.

No other ZK language provides this guarantee. In Circom, Noir, and Cairo, privacy depends on the developer correctly managing which values are public and which are private. A mistake does not produce a compiler error. It produces a privacy leak that may not be discovered until an attacker exploits it. Compact makes privacy a compiler guarantee rather than a developer responsibility.

The tradeoff is clear: Compact contracts are locked to Midnight's proof system (PLONK on BLS12-381), token model (Zswap), and ledger architecture. They cannot be deployed on another chain. In exchange, the developer gets something no general-purpose approach can offer: the compiler will not let you accidentally show the audience what is behind the curtain.

---


## Summary

Compact's disclosure analysis rejects at compile time any program where a witness value reaches a public surface without an explicit `disclose()` call, making privacy a compiler guarantee rather than a developer responsibility. No other ZK language provides this guarantee; the tradeoff is lock-in to Midnight's PLONK-on-BLS12-381 stack and Zswap token model.

## Key claims

- Witness values are private by default; `disclose()` is the explicit consent mechanism, not a prohibition.
- The `Lnodisclose` pass runs before any code generation; compilation fails if any undeclared disclosure path exists.
- Three leakage categories caught: ledger operations, circuit return values, kernel operations (token transfers, balance queries).
- A naive private voting contract generated 11 disclosure errors; compiler-forced redesign (Merkle trees + nullifiers) was architecturally superior.
- No other ZK language (Circom, Noir, Cairo) provides compile-time privacy guarantees.
- Lock-in: PLONK on BLS12-381, Zswap token model, Midnight ledger only.

## Entities

- [[bls12-381]]
- [[midnight]]
- [[plonk]]

## Dependencies

- [[ch03-under-constrained-circuits-the-dominant-failure-mode]] — the failure mode this approach addresses
- [[ch03-the-four-philosophies]] — positions Compact within Philosophy D
- [[ch03-midnight-compiler-ir-circuit]] — full 26-pass pipeline and three-artifact output this analysis feeds into
- [[ch04-the-disclose-boundary-midnight-s-witness-architecture]] — Layer 3 view of the same disclose boundary

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P2] (B) "The Midnight developer guide documents that the first attempt at implementing a private voting contract…was rejected with 11 disclosure errors" — attributed to "the Midnight developer guide" but no URL, version, or section is given. Should link or date the source.
- [P2] (B) No citations in "Sources cited" despite specific implementation details (26-pass pipeline, three leakage categories, 11-error voting contract redesign). These are Compact-specific engineering claims that should trace to documentation or a technical paper.
- [P2] (A) The code example uses `disclose(get_balance())` and assigns to `my_balance`, but the preceding prose says "The `disclose()` call is the developer's explicit declaration: 'I acknowledge that this private value will influence public state.'" The explanation conflates two distinct functions of `disclose()`: making the value available inside the circuit (constrained) vs acknowledging that it influences *public* state. Compact's disclosure analysis catches the latter; the former is automatic for any circuit input. The distinction should be tightened.
- [P3] (D) The section's claim that "no other ZK language provides this guarantee" is unqualified. Leo's record model provides a structural (if less granular) privacy guarantee. The comparison should acknowledge that Leo's approach is different but not entirely without compiler-enforced bounds.
- [P3] (E) The section ends abruptly after the tradeoff paragraph. A brief note on whether disclosure analysis catches *over*-constraining (revealing more than necessary) as well as under-constraining would complete the picture.

## Links

- Up: [[03-choreographing-the-act]]
- Prev: [[ch03-under-constrained-circuits-the-dominant-failure-mode]]
- Next: [[ch03-midnight-compiler-ir-circuit]]
