---
title: "The Four Philosophies"
slug: ch03-the-four-philosophies
chapter: 3
chapter_title: "Choreographing the Act"
heading_level: 2
source_lines: [808, 1024]
source_commit: 53f41415d307dcd4ed73d852dfd6aa97146e882f
status: reviewed
word_count: 3720
---

## The Four Philosophies

Every approach to Layer 2 answers the same question differently: how should a developer express a computation that will be proven in zero knowledge?

Four distinct philosophies have emerged. Each makes a different bet about what matters most.

**Philosophy A: EVM-Compatible.** Prove the Ethereum Virtual Machine itself. The developer writes Solidity, the same language used for ordinary Ethereum smart contracts. The proof system executes the EVM bytecode and proves that execution was correct. The advantage is obvious: every existing Ethereum application "just works." The Solidity ecosystem -- its tooling, its auditors, its libraries, its millions of lines of battle-tested code -- transfers wholesale.

The leading examples are Scroll, with $748 million in total value locked as of early 2026, and Linea (ConsenSys), with over $2 billion. Both prove EVM execution using different strategies: Scroll uses a custom zkEVM circuit, while Linea has been converging toward a RISC-V backend with EVM compatibility layered on top.

The disadvantage is equally obvious: the EVM was not designed for proving. It has 256-bit arithmetic (proof systems prefer 31-bit or 64-bit fields). It has dynamic gas metering. It has a complex memory model. Proving every quirk of the EVM is computationally expensive -- like translating a novel into a language that has no word for half the concepts.

The cost of faithful reproduction has a concrete data point. Polygon acquired Hermez, the team behind one of the most ambitious zkEVM implementations, for approximately $250 million (Polygon, "Polygon Acquires Hermez Network," August 2021). The project aimed to prove every Ethereum opcode at the circuit level. It was technically impressive. It was also, in the end, commercially unviable. In 2025, Polygon announced the sunsetting of zkEVM Mainnet Beta. The Hermez team, led by co-founder Jordi Baylina (who also co-created Circom), spun off to form ZisK -- and pivoted to RISC-V. The person who knew more about EVM-compatible ZK proving than almost anyone else alive concluded that the direct approach was not the path forward.

The lesson is not that EVM compatibility is wrong. Scroll and Linea are thriving -- Scroll uses a custom zkEVM circuit that abstracts away the most expensive opcodes, while Linea has been converging toward a RISC-V backend with EVM compatibility layered on top. The lesson is that *how* you achieve compatibility matters enormously. A $250 million investment with a world-class team is not sufficient if the architectural approach creates an exponential constraint-generation problem. Abstract where you can. Approximate where you must. And keep one eye on the RISC-V projects that may make your compatibility layer unnecessary.

**Philosophy B: ZK-Native ISA.** Design a new instruction set from scratch, optimized for proving. The developer learns a new language, but every instruction translates efficiently into polynomial constraints. Cairo is the canonical example. Its instruction set was co-designed with StarkWare's STARK proof system. Layer 2 was literally shaped by Layer 4 -- the language exists *because* of the arithmetization.

Cairo works over the Stark prime -- $p = 2^{251} + 17 \cdot 2^{192} + 1$ -- a 252-bit field sized for elliptic-curve scalars. Its execution trace model, with columns for program counter, flags, and operands, and polynomial constraints between adjacent rows, became the template for every subsequent zkVM. The small-field successors -- Goldilocks (Plonky2, Plonky3, RISC Zero), BabyBear (SP1), M31 (Stwo) -- inherited the trace model but replaced the large prime with a word-sized one so that multiplication maps onto native CPU instructions. Cairo bet on algebraic efficiency over developer familiarity, and for the Starknet ecosystem, that bet paid off: it is the most battle-tested ZK system after Circom, handling real assets on mainnet since 2020.

The cost is ecosystem isolation. Cairo programs do not run anywhere except Starknet. The tooling, libraries, and developer community are Cairo-specific. Every line of code is a bet on one ecosystem. But that bet has paid returns: Starknet processes real assets, real DeFi, real NFTs. Cairo is not a research project. It is production infrastructure.

