---
title: "Governance: The Achilles Heel"
slug: ch08-governance-the-achilles-heel
chapter: 8
chapter_title: "Layer 7 -- The Verdict"
heading_level: 2
source_lines: [3677, 3778]
source_commit: b3ed881318761d3fd0e65ead7ea58e3f6536ccf9
status: reviewed
word_count: 2734
---

## Governance: The Achilles Heel

If Fiat-Shamir bugs are the most exploited *implementation* vulnerability in zero-knowledge systems, governance is the most exploited *architectural* vulnerability. And unlike Fiat-Shamir bugs, governance vulnerabilities cannot be fixed with better code review. They are features, not bugs.

Here the story changes genre. Until now, we have been watching a technical narrative -- mathematicians and engineers building increasingly sophisticated proof systems. Now the camera pulls back, and the audience discovers it has been watching a different show than it thought. The threats at Layer 7 are not mathematical. They are human.

### The Beanstalk Flash Loan Attack ($182M, April 2022)

Beanstalk was a permissionless stablecoin protocol -- a DeFi project built on the idea that an algorithmic stablecoin (called Bean) could maintain its dollar peg through a credit-based system of debt, deposits, and incentive cycles. The protocol had attracted over $100 million in total value locked. It had a community. It had audits. It had a governance mechanism that allowed holders of the protocol's internal Stalk token to propose and vote on changes to the system's parameters, its contracts, its entire economic logic.

The mathematics were sound. The smart contracts were audited. The governance mechanism was functioning exactly as designed.

That last sentence is the important one. Remember it.

Beanstalk's governance had one feature that seemed reasonable at the time: the emergency commit threshold. If a proposal attracted more than two-thirds of total Stalk voting power, it could be executed immediately -- no waiting period, no time lock, no multi-day deliberation window. The designers' reasoning was practical: if a supermajority of stakeholders agreed on something, why force them to wait? Speed was a feature. In a fast-moving DeFi market, the ability to respond quickly to exploits or market conditions was considered an advantage.

On April 17, 2022, at approximately 12:24 UTC, someone demonstrated why speed is also a weapon.

The attacker -- whose identity remains unknown to this day -- began by taking flash loans from three decentralized lending protocols: Aave, Uniswap V2, and SushiSwap. A flash loan is a peculiar instrument unique to programmable blockchains: it allows you to borrow any amount of money, provided you repay it within the same transaction. If you cannot repay, the entire transaction reverts as if it never happened. The borrowing cost is essentially zero -- just gas fees and a small protocol fee. There is no credit check. There is no collateral. There is no application form. You simply ask for the money, use it, and return it, all within a single atomic operation that takes seconds.

On this day, the attacker borrowed approximately $1 billion in assets. One billion dollars, for thirteen seconds.

With the borrowed capital, the attacker swapped into Beanstalk's liquidity pools, acquiring enough of the protocol's Stalk and Seed tokens to control over 67% of total governance voting power. This was not a theoretical majority. It was an absolute supermajority -- enough to clear the emergency commit threshold.

Then came the proposals. BIP-18 was the payload: a governance proposal whose code, when executed, would transfer all of Beanstalk's protocol reserves -- every Bean, every LP token, every asset in the Silo -- to a wallet controlled by the attacker. The code was not hidden. It was right there on the blockchain, readable by anyone who looked. But governance proposals are submitted and voted upon, not scrutinized line by line in the seconds between submission and execution, and nobody was watching for a proposal backed by a billion dollars of borrowed voting power.

BIP-19 was the other proposal: a donation of $250,000 to the Ukraine war relief wallet. Whether this was misdirection, moral compensation, ironic commentary, or simply a way to make the governance transaction look routine is a question the attacker left permanently unanswered. It remains one of the small, unsettling details that elevate this from a theft to a performance.

The attacker voted on BIP-18 with the borrowed supermajority. The emergency commit threshold was cleared. The governance system did what governance systems do: it executed the will of the majority. The protocol's reserves flowed from the Silo to the attacker's address. The attacker unwound the liquidity positions, converted the assets, repaid the flash loans to Aave, Uniswap, and SushiSwap -- in full, with fees -- and pocketed the difference.

Thirteen seconds. Borrow, vote, execute, extract, repay. The entire heist was a single atomic transaction on Ethereum. If any step had failed -- if the flash loan had been too small, if the voting power had been insufficient, if the repayment had come up short -- every step would have reverted, and the blockchain would have recorded nothing. But no step failed. The transaction succeeded. The money was gone.

