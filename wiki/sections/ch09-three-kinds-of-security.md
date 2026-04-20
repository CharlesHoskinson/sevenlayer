---
title: "Three Kinds of Security"
slug: ch09-three-kinds-of-security
chapter: 9
chapter_title: "Privacy-Enhancing Technologies"
heading_level: 2
source_lines: [4079, 4106]
source_commit: 53f41415d307dcd4ed73d852dfd6aa97146e882f
status: reviewed
word_count: 972
---

## Three Kinds of Security

These four technologies provide fundamentally different *types* of security guarantees, and conflating them leads to bad architecture decisions. This is the part where precision matters more than analogy.

**Information-theoretic security** means the guarantee holds even against an adversary with unlimited computational power. No mathematical breakthrough, no quantum computer, no advance in algorithms can break it. MPC with honest majority (e.g., Shamir secret sharing where more than half the participants are honest) achieves this. The security follows from information theory, not computational hardness. The caveats: you need an honest majority, and the communication cost scales with the number of parties and the complexity of the computation.

**Computational security** means the guarantee holds against adversaries bounded to polynomial-time computation. It rests on assumptions: "discrete logarithms are hard," "the Learning With Errors problem is hard," "the Ring-LWE problem is hard." ZKPs and FHE provide computational security. If the underlying hardness assumption falls -- as discrete logarithm will fall to Shor's algorithm on a sufficiently large quantum computer -- the security evaporates retroactively. Every proof ever generated under that assumption becomes suspect. The lock does not weaken. It ceases to exist.

**Heuristic security** means the guarantee rests on practical observations rather than formal proof. Trusted Execution Environments (TEEs) like Intel SGX, AMD SEV, and ARM CCA provide heuristic security. The hardware manufacturer attests that the enclave is isolated. But SGX has been broken by Spectre, Meltdown, Foreshadow (Van Bulck et al., USENIX Security 2018), Plundervolt (Murdock et al., IEEE S&P 2020), SGAxe (Van Schaik et al., 2020), and AEPIC Leak (Borrello et al., USENIX Security 2022). AMD SEV has shown vulnerabilities (SEVered, CipherLeaks). Intel SGX was deprecated on consumer processors beginning with 11th/12th generation client chips in 2021. The 2025 attacks Battering RAM (De Meulemeester, Oswald, Verbauwhede, and Van Bulck; KU Leuven, Birmingham, and Durham, disclosed September 2025) at approximately €50 and Wiretap (disclosed simultaneously in the US, at roughly $1,000) demonstrated physical attacks at commodity prices against confidential computing on current Intel and AMD server parts. TEE security is real in practice against most adversaries, but it lacks the mathematical foundation of cryptographic privacy and carries an expiration date set by the next side-channel attack. It is a stage built from plywood rather than steel: functional, but not what you want for the long run.

The metaphor of plywood is generous. To understand TEEs concretely, picture a room within a room. Your CPU -- the physical chip on the motherboard -- creates an isolated memory region called an enclave. Code and data inside the enclave are encrypted in RAM. The operating system cannot read the enclave's memory. The hypervisor cannot read it. Even a system administrator with root access and physical possession of the machine cannot read it. The CPU itself enforces the boundary: any attempt to access enclave memory from outside the enclave returns encrypted garbage. Intel SGX (Software Guard Extensions) pioneered this architecture. ARM TrustZone implements a similar concept at the processor level, splitting the chip into a "secure world" and a "normal world" with hardware-enforced isolation between them.

The promise is strong: you can run sensitive computation on an untrusted machine, and the machine's owner cannot observe or tamper with it. Cloud computing without trusting the cloud. The allure is obvious. The history is cautionary.

Foreshadow (August 2018; Van Bulck et al., USENIX Security 2018) broke SGX isolation through a speculative execution attack. The CPU's branch predictor, trying to execute instructions ahead of time for performance, would speculatively read enclave memory and leave traces in the L1 cache. An attacker could measure cache timing to reconstruct the enclave's secrets. The attack required no physical access -- it could be performed by a process running alongside the enclave on the same machine. Intel patched it with microcode updates, but the patch reduced performance, and the underlying vulnerability -- that speculative execution can leak secrets across security boundaries -- proved to be architectural, not incidental.