The evolution from Cairo 0 to Cairo 1.0 is itself instructive. The original Cairo was barely recognizable as a programming language -- it looked more like assembly with syntactic sugar. Cairo 1.0 aligned with mainstream language features: Rust-like syntax, a borrow checker, generic types. The lesson for the field: even a language designed for proof efficiency eventually converges toward familiar developer ergonomics, because adoption requires accessibility.

**Philosophy C: General-Purpose ISA.** Prove a standard processor. RISC-V has won this category so decisively that it is no longer a competition. SP1 (Succinct), RISC Zero, Airbender (ZKsync), ZisK, Jolt, and Pico Prism all target RISC-V.

Why RISC-V and not some other instruction set? Three properties converged. First, RISC-V is an open standard with no licensing fees -- any team can build a zkVM around it without negotiating with a chip vendor. Second, the RISC-V instruction set is small and regular: roughly 40 base instructions, each with a predictable structure, which makes the arithmetization (the process of encoding each instruction as polynomial constraints) manageable. Contrast this with x86, whose instruction set has thousands of opcodes with variable-length encoding. Third, and most importantly, the existing compiler infrastructure already targets RISC-V. The LLVM backend, GCC, and the Rust compiler all produce RISC-V machine code. This means the developer writes standard Rust, C, or C++, the compiler produces RISC-V machine code, the zkVM executes that code, and the proof system proves the execution. Standard toolchains, standard debuggers, standard testing frameworks. The ZK-specific complexity hides entirely behind the compilation boundary.

The architectural insight is worth stating explicitly: instead of designing constraints around a custom instruction set (as Cairo does), Philosophy C proves a standard processor and lets decades of compiler engineering handle the optimization. Cairo aligns its ISA with the algebraic structure of the proof system -- every instruction maps cleanly to polynomial constraints -- which minimizes the proving overhead per instruction. RISC-V does not have this alignment. A RISC-V multiply instruction produces more constraints than a Cairo multiply. But the tradeoff is ecosystem reach: Cairo requires learning Cairo. RISC-V requires learning nothing new. For a field where the developer talent pool is measured in thousands, not millions, this tradeoff has decisively favored RISC-V.

Airbender, ZKsync's RISC-V prover, illustrates the performance frontier: 21.8 million RISC-V cycles proven per second on a single NVIDIA H100 GPU (ZKsync, "Airbender: GPU-Accelerated RISC-V Proving," June 2025). For context, a typical Ethereum block involves roughly 100-400 million cycles, meaning a single GPU can prove a block in 5-20 seconds. Even projects that started with EVM compatibility are converging on RISC-V. ZKsync's Airbender proves RISC-V execution and layers EVM compatibility on top. The trend is clear: RISC-V is the assembly language of the zero-knowledge world.

**Philosophy D: Application-Specific DSL.** This is the philosophy that does not fit the evolutionary narrative. Instead of proving a processor, these languages prove *state transitions*. Instead of hiding ZK complexity behind a compilation boundary, they make privacy a first-class language concept.

Three languages define this category.

*Compact* (Midnight/IOG) is a TypeScript-like language for privacy-preserving smart contracts. Its compiler produces three artifacts from a single source file: a ZKIR circuit (the constraint system), TypeScript bindings (the application interface), and proving keys (the cryptographic setup material). No other ZK language generates all three from one source. More importantly, Compact's compiler includes a *disclosure analysis* pass that statically rejects any program where a private value might leak to a public surface without explicit developer consent. We will return to this in detail.

*Noir* (Aztec Labs) is a Rust-inspired, backend-agnostic ZK language. It compiles to an Abstract Circuit Intermediate Representation (ACIR). Noir does not target a specific proof system -- it targets multiple backends. This makes it the closest thing the ZK world has to a "write once, prove anywhere" language.

Noir's 1.0 release landed in late 2025 as the language's first stable version. It became an officially recognized language on GitHub. NoirCon conferences have been held (NoirCon0 in November 2024). The ecosystem includes over 600 projects and 900 GitHub stars. Key adopters include zkEmail, zkPassport, and zkLogin. Aztec's Ignition Chain launched in November 2025 as a decentralized L2 on Ethereum, with 185+ operators across five continents and thousands of sequencers -- and its core cryptography was written in Noir (Aztec Network, "Aztec Ignition Chain Update," 2025).

