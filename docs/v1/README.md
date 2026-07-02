# The Compliance Engine, explained from scratch

**Start here.** This is a plain-English tour of what this system actually does —
no prior knowledge of compliance, the cloud, or code needed. Read the docs in
order; each one is short.

> ⚠ **This is a Phase-I prototype. Every run today is a mock / practice run.**
> It uses fake (fixture) data and runs Terraform in preview mode only — nothing
> is deployed to a real cloud, and no real credentials are used. Every document
> it produces is stamped **NON-EVIDENTIARY** — a demonstration artifact, *not* a
> real government submission. We say so plainly wherever it matters.

## Reading order

1. **[00 — What is this?](00-what-is-this.md)** — The big picture in one sitting:
   the problem, the one big idea, the two machines, and the two safety gates.
2. **[01 — The Order](01-the-order.md)** — How a contract becomes a signed
   "build order" (the *Order Compiler*), and the first safety gate.
3. **[02 — The Factory](02-the-factory.md)** — How the Order gets executed:
   plan the environment, check it, gather evidence, run automated checks.
4. **[03 — Machines vs. humans](03-machine-vs-human.md)** — The golden rule:
   machines gather evidence, but only a human can declare a rule "met."
5. **[04 — The proof](04-the-proof.md)** — What comes out: the BOM, the SSP, the
   SPRS score, and how it's all fingerprinted so it can't be quietly altered.
6. **[05 — Try it yourself](05-try-it.md)** — Run the demo in one command and
   see each artifact appear.
7. **[06 — Glossary](06-glossary.md)** — Every jargon word in one place.

**[06 — Glossary](06-glossary.md) can be read at any time** — jump to it whenever
a word is unfamiliar. The other docs link to it on first use.

## In one sentence

A machine that **builds a secure cloud environment and produces the proof that
it's compliant as the same action** — shown here as a fully-wired mock run.

**Next: [00 — What is this?](00-what-is-this.md)**
