# Prior work arguing about assumption maturity, scrutiny, and confidence

Scope: works that argue, qualitatively or semi-quantitatively, about how much scrutiny public-key hardness assumptions have received, and how confidence should relate to the cryptanalysis an assumption has survived. A separate researcher covers explicit numeric quantification. Compiled 2026-10-09.

How sources were checked. Each entry below was opened at the listed URL or DOI. Bibliographic data was confirmed against the publisher page (Springer, Nature), the Crossref API record, the IACR ePrint landing page, the NIST PDF title page, or the author's own page. Claims come from full text where the full text was readable: the NIST IRs, Nature 2017, Bernstein's J. Cryptology 2024 paper, Peikert's survey, the Goldwasser–Kalai Springer full text, and the blog and project pages. Where only the abstract could be read, the entry says so. Full-text PDFs on eprint.iacr.org sit behind a bot-verification wall, and dblp returned "access denied" (Anubis) or HTTP 429. Neither was used, and no bot check was bypassed.

Abbreviations: KQ1, KQ2 and KQ3 are the three key questions (the three sections below).

---

## KQ1. What do these works claim about the relationship between amount/duration of scrutiny and confidence?

### Takeaway
Every thread agrees that confidence in an assumption comes mainly from attacks that have failed over time. NIST's own reports say this outright (McEliece's long attack history, the 3–5 years of public scrutiny it planned to allow, PQC getting less scrutiny than deployed RSA/ECC). Critics disagree about what counts as enough scrutiny and how to weigh it:
- Bernstein argues the stability of the best-attack exponent matters more than age or paper count.
- Theorists (Naor, Goldwasser–Kalai) treat falsifiability and simplicity as preconditions for scrutiny to mean anything. Goldwasser–Kalai explicitly leave "how well studied" out of their classification.
- SIKE (11 years from proposal to break) and Rainbow (17 years) are the standard counterexamples to treating duration alone as evidence.

None of these works measures cumulative public effort per assumption class. That is the gap our study fills.

### Cited Findings

#### Thread 1 — Theory of cryptographic assumptions

