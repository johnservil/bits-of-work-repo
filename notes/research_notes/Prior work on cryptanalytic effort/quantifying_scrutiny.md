# Prior attempts to quantify cryptanalytic effort or public scrutiny per hardness assumption

Scope note (2026-10-09). Every source below was opened and its metadata checked against the
verifying URL given. Items I could not verify are listed under the Gaps of the relevant question.
"Relation to our study" says whether a source pre-empts, partially overlaps with, or only gives
context for the 2026 study (paper counts, author FTE-years and records per PKE assumption).

## Q1. Has anyone counted papers, people or person-years of cryptanalysis per hardness assumption or per cryptosystem?

### Takeaway
I found no prior work that does what our study does: measure, across assumption classes, how much
public cryptanalysis each PKE assumption has received, using paper counts, author headcounts or
person-years. The closest work counts in three narrower ways. (a) Bernstein (2023) counts breaks
among NIST PQC submissions, not effort, and names cryptanalytic attention as an open question.
(b) The Classic McEliece rationale counts about 30 attack papers on one assumption. (c) Zheng & Kang
(2024) run a Scopus bibliometric study of a single attack technique, lattice attacks on RSA: 400
papers and 61 core authors. The only person-year figure I found is an anecdote: the NESSIE claim
that IBM spent "17 man-years" on DES.