Noir breaks the three-philosophy taxonomy because it is neither ISA-based nor chain-specific: it is a universal circuit language. Its privacy model is annotation-based -- all inputs are private unless explicitly declared `pub` -- but it lacks the compile-time disclosure analysis that Compact provides. The developer bears responsibility for correctly managing the public/private boundary. In exchange, Noir programs can target any proving backend that accepts ACIR, making them portable across proof systems in a way that no other ZK language achieves.

*Leo* (Aleo) is a privacy-first language for the Aleo blockchain, with syntax borrowing from Rust and TypeScript. Leo targets Aleo's record-based (UTXO-like -- a UTXO, or Unspent Transaction Output, is a model where each digital coin is a discrete object created by one transaction and consumed by another, like physical bills in a wallet) privacy model and includes hooks for formal verification. With over 400,000 CLI downloads, Leo represents the privacy-specialized variant of the application DSL approach.

To understand why these three languages matter -- why they are not merely syntactic alternatives to writing Rust and compiling to RISC-V -- you need to see what development actually looks like in each one. The differences are not cosmetic. They are structural. Each language imposes a different mental model on the developer, and that mental model determines what classes of bug are possible, what classes of privacy leak are preventable, and what the compiler can guarantee before a single proof is generated.

### Compact: Privacy by Compilation

Consider a simple scenario: a private token transfer. The sender wants to prove they have sufficient balance without revealing what that balance is. In Compact, the developer writes something that looks, at first glance, like an ordinary TypeScript function:

```typescript
export circuit transfer(
  recipient: Bytes<32>,
  amount: Unsigned Integer
): [] {
  const my_balance = disclose(get_balance());
  assert(my_balance >= amount, "insufficient funds");

  const new_sender_balance = my_balance - amount;
  const new_recipient_balance = get_recipient_balance(recipient) + amount;

  ledger.sender_balances[sender()] = new_sender_balance;
  ledger.recipient_balances[recipient] = new_recipient_balance;
}
```

The keyword `circuit` is the first departure from ordinary programming. This function will not execute on a server. It will be compiled into a zero-knowledge circuit -- a set of polynomial constraints that a prover can satisfy and a verifier can check. Every variable inside this function will become a wire in that circuit. Every operation will become a gate.

The keyword `disclose` is the second departure, and the more consequential one. The function `get_balance()` is a witness function -- it retrieves the sender's private balance from off-chain storage. That value is, by default, not available inside the circuit at all. The `disclose()` call makes it available as a circuit input -- it is the developer's explicit declaration: "I acknowledge that this witness value will enter the constraint system and may thereby influence public state." Without it, the compiler rejects any program that tries to use the witness value within a circuit. Not at runtime. Not during testing. At compile time, before any proof is generated, before any key material is created, before any circuit is emitted.

The practical consequence is that a developer cannot accidentally write a transfer function that leaks the sender's balance. They can intentionally bring a witness value into scope -- `disclose()` is an explicit consent mechanism, not a prohibition. But the accidental case, which accounts for the majority of real-world privacy bugs, is eliminated by the compiler's disclosure analysis pass.

The compilation itself is worth understanding. Compact's 26-pass nanopass pipeline transforms the source through a sequence of increasingly specialized intermediate languages. The program begins as `Lsrc` -- essentially the developer's TypeScript-like code. It passes through type inference (`Ltypes`), where the compiler determines the bit-width of every value. It passes through disclosure analysis (`Lnodisclose`), where the compiler traces every data-flow path from witness inputs to public outputs. It passes through loop unrolling (`Lunrolled`), where bounded loops are expanded into straight-line code -- necessary because ZK circuits have no concept of iteration. It passes through circuit flattening (`Lflattened`), where nested expressions are decomposed into individual gates. And it emerges as ZKIR: a JSON-formatted circuit description ready for the proof system.

At no point does the developer interact with constraints, gates, or polynomials. The entire mathematical substrate is hidden behind the compilation boundary. The developer writes TypeScript-like code. The compiler produces a zero-knowledge circuit. The gap between intent and implementation -- the gap where under-constrained bugs live -- is bridged by the compiler, not by the developer.

