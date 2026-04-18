---
title: "Pricing Attacks"
slug: ch08-pricing-attacks
chapter: 8
chapter_title: "Layer 7 -- The Verdict"
heading_level: 2
source_lines: [3889, 3937]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1160
---

## Pricing Attacks

The relationship between verification costs and data availability costs creates exploitable seams. A 2025 study by Chaliasos et al. identified two novel attack classes that exploit mismatches in how rollups price their three cost dimensions: L2 execution, L1 data availability, and L1 settlement/proving.

### DA-Saturation Attacks

An attacker floods an L2 with data-heavy, compute-light transactions -- essentially random calldata followed by a STOP opcode. Each such transaction is cheap in L2 gas (the computation is trivial) but expensive in L1 DA cost (it fills blob space with incompressible junk). The study found that sustained denial-of-service on Linea cost as little as 0.87 ETH per hour, and on Optimism roughly 2 ETH per 30 minutes.

The effects cascade: the L2 is congested, finality delays increase by 1.45x to 2.73x compared to direct L1 blob stuffing, and the rollup operator hemorrhages money because the fees collected from the spam transactions do not cover the L1 DA costs. All major rollups studied were found susceptible. Four bug bounties, each worth tens of thousands of dollars, were paid.

### Prover-Killer Attacks

These exploit the mismatch between EVM gas metering and ZK proving costs. Not all EVM opcodes are equally expensive to prove in zero knowledge. The study measured "cycles per gas" ratios -- how many proving cycles are needed per unit of gas cost:

| Opcode / Precompile | EVM Gas | Proving Cycles/Gas | Attack Leverage |
|---------------------|---------|-------------------|-----------------|
| JUMPDEST | 1 | 1,039.79 | Very High |
| MODEXP | (varies) | 2,961.72 | Extreme |
| BN_PAIRING | 45,000+ | 1,642.15 | High |
| SHA256 | 60+ | Moderate | Moderate |

These metrics are proving-system-specific; the exact ratios differ for SP1, RISC Zero, and Cairo-based provers. The table reflects one particular zkEVM implementation measured by the study, but the general pattern -- that some opcodes are orders of magnitude more expensive to prove than their EVM gas implies -- holds across all systems.

A MODEXP attack -- filling blocks with maximum-cost modular exponentiation operations -- delayed finality by 94x (over 8 hours) and cost the rollup operator $42.26 per attack block. The rollup's proving system crashed after 10,266 seconds.

### The Concrete Scenarios

These are not theoretical concerns. They are playbooks.

**DA-saturation in practice.** An attacker constructs transactions that contain the maximum possible calldata -- random bytes, incompressible by design -- followed by a STOP opcode. The EVM execution cost is negligible: STOP costs 0 gas, and the transaction is technically valid. But the data must be posted to L1 for data availability, and incompressible random data consumes maximum blob space. The attacker submits these transactions continuously, filling every blob slot in every Ethereum block with garbage.

The immediate effect: blob fees spike. Ethereum's blob fee market operates under EIP-1559 dynamics -- when blobs are consistently full, the base fee increases exponentially. Under sustained saturation, blob fees can increase by 100x or more within minutes. Every legitimate rollup that needs to post data to Ethereum sees its operating costs spike proportionally. The attacker pays blob fees too, of course, but the attacker's cost is the cost of the attack. Every other rollup's cost is collateral damage.

The secondary effect is subtler and worse: rollup operators, facing unexpectedly high L1 costs, must choose between posting data at a loss (subsidizing operations from their treasury), delaying batch submissions (increasing finality time for users), or raising L2 fees (driving users to competitors). The attacker does not need to sustain the attack indefinitely. A few hours of blob saturation can cause lasting reputational and economic damage to rollups that depend on predictable L1 costs.

The defense is multidimensional fee pricing on the L2 side: a separate DA fee component that adjusts dynamically based on actual L1 blob costs, passed through to users in real time rather than absorbed by the operator. Several rollups have implemented this in response to the Chaliasos findings, but the adjustment is inherently reactive -- the fee increases *after* the attack begins, which means the operator absorbs losses during the lag period.