AEPIC Leak (August 2022; Borrello et al., USENIX Security 2022) was worse. It exploited a bug in Intel's Advanced Programmable Interrupt Controller to read stale data from the enclave's memory hierarchy. Unlike Foreshadow, which required careful cache timing, AEPIC Leak provided architecturally guaranteed data leakage -- the CPU would hand you the enclave's data directly if you asked the right hardware register. No timing side channel, no statistical analysis. A clean read.

Downfall (August 2023; Moghimi, 2023; Intel advisory INTEL-SA-00828, CVE-2022-40982) exploited the Gather instruction, which loads data from scattered memory locations into a vector register. The vulnerability allowed an attacker to read data from other security domains -- including SGX enclaves -- by observing the contents of internal CPU buffers during Gather operations. Intel's mitigation involved disabling the optimization that made Gather fast, resulting in up to 50% performance degradation for workloads that depended on it.

Intel quietly deprecated SGX on 11th/12th-generation consumer processors (and later) beginning in 2021. The feature remains available on server-class Xeon processors, where it is marketed for cloud confidential computing. But the deprecation on consumer chips tells a story: Intel concluded that the attack surface was too large and the performance cost of mitigations too high for a feature intended to run on every laptop. The room within a room is still available -- but only in the data center, where the threat model is different and the economic calculus favors the convenience of hardware isolation despite its known fragility.

For the system architect, this taxonomy matters because it determines *what you are actually trusting*. If your system uses MPC with honest majority for the core computation and ZKPs for the verifiable output, you have information-theoretic privacy for the computation and computational privacy for the proof. If you then run the whole thing inside a TEE, the TEE adds performance (fast) and convenience (no complex protocol choreography) but does not strengthen the privacy beyond what the cryptography already provides -- and may weaken it if the TEE is compromised. This is the practical meaning of the heuristic-security tier: not worthless, but fragile in ways that information-theoretic and computational guarantees are not.

The magician's guarantee depends on which lock protects the trick. Information-theoretic security is a lock that cannot be picked, even with infinite time. Computational security is a lock that cannot be picked in practice -- but a quantum locksmith might change the calculus. Heuristic security is a lock that has never been picked, without proof that it cannot be.

---


## Summary

Distinguishes information-theoretic, computational, and heuristic security guarantees across the PET families. TEEs (Intel SGX, AMD SEV) provide heuristic security that has been repeatedly broken by side-channel attacks including Foreshadow (2018), AEPIC Leak (2022), Downfall (2023), and commodity-price physical attacks Battering Ram and Wiretap (2025); Intel deprecated SGX on consumer processors from 12th generation onward.

## Key claims

- Information-theoretic security (e.g., Shamir MPC with honest majority) holds against unbounded adversaries including quantum computers.
- Computational security (ZKPs, FHE) falls if the underlying hardness assumption is broken — Shor's algorithm breaks discrete log retroactively.
- TEE security is heuristic: SGX broken by Spectre, Meltdown, Foreshadow, Plundervolt, SGAxe, AEPIC Leak, Downfall.
- AEPIC Leak (August 2022) gave architecturally guaranteed data reads from enclave memory via a hardware register bug.
- Downfall (August 2023) caused up to 50% performance degradation from Intel's Gather-instruction mitigation.
- Battering Ram (~$50) and Wiretap (~$1,000) demonstrated physical TEE attacks at commodity prices in 2025.
- Intel SGX deprecated on consumer processors (12th generation+) from 2021; remains on server Xeons.
- Stacking a TEE on top of MPC + ZKP does not strengthen privacy — and may weaken it if the TEE is compromised.

## Entities

- [[fhe]]
- [[mpc]]
- [[zkps]]

## Dependencies

- [[ch09-the-four-pillars]] — establishes the four PETs whose security types are classified here
- [[ch09-the-decision-matrix]] — uses this taxonomy as input to the trust-model question
- [[ch07-three-hardness-assumptions-three-worlds]] — underlying hardness for computational security

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

## Links

- Up: [[09-privacy-enhancing-technologies]]
- Prev: [[ch09-the-four-pillars]]
- Next: [[ch09-composability-when-one-pet-is-not-enough]]