To connect this back to our running example: what would the Sudoku proof look like in Compact? The structure is surprisingly clean:

```typescript
export circuit verify_sudoku(
  puzzle: Unsigned Integer[16]   // public: the given clues (0 = blank)
): [] {
  const solution = disclose(get_solution());
  // For each cell: assert value is 1-4
  // For each row: assert all four values distinct
  // For each column: assert all four values distinct
  // For each 2x2 box: assert all four values distinct
  // For each given clue: assert solution matches puzzle
}
```

The `disclose(get_solution())` call is the load-bearing line. The solution -- the completed 4x4 grid -- is a witness value, retrieved from the prover's private state. The `disclose()` makes it available to the circuit's constraints. The puzzle is a public input, visible to the verifier. The proof certifies: "I know a valid completion of this puzzle." The verifier learns nothing about the solution itself -- not a single filled-in cell.

### Noir: Write Once, Prove Anywhere

Noir takes a different approach to the same problem. Where Compact is chain-specific and privacy-first, Noir is backend-agnostic and correctness-first. A Noir program compiles not to a specific proof system's constraint format, but to ACIR -- Abstract Circuit Intermediate Representation -- which can then be lowered to any compatible backend.

Consider the same token transfer scenario in Noir:

```rust
fn main(
    sender_balance: Field,
    amount: pub Field,
    recipient_balance: Field,
) -> pub Field {
    assert(sender_balance >= amount);
    let new_recipient_balance = recipient_balance + amount;
    new_recipient_balance
}
```

The privacy model is visible in the function signature. Parameters without the `pub` keyword are private -- they are part of the witness, known only to the prover. Parameters marked `pub` are public inputs, visible to the verifier. The return value, also marked `pub`, is the public output.

This is simpler than Compact's disclosure analysis. There is no `disclose()` mechanism, no 26-pass pipeline tracing data-flow paths. The developer declares privacy at the function boundary: this input is private, that input is public, and the compiler enforces the declaration. It is the developer's responsibility to get the declaration right. Noir will not warn you if you accidentally mark a sensitive value as `pub`. But it will guarantee that every private input remains invisible to the verifier -- that the proof reveals nothing about private inputs beyond what the public outputs logically imply.

Where Noir stands apart is composability. A Noir developer can write a library of circuit components -- hash functions, signature verifiers, Merkle tree checkers -- and reuse them across projects targeting different proof systems. The same Noir code that runs on Aztec's Barretenberg backend today could, in principle, run on a PLONK backend, a Groth16 backend, or a future proof system that does not yet exist. This is not theoretical: the Noir ecosystem already includes standard libraries for common cryptographic primitives, and projects like zkEmail, zkPassport, and zkLogin use these libraries to build real applications.

A more realistic Noir program demonstrates the language's expressiveness. Here is a simplified credential verification -- proving you are over 18 without revealing your birthdate:

```rust
use std::hash::poseidon;

fn main(
    birth_year: Field,
    birth_month: Field,
    birth_day: Field,
    credential_hash: pub Field,
    current_year: pub Field,
    threshold_age: pub Field,
) {
    // Verify the credential hash matches the private birthdate
    let computed_hash = poseidon::bn254::hash_3([birth_year, birth_month, birth_day]);
    assert(computed_hash == credential_hash);

    // Verify age threshold without revealing exact birthdate
    let age = current_year - birth_year;
    assert(age >= threshold_age);
}
```

The developer writes Rust-like code. The standard library provides cryptographic primitives. The compiler handles the translation to constraints. The program is readable, auditable, and portable across proof backends. What the program cannot do -- what no Noir program can do -- is enforce at compile time that the developer has not accidentally marked `birth_year` as `pub`. That responsibility rests with the developer, not the compiler.

### Leo: Privacy as a Record System

Leo takes a third approach, one rooted in Aleo's record-based execution model. Where Compact models privacy as a property of data flow and Noir models it as a property of function signatures, Leo models privacy as a property of *records* -- discrete objects that are created, consumed, and transferred, much like physical banknotes.

A Leo token transfer looks different from both Compact and Noir:

```rust
program token.aleo {
    record Token {
        owner: address,
        amount: u64,
    }

    transition transfer(
        input: Token,
        recipient: address,
        amount: u64,
    ) -> (Token, Token) {
        let remaining: u64 = input.amount - amount;

        let sender_token: Token = Token {
            owner: self.caller,
            amount: remaining,
        };

        let recipient_token: Token = Token {
            owner: recipient,
            amount: amount,
        };

        return (sender_token, recipient_token);
    }
}
```

The keyword `record` defines a private data structure. Records in Leo are encrypted on-chain -- only the owner can decrypt them. When a `transition` consumes a record and produces new records, the old record is nullified (marked as spent) and the new records are encrypted for their respective owners. The entire UTXO lifecycle -- creation, transfer, consumption -- is expressed in the language itself.

The keyword `transition` is Leo's equivalent of Compact's `circuit`. It defines a function that will be proven in zero knowledge. But where Compact's circuits operate on abstract state and Noir's functions operate on field elements, Leo's transitions operate on records -- typed, owned, encrypted objects with a lifecycle managed by the Aleo runtime.

Leo's privacy model is structural rather than analytical. Privacy does not emerge from a disclosure analysis pass or from `pub` annotations on function parameters. It emerges from the record model itself: records are encrypted, transitions consume and produce records, and the only public artifact is a nullifier (proving a record was spent) and a commitment (proving a new record was created). The developer does not choose what is private. Everything inside a record is private by default. Publicity is the exception, declared through explicit `public` annotations on transition inputs.

The tradeoff is the same one that appears throughout Philosophy D: Leo programs run only on Aleo. The record model, the transition semantics, the encryption scheme -- all are Aleo-specific. But for developers building on Aleo, Leo provides something that general-purpose languages cannot: a programming model where privacy is not a layer of annotation on top of ordinary computation, but the fundamental unit of state.

### The Philosophy D Synthesis

What unites Philosophies A, B, and C is a shared assumption: the developer does not need to think about privacy. The proof system guarantees computational integrity -- it proves the computation was done correctly. But it says nothing about what information the computation reveals. Whether to encrypt inputs, hide outputs, or shield metadata is left to the application layer, if it is considered at all.

What unites the three Philosophy D languages is the opposite conviction: privacy cannot be an afterthought. The language itself knows the difference between public and private. Each takes a different route to that guarantee. Compact runs a disclosure-analysis pass and rejects programs where private values might reach a public surface without explicit consent. Noir puts the privacy boundary in the function signature and enforces what the developer declared -- but does not try to detect what they forgot. Leo encodes privacy structurally, in an encrypted record model where everything is private by default and publicity is the exception.

Philosophy D breaks the shared assumption of A, B, and C. Privacy is not a layer above the language -- it is embedded in the language itself.

The following table summarizes the four philosophies:

| Philosophy | Representative | What It Proves | Privacy Model | Developer Experience | Tradeoff |
|---|---|---|---|---|---|
| **A: EVM-Compatible** | Scroll, Linea | EVM execution | None (transparent) | Familiar (Solidity) | Proving the EVM is expensive |
| **B: ZK-Native ISA** | Cairo (Starknet) | Custom CPU trace | None (transparent) | New language required | Locked to one ecosystem |
| **C: General-Purpose ISA** | SP1, RISC Zero, Airbender | RISC-V execution | None (transparent) | Familiar (Rust, C++) | Arithmetization overhead |
| **D: Application DSL** | Compact / Noir / Leo | State transitions or circuits | Compact: compiler-enforced (disclosure analysis); Noir: annotation-based (developer responsibility); Leo: structural (record model) | Domain-specific syntax | Locked to one chain (Compact/Leo) or one IR (Noir) |

The taxonomy is not a ranking. Each philosophy serves a different constituency. The following decision guide distills each philosophy's sweet spot:

| Philosophy | Choose This When | Avoid When |
|-----------|-----------------|------------|
| **A: EVM-Compatible** | Existing Solidity codebase; need L1 security inheritance; team knows EVM tooling | Building from scratch; performance-critical new system; proving cost is binding constraint |
| **B: ZK-Native ISA** | Maximum proving efficiency; willing to learn Cairo; building within Starknet ecosystem | Need ecosystem portability; team cannot invest in new language; multi-chain deployment required |
| **C: General-Purpose ISA** | Standard Rust/C++ codebase; want ecosystem portability; broadest developer pool; zkVM as proving backend | Need compile-time privacy enforcement; need lowest possible proof latency for simple circuits |
| **D: Application DSL** | Privacy-preserving smart contracts; want compiler-enforced disclosure rules; domain-specific state model | Need general-purpose computation; team wants familiar language; multi-backend portability (except Noir) |

To make these four philosophies concrete: **Philosophy A** is like translating a novel into a language that has no word for half the concepts -- faithful but expensive. **Philosophy B** is like building a custom theater for a specific play -- the acoustics are perfect, but the theater can only stage that one production. **Philosophy C** is like staging the play in any theater in the world by writing it for a universal stage: RISC-V is the universal stage, and the play (your Rust program) works anywhere. **Philosophy D** is like writing a play where the script physically prevents the actors from breaking character -- in Compact, the compiler will not let a private value reach a public surface without explicit consent. Philosophy A serves Ethereum developers who want to reuse existing code. Philosophy B serves ecosystems willing to invest in a custom stack for maximum proof efficiency. Philosophy C serves the broadest developer community with the least friction. Philosophy D serves applications where privacy is not optional -- where the language must prevent the developer from accidentally revealing what should stay hidden.

---


## Summary

Four philosophies govern how developers express computations for ZK proving: EVM-compatible (Scroll, Linea), ZK-native ISA (Cairo/Starknet), general-purpose ISA (RISC-V via SP1, RISC Zero, Airbender, ZisK, Pico), and application-specific DSLs (Compact, Noir, Leo). Philosophies A–C treat privacy as the application's problem; Philosophy D embeds privacy in the language, with Compact's compiler rejecting accidental leakage at compile time.

## Key claims

- Polygon acquired Hermez for ~$250 million; the project was sunsetted in 2025 after proving EVM opcodes directly proved commercially unviable.
- RISC-V has ~40 base instructions versus thousands of x86 opcodes, making arithmetization manageable.
- Airbender proves 21.8 million RISC-V cycles/second on a single H100; a typical Ethereum block (~100–400 million cycles) takes 5–20 seconds.
- RISC Zero's R0VM 2.0 reduced Ethereum block proving from 35 minutes to 44 seconds.
- Compact's 26-pass nanopass pipeline includes a `Lnodisclose` disclosure-analysis stage that rejects accidental leakage at compile time.
- Noir 1.0 pre-released late 2025; Aztec's Ignition Chain launched November 2025 with 185+ operators and 3,400+ sequencers.
- Leo (Aleo): 400,000+ CLI downloads; privacy modeled via encrypted records (UTXO lifecycle).
- Goldilocks prime ($2^{64} - 2^{32} + 1$) adopted by Cairo and reused by RISC Zero, SP1, and others.

## Entities

- [[airbender]]
- [[arithmetization]]
- [[bn254]]
- [[fri]]
- [[goldilocks]]
- [[h100]]
- [[midnight]]
- [[nvidia]]
- [[pico]]
- [[plonk]]
- [[polygon]]
- [[poseidon]]
- [[prism]]
- [[starknet]]
- [[sudoku]]
- [[utxo]]
- [[zisk]]

## Dependencies

- [[ch03-from-circuits-to-virtual-machines-a-brief-evolution]] — evolutionary context for the four philosophies
- [[ch03-compact-s-disclosure-analysis]] — deep-dive on Compact's disclosure analysis pass
- [[ch03-midnight-compiler-ir-circuit]] — details on ZKIR output and three-artifact compilation
- [[ch05-layer-4-arithmetization]] — arithmetization overhead referenced for Philosophy C

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [P3] (E) Leo is described briefly relative to Compact and Noir; its formal verification hooks and the Aleo snarkVM architecture are mentioned but not explained. The section's depth is uneven across the three DSLs.

## Links

- Up: [[03-choreographing-the-act]]
- Prev: [[ch03-from-circuits-to-virtual-machines-a-brief-evolution]]
- Next: [[ch03-the-developer-s-actual-experience]]