Total protocol loss: $182 million in value destroyed. Net extraction by the attacker: approximately $77 million in non-Bean assets -- the portion that had real market value independent of the now-collapsed protocol. The Bean stablecoin depegged immediately and never recovered. The protocol's entire treasury was emptied in a single block.

The root cause was not a code vulnerability. No contract was exploited in the traditional sense. No buffer was overflowed. No access control was bypassed. No reentrancy was triggered. The governance mechanism worked exactly as designed. It accepted a vote from a stakeholder with a supermajority. It executed the proposal that the supermajority approved. It transferred the funds that the proposal specified. Every line of code behaved correctly.

The system was not broken. The system was *used*.

The lesson lands differently depending on who you are. If you are a protocol designer, the lesson is about time locks and minimum voting periods and the danger of emergency execution without delay. If you are a governance theorist, the lesson is about the difference between ownership and rental -- the attacker did not own the voting power; he rented it for the cost of a flash loan fee. If you are building a ZK rollup with token-weighted governance over an upgradeable verifier contract, the lesson is existential: governance that can be rented by the hour is governance that can be captured in seconds. The flash loan is the instrument. The vulnerability is the assumption -- the assumption that token holders are stakeholders, that voting power reflects long-term commitment, that the people who hold the keys today will hold them tomorrow. Flash loans dissolve that assumption into nothing. For the thirteen seconds that matter, anyone with gas money is a supermajority stakeholder.

### The Tornado Cash Governance Attack (May 2023)

Tornado Cash was a privacy protocol built on zero-knowledge proofs -- the very technology this book describes. It used ZK proofs to break the on-chain link between depositors and withdrawers. You deposit ETH into a pool, receive a cryptographic note, and later withdraw from the pool using a ZK proof that demonstrates you possess a valid note without revealing which deposit was yours. The cryptography was elegant, well-audited, and provably sound. The protocol's privacy guarantees were genuine. Its governance was controlled by a DAO with TORN token voting, and the governance was not.

The attack, when it came in May 2023, unfolded like a stage magic trick -- not the kind where a rabbit appears from a hat, but the kind where the audience watches the magician's right hand while the left hand replaces the entire stage.

To understand the trick, you need to understand two pieces of Ethereum infrastructure that most users never think about.

The first is `CREATE2`. On Ethereum, when you deploy a contract, it gets an address. Normally, this address is derived from the deployer's address and a nonce (a sequential counter), so it is effectively unpredictable. `CREATE2`, introduced in EIP-1014, changes the formula: the new contract's address is derived from the deployer's address, a chosen salt, and the *hash of the bytecode being deployed*. This means you can calculate a contract's address before deploying it. More importantly -- and this is what the trick turns on -- if you deploy an intermediary factory contract that itself uses `CREATE` (the old opcode), and that factory deploys a child contract, and then you destroy both the factory and the child via `selfdestruct`, and then you redeploy the factory at its original `CREATE2` address, the factory's nonce resets to zero, and it can deploy a *completely different* child contract at the *same address* where the original child lived. The address is reused. The code is not.

The second is the proxy pattern. Tornado Cash's governance system, like many DAO governance contracts, used a proxy architecture (EIP-1967/UUPS). In a proxy pattern, there is a permanent proxy contract at a fixed address that users interact with. This proxy does not contain the actual governance logic. Instead, it contains a pointer -- a storage slot at a specific, standardized location -- that holds the address of an *implementation* contract. When you call a function on the proxy, the proxy uses `delegatecall` to forward your call to whatever implementation contract the pointer currently references. The proxy's storage is used, but the implementation's code runs. This means whoever can change the pointer controls what code executes when anyone interacts with the governance system. Change the pointer, and you change the governance -- silently, without deploying a new visible contract, without changing the address that everyone knows and trusts.

Now the trick.

The attacker submitted a governance proposal to the Tornado Cash DAO. The proposal looked benign. Its description claimed it was identical to Proposal 16, a previously approved and uncontroversial proposal that penalized certain relayers for cheating. The voters did what voters do in a DAO with dozens of proposals per month: they read the description, saw it matched something familiar, and voted yes. They did not decompile and audit the proposal's bytecode. Why would they? The description said it was the same proposal. Reviewing raw EVM bytecode is not a skill most governance participants possess, and the social norm in DAO governance is to review descriptions, not opcodes.

