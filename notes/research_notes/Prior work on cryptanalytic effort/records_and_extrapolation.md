# Prior work on cryptanalytic records and extrapolation to deployed parameters (comparators for the "frontier gap")

Compiled 2026-10-09. Scope: work that (a) tracks public cryptanalytic computational records, (b) extrapolates from records or cost models to deployed parameters, (c) compares problem families or tracks how fast records advance. Quantum estimates are limited to three items (Q4 below).

How items were verified: bibliographic metadata was checked against the Crossref API record for the DOI (api.crossref.org/works/{DOI}), the IACR ePrint landing page, arXiv abstract pages, publisher or agency pages, or the PDF itself. The URL given for each entry is the one opened. dblp could not be used: it returned an anti-bot challenge page, which was not bypassed. Several ePrint and iacr.org PDFs returned HTTP 403, so the full text of three record papers was read from open repository copies instead (CWI, NSF PAR, a mirror of the Lenstra-Verheul preprint). Quotations are 15 words or fewer, and everything else is paraphrased.

---

## Key question 1: Has anyone computed a cross-family "gap to frontier" measure like ours? Who, and how?

### Takeaway
I found no prior work that computes the project's quantity: log2(work for the deployed target) minus log2(work of the largest public solve), using one cost model at both ends, across ECDLP, lattices, codes and factoring. The closest precedents are of four kinds:
- Lenstra-school key-size equivalence models (Lenstra-Verheul 2001; Lenstra 2004; keylength.com) are calibrated on record data but output equivalent key sizes, and they cover only classical families.
- Bos-Kaihara-Kleinjung-Lenstra-Montgomery (2009) assess risk from the latest records for two families, RSA-1024 and 160-bit ECC. This is the nearest single analogue.
- Universal cost currencies (energy: Lenstra-Kleinjung-Thomé 2013; cloud dollars: Kleinjung-Lenstra-Page-Smart 2012) cover all primitives but price the attack itself, not the distance from public records.
- Single-family record papers extrapolate their own record to deployed sizes (RSA-768 to RSA-1024; Esser-May-Zweydinger to McEliece; Certicom to 163-bit ECC).

No post-quantum family (lattices, codes) appears in any cross-family record-gap comparison I found.

### Cited Findings