- **Naor, M. "On Cryptographic Assumptions and Challenges." In *Advances in Cryptology – CRYPTO 2003*, Springer LNCS, pp. 96–109, 2003. DOI 10.1007/978-3-540-45146-4_6.** Verified at [Springer](https://link.springer.com/chapter/10.1007/978-3-540-45146-4_6) and the Crossref record. The Springer page does not show the LNCS volume number; it is believed to be 2729, from memory, not verified.
  - Claim: proposes classifying assumptions by how hard it is to falsify them through a public "challenge" (competition) to their validity. It names cryptographic tasks, block ciphers first, that lack a good challenge of this kind (abstract).
  - Relevance: this is the founding framing in which confidence comes from an assumption being publicly exposed to refutation. It does not measure how much refutation effort any assumption has actually received.
- **Goldwasser, S., Tauman Kalai, Y. "Cryptographic Assumptions: A Position Paper." In *Theory of Cryptography (TCC 2016-A)*, Springer LNCS, pp. 505–522, 2016. DOI 10.1007/978-3-662-49096-9_21. ePrint 2015/907.** Verified at [Springer, full text](https://link.springer.com/chapter/10.1007/978-3-662-49096-9_21) and the [ePrint landing page](https://eprint.iacr.org/2015/907). The volume (believed to be 9562) is not shown on the page.
  - Claim: notes a recent proliferation of complex assumptions tangled up with the constructions that use them. Proposes "complexity assumptions" (independent of constructions, falsifiable) as the standard, and says any new assumption must be "an open invitation to refute or simplify".
  - Key point for us: the authors say their classification does not include robustness measures such as how well studied an assumption is, whether quantum attacks break it, or whether it has a worst-case/average-case reduction. They also list Factoring, RSA, DL, LPN and LWE together as traditional "well-studied" search assumptions.
  - Relevance: the leading theory position paper leaves amount-of-study as an unquantified, separate axis. Our study measures that axis.
- **Gentry, C., Wichs, D. "Separating succinct non-interactive arguments from all falsifiable assumptions." *STOC 2011*, pp. 99–108. DOI 10.1145/1993636.1993651. ePrint 2010/610.** Verified via the [Crossref record](https://api.crossref.org/works/10.1145/1993636.1993651) and the [ePrint landing page](https://eprint.iacr.org/2010/610).
  - Claim: formalizes a falsifiable assumption as a game with an efficient challenger, in the spirit of Naor 2003. Shows that black-box reductions cannot base SNARGs on any falsifiable assumption, including OWF, DDH, RSA and LWE (abstract).
  - Relevance: background only. It establishes falsifiability as the standard currency for "standard assumptions" and says nothing about scrutiny levels.
- **Peikert, C. "A Decade of Lattice Cryptography." *Foundations and Trends in Theoretical Computer Science* 10(4):283–424, 2016. DOI 10.1561/0400000074. ePrint 2015/939.** Verified via [Crossref](https://api.crossref.org/works/10.1561/0400000074) and the [ePrint landing page](https://eprint.iacr.org/2015/939). Full text read from the [author PDF](https://web.eecs.umich.edu/~cpeikert/pubs/lattice-survey.pdf).
  - Claims:
    - The survey explicitly does not cover cryptanalysis or concrete parameters.
    - It says NTRU has withstood significant cryptanalytic effort when properly parameterized, while early parameterizations were too compact.
    - It says ideal lattices have not been studied nearly as deeply computationally, so hardness conjectures about them "may not yet deserve as much confidence" (§4.3).
  - Relevance: a leading lattice theorist concedes that confidence in structured lattices depends on depth of study, which was then less than for general lattices. This motivates splitting structured from plain lattices.
- **Peikert, C. "What does GCHQ's 'cautionary tale' mean for lattice cryptography?" Blog post, 19 Feb 2015.** Verified at [web.eecs.umich.edu/~cpeikert/soliloquy.html](https://web.eecs.umich.edu/~cpeikert/soliloquy.html).
  - Claims:
    - The Soliloquy break targets a specialized principal-ideal problem with no worst-case reduction.
    - Many experts have tried and failed to beat generic attacks on Ideal-SVP, so the failed effort is evidence.
    - The reliance on short generators went unnoticed by experts for years.
  - Relevance: argues confidence from failed attack effort, paired with reductions. Also an early example that "years unnoticed" is weak evidence when few people are looking.
- **Crockett, E., Peikert, C. "Challenges for Ring-LWE." Cryptology ePrint Archive, Paper 2016/782 (preprint).** Verified at [ePrint 2016/782](https://eprint.iacr.org/2016/782).
  - Claim: as lattice cryptography enters practice there is an increasing need for further cryptanalytic effort and higher-confidence estimates. Publishes Ring-LWE/LWR challenge instances to attract that effort (abstract).
  - Relevance: puts Naor's challenge idea into practice for lattices. Implicitly concedes that lattice cryptanalytic effort was insufficient as of 2016.
- **van de Graaf, J., Lenstra, A. K. "Delphi: sharing assessments of cryptographic assumptions." Cryptology ePrint Archive, Paper 2024/157 (preprint).** Verified at [ePrint 2024/157](https://eprint.iacr.org/2024/157).
  - Claim: says assessing assumption strength is key to risk evaluation, and builds an online questionnaire to collect and publish researchers' beliefs about the strength of major assumptions (abstract).
  - Relevance: a direct expert-elicitation alternative to our bibliometric approach. No results were located; see Gaps.

#### Thread 2 — Koblitz & Menezes ("Another look" and related)

- **Koblitz, N., Menezes, A. "The brave new world of bodacious assumptions in cryptography." *Notices of the AMS* 57(3):357–365, 2010.** Verified at the [authors' page](https://math.uwaterloo.ca/~ajmeneze/anotherlook/ams2.shtml), which links the [AMS PDF](http://www.ams.org/notices/201003/rtx100300357p.pdf). The AMS PDF returned 403, so only the abstract was read.
  - Claim: newcomers would expect proofs to rest on a few well-studied natural problems. Instead many proofs rely on a "menagerie" of elaborate, unusual problems whose hardness has little support.
  - Relevance: the classic statement that confidence requires long study of natural problems, and that new assumptions lack it.
- **Koblitz, A. H., Koblitz, N., Menezes, A. "Elliptic curve cryptography: The serpentine course of a paradigm shift." *Journal of Number Theory* 131(5):781–814, 2011. DOI 10.1016/j.jnt.2009.01.006. ePrint 2008/390.** Verified via [Crossref](https://api.crossref.org/works/10.1016/j.jnt.2009.01.006), the [ePrint landing page](https://eprint.iacr.org/2008/390) and the [authors' page](https://math.uwaterloo.ca/~ajmeneze/anotherlook/serpentine.shtml). Abstract only; the full text was not accessible.
  - Claim: over about sixteen years ECC went from widely mistrusted or misunderstood to almost unquestioned acceptance. The authors contrast this history with an "Ideal Model" of cryptographic R&D (abstract).
  - Relevance: the main historical case study of how long ECDLP took to earn trust. It gives a duration (about 16 years) but not an effort measure.
- **Koblitz, N., Menezes, A. "A Riddle Wrapped in an Enigma." *IEEE Security & Privacy* 14(6):34–42, 2016. DOI 10.1109/MSP.2016.120. Longer version: ePrint 2015/1018.** Verified via [Crossref](https://api.crossref.org/works?query.bibliographic=Koblitz+Menezes+riddle+wrapped+in+an+enigma&rows=3), the [ePrint landing page](https://eprint.iacr.org/2015/1018) and the [authors' page](https://math.uwaterloo.ca/~ajmeneze/anotherlook/miscellaneous.shtml), which lists it as an abridged version in IEEE S&P 14 (2016).
  - Claim: evaluates theories about why NSA's August 2015 PQC statement played down ECC (abstract).
  - Limitation: the full text could not be read, so its specific statements on PQC/ECC maturity are not recorded here (see Gaps).
- **Koblitz, N., Menezes, A. "Critical perspectives on provable security: Fifteen years of 'another look' papers." *Advances in Mathematics of Communications* 13(4):517–558, 2019. DOI 10.3934/amc.2019034. ePrint 2019/1336.** Verified via [Crossref](https://api.crossref.org/works/10.3934/amc.2019034) and the [ePrint landing page](https://eprint.iacr.org/2019/1336).
  - Claim: a guide to their critiques of security "proofs", with new examples (abstract).
  - Relevance: the citable umbrella reference for the K&M position that proofs do not replace cryptanalytic history. The full text was not read.
- **Koblitz, N., Menezes, A. "Another look at security definitions." *Advances in Mathematics of Communications* 7(1):1–38, 2013. DOI 10.3934/amc.2013.7.1. ePrint 2011/343.** Verified via [Crossref](https://api.crossref.org/works/10.3934/amc.2013.7.1) and the [authors' page](https://math.uwaterloo.ca/~ajmeneze/anotherlook/definitions.shtml).
  - Claim: real uncertainty about which security definitions are correct, as models miss attack types (abstract).
  - Relevance: low. It concerns definitions, not assumption maturity. Cite only if the "proofs vs. cryptanalysis" theme is wanted.

#### Thread 3 — Bernstein (and Lange) on cryptanalytic attention and risk

- **Bernstein, D. J., Lange, T. "Post-quantum cryptography." *Nature* 549(7671):188–194, 2017. DOI 10.1038/nature23461. Preprint: ePrint 2017/314.** Verified, full text read, at [nature.com](https://www.nature.com/articles/nature23461) and via [Crossref](https://api.crossref.org/works/10.1038/nature23461).
  - On selection: the authors say their list of systems "is biased towards proposals that have survived decades of study".
  - On McEliece:
    - Dozens of ISD papers have left the pre-quantum attack exponent c in (c+o(1))^w unchanged, which they call a remarkably stable track record.
    - McEliece's original 2^64-target parameters took more than 2^60 CPU cycles to break 30 years later.
    - Original McEliece/Niederreiter are the only PQ encryption systems with enough study to recommend.
  - On lattices: the attack avenues (cyclotomic structure; recent exponent improvements for generic lattices) are new and "not adequately explored". Much more research is needed for confidence.
  - Relevance: the canonical "stability of best-attack exponent" argument for codes over lattices.
- **Bernstein, D. J. "Cryptographic Competitions." *Journal of Cryptology* 37, Article 7, 2024 (published online 8 Dec 2023). DOI 10.1007/s00145-023-09467-1. ePrint 2020/1608.** Verified via the PDF header (J Cryptol (2024) 37:7, received 2020, accepted April 2023) from [par.nsf.gov](https://par.nsf.gov/servlets/purl/10485678) and [Crossref](https://api.crossref.org/works/10.1007/s00145-023-09467-1). Full text read.
  - §3.2 says breaking an algorithm can take "years or even decades of public attack development". Examples: MD5, 12 years to a public collision; SIKE, advertised as "a decade unscathed" and then broken.
  - §3.2 also models p(M), the probability a proposal is publicly broken within M months. It estimates p(12) ≈ 1/3 from 5 of the 15 AES submissions being broken within 12 months. It argues that a winner chosen after 36 months is breakable with probability (p(∞)−p(36))/(1−p(36)), which may exceed 1%.
  - §3.3 ("The Overworked Cryptanalyst") argues the binding constraint is cryptanalyst throughput: a limited pool of experts spread across many proposals. It quotes the NESSIE comment that AES-finalist evaluation effort was very limited compared with IBM's 17 man-years on DES.
  - Relevance: the closest prior argument that scrutiny is a scarce, measurable resource. This is directly the premise of our study.
- **Bernstein, D. J. "Double encryption: Analyzing the NSA/GCHQ arguments against hybrids." Blog post, 2024-01-02.** Verified at [blog.cr.yp.to/20240102-hybrid.html](https://blog.cr.yp.to/20240102-hybrid.html).
  - Base rates: of 69 NIST round-1 PQC submissions (2017), 48% were broken by then (smallest parameters weaker than AES-128). Of the 48 unbroken in round 1, 25% were broken later. Of the 28 round-2 submissions, 36% were broken.
  - Asks where the studies of how often cryptosystems fail are, and challenges agencies to quantify "breakthrough" risk.
  - Relevance: semi-quantitative base rates; see KQ2.
- **Bernstein, D. J. "McEliece standardization: Looking at what's happening, and analyzing rationales." Blog post, 2025-04-23.** Verified at [blog.cr.yp.to/20250423-mceliece.html](https://blog.cr.yp.to/20250423-mceliece.html).
  - Claims the core argument for McEliece is how well its security has held up, "not just its age, and not just the number of papers".
  - Contrasts a 2010 lattice paper's "2^150" estimate for dimension 256 with NIST's current 2^135–2^158 window for dimension 512.
  - Disputes NIST IR 8545's statement that recent algebraic attacks weaken the "long history" argument.
  - Relevance: explicitly separates three metrics (age, paper count, stability). Our study measures paper count, so the distinction should be acknowledged.
- **Bernstein, D. J. "Understanding lattice risks: Many differences between marketing and reality." Blog post, 2026-06-30.** Verified at [blog.cr.yp.to/20260630-risk.html](https://blog.cr.yp.to/20260630-risk.html).
  - Argues that cumulative small improvements from many attack papers moved lattice security estimates. FrodoKEM's dimension increase is his example.
  - Asks whether today's ML-KEM dimensions will look as naive in 15 years.
  - Calls worst-case/average-case reductions an alarm bell rather than a comfort.
  - Relevance: a 2026 statement of the "lattice estimates keep eroding" position.
- **Bernstein, D. J., Chuengsatiansup, C., Lange, T., van Vredendaal, C. "NTRU Prime: Reducing Attack Surface at Low Cost." In *Selected Areas in Cryptography – SAC 2017*, Springer LNCS, pp. 235–260, 2018. DOI 10.1007/978-3-319-72565-9_12. ePrint 2016/461.** Verified via [Crossref](https://api.crossref.org/works/10.1007/978-3-319-72565-9_12) and the [ePrint landing page](https://eprint.iacr.org/2016/461). The volume (believed to be 10719) was not shown.
  - Claim: several ideal-lattice systems have been broken by attacks that exploit ring structure, and the same structures appear in NTRU and Ring-LWE proposals. NTRU Prime removes them (abstract).
  - Relevance: the "attack surface" argument, in which structure that has had less study is a risk independent of time.
- **NTRU Prime Risk-Management Team. "Risks of lattice KEMs." 99 pp., 2021-10-31.** URL: https://ntruprime.cr.yp.to/latticerisks-20211031.pdf. Existence, date and contents were verified via the [NTRU Prime warnings page](https://ntruprime.cr.yp.to/warnings.html); the PDF itself could not be fetched.
  - Claim: lattice cryptography is much riskier than commonly acknowledged. The document classifies "known attack avenues not ruled out by theorems" per KEM in a table (structured lattices, cyclotomics, quotients, extra samples, and others).
  - Relevance: a qualitative per-scheme risk taxonomy, not an effort measure.
- **Bernstein, D. J., Lange, T. "Non-randomness of S-unit lattices." Cryptology ePrint Archive, Paper 2021/1428 (preprint).** Verified at [ePrint 2021/1428](https://eprint.iacr.org/2021/1428).
  - Claim: S-unit attacks are a fast-developing line against structured lattices. Previously claimed "barriers" rest on spherical models that underestimate these attacks (abstract).
  - Relevance: an example of how much of structured-lattice cryptanalysis is recent and still moving.
- **Bernstein, D. J. "Visualizing size-security tradeoffs for lattice-based encryption." Cryptology ePrint Archive, Paper 2019/655 (preprint).** Verified at [ePrint 2019/655](https://eprint.iacr.org/2019/655).
  - Claim: gives reasons to distrust graphs that compare lattice systems' security against known attacks, because of problems with both the data points and the graphing (abstract).
  - Relevance: tangential; it is about the instability of lattice security estimates rather than scrutiny.
- **Classic McEliece team. Project website, "Intro" and "Papers" pages (accessed 2026-10-09).** [classic.mceliece.org](https://classic.mceliece.org/) and [papers](https://classic.mceliece.org/papers.html).
  - Claim: the McEliece security level "has remained remarkably stable, despite half a century of attack papers".
  - The Papers page traces ISD to Prange (1962) and lists attack literature by category. My count on 2026-10-09: 60 ISD, 33 other attack strategies, 8 chosen-ciphertext, 18 side-channel/fault, 43 further papers.
  - Relevance: a submitter-curated attack bibliography. It can serve as a recall check for our syndrome-decoding class (overlaps with our study).

#### Thread 4 — NIST PQC reports

- **Chen, L., Jordan, S., Liu, Y.-K., Moody, D., Peralta, R., Perlner, R., Smith-Tone, D. *Report on Post-Quantum Cryptography.* NISTIR 8105, April 2016. DOI 10.6028/NIST.IR.8105.** Verified via the [NIST PDF](https://nvlpubs.nist.gov/nistpubs/ir/2016/NIST.IR.8105.pdf) title page; full text read.
  - PQ proposals "have not received nearly as much scrutiny" as currently deployed algorithms. The only exception is hash-based signatures.
  - The lack of known attacks is what justifies today's public-key cryptography.
  - McEliece (1978) "has not been broken since". Many multivariate schemes have been broken.
  - Isogenies, like braid-group proposals, have had too little analysis for much confidence.
  - The submission deadline was set to allow "3 to 5 years of public scrutiny".
- **Alagic, G., et al. *Status Report on the First Round of the NIST PQC Standardization Process.* NISTIR 8240, January 2019. DOI 10.6028/NIST.IR.8240.** Verified via the [NIST PDF](https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.8240.pdf); full text read.
  - NIST weighed "the overall quantity, quality, and maturity of analysis" of each candidate.
  - NTRU has been "reasonably-well understood and scrutinized for decades".
  - Classic McEliece has a long history of analysis that has not significantly changed attack complexity.
  - BIKE's QC-MDPC basis is fairly new (2010s). Rank-metric codes are new and less studied than Hamming-metric codes or lattices.
  - SIKE's problem "has not been studied as much" as others.
- **Alagic, G., et al. *Status Report on the Second Round of the NIST PQC Standardization Process.* NISTIR 8309, July 2020. DOI 10.6028/NIST.IR.8309.** Verified via the [NIST PDF](https://nvlpubs.nist.gov/nistpubs/ir/2020/NIST.IR.8309.pdf); full text read.
  - Goppa-code McEliece has been well known "for over 40 years with only incremental improvements on attacks", which inspires confidence.
  - MLWE is "a relatively young problem", but no known attack beats plain LWE.
  - HQC has "a mature analysis". The security analyses of ROLLO and RQC need more time to mature.
  - Cryptanalytic results "undermined NIST's confidence in the maturity" of some schemes.
- **Alagic, G., et al. *Status Report on the Third Round of the NIST PQC Standardization Process.* NIST IR 8413-upd1, July 2022 (updated September 2022). DOI 10.6028/NIST.IR.8413-upd1.** Verified via the [NIST PDF](https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8413-upd1.pdf) and the [CSRC page](https://csrc.nist.gov/pubs/ir/8413/upd1/final); full text read.
  - Kyber "inherits a strong theoretical security foundation from decades of lattice cryptography literature" and has been "thoroughly analyzed".
  - NTRU (1996) remains unbroken, and "This long security analysis provides confidence".
  - Classic McEliece: confidence rests mostly on the 1978 scheme's long history of surviving cryptanalysis. NIST is "confident in the security", but there is no urgency because of key size.
  - SIKE "needs further study, as it is still a relatively new scheme".
  - Attacks on GeMSS and Rainbow "undermined NIST's confidence in its maturity". The Rainbow key recovery took a little over two days on a laptop.
  - A break of any structured lattice would reduce confidence in all of them, so NIST will hedge with a non-lattice KEM.
  - NIST values a diversity of assumptions so that a single breakthrough does not leave no standard.
- **Alagic, G., Bros, M., Ciadoux, P., Cooper, D., Dang, Q., Dang, T., Kelsey, J., Lichtinger, J., Liu, Y.-K., Miller, C., Moody, D., Peralta, R., Perlner, R., Robinson, A., Silberg, H., Smith-Tone, D., Waller, N. *Status Report on the Fourth Round of the NIST PQC Standardization Process.* NIST IR 8545, March 2025. DOI 10.6028/NIST.IR.8545.** Verified via the [CSRC page](https://csrc.nist.gov/pubs/ir/8545/final) and the [NIST PDF](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8545.pdf); full text read.
  - All fourth-round candidates were chosen to rest on assumptions that differ significantly from ML-KEM's, to reduce the risk that a single cryptanalytic breakthrough leaves no viable standard.
  - HQC was chosen over BIKE because its decryption-failure-rate (DFR) analysis is "more mature and stable". NIST says it has confidence in the IND-CPA security of both.
  - Classic McEliece:
    - Confidence was "mostly established based on the scheme's long history of surviving cryptanalysis".
    - ISD dates to Prange (1962), and "most of the change in concrete security is due to improvements that were discovered more than 30 years ago".
    - Recent algebraic and distinguisher work "somewhat weaken[s] the argument" from long history. The case for treating it as especially conservative is "somewhat undermine[d]".
    - It was not selected because of limited demand and the parallel ISO process.
- **NIST. "NIST Selects HQC as Fifth Algorithm for Post-Quantum Encryption." News release, 11 March 2025.** Verified at [nist.gov](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption).
  - Calls HQC a backup "in case ML-KEM proves to be vulnerable", resting on error-correcting codes rather than structured lattices.

#### Thread 5 — Breaks after long scrutiny (base rates)

- **Castryck, W., Decru, T. "An Efficient Key Recovery Attack on SIDH." In *Advances in Cryptology – EUROCRYPT 2023*, Springer LNCS, pp. 423–447, 2023. DOI 10.1007/978-3-031-30589-4_15. ePrint 2022/975.** Verified via [Crossref](https://api.crossref.org/works/10.1007/978-3-031-30589-4_15) and the [ePrint landing page](https://eprint.iacr.org/2022/975).
  - Claim: heuristic polynomial-time key recovery using Kani's reducibility criterion and the torsion-point images. SIKEp434 falls in about ten minutes on one core (abstract).
  - Base-rate data point: SIDH was proposed by Jao and De Feo in 2011 (next entry), so about 11 years passed from proposal to break.
- **Jao, D., De Feo, L. "Towards Quantum-Resistant Cryptosystems from Supersingular Elliptic Curve Isogenies." In *Post-Quantum Cryptography (PQCrypto 2011)*, LNCS, pp. 19–34, 2011. DOI 10.1007/978-3-642-25405-5_2.** Verified via the Crossref record ([doi.org](https://doi.org/10.1007/978-3-642-25405-5_2)).
  - Use: the proposal date for the SIKE base-rate calculation.
- **Costello, C. "The Case for SIKE: A Decade of the Supersingular Isogeny Problem." Cryptology ePrint Archive, Paper 2021/543 (preprint, last revised 2021-06-17).** Verified at [ePrint 2021/543](https://eprint.iacr.org/2021/543).
  - Claim: written for SIDH's 10th anniversary, it defends SIKE on points including "the rise of classical hardness" and concrete cryptanalytic clarity. It offers $55k in challenge prizes and urges other schemes to create comparable challenges (abstract).
  - Relevance: the clearest documented case of a decade-of-scrutiny argument published about a year before a total break. Bernstein (J. Cryptology 2024, §3.2) uses it as exactly that example.
- **Beullens, W. "Breaking Rainbow Takes a Weekend on a Laptop." In *Advances in Cryptology – CRYPTO 2022*, Springer LNCS, pp. 464–479, 2022. DOI 10.1007/978-3-031-15979-4_16. ePrint 2022/214.** Verified at [Springer](https://link.springer.com/chapter/10.1007/978-3-031-15979-4_16) and the [ePrint landing page](https://eprint.iacr.org/2022/214).
  - Claim: key recovery for the SL1 parameters of a NIST finalist in about 53 hours on a laptop (abstract).
- **Ding, J., Schmidt, D. "Rainbow, a New Multivariable Polynomial Signature Scheme." In *Applied Cryptography and Network Security (ACNS 2005)*, LNCS, pp. 164–175, 2005. DOI 10.1007/11496137_12.** Verified via the Crossref record ([doi.org](https://doi.org/10.1007/11496137_12)).
  - Use: Rainbow's proposal date. About 17 years passed to a practical key recovery, although Rainbow had suffered partial attacks before 2022 (NIST IR 8413 records a loss of 20–55 bits earlier in round 3).
- **Mojaveri, S. J., Khosravi, A. "The McEliece Cryptosystem After Nearly Five Decades: A Survey of Security, Cryptanalysis, and Future Directions." Cryptology ePrint Archive, Paper 2026/1512 (preprint, 2026).** Verified at [ePrint 2026/1512](https://eprint.iacr.org/2026/1512) (title and preprint status); author names come from the repository's ePrint metadata.
  - Claim: argues McEliece's history supports neither "unchanged" nor "broken" narratives. Its longevity reflects a conservative foundation that survived repeated reassessment while parameters evolved (abstract).
  - Relevance: a 2026 counterweight to simple age-based arguments.

#### Government position (adjacent, useful for motivation)

- **ANSSI. *ANSSI views on the Post-Quantum Cryptography transition.* Position paper, 2022 (web listing dated 4 Jan 2022).** Verified at [messervices.cyber.gouv.fr](https://messervices.cyber.gouv.fr/guides/en-anssi-views-post-quantum-cryptography-transition).
  - Claim: PQC algorithms are not yet mature, "Many aspects lack cryptanalytical hindsight", and immaturity will persist after NIST's standards appear. Hybridation with pre-quantum cryptography is mandatory during the transition phases.
  - Note: one source dates the PDF header 30 March 2022.

### Inferences
- The field's working epistemology is that confidence ≈ survived attack effort × time, discounted by structure. That is stated qualitatively in every NIST report from 8105 to 8545, but nobody measures the "effort" term per assumption. Our bibliometric counts give that term a number.
- Three distinct maturity metrics are in use and are often conflated. Our study should say which one it measures (the second) and why:
  1. calendar age since proposal (NIST: "decades", "relatively young");
  2. volume of attack work (Bernstein–Lange: "dozens of attack papers"; the Classic McEliece paper list);
  3. stability of the best-attack exponent or concrete estimate (Bernstein; NIST 8545 on ISD improvements predating 1995).
- The SIKE and Rainbow breaks show that calendar age is a poor proxy when the attacker pool is small. That supports measuring effort, not duration. It is an inference that small attention explains these breaks; the sources show only duration and break.

### Gaps
- Theory works (Naor, Goldwasser–Kalai, Gentry–Wichs) do not say how long an assumption must be studied. Goldwasser–Kalai explicitly leave "how well studied" outside their framework. I found no theory paper that states a minimum scrutiny period.
- NIST's "3 to 5 years" (8105) is a process schedule, not a stated sufficiency threshold.

---

## KQ2. Do any of them estimate the amount of scrutiny numerically?

### Takeaway
Only partially. Numbers in this literature are base rates of breaks, durations, or curated paper lists, not measured effort per assumption. The closest items are:
- Bernstein's break-rate statistics for NIST PQC submissions and his p(M) model;
- the Classic McEliece curated attack-paper list;
- the NESSIE "17 man-years" figure for DES, which Bernstein quotes.

These overlap with our study and should be cited as precursors or recall checks.

### Cited Findings
- 69 NIST round-1 submissions: 48% broken by Jan 2024. Of the 48 that survived round 1, 25% were broken later. Of the 28 round-2 submissions, 36% were broken. — [Bernstein blog 2024-01-02](https://blog.cr.yp.to/20240102-hybrid.html)
- p(12) ≈ 1/3 from 5 of the 15 AES submissions publicly broken within 12 months. This is a model of the probability that a winner is breakable after M months of scrutiny, and a call for more data. — [Bernstein, J. Cryptology 2024, §3.2](https://doi.org/10.1007/s00145-023-09467-1)
- The NESSIE comments on the AES finalists compared the "very limited" effort on finalists with "17 man-years spent by IBM on DES". This is an effort-in-person-years figure, quoted secondhand. — [Bernstein, J. Cryptology 2024, §3.3](https://doi.org/10.1007/s00145-023-09467-1); the original NESSIE document was not opened (see Gaps).
- Curated McEliece attack bibliography (counted 2026-10-09): 60 ISD papers (from Prange 1962), 33 other attack strategies, 8 CCA, 18 side-channel/fault, 43 further. — [classic.mceliece.org/papers.html](https://classic.mceliece.org/papers.html)
- "Dozens of attack papers" on ISD with a stable exponent. McEliece's original 2^64-target parameters needed more than 2^60 CPU cycles to break 30 years later. — [Bernstein & Lange, Nature 2017](https://www.nature.com/articles/nature23461)
- Most ISD concrete-security change came from improvements more than 30 years old; ISD originates in 1962. — [NIST IR 8545 §3.3](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8545.pdf)
- Durations: ECC took about 16 years to gain acceptance ([Koblitz, Koblitz & Menezes 2011](https://doi.org/10.1016/j.jnt.2009.01.006)). SIDH ran about 11 years from 2011 proposal ([Jao & De Feo](https://doi.org/10.1007/978-3-642-25405-5_2)) to break ([Castryck & Decru](https://doi.org/10.1007/978-3-031-30589-4_15)). Rainbow ran about 17 years from 2005 ([Ding & Schmidt](https://doi.org/10.1007/11496137_12)) to practical key recovery ([Beullens](https://doi.org/10.1007/978-3-031-15979-4_16)). MD5 took 12 years to a public collision ([Bernstein 2024](https://doi.org/10.1007/s00145-023-09467-1)).
- Lattice estimate drift: a 2010 paper estimated 2^150 for dimension 256, while NIST's current window for dimension-512 Kyber is 2^135–2^158. — [Bernstein blog 2025-04-23](https://blog.cr.yp.to/20250423-mceliece.html). This is Bernstein's comparison, and the numbers are his quotations of the sources.
- Expert-belief elicitation (Delphi) is proposed but no aggregated results were found. — [van de Graaf & Lenstra, ePrint 2024/157](https://eprint.iacr.org/2024/157)

### Inferences
- No work found here counts papers or authors per assumption class across ECDLP, lattices and codes on a common basis. Bernstein's 2024 call for "studies of how often cryptosystems fail" and his "overworked cryptanalyst" throughput argument both point to that missing measurement.
- The Classic McEliece list (about 101 papers across the ISD, other-attack and CCA sections combined) can be compared with our 290 syndrome-decoding papers. It is a submitter-curated list, so differences in inclusion criteria are expected, and it is useful as a recall check.

### Gaps
- The original NESSIE "17 man-years" document was not opened. The figure is cited secondhand via Bernstein 2024.
- The 2020 Bernstein talk cited for "PDF page 91" breakage counts was not opened.
- No Delphi results were located.

---

## KQ3. What do they say comparing ECDLP vs lattices vs codes in terms of maturity?

### Takeaway
Rough consensus ordering across sources: ECDLP/RSA (deployed, most scrutinized pre-quantum; NIST 8105) > binary-Goppa McEliece (oldest PQ system, most stable attack exponent; NIST 8240/8309/8413/8545, Bernstein–Lange) ≥ plain LWE/NTRU (decades of lattice work, but estimates keep shifting) > structured/module lattices (MLWE "relatively young"; ideal lattices less studied, per Peikert) ≈ quasi-cyclic codes (BIKE/HQC, 2010s) > isogenies and multivariate (less studied, then broken).

The live disagreement: NIST and the lattice community treat lattices as "thoroughly analyzed". Bernstein/NTRU Prime treat the continuing erosion of lattice security estimates and structure-specific attack avenues as evidence of immaturity, and argue that NIST's 2025 downgrade of McEliece's "long history" argument gets the comparison backwards.

### Cited Findings
- **ECDLP and RSA vs PQ**
  - Deployed algorithms have received far more scrutiny than any PQ proposal. — [NISTIR 8105](https://nvlpubs.nist.gov/nistpubs/ir/2016/NIST.IR.8105.pdf)
  - ANSSI requires hybrids with well-understood pre-quantum cryptography because PQ "lack[s] cryptanalytical hindsight". — [ANSSI 2022](https://messervices.cyber.gouv.fr/guides/en-anssi-views-post-quantum-cryptography-transition)
  - ECC itself needed about 16 years to win acceptance. — [Koblitz, Koblitz & Menezes 2011](https://doi.org/10.1016/j.jnt.2009.01.006)
- **Codes (Goppa) vs lattices**
  - NIST: McEliece's long history with only minor changes to best-attack complexity is the basis of confidence. — [NISTIR 8240](https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.8240.pdf), [NISTIR 8309](https://nvlpubs.nist.gov/nistpubs/ir/2020/NIST.IR.8309.pdf), [NIST IR 8413](https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8413-upd1.pdf)
  - NIST 2025: recent algebraic and distinguisher progress "somewhat undermines" treating McEliece as especially conservative. — [NIST IR 8545](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8545.pdf)
  - Bernstein disputes this: the cited papers failed to reduce McEliece security, while lattice attacks keep succeeding. — [blog 2025-04-23](https://blog.cr.yp.to/20250423-mceliece.html)
  - Bernstein–Lange: McEliece/Niederreiter are the only PQ encryption systems studied enough to recommend, and lattices need much more research. — [Nature 2017](https://www.nature.com/articles/nature23461)
- **Plain vs structured lattices**
  - NIST: MLWE is relatively young but no worse than LWE under known attacks. — [NISTIR 8309](https://nvlpubs.nist.gov/nistpubs/ir/2020/NIST.IR.8309.pdf)
  - NIST: Kyber has been thoroughly analyzed, while a structured-lattice break would hit all structured-lattice schemes. — [NIST IR 8413](https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8413-upd1.pdf)
  - Peikert: ideal lattices are much less studied computationally. — [Peikert 2016](https://doi.org/10.1561/0400000074)
  - Ring structure has enabled breaks of some ideal-lattice systems. — [NTRU Prime, SAC 2017](https://doi.org/10.1007/978-3-319-72565-9_12); [Bernstein & Lange, S-unit](https://eprint.iacr.org/2021/1428); [NTRU Prime risk table](https://ntruprime.cr.yp.to/warnings.html)
- **QC codes and other families**
  - BIKE's basis dates from the 2010s. Rank-metric codes are less studied than Hamming-metric codes or lattices. — [NISTIR 8240](https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.8240.pdf)
  - HQC's DFR analysis is "more mature and stable" than BIKE's. — [NIST IR 8545](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8545.pdf)
  - HQC was selected as a backup on different mathematics. — [NIST news 2025](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption)
- **Isogenies and multivariate**
  - Isogenies had "not been studied as much" (2019), and SIKE was "relatively new" (2022). — [NISTIR 8240](https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.8240.pdf), [NIST IR 8413](https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8413-upd1.pdf)
  - Many multivariate schemes were broken. — [NISTIR 8105](https://nvlpubs.nist.gov/nistpubs/ir/2016/NIST.IR.8105.pdf)
  - Rainbow and GeMSS breaks undermined confidence in multivariate maturity. — [NIST IR 8413](https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8413-upd1.pdf)

### Inferences
- The qualitative "maturity" claims are mostly about age and estimate stability, not effort. Our finding (provisional, from SUMMARY.md) bears on this: lattices have received about 1.3–2.6× the cumulative visible effort of ECDLP, all since 2016, while syndrome decoding has received about 0.6–0.8×. That partly reverses the folk ordering. Lattices are "young" in calendar terms but no longer under-studied by volume. Codes are old but have had less total visible effort than ECDLP.
- NIST's grounds for keeping McEliece out of FIPS are non-security (demand, ISO). Its maturity language for McEliece has weakened over time: 8309 says the long history "inspires" confidence, while 8545 says recent work "somewhat weaken[s]" the long-history argument. Our effort data could inform that debate, but it cannot settle the stability-vs-volume disagreement.

### Gaps
- **Unverified or not fully read items**
  - Full text of Koblitz & Menezes "A Riddle Wrapped in an Enigma" (ePrint PDF behind a bot check; IEEE paywalled). Its specific statements about lattice/PQC maturity versus ECC are therefore not recorded.
  - Full texts of "Serpentine course" (JNT, ScienceDirect 403) and "Bodacious assumptions" (AMS PDF 403). Only abstracts were read.
  - Full text of Costello 2021/543. Its ten points, including how it argues "rise of classical hardness", were not read.
  - "Risks of lattice KEMs" PDF (fetch failed on an HTTP parse error). Only the summary table on the warnings page was read.
- **Not located or not attempted**
  - pqc-forum threads (Google Groups) were not accessed. No specific NIST/pqc-forum statements on "maturity" outside the IRs are recorded.
  - Commentary drawing "lessons about scrutiny duration" from SIKE beyond Bernstein 2024 and NIST IR 8545: a search did not surface a verifiable primary source. Steven Galbraith's ellipticnews blog was named in the brief but not found.
  - BSI TR-02102-1 / "Quantum-safe cryptography" guidance recommending FrodoKEM and Classic McEliece as conservative choices: seen only in secondary sources and slides, so not listed as verified.
  - Micciancio & Regev, "Lattice-based cryptography" (2009 book chapter): not checked.
  - Bernstein's 2016 blog "Some challenges in post-quantum standardization": seen in the blog index but not read.
- **Index access**: dblp was blocked (Anubis access-denied and HTTP 429), so dblp was not used for verification. Crossref, publishers, ePrint landing pages and NIST were used instead. LNCS volume numbers for Naor 2003 (2729), Goldwasser–Kalai 2016 (9562), NTRU Prime SAC 2017 (10719) and Castryck–Decru (14008) come from memory and were not shown on the verifying pages. Check them before typesetting.
