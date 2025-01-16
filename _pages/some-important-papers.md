---
layout: default
---

<h1 style="color: #cc0000;">some important papers</h1>

This is an (under-development) cryptography glossary that I am working on. In the past I've had a great deal of difficulty finding important or classical papers whenever I want them, so this is a series of links that lead to some important papers worth reading, sorted by category.

<h3 style="color: #cc0000;">my notes</h3>

+ [**A Note on Black-Box Separations and Key Agreement from OWFs**](https://matcauthon49.github.io/assets/black-box-note.pdf), an exposition on Impaliazzo and Rudich's 1989 result separating key agreement from one-way permutations.
+ [**Notes on Finite Fields**](https://matcauthon49.github.io/assets/ff.pdf), a brief primer on finite fields.
+ [**Notes on O-Notation**](https://matcauthon49.github.io/assets/big-o-note.pdf), a short note I wrote on O-notation in undergrad.
+ [**Packed Secret Sharing**](https://matcauthon49.github.io/assets/secret-sharing.pdf), a short note that explains the multi-secret sharing procedure of [FY92].

<h3 style="color: #cc0000;">assumptions</h3>

+ [**The Decision Diffie-Hellman Problem**](https://crypto.stanford.edu/~dabo/pubs/papers/DDH.pdf), *(1998), Boneh.* A survey on DDH.

+ [**Public-Key Cryptosystems Based on Composite Degree Residuosity Classes**](https://link.springer.com/chapter/10.1007/3-540-48910-X_16), *(1999), Paillier.* Introduced DCR and variants.

<h3 style="color: #cc0000;">foundations</h3>

+ [**New Directions in Cryptography**](https://ieeexplore.ieee.org/document/1055638), *(1976), Diffie and Hellman*. Introduced  Public-Key Cryptography.

+ [**The Knowledge Complexity of Interactive Proof-Systems**](https://dl.acm.org/doi/10.1145/22145.22178), *(1985), Goldwasser, Micali and Rackoff*. Introduced interactive proofs and zero-knowledge.

+ [**The random oracle methodology, revisited**](https://dl.acm.org/doi/10.1145/1008731.1008734), *(1998), Canetti, Goldreich, Halevi*. Constructs a scheme that is secure in the ROM but insecure when it is replaced with any hash function.

+ [**How to go beyond the black-box simulation barrier**](https://ieeexplore.ieee.org/document/959885), *(2001), Barak*. The first non-black-box technique for constructing a zero-knowledge proof simulator, constructs a concurrent zero-knowledge proof system.

+ [**On the (Im)possibility of Obfuscating Programs**](https://www.boazbarak.org/Papers/obfuscate.pdf), *(2001), Barak, Goldreich, Impagliazzo, Rudich, Sahai, Vadhan, Yang*. Shows the impossibility of software obfuscation.

<h3 style="color: #cc0000;">encryption</h3>

+ [**Design and Analysis of Practical Public-Key Encryption Schemes Secure against Adaptive Chosen Ciphertext Attack**](https://eprint.iacr.org/2001/108), *(2001), Cramer, Shoup.* A CCA-Secure Encryption Scheme based on DDH.

+ [**Circular and Leakage Resilient Public-Key Encryption Under Subgroup Indistinguishability (or: Quadratic Residuosity Strikes Back)**](https://eprint.iacr.org/2010/226), *(2010), Brakerski, Goldwasser.* A provably KDM-secure encryption scheme from QR, DCR and related assumptions.