**Closest cross-family, record-calibrated work**
- Lenstra and Verheul base key-size guidelines for symmetric ciphers, RSA, finite-field DL and prime-field elliptic-curve DL on a set of hypotheses they state explicitly, combined with existing data points about each system. They describe the method as "uniform mechanical", and computing effort is measured in Mips-Years. They calibrate against the 1997 Internet DES key search, among other data points. — [Lenstra & Verheul, preprint text (Nov 1999) of J. Cryptology 14(4):255-293 (2001)](https://cdimage.debian.org/mirror/archive/ftp.sunet.se/pub/security/docs/crypt/cryptosizes.pdf); bibliographic metadata verified at [Crossref 10.1007/s00145-001-0009-4](https://api.crossref.org/works/10.1007/s00145-001-0009-4)
- keylength.com (BlueKrypt; Damien Giry, approved by J.-J. Quisquater) implements and compares the following methods: Lenstra-Verheul (2000), Lenstra updated equations (2004), ECRYPT-CSA (2018), NIST (2020), ANSSI (2014), NSA CNSA (2016), RFC 3766 (2004) and BSI (2020). Its Lenstra-2004 page offers a "double Moore" factoring law (the cost of factoring a fixed modulus halves every 9 months: hardware improvement plus algorithmic improvement) and a "triple Moore" law (halving every 6 months). — [keylength.com home](https://www.keylength.com/en/); [keylength.com Lenstra 2004 page](https://www.keylength.com/en/2/)
- Bos, Kaihara, Kleinjung, Lenstra and Montgomery assess, from "the latest practical data" of large factoring and ECDLP computations, the risk of continuing to use 1024-bit RSA and 160-bit ECC against an open-community effort. Their conclusions: the RSA-1024 risk is small until at least 2014, and they "would be surprised" if a public effort made a dent in 160-bit prime-field ECC by 2020. This is a two-family distance-from-records analysis. — [ePrint 2009/389](https://eprint.iacr.org/2009/389)
- Lenstra, Kleinjung and Thomé propose a "universal security" measure that puts all primitives on the same footing, so that comparable security can be chosen across the board. The title's "pools, lakes" refers to an energy-based yardstick. — [ePrint 2013/635](https://eprint.iacr.org/2013/635); published as LNCS, Springer 2013, pp. 121-124, [Crossref 10.1007/978-3-642-42001-6_9](https://api.crossref.org/works/10.1007/978-3-642-42001-6_9)
- Kleinjung, Lenstra, Page and Smart estimate key strength as the money needed to recover a symmetric or private key by renting cloud computation (updated with 2012 Amazon prices). They supply tools to regenerate the estimates as algorithms improve. — [ePrint 2011/254](https://eprint.iacr.org/2011/254); INDOCRYPT 2012, LNCS pp. 17-39, [Crossref 10.1007/978-3-642-34931-7_3](https://api.crossref.org/works/10.1007/978-3-642-34931-7_3)
- Smart and Thomé give a history of how cryptographic key sizes have been determined for different schemes. The chapter summary describes it as an overview of improvements over time in estimating the security level of the main hardness assumptions. — [ePrint 2021/894](https://eprint.iacr.org/2021/894); chapter 11 of Bos & Stam (eds.), *Computational Cryptography*, CUP 2021, pp. 314-334, [Crossref 10.1017/9781108854207.014](https://api.crossref.org/works/10.1017/9781108854207.014); [Cambridge chapter page](https://resolve-he.cambridge.org/core/books/abs/computational-cryptography/history-of-cryptographic-key-sizes/3BA395F0175F622090AC7C14EA98C3A4)
- The ECRYPT-CSA 2018 report tabulates the key sizes that Lenstra-Verheul 2000, Lenstra 2004, IETF 2004 (RFC 3766), SECG 2009 and others assign to the same symmetric level. At 128 bits the RSA modulus ranges from 3072 bits (SECG) through 3253 (IETF) and 4440 (Lenstra 2004) to 5888 (Lenstra-Verheul), so the models differ mainly on RSA. — [ECRYPT-CSA D5.4 (2018), Table 4.1, archived PDF](https://web.archive.org/web/2023id_/https://www.ecrypt.eu.org/csa/documents/D5.4-FinalAlgKeySizeProt.pdf)

**Single-family "distance from record" statements in record papers**
- RSA-768 paper: factoring a 1024-bit modulus would be "about a thousand times harder", and a 512-bit one was several thousand times easier. Because 512-bit was first factored in 1999, 1024-bit could be factored within the next decade by a similar academic effort, and phasing out RSA-1024 within 3-4 years would be prudent. — [Kleinjung et al., CWI open copy](https://ir.cwi.nl/pub/16870/16870D.pdf)
- RSA-240/DLP-240 paper: the authors decline to compare with RSA-768, saying it "would have very limited meaning", and compare with DLP-768 instead. The L(1/3) formula predicts DLP-240 to be about 2.25x harder than DLP-768. Yet the relation collection, timed on the DLP-768 hardware, took about 3100 core-years against DLP-768's ~4000. They call the timeline of previous records "misleading". — [Boudot et al., NSF PAR open copy](https://par.nsf.gov/servlets/purl/10273009)
- Certicom: the 109-bit challenges are solved. The 131-bit challenges need "significantly more resources" but "may be within reach". All Level II challenges (163-359 bits) are believed infeasible, possibly excepting 163-bit. Estimates are given in Pentium-100 machine-days from iteration-rate measurements. — [Certicom ECC Challenge details PDF (2009 version)](https://www.certicom.com/content/dam/certicom/images/pdfs/challenge-2009.pdf); [Certicom challenge page](https://www.certicom.com/content/certicom/en/the-certicom-ecc-challenge.html)
- Esser-May-Zweydinger extrapolate from their McEliece-1223/1284 records and find the round-3 Classic McEliece 192- and 256-bit parameter sets overestimated by roughly 20 and 10 bits; BIKE and HQC levels were confirmed. — [ePrint 2021/1634](https://eprint.iacr.org/2021/1634)
- Dallaire-Demers, Doyle and Foo (2025, rev. 2026) build a ladder of ECDLP challenges on secp256k1-shaped curves from 6 to 256 bits. They "calibrate classical cost against Pollard's rho records" and quantum cost against Shor resource estimates. This is a single-family record ladder up to the deployed size, aimed at tracking quantum progress. — [arXiv 2508.14011](https://arxiv.org/abs/2508.14011)

**Statements that rigorous extrapolation from records is hard**
- Thomé (NIST Crypto Reading Club, 2024-03-20): records are very important data points for assessing hardness, but "it is quite hard to extrapolate from there in a rigorous way". — [NIST CSRC presentation page](https://csrc.nist.gov/presentations/2024/crclub-2024-03-20)
- Le Gluher, Spaenlehauer and Thomé show that the o(1) term in the NFS complexity converges very slowly. Its series expansion appears to start converging only for N > exp(exp(25)), which "raises doubts" about NFS estimates that set the o(1) term to zero. — [arXiv 2007.02730](https://arxiv.org/abs/2007.02730) (comments: accepted for publication in *Mathematical Cryptology*)

### Inferences
- The project's frontier gap appears new in three ways together: (i) it covers post-quantum families (lattices, codes) next to ECDLP and factoring; (ii) it uses one cost model at both ends of each gap; (iii) it reports the result as a log2 distance from demonstrated public capability rather than as an equivalent key size or a dollar or energy cost. The closest conceptual ancestor is Bos et al. 2009/389 (two families, from records). The closest methodological ancestor is Lenstra-Verheul (explicit hypotheses applied mechanically to record data points).
- Consistency check (my arithmetic, using the project's leading-GNFS formula F(b) from analysis/normalization_method.md): F(1024) − F(768) = 10.25 bits ≈ 1,220x, which matches the RSA-768 paper's "about a thousand times harder". F(795) − F(768) = 1.17 bits ≈ 2.25x, which matches Boudot et al.'s L(1/3) figure. The leading-term model used for RSA therefore reproduces the record authors' own extrapolations. Le Gluher-Spaenlehauer-Thomé is the citable caveat for the much longer jump from 896 to 2048 bits.
- Boudot et al.'s remark on the "misleading" timeline supports reporting gaps per cost model rather than per calendar date. Their same-hardware comparison is the precedent for normalizing compute to a reference core when totals are reported.

### Gaps
- dblp (anti-bot page) and most iacr.org PDFs (HTTP 403) were unavailable. The finding that no cross-family record-gap measure exists rests on web, Crossref and OpenAlex searches and on the reference lists of the surveys above; it should be read as "not found", not "does not exist".
- I could not open the full text of Lenstra-Kleinjung-Thomé 2013 or Kleinjung-Lenstra-Page-Smart 2012, so their per-primitive numbers (which primitives, which dollar or energy figures) are not recorded here.
- I found no prior work that puts lattice (SVP-challenge) or decoding-challenge records alongside factoring or ECDLP records on a common gap scale.

---

## Key question 2: What are the canonical citable sources for each family's records and extrapolation methodology?

### Takeaway
Each family has a stable set of canonical record sources and estimator tools, listed below in canonical-first order with verified bibliographic data. Two corrections were found during verification:
- Buchmann-Lindner-Rückert (PQCrypto 2008) has three authors; Schneider is not one of them.
- The ECRYPT-CSA 2018 report still cites 109-bit ECDLP records, although the 112-bit (2009) and 117-bit (2016) results already existed.

### Cited Findings

#### A. Key-size and security-level extrapolation literature (canonical first)

1. **Lenstra, A. K., & Verheul, E. R. (2001). Selecting Cryptographic Key Sizes. *Journal of Cryptology* 14(4):255-293.** DOI 10.1007/s00145-001-0009-4. Verified: [Crossref](https://api.crossref.org/works/10.1007/s00145-001-0009-4). Earlier version: *Datenschutz und Datensicherheit* 24(3), 2000, per ECRYPT-CSA ref. [369] ([PDF](https://web.archive.org/web/2023id_/https://www.ecrypt.eu.org/csa/documents/D5.4-FinalAlgKeySizeProt.pdf)).
   - Summary: Derives lower bounds on key sizes for symmetric, RSA, finite-field DL and ECC from explicit hypotheses about Moore's law, budgets and cryptanalytic progress, calibrated on DES key search and factoring data. This is the canonical "records + Moore's law → deployed sizes" method ([preprint text](https://cdimage.debian.org/mirror/archive/ftp.sunet.se/pub/security/docs/crypt/cryptosizes.pdf)).
   - Relevance: the methodological ancestor of the frontier gap. It is cross-family, but its output is an equivalent key size rather than a log2 distance from records.
2. **Lenstra, A. K. (2004). Key Lengths. In H. Bidgoli (ed.), *The Handbook of Information Security*, Vol. II, pp. 617-635. Wiley.** No DOI found. Verified via secondary indices: ECRYPT-CSA D5.4 ref. [366] gives volume, pages and Wiley 2004 ([PDF](https://web.archive.org/web/2023id_/https://www.ecrypt.eu.org/csa/documents/D5.4-FinalAlgKeySizeProt.pdf)); keylength.com gives "Handbook of Information Security, 06/2004" ([page](https://www.keylength.com/en/2/)).
   - Caveat: the EPFL Infoscience record ([link](https://infoscience.epfl.ch/handle/20.500.14299/65745)) gives the year as 2006 (seen in a search snippet; the page returned HTTP 429 when opened). The year 2004 vs 2006 is unresolved, probably manuscript date vs print date.
   - Summary: Updated Lenstra equations. keylength.com implements them with "double/triple Moore" options ([page](https://www.keylength.com/en/2/)).
3. **Lenstra, A. K. (2001). Unbelievable Security: Matching AES Security Using Public Key Systems. ASIACRYPT 2001, LNCS, pp. 67-86.** DOI 10.1007/3-540-45682-1_5. Verified: [Crossref](https://api.crossref.org/works/10.1007/3-540-45682-1_5).
   - Summary: Bibliographic data only checked; full text not read. Per its title, it addresses which public-key sizes match AES security levels. It is an early cross-family equivalence paper.
4. **Lenstra, A. K., Kleinjung, T., & Thomé, E. (2013). Universal Security: From Bits and Mips to Pools, Lakes – and Beyond. LNCS, Springer, pp. 121-124.** DOI 10.1007/978-3-642-42001-6_9; ePrint 2013/635. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-642-42001-6_9); [ePrint](https://eprint.iacr.org/2013/635).
   - Summary: Proposes one universal, energy-based security measure for all primitives.
   - Relevance: a cross-family common currency, the conceptual alternative to our per-family cost models.
5. **Kleinjung, T., Lenstra, A. K., Page, D., & Smart, N. P. (2012). Using the Cloud to Determine Key Strengths. INDOCRYPT 2012, LNCS, pp. 17-39.** DOI 10.1007/978-3-642-34931-7_3; ePrint 2011/254. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-642-34931-7_3); [ePrint](https://eprint.iacr.org/2011/254).
   - Summary: Uses cloud rental prices to put a dollar cost on key recovery, with tools to update the cost as algorithms improve.
   - Relevance: a precedent for converting compute to a common unit, like our 2020 core-year conversion.
6. **Bos, J. W., Kaihara, M. E., Kleinjung, T., Lenstra, A. K., & Montgomery, P. L. (2009). On the Security of 1024-bit RSA and 160-bit Elliptic Curve Cryptography. IACR ePrint 2009/389.** Verified: [ePrint](https://eprint.iacr.org/2009/389).
   - Summary: Risk assessment for RSA-1024 and ECC-160 based on the latest factoring and ECDLP record computations (see Q1).
   - Relevance: the closest prior "distance from records" analysis.
7. **Lenstra, A., Tromer, E., Shamir, A., Kortsmit, W., Dodson, B., Hughes, J., & Leyland, P. (2003). Factoring Estimates for a 1024-Bit RSA Modulus. ASIACRYPT 2003, LNCS, pp. 55-74.** DOI 10.1007/978-3-540-40061-5_4. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-540-40061-5_4).
   - Summary: Bibliographic data only checked; full text not read. It is the cost estimate for factoring at the next deployed size that the RSA-768 paper cites (ref. 21 there).
8. **Orman, H., & Hoffman, P. (2004). Determining Strengths For Public Keys Used For Exchanging Symmetric Keys. RFC 3766 (BCP 86).** DOI 10.17487/RFC3766. Verified: [Crossref](https://api.crossref.org/works/10.17487/RFC3766).
   - Summary: IETF key-strength equivalences. Its 128-bit level maps to RSA-3253 and a 242-bit subgroup in ECRYPT-CSA Table 4.1 ([PDF](https://web.archive.org/web/2023id_/https://www.ecrypt.eu.org/csa/documents/D5.4-FinalAlgKeySizeProt.pdf)).
9. **Giry, D. (BlueKrypt). Keylength – Cryptographic Key Length Recommendation. https://www.keylength.com (v32.3, page dated May 24, 2020; accessed 2026-10-09).** Verified: [site](https://www.keylength.com/en/).
   - Summary: Calculator and side-by-side comparison of 8 recommendation methods (see Q1).
   - Relevance: the standard web citation for key-size equivalences.
10. **Smart, N. P. (ed.) et al. (2018). Algorithms, Key Size and Protocols Report (2018). ECRYPT-CSA, H2020-ICT-2014 Project 645421, Deliverable D5.4, 28 Feb 2018.** Verified: [archived PDF](https://web.archive.org/web/2023id_/https://www.ecrypt.eu.org/csa/documents/D5.4-FinalAlgKeySizeProt.pdf). The live ecrypt.eu.org URL returned HTTP 502.
    - Summary: Notes factoring-record progress (RSA-576 in 2003, RSA-640 in 2005, RSA-768 in 2009) and recommends at least 3072-bit RSA for new systems. It cites 109-bit prime and binary ECDLP records as the largest. Table 4.1 compares the equivalence models.
    - Relevance: the canonical EU recommendation. It shows that standards documents lag the record literature.
11. **ENISA (2014). Algorithms, key size and parameters report – 2014. Published 21 Nov 2014.** Verified: [ENISA page](https://www.enisa.europa.eu/publications/algorithms-key-size-and-parameters-report-2014).
    - Summary: ENISA's guidelines for decision makers. It updates the 2013 report and is the predecessor of the ECRYPT-CSA reports.
12. **Barker, E. (2020). Recommendation for Key Management: Part 1 – General. NIST SP 800-57 Part 1 Rev. 5, May 2020.** DOI 10.6028/NIST.SP.800-57pt1r5. Verified: [Crossref](https://api.crossref.org/works/10.6028/NIST.SP.800-57pt1r5).
    - Summary: NIST security-strength categories (e.g., RSA-2048 = 112 bits).
    - Relevance: the convention the project explicitly keeps separate from its GNFS gap (normalization_method.md §4).
13. **Smart, N. P., & Thomé, E. (2021). History of Cryptographic Key Sizes. In J. Bos & M. Stam (eds.), *Computational Cryptography: Algorithmic Aspects of Cryptology*, pp. 314-334. Cambridge University Press.** DOI 10.1017/9781108854207.014; ePrint 2021/894. Verified: [Crossref](https://api.crossref.org/works/10.1017/9781108854207.014); [ePrint](https://eprint.iacr.org/2021/894).
    - Summary: Historical review of how key sizes and security estimates evolved per hardness assumption.
    - Relevance: the best single modern survey for the related-work paragraph.
14. **Albrecht, M. R., & Ducas, L. (2021). Lattice Attacks on NTRU and LWE: A History of Refinements. Same volume, pp. 15-40.** DOI 10.1017/9781108854207.004; ePrint 2021/799. Verified: [Crossref](https://api.crossref.org/works/10.1017/9781108854207.004); [ePrint](https://eprint.iacr.org/2021/799).
    - Summary: The lattice counterpart. It traces how concrete lattice estimates have been refined.
    - Relevance: context for why the project measures lattices in sieving dimension.

#### B. Factoring / finite-field DL records with explicit extrapolation

15. **Kleinjung, T., Aoki, K., Franke, J., Lenstra, A. K., Thomé, E., Bos, J. W., Gaudry, P., Kruppa, A., Montgomery, P. L., Osvik, D. A., te Riele, H., Timofeev, A., & Zimmermann, P. (2010). Factorization of a 768-Bit RSA Modulus. CRYPTO 2010, LNCS, pp. 333-350.** DOI 10.1007/978-3-642-14623-7_18; ePrint 2010/006. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-642-14623-7_18); [ePrint](https://eprint.iacr.org/2010/006); text read from the [CWI copy](https://ir.cwi.nl/pub/16870/16870D.pdf).
    - Summary: RSA-768 by NFS. The paper extrapolates that 1024-bit would be ~1000x harder, that factoring it by a similar academic effort within a decade is not unreasonable, and that the 1024-bit matrix step should be feasible by 2020. It also says that, unless something dramatic happens, an open academic effort cannot factor 1024-bit within five years, and "after that, all bets are off".
16. **Boudot, F., Gaudry, P., Guillevic, A., Heninger, N., Thomé, E., & Zimmermann, P. (2020). Comparing the Difficulty of Factorization and Discrete Logarithm: A 240-Digit Experiment. CRYPTO 2020, LNCS, pp. 62-91.** DOI 10.1007/978-3-030-56880-1_3; ePrint 2020/697. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-030-56880-1_3); [ePrint](https://eprint.iacr.org/2020/697); text read from the [NSF PAR copy](https://par.nsf.gov/servlets/purl/10273009).
    - Summary: RSA-240 and DLP-240 (795 bits) computed on the same hardware and software. They were "significantly less expensive than anticipated based on previous records"; the same-hardware comparison with DLP-768 is given in Q1. The final page reports RSA-250.
17. **Boudot, F., Gaudry, P., Guillevic, A., Heninger, N., Thomé, E., & Zimmermann, P. (2022). The State of the Art in Integer Factoring and Breaking Public-Key Cryptography. *IEEE Security & Privacy* 20(2):80-86.** DOI 10.1109/MSEC.2022.3141918. Verified: [Crossref query result](https://api.crossref.org/works/10.1109/MSEC.2022.3141918); [HAL record hal-03691141](https://hal.archives-ouvertes.fr/hal-03691141) (seen via search; HAL pages behind Anubis bot-check were not opened).
    - Summary: Reviews the classical state of the art and the authors' records for factoring, finite-field DL and ECDLP.
    - Relevance: a short citable overview for the three classical families.
18. **Brent, R. P. (2000). Recent Progress and Prospects for Integer Factorisation Algorithms. COCOON 2000, LNCS, pp. 3-22.** DOI 10.1007/3-540-44968-x_2. Verified: [Crossref](https://api.crossref.org/works/10.1007/3-540-44968-x_2); text read from the [author PDF](https://maths-people.anu.edu.au/brent/pd/rpb196sp.pdf).
    - Summary: Combining the GNFS time bound with Moore's law, D^(1/3) (D = decimal digits of the largest general number factored) should grow roughly linearly in calendar year. The fit is Y = 13.24·D^(1/3) + 1928.6, which extrapolates to 1024-bit (D = 309) in 2018. The paper also extrapolates ECM records.
    - Relevance: the canonical record-progress-rate model (see Q3).
19. **Odlyzko, A. M. (1995). The Future of Integer Factorization. *CryptoBytes* (RSA Laboratories) 1(2):5-12.** Verified: [Odlyzko's publication list](https://www-users.cse.umn.edu/~odlyzko/doc/cnt.html). The PDF ([link](https://www-users.cse.umn.edu/~odlyzko/doc/future.of.factoring.pdf)) has non-extractable fonts.
    - Summary (from secondary descriptions only, see Gaps): projects factoring records from hardware growth plus algorithmic progress.
20. **Le Gluher, A., Spaenlehauer, P.-J., & Thomé, E. (2020-). Refined Analysis of the Asymptotic Complexity of the Number Field Sieve. arXiv:2007.02730.** Accepted for publication in *Mathematical Cryptology* per the arXiv comment. Verified: [arXiv](https://arxiv.org/abs/2007.02730).
    - Summary: The o(1) term in L[1/3] converges extremely slowly, which casts doubt on estimates that set it to zero.
    - Relevance: the direct caveat for the project's leading-GNFS RSA gap.

#### C. ECDLP records and extrapolation

21. **Certicom Corp. (1997–). The Certicom ECC Challenge; ECC Challenge details (PDF, 2009 version).** Verified: [challenge page](https://www.certicom.com/content/certicom/en/the-certicom-ecc-challenge.html); [details PDF](https://www.certicom.com/content/dam/certicom/images/pdfs/challenge-2009.pdf).
    - Summary: Lists solved exercises (79-bit, 89-bit, 97-bit) and challenges (ECCp-109 in Nov 2002, ECC2-109 in Apr 2004). It estimates cost in machine-days from Pentium-100 rho iteration rates. The 131-bit challenges remain open on the 2025 page.
    - Relevance: the original "challenge ladder" with built-in extrapolation.
22. **Bos, J. W., Kaihara, M. E., Kleinjung, T., Lenstra, A. K., & Montgomery, P. L. (2012). Solving a 112-bit Prime Elliptic Curve Discrete Logarithm Problem on Game Consoles Using Sloppy Reduction. *International Journal of Applied Cryptography* 2(3):212–(end page not in record).** DOI 10.1504/IJACT.2012.045590. Verified: [Crossref](https://api.crossref.org/works/10.1504/IJACT.2012.045590).
    - Summary: The secp112r1 record on PlayStation 3s. Announced 2009 as LACAL's "PlayStation 3 computing breaks 2^60 barrier" (ECRYPT-CSA ref. [113]).
23. **Bernstein, D. J., Engels, S., Lange, T., Niederhagen, R., Paar, C., Schwabe, P., & Zimmermann, R. (2016). Faster Elliptic-Curve Discrete Logarithms on FPGAs. IACR ePrint 2016/382.** Verified: [ePrint](https://eprint.iacr.org/2016/382).
    - Summary: The abstract reports a new ECDL size record (sect113r2) and benchmarks smaller attacks "to demonstrate reliability of the estimates". It also covers a curve over a 127-bit field for scalability.
    - Note: the 117.35-bit generic record that the project uses as its frontier is attributed in records/ecdlp/binary127-117bit-fpga-2016.yaml to the Dec 2016 revision and an NMBRTHRY announcement, which I did not open (see Gaps).
24. **Bailey, D. V., Batina, L., Bernstein, D. J., Birkner, P., Bos, J. W., Chen, H.-C., Cheng, C.-M., van Damme, G., de Meulenaer, G., Dominguez Perez, L. J., Fan, J., Güneysu, T., Gurkaynak, F., Kleinjung, T., Lange, T., Mentens, N., Niederhagen, R., Paar, C., Regazzoni, F., Schwabe, P., Uhsadel, L., Van Herrewege, A., & Yang, B.-Y. (2009). Breaking ECC2K-130. IACR ePrint 2009/541.** Verified: [ePrint](https://eprint.iacr.org/2009/541).
    - Summary: A parallel-rho attack design for ECC2K-130 across CPUs, Cells, GPUs and FPGAs, with ASIC estimates.
    - Relevance: a worked cost extrapolation to the next Certicom level, which Certicom still lists as unsolved.
25. **Galbraith, S. D., & Gaudry, P. (2016). Recent Progress on the Elliptic Curve Discrete Logarithm Problem. *Designs, Codes and Cryptography* 78(1):51-72.** DOI 10.1007/s10623-015-0146-7. Verified: [Crossref](https://api.crossref.org/works/10.1007/s10623-015-0146-7).
    - Summary: The standard ECDLP survey for the state of generic and structured attacks.

#### D. Lattice records, extrapolation, and estimators

26. **Buchmann, J., Lindner, R., & Rückert, M. (2008). Explicit Hard Instances of the Shortest Vector Problem. PQCrypto 2008, LNCS, pp. 79-94.** DOI 10.1007/978-3-540-88403-3_6. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-540-88403-3_6). Three authors only.
    - Summary: The origin of the Darmstadt lattice challenge.
27. **TU Darmstadt SVP Challenge. https://www.latticechallenge.org/svp-challenge/ (accessed 2026-10-09).** Verified: [site](https://www.latticechallenge.org/svp-challenge/).
    - Summary: Goldstein-Mayer random lattices with a hall of fame. Its stated aim is to assess SVP algorithms and compare sieving with enumeration. The steering committee listed is Buchmann, Ding (chair), Krämer, Takagi and Yang. The site also links the ideal-lattice, LWE, decoding and MQ challenges.
28. **Albrecht, M. R., Ducas, L., Herold, G., Kirshanova, E., Postlethwaite, E. W., & Stevens, M. (2019). The General Sieve Kernel and New Records in Lattice Reduction. EUROCRYPT 2019, LNCS, pp. 717-746.** DOI 10.1007/978-3-030-17656-3_25; ePrint 2019/089. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-030-17656-3_25); [ePrint](https://eprint.iacr.org/2019/089).
    - Summary: G6K and the SVP-challenge records up to dimension 155. The project's sources file records that the authors call their timing fits unreliable for extrapolation (analysis/normalization_sources.json, from the CWI copy).
29. **Ducas, L., Stevens, M., & van Woerden, W. (2021). Advanced Lattice Sieving on GPUs, with Tensor Cores. EUROCRYPT 2021, LNCS, pp. 249-279.** DOI 10.1007/978-3-030-77886-6_9; ePrint 2021/141. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-030-77886-6_9); [ePrint](https://eprint.iacr.org/2021/141).
    - Summary: SVP challenge dimension 180, up from 155, in 51.6 days on 4 NVIDIA Turing GPUs with 1.5 TB RAM (ePrint abstract).
    - Relevance: the source of the project's high-end 0.367 slope.
30. **Zhao, Z., Ding, J., & Yang, B.-Y. (2025). Sieving with Streaming Memory Access. *IACR TCHES* 2025(2):362-384.** DOI 10.46586/tches.v2025.i2.362-384. Verified: [TCHES page metadata](https://tches.iacr.org/index.php/TCHES/article/view/12051).
    - Summary: bgj-family sieves (SVP-179/183 records) with a gate model calibrated on practice. They estimate Kyber-512 at 2^140.1–2^146.1 gates (project's sources file).
31. **Zhao, Z., & Ding, J. (2026). Towards Large-Scale Lattice Attack: New Lattice Records by Disk-Based Sieving. EUROCRYPT 2026, LNCS, pp. 154-182.** DOI 10.1007/978-3-032-25327-9_6. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-032-25327-9_6).
    - Summary (from a search-result snippet of the Springer abstract; the page itself redirected to a login): claims a clear path to SVP-260 at reasonable cost in about a year.
    - Relevance: the most recent record-setters' own extrapolation.
32. **Chen, Y., & Nguyen, P. Q. (2011). BKZ 2.0: Better Lattice Security Estimates. ASIACRYPT 2011, LNCS, pp. 1-20.** DOI 10.1007/978-3-642-25385-0_1. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-642-25385-0_1).
    - Summary: Bibliographic data only checked. It is the origin of BKZ simulation (the "CN11" simulator that NIST's estimator run uses).
33. **Albrecht, M. R., Player, R., & Scott, S. (2015). On the Concrete Hardness of Learning with Errors. *Journal of Mathematical Cryptology* 9(3):169-203.** DOI 10.1515/jmc-2015-0016. Verified: [Crossref](https://api.crossref.org/works/10.1515/jmc-2015-0016).
    - Summary: The paper behind the LWE estimator. Its successor is the Lattice Estimator ([GitHub malb/lattice-estimator](https://github.com/malb/lattice-estimator)).
34. **Albrecht, M. R., Curtis, B. R., Deo, A., Davidson, A., Player, R., Postlethwaite, E. W., Virdia, F., & Wunderer, T. (2018). Estimate all the {LWE, NTRU} schemes! SCN 2018.** ePrint 2018/331. Verified: [ePrint](https://eprint.iacr.org/2018/331).
    - Summary: Applies all cost models to all NIST lattice submissions.
    - Relevance: a precedent for applying one model across many targets.
35. **NIST (2023). FAQ on Kyber512. December 2023.** Verified: [NIST PDF](https://csrc.nist.gov/csrc/media/Projects/post-quantum-cryptography/documents/faq/Kyber-512-FAQ.pdf).
    - Summary: Spec gate count 2^151 (uncertainty 2^135–2^165). Lattice Estimator 2^142.2 plus hidden overheads gives a best gate estimate of about 2^147 (2^145 with more than 2^105 bits of memory). A realistic memory-cost estimate is about 2^160 (range 2^140–2^180). Sieving exponent constants: 0.292 (BDGL), 0.3294 (k = 2) and 0.349 (k = 1). coreSVP 2^118 "should not be interpreted as concrete gate counts".
    - Relevance: an authoritative source for the slope range and target values the project uses.

#### E. Code-based records and estimators

36. **Decoding Challenge (Challenges for code-based problems). https://decodingchallenge.org (accessed 2026-10-09).** Verified: [site](https://decodingchallenge.org/).
    - Summary: Assesses practical hardness of syndrome decoding, low-weight codeword search, large-weight ternary SD, and "NIST-like" Goppa-McEliece (rate 0.8) and quasi-cyclic tracks. It uses random codes with the same rate and weight as NIST candidates, to assess generic decoding.
    - Authorship: not confirmed (see Gaps). The site's Documentation and Contact pages returned errors.
37. **Esser, A., May, A., & Zweydinger, F. (2022). McEliece Needs a Break – Solving McEliece-1284 and Quasi-Cyclic-2918 with Modern ISD. EUROCRYPT 2022, LNCS, pp. 433-457.** DOI 10.1007/978-3-031-07082-2_16; ePrint 2021/1634. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-031-07082-2_16); [ePrint](https://eprint.iacr.org/2021/1634).
    - Summary: The first MMT/BJMM records, extrapolated to deployed parameters (see Q1).
38. **Narisada, S., Uemura, S., Okada, H., Furue, H., Aikawa, Y., & Fukushima, K. (2024). Solving McEliece-1409 in One Day — Cryptanalysis with the Improved BJMM Algorithm. ISC 2024, LNCS, pp. 3-23.** DOI 10.1007/978-3-031-75764-8_1; ePrint 2024/393. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-031-75764-8_1); [ePrint](https://eprint.iacr.org/2024/393).
    - Summary: The n=1409 Goppa-track record, which is the project's frontier endpoint.
39. **Esser, A., & Bellini, E. (2022). Syndrome Decoding Estimator. PKC 2022, LNCS, pp. 112-141.** DOI 10.1007/978-3-030-97121-2_5. Verified: [Crossref](https://api.crossref.org/works/10.1007/978-3-030-97121-2_5).
    - Summary: ISD cost estimator under different memory-cost models; the source of the project's reference values for mceliece348864 and HQC-128.
40. **Esser, A., Verbel, J., Zweydinger, F., & Bellini, E. (2024). SoK: CryptographicEstimators – a Software Library for Cryptographic Hardness Estimation. ASIA CCS 2024, pp. 560-574.** DOI 10.1145/3634737.3645007; ePrint 2023/589. Verified: [Crossref](https://api.crossref.org/works/10.1145/3634737.3645007); [ePrint](https://eprint.iacr.org/2023/589); [GitHub Crypto-TII/CryptographicEstimators](https://github.com/Crypto-TII/CryptographicEstimators).
    - Summary: A unified estimator library for SD, MQ, MinRank and other problems.
    - Relevance: the multi-family estimator counterpart to the Lattice Estimator. It estimates targets, not distances from records.

### Inferences
- For each family, the citable pair is "record paper + estimator". Factoring: Kleinjung 2010 / Boudot 2020, with GNFS L[1/3] plus Le Gluher-Spaenlehauer-Thomé. ECDLP: Bernstein et al. 2016 / Bos et al. 2012 / Certicom, with the rho formula and Galbraith-Gaudry. Lattices: G6K 2019 / DSvW 2021 / ZDY 2025 / ZD 2026, with the Lattice Estimator and the NIST FAQ. Codes: EMZ 2022 / Narisada 2024, with the SD Estimator and CryptographicEstimators. Only the factoring and code papers state numeric extrapolations to deployed parameters in their abstracts or introductions.
- The estimators (Lattice Estimator, SD Estimator, CryptographicEstimators) all price the deployed target. None reports the record instance in the same model. This supports the project's choice to put both endpoints into one model by hand.

### Gaps
- The customary citation "N. Aragon, J. Lavauzelle, M. Lequesne, decodingchallenge.org, 2019" could not be verified: the site's contact and documentation pages are broken, and a web search returned nothing.
- The SVP-challenge site gives no authors for citation. The customary "M. Schneider, N. Gama, SVP Challenge (2010)" is unverified.
- I could not open the Springer page or full text of Zhao-Ding 2026, so its claim about SVP-260 relies on a search snippet.
- I did not verify the NMBRTHRY announcement of the 117.35-bit ECDLP solve, or the Dec 2016 ePrint revision, myself.

---

## Key question 3: Prior work comparing across families or tracking record progress rates over time

### Takeaway
Rates of record progress have been modeled for factoring only:
- Odlyzko (1995) projected factoring records from hardware plus algorithmic gains.
- Brent (2000) fitted D^(1/3) linear in year.
- Lenstra's "double/triple Moore" laws model the falling cost of factoring a fixed modulus.

Cross-family comparisons exist only as key-size equivalences (Lenstra-Verheul, Lenstra 2004, RFC 3766, ECRYPT/NIST tables) or common-currency costings (energy, cloud dollars). I found no rate-of-progress study for lattice or decoding records, and none comparing progress rates across families.

### Cited Findings
- Brent's fit Y = 13.24·D^(1/3) + 1928.6, motivated by the GNFS bound plus Moore's law, extrapolates to 1024-bit general factoring in 2018. — [Brent 2000, author PDF](https://maths-people.anu.edu.au/brent/pd/rpb196sp.pdf)
- Lenstra's double-Moore law: the cost of factoring a fixed modulus halves every 9 months (Moore's law on equipment plus an equal algorithmic factor). The triple-Moore variant halves every 6 months. — [keylength.com Lenstra 2004 page](https://www.keylength.com/en/2/)
- ECRYPT-CSA charts RSA-challenge progress as RSA-576 (2003), RSA-640 (2005), RSA-768 (2009). — [ECRYPT-CSA D5.4](https://web.archive.org/web/2023id_/https://www.ecrypt.eu.org/csa/documents/D5.4-FinalAlgKeySizeProt.pdf)
- RSA-768 authors: in 2009 a 1024-bit modulus looked more than five times easier than a 768-bit one had looked in 1999. This is a direct statement of how fast the frontier had moved. — [Kleinjung et al., CWI copy](https://ir.cwi.nl/pub/16870/16870D.pdf)
- Boudot et al.: the RSA-768 (2009) and DLP-768 (2016) records are a misleading timeline, because DLP-768 needed more resources (raw core-year ratio about 3.5x). — [Boudot et al., NSF PAR copy](https://par.nsf.gov/servlets/purl/10273009)
- Odlyzko's 1995 CryptoBytes article is the canonical early projection of factoring records. — [Odlyzko publication list](https://www-users.cse.umn.edu/~odlyzko/doc/cnt.html). A secondary search summary said his 2010 retrospective judged the projection too optimistic; I did not open that retrospective.

### Inferences
- Brent's line, checked by me against the project's records: it predicts D = 270 digits (RSA-896) around 2014 and D = 309 (RSA-1024) around 2018 (computed from his published fit). The project's records put RSA-896 in 2026, with RSA-1024 still open. Public factoring has therefore run about a decade behind Brent's 2000 trend line, which supports Odlyzko's reported verdict that the 1990s projections were too optimistic. The same fit puts 2048 bits (D = 617) at about 2041. This is an illustration only, not a prediction.
- The project's planned "how fast does each gap shrink" tracking (normalization_method.md §6) would be the first cross-family progress-rate comparison that I could find. The project's observation that a slope fitted to SVP records measures progress rather than cost growth has a factoring precedent: Brent's fit likewise combines hardware and algorithmic progress.

### Gaps
- I found no published progress-rate fit for SVP-challenge, ideal-lattice or decoding-challenge records, and no ECDLP progress-rate analysis beyond the Certicom and Lenstra-Verheul style extrapolations.
- Not verified: Silverman, "A Cost-Based Security Analysis of Symmetric and Asymmetric Key Lengths", RSA Laboratories Bulletin 13 (2000). It is often cited as an early cross-family cost model, but I could not locate a verifiable index entry (an OpenAlex search returned nothing).

---

## Key question 4 (scope-limited): Canonical quantum resource-estimate citations

### Takeaway
Two canonical RSA-2048 estimates, both verified. Gidney-Ekerå 2021 estimates 8 hours with 20 million noisy qubits; Gidney 2025 estimates under a week with under a million noisy qubits under the same hardware assumptions. A 2025-26 ECDLP challenge-ladder paper links classical rho records to quantum estimates.

### Cited Findings
- Gidney, C., & Ekerå, M. (2021). How to Factor 2048 Bit RSA Integers in 8 Hours Using 20 Million Noisy Qubits. *Quantum* 5:433. DOI 10.22331/q-2021-04-15-433. — [Crossref](https://api.crossref.org/works/10.22331/q-2021-04-15-433)
- Gidney, C. (2025). How to Factor 2048 Bit RSA Integers with Less than a Million Noisy Qubits. arXiv:2505.15917 (submitted 21 May 2025). Estimate: under a week with fewer than one million noisy qubits, under the same assumptions as 2019: 0.1% gate error, 1 µs surface-code cycle, 10 µs reaction time. — [arXiv](https://arxiv.org/abs/2505.15917)
- Dallaire-Demers, P.-L., Doyle, W., & Foo, T. (2025, v2 2026-03-25). Brace for Impact: ECDLP Challenges for Quantum Cryptanalysis. arXiv:2508.14011. Their scenarios place the 256-bit instance in a 2027–2033 window, under explicit assumptions. — [arXiv](https://arxiv.org/abs/2508.14011)

### Inferences
- Of these, only Dallaire-Demers et al. connect classical record data to deployed-size targets, and for one family only.

### Gaps
- A secondary article claimed a February 2026 qLDPC-based RSA-2048 estimate (Iceberg Quantum "Pinnacle", under 100,000 physical qubits). I did not verify it against a primary source, and it is excluded.
- Other unverified or set-aside items:
  - The ECRYPT II yearly key-size reports (2008–2012).
  - BSI TR-02102 and ANSSI RGS. These are listed by keylength.com only; the primaries were not opened.
  - The LNCS volume number for Lenstra-Kleinjung-Thomé 2013. I believe it is LNCS 8260, but Crossref's container title was malformed, so it is unconfirmed.
  - The NIST FAQ's ref. [15] on "hidden overheads" of BDGL sieving, not opened.