### Cited Findings
- **Bernstein, D. J. "Quantifying risks in cryptographic selection processes." IACR ePrint 2023/1838 (2023, rev. 2023-12-02).**
  - It compares the known-failure rates of three groups of NIST PQC submissions. 33 of the 69 round-1 submissions are broken (about 48%). 12 of the 48 submissions not broken during round 1 are broken (25%). 10 of the 28 selected for round 2 are broken (about 36%). The paper reports the differences as statistically significant.
  - It measures outcomes (broken or not), not effort. It explicitly lists as an untested hypothesis ("Hypothesis 6") that NIST selection draws more cryptanalytic attention, and says studying this "would be interesting". That leaves effort measurement open.
  - Relation to our study: closest in spirit, a quantitative risk study of PQC assumptions, but it does not pre-empt us. It counts breaks per submission, not papers or people per assumption. — [ePrint 2023/1838](https://eprint.iacr.org/2023/1838); [full text, cr.yp.to](https://cr.yp.to/papers/qrcsp-20231202.pdf)
- **Bernstein, D. J. "Cryptographic Competitions." Journal of Cryptology 37, article 7 (published online 2023-12-08; issue 2024); ePrint 2020/1608.**
  - It tabulates how many submissions survived each phase of DES, AES, eSTREAM, SHA-3, CAESAR, NISTPQC and NISTLWC. For example, NISTPQC went from 69 to 26 to 15 candidates, and eSTREAM from 34 to 27 to 16 to 8.
  - It argues qualitatively that public cryptanalysis is throughput-limited: the world has a limited number of experts able and willing to do it. It also says it is unclear whether competitions raise "analysis per year per submission".
  - It proposes a model in which each proposal has probability p(M) of being publicly broken within M months. The later qrcsp paper reports that this model estimated p(12) ≈ 1/3 from the 15 AES submissions.
  - Relation to our study: context and motivation. It poses effort-per-target questions without measuring them. — [ePrint 2020/1608](https://eprint.iacr.org/2020/1608); [DOI 10.1007/s00145-023-09467-1 (Crossref-verified)](https://doi.org/10.1007/s00145-023-09467-1); [PDF](https://cr.yp.to/papers/competitions-20201225.pdf)
- **Classic McEliece team. "Classic McEliece: conservative code-based cryptography: design rationale." 23 October 2022.**
  - It lists "30 publications" after 1978 that study the one-wayness of McEliece and introduce better non-quantum attacks: Clark–Cain 1981 through Carrier–Debris-Alazard–Meyer-Hilfiger–Tillich 2022. It argues that all of these improvements vanish into the o(1) term of the key-size formula.
  - This is a hand-curated paper count for one assumption (generic binary-Goppa syndrome decoding / ISD), used to argue for confidence.
  - Relation to our study: partial overlap for the syndrome-decoding class only. It is a useful external check on our ISD subset; we count about 290 syndrome-decoding papers overall, so their 30 is a narrow "core ISD" list. — [classic.mceliece.org rationale PDF](https://classic.mceliece.org/mceliece-rationale-20221023.pdf); companion [guide for security reviewers, 2022-10-23](https://classic.mceliece.org/mceliece-security-20221023.pdf)
- **Zheng, M. and Kang, H. "Lattice-based cryptanalysis of RSA-type cryptosystems: a bibliometric analysis." Cybersecurity 7, article 74 (2024).**
  - It searches Scopus with the keywords "lattice" and "RSA", then screens the results by hand, finding 400 publications from 1996 to 2023.
  - It identifies 61 core authors (those with 4 or more papers) who wrote 275 of the papers (68.75%). It also maps countries, institutions and co-authors with CiteSpace and VOSviewer.
  - Relation to our study: the closest methodological precedent, a bibliometric count of attack papers and authors for one attack line on one assumption family. Its scope is one technique (Coppersmith-style lattice attacks), not effort across assumptions. It can serve as a cross-check for part of our factoring class. — [DOI 10.1186/s42400-024-00289-7 (Crossref-verified)](https://doi.org/10.1186/s42400-024-00289-7); [Springer article page](https://link.springer.com/article/10.1186/s42400-024-00289-7)
- **NESSIE project (B. Preneel, A. Bosselaers, V. Rijmen, … , L. Knudsen, H. Raddum; editor S. Murphy). "Comments by the NESSIE Project on the AES Finalists." NESSIE deliverable D04, NES/DOC/RHU/WP3/D04/1 (2000).**
  - It states that security evaluation of the five AES finalists was "very limited", compared with "the 17 man-years spent by IBM on DES in the 1970s".
  - It notes that most AES3 papers were about performance rather than security.
  - This is the only explicit person-year comparison of scrutiny between primitives that I found. Bernstein's competitions paper (§3.3) quotes it.
  - Relation to our study: context and anecdote. It is a single person-year figure and its original source is not given. — [NESSIE D04 PDF (Wayback copy of cosic.esat.kuleuven.be)](https://web.archive.org/web/2005/https://www.cosic.esat.kuleuven.be/nessie/deliverables/D4_NessieAESInput.pdf)
- **Gupta, B. and Rana, S. "GAUGE: A Formal Framework for Measuring Cryptographic Security under Heterogeneous Adversary Cost Models." arXiv:2609.17281 (submitted 2026-09-15).**
  - Its Appendix D builds "CryChron", a chronology of 22 assumption "generations": 10 observed breaks (e.g., Merkle–Hellman, HFE, MD5, SFLASH, GGH, NTRUSign, SHA-1, SIDH, Rainbow) and 12 right-censored, unbroken generations (SHA-2, SHA-3, NTRU, LWE, R-LWE, M-LWE, NTRU Prime, CSIDH, McEliece–Goppa, RSA, FF-DLP, ECDLP).
  - It fits survival models to time-to-break. It records birth year and age at break or censoring only, with no effort or paper counts.
  - It also derives a "lattice-sieving drift" of about 9.79 bits per year: the sieving exponent fell from 0.415 to 0.292, which at β = 637 is about 78 bits over 2008–2016.
  - Relation to our study: partial overlap on time-to-break per assumption, a complementary measure. It does not quantify effort. Preprint, not peer-reviewed. — [arXiv abs](https://arxiv.org/abs/2609.17281); [HTML v1](https://arxiv.org/html/2609.17281v1)
- **Lenstra, A. K. and Verheul, E. R. "Selecting Cryptographic Key Sizes." Journal of Cryptology 14(4):255–293 (2001).**
  - It models future cryptanalytic progress as a fixed rate. Its 1999 summary version states the hypothesis directly: assume the pace from 1970 to 1999 continues; for classical public-key systems, cryptanalytic progress halves attack cost every 18 months, like Moore's law; for elliptic curves, consider both "no progress" and "progress à la Moore".
  - Relation to our study: context. It quantifies progress rates by assumption class, not effort. — [DOI 10.1007/s00145-001-0009-4 (Crossref-verified)](https://doi.org/10.1007/s00145-001-0009-4); [summary version PDF (cs.ru.nl)](https://www.cs.ru.nl/E.Verheul/papers/cce1999/CCE1999.pdf)
- **Bibliometric studies of PQC as a field** (none splits out cryptanalysis by assumption):
  - **Hasija, T., Ramkumar, K. R., Kaur, A., Bali, M. S. "Exploring the landscape of post quantum cryptography: a bibliometric analysis of emerging trends and research impact." Journal of Big Data 12, article 225 (2025).** 14,230 Scopus records; performance analysis, citations and bibliographic coupling. — [DOI 10.1186/s40537-025-01269-5 (Crossref/OpenAlex-verified)](https://doi.org/10.1186/s40537-025-01269-5)
  - **Hanafi, B. and Ali, M. "Analyzing the research impact in post quantum cryptography through scientometric evaluation." Discover Computing 28, article 32 (2025).** 2,874 WoS+Scopus articles; reports 623 PQC publications in 2023. — [DOI 10.1007/s10791-025-09507-3 (Crossref/OpenAlex-verified)](https://doi.org/10.1007/s10791-025-09507-3)
  - **Pal, J. K. "Scientometric dimensions of cryptographic research." Scientometrics 105(1):179–202 (2015).** Covers the whole field for 2001–2010: growth, authorship and Lotka's law. "Cryptanalysis" appears only as a keyword. — [DOI 10.1007/s11192-015-1661-z (Crossref-verified)](https://doi.org/10.1007/s11192-015-1661-z); [ISI repository page](https://digitalcommons.isical.ac.in/journal-articles/2285)
  - Relation to our study: context only. They count PQC research in general (mostly constructions and implementations), with no attack/construction split and no per-assumption effort.
- **Checked and found not pre-emptive:**
  - **Radanliev, P. "AI-Driven Adaptive Adversaries and the Erosion of Cryptographic Trust in Public Key Systems." arXiv:2605.24542 (2026-05-23).** The abstract concerns AI-driven implementation-level attacks. It gives no per-assumption counts of attack papers (abstract-level check only). — [arXiv](https://arxiv.org/abs/2605.24542)
  - **Mojaveri, S. J. and Khosravi, A. "The McEliece Cryptosystem After Nearly Five Decades: A Survey of Security, Cryptanalysis, and Future Directions." IACR ePrint 2026/1512 (2026).** It sorts nearly five decades of McEliece cryptanalysis into six categories, qualitatively, with no counts in the abstract. — [ePrint 2026/1512](https://eprint.iacr.org/2026/1512)
  - **Jorstad, N. D. and Smith, L. T. "Cryptographic Algorithm Metrics." Institute for Defense Analyses, Jan 1997 (20th NISSC proceedings).** It proposes an adjectival "strength" scale from key length, complexity and best attack. It does not measure the amount of scrutiny. — [csrc.nist.gov PDF](https://csrc.nist.gov/files/pubs/conference/1997/10/10/proceedings-of-the-20th-nissc-1997/final/docs/128.pdf)
- **Context surveys of attack histories** (qualitative histories, not effort counts):
  - **Albrecht, M. and Ducas, L. "Lattice Attacks on NTRU and LWE: A History of Refinements." In Computational Cryptography (Cambridge University Press, 2021), pp. 15–40; ePrint 2021/799.** — [ePrint 2021/799](https://eprint.iacr.org/2021/799); [DOI 10.1017/9781108854207.004 (Crossref-verified)](https://doi.org/10.1017/9781108854207.004)
  - **Galbraith, S. D. and Gaudry, P. "Recent progress on the elliptic curve discrete logarithm problem." Designs, Codes and Cryptography 78(1):51–72 (online 2015, issue 2016).** Metadata verified only. — [DOI 10.1007/s10623-015-0146-7](https://doi.org/10.1007/s10623-015-0146-7)

### Inferences
- The specific combination in our study appears to be new, as far as these searches reach: classified attack-paper counts for each PKE assumption class from several databases, converted to author FTE-years and compared across ECDLP, lattices, syndrome decoding and factoring/FF-DLP. Prior quantitative work counts outcomes (Bernstein 2023; GAUGE 2026), counts papers for one assumption or one technique (Classic McEliece; Zheng & Kang 2024), or models progress rates (Lenstra–Verheul).
- Zheng & Kang's 61 "core authors" (≥4 papers) is a precedent for an author-based effort proxy within one attack line. That supports, but does not pre-empt, our author-map/FTE approach.
- Bernstein 2023 explicitly leaves "how much cryptanalytic attention each system gets" as an open question. That is a natural hook for positioning our study.

### Gaps
- I could not find the original source of the "17 man-years spent by IBM on DES" figure. NESSIE D04 gives no citation, and a search of Coppersmith's 1994 DES paper context turned up nothing. Treat it as a secondhand figure.
- I did not open the full text of Hasija et al. (2025) or Hanafi & Ali (2025); Springer blocked automated access. Abstracts say nothing about a per-family or attack-only breakdown. A tabulation by lattice/code/multivariate family may exist inside and is unconfirmed.
- I did not open Radanliev (2026) in full. Its "bibliometric step" was mentioned only in a search snippet, so I could not check its per-cryptosystem counts.
- I found no study that counts distinct researchers or person-years of cryptanalysis per assumption (ECDLP, LWE, etc.) beyond the anecdotes above.

## Q2. Are there datasets or trackers of attacks or breaks on PQC candidates?

### Takeaway
Yes, but they track outcomes (attacked, broken or withdrawn), not effort. NIST's own early tallies
and Bernstein's tallies give counts of attacked or broken submissions. The PQShield "sigs zoo"
compares parameters and performance, not attacks. None of these counts the volume of cryptanalysis
per candidate or per assumption.

### Cited Findings
- **Moody, D. "Round 2 of the NIST PQC 'Competition': What was NIST thinking?" NIST slides, PQCrypto, May 2019.**
  - Within 3 weeks of posting, 12 submissions were broken or significantly attacked, and 5 were withdrawn. Four more were broken or attacked by April 2018.
  - Round 1 drew over 300 official comments; about 60% concerned roughly 10 submissions, and about half the submissions had 2 or fewer comments. The pqc-forum had about 1,300 members and 1,002 posts.
  - Relation to our study: a rare numeric NIST measure of the distribution of public attention across candidates, using comment counts. It is a useful analogue for our skewed-attention finding. — [csrc.nist.gov slides PDF](https://csrc.nist.gov/csrc/media/presentations/round-2-of-the-nist-pqc-competition-what-was-nist/images-media/pqcrypto-may2019-moody.pdf)
- **Bernstein, D. J. and Lange, T. "Post-quantum cryptography." Invited lecture slides, 2019-06-10.** A slide titled "Do cryptographers have any idea what they're doing?" reports that 22 of 69 submissions had been attacked by the end of 2018. Bernstein 2023 cites it as the baseline failure-rate observation. — [cr.yp.to talks index, #2019.06.10](https://cr.yp.to/talks.html#2019.06.10); [slides PDF](https://cr.yp.to/talks/2019.06.10/slides-dan+tanja-20190610-pqcrypto-4x3.pdf)
- **Bernstein 2023 (qrcsp)**, Q1 above. Section 4 is a per-submission dataset of breaks with explicit breakage criteria: below AES-128 cost for the smallest parameters. It is the most systematic public tally of broken PQC round-1 submissions. — [cr.yp.to PDF](https://cr.yp.to/papers/qrcsp-20231202.pdf)
- **PQShield. "NIST PQC Signatures Zoo" (GitHub: PQShield/nist-sigs-zoo).** An interactive comparison of the NIST additional-signature on-ramp candidates, covering parameters and performance; it added a round-3 page in 2026. It does not tally attack papers. — [GitHub repo](https://github.com/pqshield/nist-sigs-zoo)
- **Bernstein, D. J. "Which eSTREAM ciphers have been broken?" (paper dated 2008-02-21)** and the companion **"Stream-cipher attacks" web page (dated 2008.03.30).** The page gives a status for each cipher version: 196 entries, of which my count finds 37 "broken", 2 "broken?", 39 "withdrawn", 11 "unresolved" and 107 with an estimated security level. This is a symmetric precedent for a break tracker. — [paper PDF](https://cr.yp.to/streamciphers/broken-20080221.pdf); [attacks page](https://cr.yp.to/streamciphers/attacks.html)
- NIST's own status reports (Q4) list the attacks behind each elimination, but in prose, not as counts.

### Inferences
- Existing PQC trackers measure survival or outcomes. Our study measures inputs (papers, authors, FTE-years). The two are complementary; a natural cross-analysis would be breaks per unit of effort per assumption class.
- Moody's comment-concentration figures (about 60% of comments on about 10 of 69 submissions) suggest scrutiny was very uneven even within the competition, consistent with Bernstein's concerns.

### Gaps
- I found no maintained "PQC zoo" that records attack papers per candidate. I did not find any pqc-forum thread that tallies attack papers per candidate or assumption. Searches for an "AE Zoo" (CAESAR) and an "AES Lounge" bibliography returned nothing locatable; both remain unverified and may only exist in archived form.

## Q3. Are there analogous quantifications for symmetric primitives?

### Takeaway
Symmetric cryptography has curated bibliographies and attack trackers, the Keccak team's
third-party list being the best example, and NIST hash/LWC reports that rank candidates by
"depth" or "most" analysis. None turns these into effort estimates. A 2010s/2020s bibliometric
count of, for example, AES cryptanalysis papers was not found.

### Cited Findings
- **Keccak Team. "Third-party cryptanalysis" (keccak.team/third_party.html), accessed 2026-10-09.**
  - It lists all third-party results the team knows of on Keccak and Xoodoo: FIPS 202 / SP 800-185 / RFC 9861 instances, KangarooTwelve, Ketje, Keyak, Kravatte, Xoofff and Xoodyak.
  - My parse of the page finds about 90 entries: about 49 on unkeyed modes, 25 on keyed modes and 16 on the permutations, dated 2009–2026, with peaks of about 8–10 per year in 2017–2019, 2022 and 2025. These are my counts, not the team's; the team notes it may have missed some results.
  - Relation to our study: a direct symmetric analogue of a per-primitive attack-paper count, a curated list rather than an effort estimate. — [keccak.team third-party page](https://keccak.team/third_party.html)
- **The SHA-3 Zoo (ECRYPT Hash Function Website, IAIK TU Graz).** It tracks the best known attacks on each SHA-3 candidate and sorts results by impact. The current page says 56 of 64 submissions are public, 51 entered round 1, 14 round 2 and 5 the final. It deliberately makes no "broken" judgement. — [SHA-3 Zoo](https://ehash.isec.tugraz.at/wiki/The_SHA-3_Zoo.html)
- **Aurora, V. "Lifetimes of cryptographic hash functions" (valerieaurora.org).** A year-by-year status chart (1990–2017 columns) for popular hash functions, running from unbroken through weakened to collision found. It is a timeline of breaks, not effort. — [valerieaurora.org/hash.html](https://valerieaurora.org/hash.html)
- **Bernstein's eSTREAM break tracker**, Q2 above. — [attacks page](https://cr.yp.to/streamciphers/attacks.html)
- **NESSIE D04 (2000)**, Q1 above: AES finalists received "very limited" security evaluation compared with 17 man-years on DES, and most AES3 papers were about performance. — [Wayback PDF](https://web.archive.org/web/2005/https://www.cosic.esat.kuleuven.be/nessie/deliverables/D4_NessieAESInput.pdf)

### Inferences
- The Keccak list (about 90 results over about 17 years for a flagship primitive) gives a scale comparison for our per-assumption counts. Our ECDLP class alone has about 465 fractional papers. A per-primitive symmetric list should be compared with care, because our classes are assumption-level and span several databases.

### Gaps
- I found no published bibliometric count of AES, DES or SHA-2 cryptanalysis papers. A Microsoft Research talk abstract says only "hundreds of papers" (qualitative; not cited here as evidence).
- The AES Lounge (an ECRYPT/IAIK AES bibliography with result tables, per secondary mentions) could not be located or verified.

## Q4. Did NIST or other standards bodies try to measure "amount of analysis" numerically?

### Takeaway
No. NIST has repeatedly said it weighs the "quantity, quality, and maturity" of analysis, but its
judgements are qualitative. In the SHA-3 final report NIST explicitly considered counting
cryptanalysis papers per finalist and rejected it as "rather misleading". It used a subjective
"depth of cryptanalysis" judgement instead. The only numeric NIST attention measures I found are
counts of public comments: 136 sets of comments in AES round 2, and over 300 official comments in
PQC round 1.

### Cited Findings
- **Chang, S., Perlner, R., Burr, W. E., Sönmez Turan, M., Kelsey, J. M., Paul, S., Bassham, L. E. NISTIR 7896, "Third-Round Report of the SHA-3 Cryptographic Hash Algorithm Competition" (2012).**
  - Section 4.1.5 says it is easy but "rather misleading" to quantify analysis by counting cryptanalysis papers per finalist. It gives reasons:
    - Tweaked finalists attract papers that re-apply old attacks.
    - Some algorithms attract many small results rather than a few deep ones.
    - Weaker algorithms may attract more attacking papers.
  - NIST says it "took notice" of paper counts but relied on "depth of cryptanalysis". Table 5 pairs the security margin (e.g., Keccak 79% of rounds unbroken, JH 38%) with a subjective depth rating. NIST judged that Grøstl, Skein and BLAKE received more analysis than Keccak, and JH much less.
  - Relation to our study: the most important methodological precedent and caveat. NIST considered paper counting and argued against using it on its own. Our study should answer these three biases explicitly, for example with classification, fractional counting, author-FTE and record cross-checks. — [DOI 10.6028/NIST.IR.7896](http://dx.doi.org/10.6028/NIST.IR.7896); [nvlpubs PDF](https://nvlpubs.nist.gov/nistpubs/ir/2012/NIST.IR.7896.pdf)
- **Nechvatal, J., Barker, E., Bassham, L., Burr, W., Dworkin, M., Foti, J., Roback, E. "Report on the Development of the Advanced Encryption Standard (AES)." J. Res. NIST 106(3):511–577 (2001).** NIST received 136 sets of public comments on the finalists in round 2, as papers, emails and letters. This counts input volume, not analysis per candidate. — [nvlpubs PDF](https://nvlpubs.nist.gov/nistpubs/jres/106/3/j63nec.pdf)
- **NIST PQC status reports.**
  - Reports covered: NISTIR 8240 (Alagic et al., 2019, round 1); NISTIR 8309 (2020, round 2); NIST IR 8413-upd1 (2022, round 3); NIST IR 8545 (2025, round 4).
  - Additional-signature reports: NIST IR 8528 (2024, round 1) and NIST IR 8610 (2026, round 2).
  - NIST says it considered "the overall quantity, quality, and maturity of analysis" (wording in 8240, 8528 and 8610). It describes problems as "well-studied" and notes durations such as Rainbow "studied for about fifteen years" (8240) and UOV "studied for decades" (8610).
  - No report tabulates paper counts or effort per candidate (my full-text search of each PDF). NISTIR 8105 (2016) has no such measures either.
  - Relation to our study: confirms NIST's maturity judgements are qualitative. — [8240](https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.8240.pdf); [8309](https://nvlpubs.nist.gov/nistpubs/ir/2020/NIST.IR.8309.pdf); [8413-upd1](https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8413-upd1.pdf); [8545](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8545.pdf); [8528](https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8528.pdf); [8610](https://nvlpubs.nist.gov/nistpubs/ir/2026/NIST.IR.8610.pdf); [8105](https://nvlpubs.nist.gov/nistpubs/ir/2016/NIST.IR.8105.pdf)
- **NIST lightweight cryptography reports.**
  - **NISTIR 8369 (Sönmez Turan et al., 2021, round 2)** describes third-party analysis per candidate qualitatively, e.g., ASCON "significant third-party analysis" and Pyjamask "relatively little". — [NISTIR 8369](https://nvlpubs.nist.gov/nistpubs/ir/2021/NIST.IR.8369.pdf)
  - **NIST IR 8454 (Sönmez Turan, McKay, Chang, Bassham, Kang, Waller, Kelsey, 2023, final round)** says ASCON was "the submission with the most third-party analysis". Its Table 7 lists selected best attacks (e.g., ASCON key recovery on 7 of 12 rounds) but gives no counts. — [NIST IR 8454](https://nvlpubs.nist.gov/nistpubs/ir/2023/NIST.IR.8454.pdf)
- **Bernstein 2023 (qrcsp), §7**, notes that NIST's claim to weigh the "overall quantity" of analysis could be made measurable, e.g., by counting pages of security analysis, but has not been. — [cr.yp.to PDF](https://cr.yp.to/papers/qrcsp-20231202.pdf)

### Inferences
- The standards-body record supports a positioning claim: amount of analysis is a stated selection criterion at NIST, but it has always been judged qualitatively. NIST's one documented look at paper counting (SHA-3) rejected it on bias grounds. Our study supplies a numeric measure and should engage directly with the three biases NISTIR 7896 names.
- NIST's ordinal judgements make a usable validation target. For example, NIST said Grøstl, Skein and BLAKE received more analysis than Keccak, and JH less. A paper count on the SHA-3 finalists could be checked against these judgements as a sanity test of the paper-count method.

### Gaps
- I did not review SP 800-208 or non-NIST bodies (CRYPTREC, BSI, ANSSI, ETSI) for numeric scrutiny measures; none came up in searches.
- I could not confirm whether NIST published per-candidate counts of official comments for later PQC rounds. Moody's 2019 slides give only the round-1 summary and an early round-2 snapshot.