The vote passed. The proposal was approved by the DAO's governance process, with legitimate TORN token holders casting legitimate votes through the legitimate governance interface. Democracy had spoken.

Then the floor opened.

The proposal contract that the voters had approved contained a hidden capability: `selfdestruct`. This EVM opcode does exactly what its name suggests -- it destroys the contract at a given address, wiping its bytecode from the blockchain state and sending any remaining ETH balance to a specified recipient. After the vote passed and the proposal was executed, the attacker triggered `selfdestruct` on the proposal contract. The code that the voters had approved ceased to exist on the blockchain.

Then the attacker redeployed. Using the `CREATE2` intermediary trick described above, the attacker deployed entirely new bytecode at the same address where the original proposal contract had lived. The Tornado Cash governance system still held a reference to that address. It still trusted that address. But the code living there was now completely different from what the voters had approved.

The new code did one thing: it gave the attacker the ability to mint TORN governance tokens to themselves -- 10,000 TORN per iteration, repeatable, until the attacker held 1.2 million votes. The entire legitimate DAO held roughly 700,000 votes. The attacker now controlled a permanent, unchallengeable supermajority.

The misdirection was total. The malicious code was not present during the vote. It did not exist when the voters examined the proposal. The voters approved code A. The attacker destroyed code A and deployed code B at the same address. The governance system, still pointing at that address, treated code B as if it had the full authority of the vote that approved code A. The signed letter's text changed after the seal was broken -- and the seal still looked intact.

Impact: complete control over Tornado Cash's governance. The attacker could drain locked tokens, modify protocol parameters, brick the router contract, or do anything else the governance system was authorized to do. Approximately $2.17 million was stolen directly. The TORN token price dropped 36% as the market priced in the total capture of the protocol's decision-making apparatus. A privacy protocol whose zero-knowledge cryptography was unbroken -- whose mathematical guarantees remained perfectly sound -- was nevertheless fully compromised, because the human layer that governed it was exploitable through misdirection and code replacement.

The root cause was two vulnerabilities woven together: a social one and a technical one. The social vulnerability was that voters verified the proposal's *description* but not its *code*. This is normal human behavior. It is also, in hindsight, a systemic weakness of every DAO that presents proposals as human-readable summaries rather than requiring formal verification of the underlying bytecode. The technical vulnerability was the `selfdestruct` + `CREATE2` pattern, which allowed post-approval code replacement at a trusted address -- a capability that the governance system had no mechanism to detect or prevent.

Neither vulnerability alone would have been sufficient. Together, they allowed an attacker to go beyond exploiting the governance -- to *become* the governance. The Beanstalk attacker rented governance power for thirteen seconds. The Tornado Cash attacker did something structurally worse: he permanently replaced the governance with himself. Beanstalk was a heist. Tornado Cash was a coup.

### ZK Rollup Governance Risk

Both attacks targeted governance mechanisms that controlled upgradeable contracts. And ZK rollup verifier contracts are almost always deployed behind upgradeable proxy patterns -- the same patterns catalogued in the 2023 survey by Meisami and Bodell, which documented EIP-1967 (OpenZeppelin transparent proxy), EIP-1822 (UUPS), EIP-2535 (Diamonds), and Beacon proxies.

The proxy pattern introduces its own attack surface beyond governance: storage layout corruption when state variables are reordered across upgrades, function selector collisions between proxy admin and implementation functions, and the fundamental risk that `delegatecall` means all storage operations in the implementation affect the proxy's storage.

But the deepest risk is simpler than any of these. Whoever controls the proxy admin controls the verifier. If the governance mechanism that controls the proxy admin is vulnerable to flash loans (Beanstalk-style) or code replacement (Tornado Cash-style), then the entire rollup's security reduces to the security of its governance mechanism.

The cryptography could be perfect. The ceremony could have had a million participants. The circuits could be formally verified. None of it matters if an attacker can replace the verifier contract with one that returns `true` for every proof. Six layers of mathematical elegance, and the seventh is a multisig.

### L2Beat's Stages Framework

L2Beat, the independent rollup monitoring organization, has formalized the maturity of rollup decentralization into three stages:

**Stage 0 -- Full Training Wheels**: The rollup is effectively run by its operators. It must have source-available software for state reconstruction from L1 data, and it must have *some* proof system to qualify. But governance can override everything. Most rollup deployments begin here.

