---
layout: default
---

<script
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
  type="text/javascript">
</script>

<h1 style="color: #cc0000;">some fun stuff</h1>

I often find that these academic webpages serve as cookie-cutter enterprises devoted to being easy paper-finding resources. Which isn't really a bad thing, per se, but they do come off as devoid of personality; the subject usually ends up seeming stoic or unapproachable. It's why I usually like adding a some irrelevant information about myself. It's quite fun.

<h2 style="color: #cc0000;">about me</h2>

I like travelling quite a bit and I've lived in a bunch of different places in my life. My favorite among these places is probably Bangalore, which happens to be my hometown, followed shortly by Paris. I also spent a fantastic year and a half in Chennai. Sometimes I write about these things. I also write short stories, satirical articles, and ocassionally poetry, although I've only recently started uploading some of my work. You can find it [here](https://unfortunateepigraphies.substack.com/). It's not a very good website, but I guess it suffices. Eventually I'd like to make something out of writing.

I watch a lot of sports, though the only sport I regularly practice is running (and hiking? if you can call it one). I support Manchester United for no good reason, and I also have a soft spot for Borussia Dortmund. I also watch Formula 1, where I support McLaren. I enjoy arguing about football and F1. If you ever want to pick a fight, let me know. I'd be happy to oblige.

At some point I gave the mathematical olympiad. I did pretty okay.

<h2 style="color: #cc0000;">eight predictions for cryptography</h2>

1. There is a polynomial-time classical algorithm for factoring.
2. There is a polynomial-time quantum algorithm for LWE.
3. There is a non-black-box construction of key exchange from OWFs.
4. There will never be a quantum computer that will be able to factor a 2048-bit RSA modulus.
5. There is a construction of FHE from non-lattice-based assumptions.
6. There will never be a structural practical attack on SHA that uses the fact that it is not a random oracle.
7. iO will never be practical.
8. $$\mathsf{P}\neq\mathsf{NP}$$, but SETH is false.

<h2 style="color: #cc0000;">some papers</h2>

My area of interest is cryptography and theoretical computer science. Here's a list of some of my favorite papers.

+ **The Random Oracle Methodology, Revisited**. [Article](https://eprint.iacr.org/1998/011).
+ **A Proof of Security of Yao’s Protocol for Two-Party Computation**. [Article](https://eprint.iacr.org/2021/1453).
+ **The Rise of Paillier: Homomorphic Secret Sharing and Public-Key Silent OT**. [Article](https://eprint.iacr.org/2021/262).
+ **Extending Oblivious Transfers Efficiently**. [Article](https://www.iacr.org/archive/crypto2003/27290145/27290145.pdf).

[This](https://lostmediawiki.com/Home) is the lost media wiki, one of my favorite websites. It's devoted to finding and archiving 'lost' media -- ie, media that was once available for public viewing but can no longer be found.

<h2 style="color: #cc0000;">some open problems</h2>

+ **Zarankiewicz's Problem**. [Article](https://en.wikipedia.org/wiki/Zarankiewicz_problem). What is the maximum number of edges of a bipartite graph that does not contain $$K_{t,t}$$?
+ **Union-Closed Sets Conjecture**. [Article](https://gilkalai.wordpress.com/2022/11/17/amazing-justin-gilmer-gave-a-constant-lower-bound-for-the-union-closed-sets-conjecture/). Consider a family $$\mathcal{F}$$ of subsets of a set $$X$$ such that $$A,B\in\mathcal{F}$$ implies $$A\cup B\in\mathcal{F}$$. Then is there an element $$x\in X$$ such that $$d(x)\geq \|\mathcal{F}\|/2$$?
+ **Frankl's Antichain Conjecture**. Consider a convex family of subsets of $$[n]$$, where a family $$\mathcal{F}$$ is convex if $$A\subset B\subset C$$ and $$A$$ and $$C$$ in $$\mathcal{F}$$ implies that $$B\in\mathcal{F}$$. Then prove that there is an antichain $$\mathcal{G}$$ such that $$\|\mathcal{G}\|/\|\mathcal{F}\|\geq \binom{n}{\lfloor n/2\rfloor}/2^n$$.