**Prover-killer in practice.** An attacker submits transactions that are cheap in EVM gas but catastrophically expensive to prove in zero knowledge. The canonical example is MODEXP -- modular exponentiation with maximum-size inputs. The EVM prices MODEXP based on the size of the operands and a formula that was calibrated for native CPU execution, not for ZK circuit execution. A MODEXP operation with 256-byte base, exponent, and modulus costs roughly 200 gas in the EVM. Proving that same operation inside a ZK circuit requires the prover to decompose the modular exponentiation into field arithmetic over the proving system's native field, which involves thousands of multiplication gates per limb, per exponentiation step. The ratio of proving cost to EVM gas cost -- the "cycles per gas" metric -- reaches nearly 3,000 for MODEXP. A single MODEXP transaction can consume as much proving capacity as 3,000 normal transactions.

The attacker does not need exotic tools. They submit valid transactions -- MODEXP calls with legitimate inputs that any EVM will execute without complaint. The transactions pass all validation checks. They pay standard gas fees. They are included in blocks by the sequencer because the sequencer has no reason to reject a valid, fee-paying transaction. But when those blocks reach the prover, the prover must generate a ZK proof of the entire block's execution, including the MODEXP operations. A single block stuffed with MODEXP calls can take the prover 10,000 seconds to prove -- over 2.7 hours for a block that the sequencer produced in seconds.

If the attacker sustains this for multiple blocks, the prover falls behind. Proving latency grows. Finality -- the time before a rollup batch is verified on L1 -- stretches from minutes to hours. The rollup is technically still functioning, but its security guarantee degrades: until the proof is posted and verified, the rollup's state transitions are unproven claims, not verified facts. A sustained prover-killer attack can push a ZK rollup into a state where it behaves, from the user's perspective, more like an optimistic rollup -- running on trust rather than proof, hoping nothing goes wrong during the gap.

The defense requires the sequencer to price transactions based on their *proving cost*, not just their EVM gas cost. This is the multidimensional pricing problem: EVM gas, DA cost, and proving cost are three independent resources, and a single gas price cannot accurately reflect all three. Until rollups implement proving-cost-aware fee markets, the prover-killer attack remains viable against any ZK rollup that prices transactions using only EVM gas metering.

The root cause is fundamental: current rollup fee mechanisms use a single-dimensional gas price that bundles L2 execution, L1 DA, and proving costs into one number. When these three resources have different scarcity profiles, the bundled price necessarily misprices at least one of them. The fix is multidimensional pricing -- separate base fees for each resource type, each following its own EIP-1559-style adjustment mechanism.

---


## Summary

Two novel attack classes exploit mismatches in how rollups price their three independent cost dimensions: L2 execution, L1 data availability, and L1 proving. DA-saturation floods blob space with incompressible data at near-zero execution cost; prover-killer attacks submit EVM-cheap but ZK-expensive operations that can delay finality by 94× and crash provers. Both are defeated only by multidimensional fee pricing.

## Key claims

- DA-saturation attack: data-heavy, compute-light transactions fill L1 blob slots with incompressible calldata; sustained DoS on Linea cost as little as 0.87 ETH/hour; on Optimism ~2 ETH/30 min.
- DA-saturation increases finality delays 1.45×–2.73× over direct L1 blob stuffing; all major rollups studied were susceptible.
- Prover-killer attack exploits "cycles per gas" mismatches: JUMPDEST = 1,039.79 cycles/gas; MODEXP = 2,961.72 cycles/gas; BN_PAIRING = 1,642.15 cycles/gas.
- A block stuffed with MODEXP calls delayed finality 94× (>8 hours) and cost the operator $42.26/attack block; prover crashed after 10,266 seconds.
- Single-dimensional gas pricing necessarily misprices at least one of the three resources (L2 execution, DA, proving).
- Fix: separate EIP-1559-style base fees for each resource type; several rollups have added dynamic DA fee components post-Chaliasos.
- Source: Chaliasos et al. (2025 study); four bug bounties paid in the tens of thousands of dollars.

## Entities

- [[eip]]
- [[groth16]]

## Dependencies

- [[ch08-the-price-of-a-verdict]] — DA cost structure and blob fee dynamics that attacks exploit
- [[ch08-the-social-layer]] — Layer 7 concerns framing
- [[ch08-on-chain-verification-in-2026]] — current state of rollup fee markets

## Sources cited

- Chaliasos et al. (2025) — DA-saturation and prover-killer attack study; four bug bounties paid

## Open questions

None flagged by this section.

## Improvement notes

- [none] X — no issues found.

## Links

- Up: [[08-the-verdict]]
- Prev: [[ch08-the-deepest-symmetry]]
- Next: [[ch08-who-verifies-the-verifier]]