**Stage 1 -- Limited Training Wheels**: The proof system is fully functional. Fraud proof submission (for optimistic rollups) or verification (for ZK rollups) is permissionless. Users can exit without operator coordination through forced inclusion or escape hatches. A Security Council may override the proof system for bug fixes, but with constraints -- for example, a 6-of-8 multisig with a 7-day delay.

**Stage 2 -- No Training Wheels**: The rollup is fully managed by smart contracts. The proof system is permissionless. Users get at least 30 days' notice for unwanted upgrades. The Security Council is restricted to adjudicating on-chain-provable soundness errors only. Users are fully protected from governance attacks.

As of early 2026, most major ZK rollups are at Stage 0 or Stage 1. Achieving Stage 2 requires either formally verified verifier contracts (so bugs are unlikely enough that upgrade capability can be removed), multiple independent implementations that cross-check each other, or bounded upgrade windows with mandatory exit periods of 30 or more days.

The tension is real and irreducible. ZK verifier contracts are among the most complex smart contracts ever deployed. They implement pairing checks, polynomial evaluations, and Fiat-Shamir transcript verification in a language (Solidity, or Yul) that was not designed for this kind of arithmetic. The probability of bugs is non-trivial. But the ability to fix bugs via governance is the same ability that allows governance to introduce them.

Stage 2 is where the cryptographic guarantees from Layers 1 through 6 actually bind. Below Stage 2, they are advisory. A Stage 0 rollup with 256-bit proof security is, from the user's perspective, only as secure as the governance multisig's operational security.

---


## Summary

Governance vulnerabilities are architectural, not implementational — they cannot be fixed with better code review. Two incidents (Beanstalk $182M April 2022; Tornado Cash May 2023) show that flash-loan-rented voting power and post-approval code replacement can completely capture a protocol whose cryptography remains unbroken. L2Beat's three-stage framework quantifies how far current ZK rollups fall short of governance-resistant operation.

## Key claims

- Beanstalk (April 2022, $182M): attacker flash-loaned ~$1B, acquired >67% Stalk governance power, passed BIP-18 under the emergency-commit rule, and drained all protocol reserves in one atomic transaction of 13 seconds.
- Flash loans dissolve the assumption that token holders are long-term stakeholders; governance power can be rented for the cost of a gas fee.
- Tornado Cash (May 2023): attacker used `CREATE2` + `selfdestruct` to replace approved proposal code at the same address post-vote, minting 1.2M TORN tokens — permanent DAO takeover worth ~$2.17M direct drain; TORN dropped 36%.
- ZK rollup verifier contracts are almost always behind upgradeable proxy patterns (EIP-1967, EIP-1822, EIP-2535, Beacon), making governance the critical security variable.
- L2Beat Stage 0: governance can override everything; Stage 1: permissionless proof submission, Security Council multisig (e.g., 6-of-8, 7-day delay); Stage 2: governance cannot override the proof system, 30+ day exit windows.
- As of early 2026, no major ZK rollup has reached Stage 2.
- Below Stage 2, cryptographic strength is advisory; a Stage 0 rollup with 256-bit proof security is only as secure as its multisig.

## Entities

- [[beanstalk]]
- [[tornado cash]]
- [[fiat-shamir]]
- [[l2beat]]

## Dependencies

- [[ch08-the-social-layer]] — governance is one of the four Layer 7 concerns
- [[ch08-who-verifies-the-verifier]] — immutable vs upgradeable verifier tradeoffs
- [[ch08-case-study-midnight-and-the-three-token-architecture]] — Midnight's architectural response to governance attacks
- [[ch08-on-chain-verification-in-2026]] — current Stage distribution

## Sources cited

- Meisami and Bodell (2023) — survey of EIP-1967, EIP-1822, EIP-2535, Beacon proxy patterns
- Beanstalk post-mortem (April 2022)
- Tornado Cash governance attack analysis (May 2023)

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P3] (B) Meisami and Bodell (2023) is cited for the proxy pattern survey but no venue, title, or link is given; a full reference would strengthen the claim.

## Links

- Up: [[08-the-verdict]]
- Prev: [[ch08-when-the-transcript-lies-fiat-shamir-vulnerabilities]]
- Next: [[ch08-proof-aggregation-the-missing-layer]]
