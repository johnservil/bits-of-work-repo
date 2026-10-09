# Prior work comparing human research effort with AI compute or inference cost (math and cryptanalysis focus)

Compiled 2026-10-09. Every entry under "Cited Findings" was opened this session, at the
verifying URL given. For arXiv items, metadata came from the arXiv API, export.arxiv.org/api/query.
For ePrint items, it came from the ePrint page meta tags and history. Where only metadata was
checked, the entry says so. Any summary not drawn from the abstract or a passage read this session
is labelled "(from prior knowledge; not re-read)". Lab self-reports are marked **[lab self-report]**.
Arithmetic that is mine rather than the source's is marked **[my arithmetic]**.

---

## Q1. Has anyone previously converted accumulated human research effort on a problem into AI inference budgets or exchange rates? If so, how?

### Takeaway
I found no prior work that turns the accumulated human literature effort on a *specific open problem* or cryptographic assumption into an equivalent AI inference budget. That conversion appears to be novel to this study. Four adjacent strands exist:
- (a) aggregate "AI research effort in human-researcher equivalents" framings (MacAskill and Moorhouse; OpenAI's agent-workday metric);
- (b) economics work that converts R&D dollars into researcher counts using a wage, the same move as our $250k/research-year (Bloom et al.);
- (c) per-task human-wage vs. inference-cost comparisons (METR, GDPval, Cost-of-Pass);
- (d) qualitative warnings that the lack of past progress on an open problem may reflect neglect rather than difficulty, with partial-result literature as the better evidence of difficulty (Tao's Erdős wiki; Feng et al.).

### Cited Findings

**Closest conceptual precedents (aggregate human-equivalent framings)**
- **MacAskill, W., & Moorhouse, F. (2025). *Preparing for the Intelligence Explosion*. arXiv:2506.14863 (v1 17 Jun 2025).**
  - What it does: defines "AI research effort" as the research-relevant cognitive effort of all deployed AI systems. It proposes measuring that effort "in terms of the number of remote human researchers that would be needed to make an equivalent contribution." AI–human "parity" is the point where AI's contribution equals doubling the number of human researchers.
  - Relevance: this is a forward-looking, economy-wide exchange rate (AI compute → human-researcher equivalents). It is the reverse direction of our per-problem historical conversion, and it does not price anything in dollars. — [arXiv abs](https://arxiv.org/abs/2506.14863); passage read in the [PDF](https://arxiv.org/pdf/2506.14863v1), Sec. 3, "AI-human cognitive parity", fn. 25.
- **OpenAI (2026-09-06). "Research acceleration: The view inside OpenAI." [lab self-report]**
  - Inference spend: by mid-August 2026 the median OpenAI researcher used "more than $600 per day of inference at API prices", and the 90th-percentile researcher "more than $7,000 of tokens per day".
  - Agent effort: "the research organization uses 3.1 agent-workdays of effort for every workday of human labor" (8-hour workday basis).
  - Relevance: this is the only published per-researcher inference-dollar figure from a frontier lab. Scaled to a year, $600/day × ~250 workdays ≈ $150k [my arithmetic], the same order as the $250k/research-year convention. OpenAI itself cautions that the overall pace of progress "likely won't keep pace with these specific metrics". — [OpenAI](https://openai.com/index/research-acceleration-view-inside-openai/) (read via the browser pane; plain fetch returned 403).
- **Cunningham, T., Althoff, L., Halperin, B., Jabarian, B., Koh, A., Ramani, A., Trammell, P., Whitfill, P., & Wu, C. (2026). *The Economics of Recursive Self-Improvement*. arXiv:2609.15802 (v1 14 Sep 2026).**
  - What it does: defines "R&D automatability" as AI able to make technological improvements "at least equivalent to those made by human researchers, at an equal cost". It calibrates feedback-loop elasticities and lists empirical objects labs should disclose.
  - Relevance: it gives a definitional anchor for cost-parity between AI and human research. It does not estimate per-problem effort. — [arXiv abs](https://arxiv.org/abs/2609.15802); definition read in the [HTML](https://arxiv.org/html/2609.15802v1).

**Economics precedent for the $/research-year conversion**
- **Bloom, N., Jones, C. I., Van Reenen, J., & Webb, M. (2020). Are Ideas Getting Harder to Find? *American Economic Review* 110(4): 1104–1144. doi:10.1257/aer.20180338.**
  - Verification: metadata via Crossref.
  - Method (from prior knowledge; not re-read): the paper measures "research effort" as an effective number of researchers, R&D spending deflated by the wage of high-skilled workers. It finds research productivity falling across domains.
  - Relevance: this is the standard precedent for treating a dollar per researcher-year as the unit of research input, as our D = $250k·H/s does. — [Crossref](https://api.crossref.org/works/10.1257/aer.20180338)
- **Besiroglu, T., Emery-Xu, N., & Thompson, N. (2022). *Economic impacts of AI-augmented R&D*. arXiv:2212.08198.**
  - What it does: estimates an "idea production function" for AI in two computer-vision tasks. It finds AI idea production "notably more capital-intensive than traditional R&D".
  - Relevance: an empirical attempt to put compute (capital) and researcher labor in one production function. — [arXiv abs](https://arxiv.org/abs/2212.08198)
- **Erdil, E., Besiroglu, T., & Ho, A. (2024). *Estimating Idea Production: A Methodological Survey*. arXiv:2405.10494.** Metadata verified only. A survey of how to estimate the elasticity of research output with respect to research input (from prior knowledge; not re-read). — [arXiv abs](https://arxiv.org/abs/2405.10494)
- **Erdil, E., Potlogea, A., Besiroglu, T., Roldan, E., Ho, A., Sevilla, J., Barnett, M., et al. (2025). *GATE: An Integrated Assessment Model for AI Automation*. arXiv:2503.04941.**
  - What it does: Epoch's model combining "a compute-based model of AI development", an AI automation framework and a semi-endogenous growth model.
  - Relevance: this is Epoch's formal treatment of compute substituting for labor. It works at the macro level, not per problem. — [arXiv abs](https://arxiv.org/abs/2503.04941)

**"How much human effort has gone into problem X" (open-math problems)**
- **Tao, T., and contributors. "AI contributions to Erdős problems" wiki and its "Disclaimers and caveats" page, github.com/teorth/erdosproblems (data frozen as of 30 Jun 2026).**
  - Disclaimer 5 is headed "Absence of past progress may reflect obscurity rather than difficulty". It warns against inferring difficulty from N years open. It then states that literature "expending effort on partial results without getting a clear path to a full solution" is "stronger evidence of the problem's difficulty".
  - Disclaimer 3 warns of selection bias from unreported negative results.
  - Relevance: this is the closest published statement of the logic behind counting partial-result literature as a measure of scrutiny. — [wiki](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems); [disclaimers, raw](https://raw.githubusercontent.com/wiki/teorth/erdosproblems/Disclaimers-and-caveats.md)
- **Feng, T., Trinh, T., Bingham, G., Kang, J., Zhang, S., Kim, S., et al. (2026). *Semi-Autonomous Mathematics Discovery with Gemini: A Case Study on the Erdős Problems*. arXiv:2601.22401 (v1 29 Jan 2026).**
  - What it does: Gemini screened 700 "Open" Erdős problems. 13 were addressed: 5 by apparently novel solutions, and 8 by finding existing solutions in the literature. The authors conclude the "Open" status was "through obscurity rather than difficulty".
  - Relevance: direct evidence that time-since-posing is a poor proxy for human scrutiny, which supports literature-based effort estimates. — [arXiv abs](https://arxiv.org/abs/2601.22401)
- **Tao, T. (2026). *Mathematics in the age of AI*. arXiv:2608.16753 (v1 17 Aug 2026; essay based on Tao's ICM 2026 public lecture).**
  - Reporting bias: public evidence on AI math is subject to "severe reporting bias — successes are announced and failures are not". Key cost variables ("the number of attempts, the amount of human scaffolding, the compute expended") are frequently undisclosed.
  - First Proof: cites the First Proof second batch, where 7 of 10 research-level problems got at least one passing grade, "with compute costs on the order of tens to hundreds of dollars per problem".
  - Relevance: an authoritative citation for our failure-accounting caveat. — [arXiv abs](https://arxiv.org/abs/2608.16753); passages read in the [PDF](https://arxiv.org/pdf/2608.16753)
- **Abouzaid, M., Srivastava, N., Ward, R., & Williams, L. (2026). *First Proof Second Batch*. arXiv:2606.18119 (v1 16 Jun 2026).**
  - What it does: ten unpublished research-level problems, with known human solutions, contributed by working mathematicians. Four AI systems were tested under controlled conditions and their outputs were refereed.
  - Relevance: a controlled AI-vs-human-solution comparison. Per-problem cost is reported only via Tao's summary; I did not read the cost table in the paper itself. — [arXiv abs](https://arxiv.org/abs/2606.18119)
- **Hales, T. C., Harrison, J., McLaughlin, S., Nipkow, T., Obua, S., & Zumkeller, R. (2009/2010). *A revision of the proof of the Kepler conjecture*. arXiv:0902.0350** (published in *Discrete & Computational Geometry* 2010; venue from prior knowledge).
  - Contains the explicit person-time estimate for a mathematical project: "We estimate that it may take about twenty workyears to complete this formalization project" (Flyspeck).
  - Completion is reported in **Hales, T., Adams, M., et al., *A formal proof of the Kepler conjecture*, arXiv:1501.02155 (2015)**, "the official published account of the now completed Flyspeck project".
  - Relevance: a rare author-stated work-year estimate in mathematics. It covers formalization, not discovery. — [arXiv 0902.0350](https://arxiv.org/abs/0902.0350) (quote read in PDF p.4); [arXiv 1501.02155](https://arxiv.org/abs/1501.02155)

**Lab statements that informally compare accumulated scrutiny with AI cost, or explicitly decline to**
- Anthropic's HAWK post contrasts "two rounds of expert human review over a period of two years" with the model's "60 hours of work" and ~$100k API cost [lab self-report]. This is an informal accumulated-scrutiny vs. AI-run comparison, with no conversion of the review into person-years. — [Anthropic](https://www.anthropic.com/research/discovering-cryptographic-weaknesses)
- Epoch's FrontierMath Erdős paper calls an expected ~$10,000 per resolution "modest for the resolution of an important open problem", with no human baseline. — [arXiv:2609.25050](https://arxiv.org/html/2609.25050), Sec. 5
- AlphaProof Nexus states verbatim: "We do not intend USD as a comparison of AI and human mathematical labor." — [arXiv:2605.22763v2](https://arxiv.org/html/2605.22763v2)

### Inferences
- I found no source doing what this study does: estimate person-years of public literature on a specific problem or assumption class, then express it as an inference budget under stated multipliers. The closest precedents are aggregate (MacAskill and Moorhouse; OpenAI agent-workdays) or per-task (METR, GDPval). The study can reasonably present the per-problem conversion as new, while citing Bloom et al. for the wage-deflation convention and MacAskill and Moorhouse for "human-researcher equivalent" units.
- Tao's disclaimer 5 and Feng et al. are the best citations for the design choice of measuring scrutiny by literature rather than by years open. They also support the caveat that AI successes cluster on low-scrutiny problems.
- Two labs (DeepMind explicitly, Epoch implicitly) avoid equating AI dollars with human labor. Anthropic makes only an informal "two years of review vs 60 hours" contrast. The study's own "conditional budget comparison, not exchange rate" framing matches the caution these sources show.

### Gaps
- Toby Ord's reported essay arguing that AI-math cost figures ignore failed attempts: only aggregator summaries were found (digg.com), with no primary URL. **Unverified; do not cite.**
- Carlsmith (2020), "How much computational power does it take to match the human brain?" (Open Philanthropy), is a classic human→FLOP/s conversion. The page returned HTTP 403 to curl and was not opened in a browser. **Unverified.** Cotra's "biological anchors" report was not checked.
- I searched for, but did not find, any published person-year estimate of cumulative effort on a famous open conjecture (e.g., Riemann, Goldbach, four colour), as distinct from a formalization project. Also not found: Epoch Gradient Update pieces comparing AI math cost with mathematician salaries (search returned only forum comments, e.g. LessWrong/Manifold, which are not citable).

---

## Q2. What are the canonical citable sources for AI-vs-human cost comparisons on research or expert tasks?

### Takeaway
The canonical sources are METR's time-horizon paper (Kwa et al., NeurIPS 2025), RE-Bench, HCAST, GDPval, Cost-of-Pass, PaperBench, the METR developer RCT, and Sakana's AI Scientist cost report.
- Where they quantify cost, the per-task ratios bracket our 1×/10×/100× scenarios.
  - Kwa et al.: over 80% of successful agent runs cost under 10% of a human engineer's wage-cost (≥10×, on successes only).
  - GDPval: GPT-5 is 474× cheaper "naively" but only 1.18–1.63× once human review and redo are counted.
- The METR RCT found a 19% *slowdown*, which is evidence that s can be near or below 1× in some settings.

### Cited Findings
- **Kwa, T., West, B., Becker, J., Deng, A., Garcia, K., Hasin, M., et al. (2025). *Measuring AI Ability to Complete Long Software Tasks*. NeurIPS 2025. arXiv:2503.14499 (v1 18 Mar 2025).**
  - Title: the current arXiv title (v4) adds "Software". It is widely cited by the v1 title, "Measuring AI Ability to Complete Long Tasks" (v1 title from prior knowledge).
  - Main finding: defines the "50%-task-completion time horizon", the human-expert time of tasks AI completes at 50% success. That horizon was about 50 minutes for Claude 3.7 Sonnet and has been doubling roughly every 7 months since 2019.
  - Cost comparison (Appendix H.3): with the human expert paid "$143.61/hour (average L4 Engineer salary at Google divided by 2,000 hours), more than 80% of successful runs cost less than 10% of what it would cost for a human to perform the same task."
  - Relevance: a canonical human-time→AI-capability conversion with a wage-based cost comparison. Note it counts successful runs only. — [arXiv abs](https://arxiv.org/abs/2503.14499); App. H.3 read in the [HTML v4](https://arxiv.org/html/2503.14499v4)
- **Wijk, H., Lin, T., Becker, J., Jawhar, S., Parikh, N., Broadley, T., et al. (2024). *RE-Bench: Evaluating frontier AI R&D capabilities of language model agents against human experts*. arXiv:2411.15114.**
  - Setup: 7 ML research-engineering environments, with 71 eight-hour attempts by 61 human experts.
  - Results: at a 2-hour total budget the best agents score 4× humans. Humans narrowly lead at 8 hours and score 2× the top agent at 32 hours. Agents "generate and test solutions over ten times faster than humans, at much lower cost".
  - Relevance: the standard matched human-vs-agent time-budget comparison on research tasks, showing humans have better returns to time. — [arXiv abs](https://arxiv.org/abs/2411.15114)
- **Rein, D., Becker, J., Deng, A., Nix, S., Canal, C., O'Connel, D., Arnott, P., Bloom, R., et al. (2025). *HCAST: Human-Calibrated Autonomy Software Tasks*. arXiv:2503.17354.** Metadata verified only. This is METR's human-timed task suite underlying the time-horizon metric. — [arXiv abs](https://arxiv.org/abs/2503.17354)
- **Patwardhan, T., Dias, R., Proehl, E., Kim, G., Wang, M., Watkins, O., et al. (2025). *GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks*. arXiv:2510.04374 (v1 5 Oct 2025). OpenAI. [lab self-report]**
  - Setup: tasks from 44 occupations, written by professionals averaging 14 years of experience. Human cost is self-reported completion hours × BLS (OEWS) median hourly wage.
  - Table 2, naive speed and cost improvements over experts: GPT-5 90× faster and 474× cheaper; GPT-4o 327× and 5172×.
  - Table 2, with human review and fallback ("Try 1x" / "Try n"): GPT-5 is only 1.12–1.39× faster and 1.18–1.63× cheaper. The paper notes that "when incorporating time to review and redo work, the payoff from using a model shrinks".
  - Relevance: the clearest published demonstration that the accounting boundary (inference only vs. including supervision) moves the multiplier by over two orders of magnitude. This directly supports excluding supervision from D and labelling it an inference-budget equivalent. — [arXiv abs](https://arxiv.org/abs/2510.04374); Table 2 and Sec. 2.3/A.2 read in the [HTML](https://arxiv.org/html/2510.04374v1)
- **Erol, M. H., El, B., Suzgun, M., Yuksekgonul, M., & Zou, J. (2025). *Cost-of-Pass: An Economic Framework for Evaluating Language Models*. arXiv:2504.13359.**
  - What it does: defines cost-of-pass as the expected dollars per correct solution, i.e. per-attempt cost ÷ success rate, the same construction as Epoch's $300/3% ≈ $10k. The "frontier cost-of-pass" takes the minimum over models *and a human expert* priced at "the approx. cost of hiring an expert".
  - Relevance: the most formal per-task AI-vs-human-expert cost framework. — [arXiv abs](https://arxiv.org/abs/2504.13359)
- **Becker, J., Rush, N., Barnes, E., & Rein, D. (2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*. arXiv:2507.09089.**
  - Design: an RCT with 16 developers and 246 tasks.
  - Result: allowing AI tools *increased* completion time by 19%, although developers believed it reduced time by 20%.
  - Relevance: an empirical counterweight showing productivity multipliers can fall below 1× for expert humans working with AI. Note this measures human+AI, not autonomous AI. — [arXiv abs](https://arxiv.org/abs/2507.09089)
- **Starace, G., Jaffe, O., Sherburn, D., Aung, J., Chan, J. S., Maksin, L., et al. (2025). *PaperBench: Evaluating AI's Ability to Replicate AI Research*. arXiv:2504.01848. OpenAI.**
  - What it does: agents replicate 20 ICML 2024 papers. The best agent averaged 21.0%. Recruited ML PhDs on a subset were not yet outperformed by models.
  - Relevance: an AI-vs-human-PhD comparison on research replication. — [arXiv abs](https://arxiv.org/abs/2504.01848)
- **Lu, C., Lu, C., Lange, R. T., Foerster, J., Clune, J., & Ha, D. (2024). *The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery*. arXiv:2408.06292. Sakana AI. [self-report]**
  - What it does: each idea is "implemented and developed into a full paper at a cost of less than $15 per paper". Quality was judged by its own automated reviewer.
  - Relevance: the canonical "cost per AI-generated paper" figure. It is not a human-equivalence measure, and paper quality is not comparable to the cryptanalytic literature. — [arXiv abs](https://arxiv.org/abs/2408.06292)
- **Aghion, P., Jones, B. F., & Jones, C. I. (2017). *Artificial Intelligence and Economic Growth*. NBER Working Paper 23928 (16 Oct 2017).**
  - Verification: NBER metadata only. Its later appearance in *The Economics of Artificial Intelligence: An Agenda* (Agrawal, Gans & Goldfarb, eds., U. Chicago Press, 2019) is from prior knowledge.
  - Content (from prior knowledge; not re-read): models AI as automating tasks in goods and idea production. Baumol-type bottlenecks can limit growth.
  - Relevance: the standard economics citation for AI automating research. — [NBER](https://www.nber.org/papers/w23928)
- **Erdil, E., & Besiroglu, T. (2023). *Explosive growth from AI automation: A review of the arguments*. arXiv:2309.11690.** Metadata verified only (abstract not read this session). The standard Epoch citation on whether automating R&D labor could produce explosive growth. — [arXiv abs](https://arxiv.org/abs/2309.11690)
- **Korinek, A. (2023). Generative AI for Economic Research: Use Cases and Implications for Economists. *Journal of Economic Literature* 61(4): 1281–1317. doi:10.1257/jel.20231736.** Metadata verified via Crossref only. — [Crossref](https://api.crossref.org/works/10.1257/jel.20231736)
- **Korinek, A., & Suh, D. (2024). *Scenarios for the Transition to AGI*. arXiv:2403.12107.** Metadata verified only. Macro scenarios for AI substituting for labor, including research labor (from prior knowledge). — [arXiv abs](https://arxiv.org/abs/2403.12107)
- **Glazer, E., Erdil, E., Besiroglu, T., et al. (2024). *FrontierMath: A Benchmark for Evaluating Advanced Mathematical Reasoning in AI*. arXiv:2411.04872.** Metadata verified. This is the parent benchmark of the Erdős set. — [arXiv abs](https://arxiv.org/abs/2411.04872)
- **Cottier, B., Rahman, R., Fattorini, L., Maslej, N., Besiroglu, T., & Owen, D. (2024). *The rising costs of training frontier AI models*. arXiv:2405.21015.** Metadata verified. Relevant only to the excluded training-cost component of D. — [arXiv abs](https://arxiv.org/abs/2405.21015)

### Inferences
- The literature consistently finds large multipliers when only inference cost on successes is counted: Kwa ≥10× for 80% of successes, GDPval up to ~500×, Sakana <$15/paper. It finds near-parity once supervision, review and failures are included: GDPval ~1.2–1.6×, RE-Bench humans ahead at long budgets, METR RCT 0.84× speed. The 1×/10×/100× range spans this published spread. That is a defensible justification for using scenarios rather than one rate.
- Cost-of-Pass gives the formal name for "per-attempt cost ÷ success rate". Citing it alongside Epoch's $10k figure would make the failure-accounting step standard rather than ad hoc.

### Gaps
- None of these sources involves mathematics or cryptanalysis tasks of research-paper size. All are software, ML-engineering, or professional-deliverable tasks of hours to days. Transfer to multi-year research problems is untested.
- I did not open METR's later domain-comparison posts (e.g., time horizons across domains). The METR task-cost dataset was not checked beyond Kwa App. H.3.

---

## Q3. What are the primary disclosures for the 2026 AI math and cryptanalysis results used in the study? (verified bibliographic entries)

### Takeaway
All eleven primary sources in the study's AI-side set were opened and their authors, titles and dates confirmed. The cost figures in data/ai_effort/ai_results.yaml match the primary text for Anthropic, Epoch, AlphaProof Nexus and the OpenAI Navier–Stokes and October-6 posts. One nuance is noted below: the Anthropic post's wording on what the $100k covers.

### Cited Findings
- **Adamczewski, T. (Epoch AI), & Bloom, T. F. (U. Manchester) (2026). *FrontierMath Erdős*. arXiv:2609.25050 (v1 6 Sep 2026).**
  - Benchmark: $300 and 72 h per attempt. GPT-6 Astra scored 3% (#74 $218/15 h; #126 $247/16 h); other models scored 0.
  - Additional non-benchmark attempts cost "over $220,000 of compute", vs ~$20,000 for the benchmark run.
  - Sec. 5: "the expected cost of a resolution is roughly $10,000".
  - Sec. 3.1 says most problems "received a great deal of attention" but some were "forgotten by human mathematicians until the website popularised them".
  - Companion blog: "Announcing FrontierMath Erdős" (epoch.ai, opened, HTTP 200). The YAML records blog-vs-paper discrepancies in attempt counts and costs. — [arXiv abs](https://arxiv.org/abs/2609.25050); [HTML](https://arxiv.org/html/2609.25050); [Epoch blog](https://epoch.ai/latest/announcing-frontiermath-erdos)
- **Tsoukalas, G., Kovsharov, A., Shirobokov, S., Surina, A., Firsching, M., Bérczi, G., Ruiz, F. J. R., Suggala, A., et al. (2026). *Advancing Mathematics Research with AI-Driven Formal Proof Search*. arXiv:2605.22763 (v1 21 May 2026; v2 8 Jun 2026). Google DeepMind ("AlphaProof Nexus"). [lab self-report]**
  - Costs: "a few hundred dollars per problem" of LLM inference, plus AlphaProof at "approximately 27.5 TPU hours ($60 USD) per problem on v6e TPUs".
  - The paper states that the reported costs "do not capture the full cost of discovery". The 353-problem sweep was "a significant computational investment", with no figure given. It also disclaims USD as a labor comparison.
  - Note the title: the paper is not titled "AlphaProof Nexus"; cite it by its arXiv title. — [arXiv abs](https://arxiv.org/abs/2605.22763); [HTML v2](https://arxiv.org/html/2605.22763v2)
- **Anthropic Frontier Red Team (2026-07-28; edited 29 Jul). "Discovering cryptographic weaknesses with Claude." No individual byline. [lab self-report]**
  - Model: Claude Mythos Preview.
  - HAWK: "Finding, developing and verifying the attack took about 60 hours in total". "the full attack discovery process cost approximately $100,000 in API cost".
  - Human input on HAWK was "limited to project management". "it took two researchers nearly a month to gain confidence that the method it discovered is correct".
  - AES (7-round, MITM): about one billion output tokens. Anthropic researchers then "spent several hundred hours" validating it.
  - The post also says "Each of the results cost roughly $100,000 in API cost to develop."
  - Nuance: the post presents ~$100k as a per-result figure. Whether failed earlier campaigns are included is not stated. — [Anthropic](https://www.anthropic.com/research/discovering-cryptographic-weaknesses)
- **Straznickas, Z., & Weis, S. A. (2026). *HAWK-n Key Recovery Reduces to SVP in Dimension n/2+1*. Cryptology ePrint Archive, Paper 2026/1593** (received 2026-08-03, approved 2026-08-06; CC BY).
  - Result: key-recovery cost (gate-count model) falls for HAWK-512 from 2^150 to 2^108 and for HAWK-1024 from 2^288 to 2^182. HAWK-256 keys were recovered end-to-end "in a few hours on a single server".
  - Versions: Anthropic-hosted PDF with identical title and authors, PDF CreationDate 24 Jul 2026 23:22 EDT. — [ePrint](https://eprint.iacr.org/2026/1593); [Anthropic PDF](https://www-cdn.anthropic.com/e8d50c167ad47beeb03d6109a4a484be95cb38ea/hawk_key_recovery.pdf); [code README](https://github.com/anthropics/cryptography-research-demo/blob/main/HAWK/README.md) (HTTP 200)
- **Mureau, G., & Pellet-Mary, A. (2026). *Dimension Reduction for SVP in Hawk: A Trace-Zero Approach*. Cryptology ePrint Archive, Paper 2026/1560** (received 2026-07-30, revised 2026-08-03).
  - Result: building on Chevignard et al. (Eurocrypt'25), it reduces Hawk key recovery to exact SVP in dimension ≤ 3m/8+1, improving on Ducas's m/2+1.
  - Note: the abstract uses m for the cyclotomic conductor, so 3m/8+1 = 3n/4+1 in ring-degree notation. This is a human result with no AI attribution in the abstract. — [ePrint](https://eprint.iacr.org/2026/1560)
- **Luo, H., Jiang, K., & Pan, Y. (2026). *Lifting Symmetries for Dimension Reduction in Module-LIP: rank 2 and rank 4*. Cryptology ePrint Archive, Paper 2026/2198** (received 2026-09-24, approved 2026-09-26).
  - Context: the abstract names three independent algorithms. "The Claude-derived algorithm uses dimensions at most n/2+1, and the ChatGPT-derived and Mureau–Pellet-Mary algorithms use 3n/4+1". It states that the impact on parameters "led the HAWK team to withdraw the scheme".
  - Its own rank-2 reduction matches 3n/4+1 and "does not constitute a substantively new reduction" relative to the ChatGPT-derived one.
  - Relevance: an independent (non-lab) secondary source confirming the AI/human chronology. — [ePrint](https://eprint.iacr.org/2026/2198)
- **Anonymous research draft (attributed in the study's YAML to Hengyi Luo's group via the pqc-forum, 28 Jul 2026), *Adjoint-Lattice Reduction for the HAWK Gram-Factor Problem: A Reduction to γ-SVP in Dimension 3n/4+1*, dated 17 July 2026.**
  - Verification: the PDF was opened (HTTP 200) and its first page reads "Anonymous research draft, 17 July 2026".
  - Attribution: the GPT-5.6 attribution and the author group come from the pqc-forum post, which I did not re-open. Cite with care. — [PDF](https://harylo.github.io/files/preprints/adjoint-lattice-reduction-for-the-hawk-gram-factor-problem.pdf)
- **OpenAI (2026-09-08; updated 10 Sep). "On the Navier–Stokes Millennium Prize Problem." Author: OpenAI. [lab self-report]**
  - Model: an "internal model that is significantly more capable than GPT-6 Astra".
  - Scale: "on the order of 10,000 concurrent agents". Resolution came "about 88 hours after the first agents were launched", plus 17 h of Lean formalization via GPT-6 Astra.
  - Tokens: "Across all attempted problems, the agents sent 4.9 million messages and used about 300 billion output tokens." For Navier–Stokes alone, "2.7 million messages and … approximately 130 billion output tokens".
  - The unforced Euler disproof used "Nearly 100 agents … approximately 50 hours". No dollar figure is given. The model was swapped mid-run.
  - Note: the page lists the post under the title "An OpenAI model proposes a solution to the Navier–Stokes problem" in "Keep reading" links. The page H1 is "On the Navier–Stokes Millennium Prize Problem". — [OpenAI](https://openai.com/index/navier-stokes-solution/) (read via the browser pane; plain fetch returned 403)
- **OpenAI (2026-10-06). "Sharing AI progress in mathematics." [lab self-report]**
  - Post: "The average result used the equivalent compute of roughly three hours of ChatGPT Pro thinking."
  - Repository: openai/math README states "719 manuscripts organized into 372 families". "On average, each result used three hours of ChatGPT Pro thinking compute". "the model was posed approximately 4,000 problems". — [OpenAI](https://openai.com/index/sharing-ai-progress-in-mathematics/); [README](https://raw.githubusercontent.com/openai/math/main/README.md)
- **Fei, Y., Minzer, D., & Wang, S. (2026). *On the Hardness of 4-to-1 Games with Perfect Completeness*. arXiv:2610.12378 (v1 8 Oct 2026).** Metadata verified. This is the human comparator to OpenAI family 105. — [arXiv abs](https://arxiv.org/abs/2610.12378)
- **Alon, N., Bloom, T. F., Gowers, W. T., Litt, D., Sawin, W., Shankar, A., Tsimerman, J., Wang, V., et al. (2026). *Remarks on the disproof of the unit distance conjecture*. arXiv:2605.20695 (v1 20 May 2026).** Metadata verified. This is the expository companion to OpenAI's Erdős #90 disproof. — [arXiv abs](https://arxiv.org/abs/2605.20695)

### Inferences
- Every AI-side cost figure in the study except Epoch's comes from the lab that built the model. Epoch evaluated OpenAI and Anthropic models on its own harness, but the Astra prices it used were stand-ins (YAML note, paper fn. 8). The paper's self-evaluation caveat should extend to the OpenAI and DeepMind figures, not only Anthropic's.
- The Luo–Jiang–Pan abstract is a useful neutral citation for the claim that the HAWK withdrawal followed the AI-derived results.

### Gaps
- The pqc-forum thread (groups.google.com/a/list.nist.gov/g/pqc-forum/c/2r2u6SbHun4), the NIST/HAWK withdrawal notice, and the Quanta/NPR secondary cost estimates were not re-opened this session. They rely on the YAML's earlier collection.
- The First Proof second-batch cost table was not read directly.

---

## Q4. What prior AI-assisted cryptanalysis (pre-2026) should be cited canonically?

### Takeaway
A small canonical set suffices:
- Gohr (CRYPTO 2019) for neural distinguishers;
- the SALSA line (Wenger, Li, Lauter et al.; NeurIPS 2022 → CCS 2023 → NeurIPS 2023) for ML attacks on LWE;
- Cybench and NYU CTF Bench for LLM agents on crypto/security CTFs.

None of these reports human-effort comparisons. SALSA PICANTE states plainly that it does not threaten NIST LWE parameters.

### Cited Findings
- **Gohr, A. (2019). *Improving Attacks on Round-Reduced Speck32/64 using Deep Learning*. CRYPTO 2019 (LNCS 11693). Cryptology ePrint Archive 2019/037.** Neural-network distinguishers on Speck32/64 outperform classical differential distinguishers in a low-data chosen-plaintext setting. — [ePrint](https://eprint.iacr.org/2019/037) (pub. info: "Published by the IACR in CRYPTO 2019")
- **Wenger, E., Chen, M., Charton, F., & Lauter, K. (2022). *SALSA: Attacking Lattice Cryptography with Transformers*. NeurIPS 2022. arXiv:2207.04785.** Transformers recover secrets of small-dimension LWE with sparse binary secrets. — [arXiv abs](https://arxiv.org/abs/2207.04785)
- **Li, C., Sotáková, J., Wenger, E., Malhou, M., Garcelon, E., Charton, F., & Lauter, K. (2023). *SALSA PICANTE: a machine learning attack on LWE with binary secrets*. ACM CCS 2023, doi:10.1145/3576915.3623076. arXiv:2303.04178; ePrint 2023/340.**
  - Result: recovers secrets up to n=350, h≈n/10.
  - The authors state it "does not threaten NIST's proposed LWE standards".
  - Verification: the CCS venue and DOI come from search-result metadata (deepai / paperswithcode); the arXiv record was verified. — [arXiv abs](https://arxiv.org/abs/2303.04178); [ePrint](https://eprint.iacr.org/2023/340)
- **Li, C. Y., Wenger, E., Allen-Zhu, Z., Charton, F., & Lauter, K. (2023). *SALSA VERDE: a machine learning attack on Learning With Errors with sparse small secrets*. NeurIPS 2023. arXiv:2306.11641.** Extends the attack to ternary and Gaussian secrets. — [arXiv abs](https://arxiv.org/abs/2306.11641)
- **Stevens, S., Wenger, E., Li, C., Nolte, N., Saxena, E., Charton, F., & Lauter, K. (2024). *Salsa Fresca: Angular Embeddings and Pre-Training for ML Attacks on Learning With Errors*. arXiv:2402.01082.** Metadata verified. — [arXiv abs](https://arxiv.org/abs/2402.01082)
- **Zhang, A. K., Perry, N., Dulepet, R., Ji, J., Menders, C., Lin, J. W., Jones, E., Hussein, G., et al. (2024). *Cybench: A Framework for Evaluating Cybersecurity Capabilities and Risks of Language Models*. ICLR 2025 (Oral). arXiv:2408.08926.**
  - What it does: a professional-CTF benchmark that includes crypto tasks. Difficulty is calibrated by human first-solve time (from prior knowledge).
  - Relevance: an early "human-time-calibrated" security benchmark. — [arXiv abs](https://arxiv.org/abs/2408.08926)
- **Shao, M., Jancheska, S., Udeshi, M., Dolan-Gavitt, B., Xi, H., Milner, K., Chen, B., Yin, M., et al. (2024). *NYU CTF Bench: A Scalable Open-Source Benchmark Dataset for Evaluating LLMs in Offensive Security*. arXiv:2406.05590.** Metadata verified. — [arXiv abs](https://arxiv.org/abs/2406.05590)
- Adjacent unit-conversion precedent in cryptography (not human effort): **Lenstra, A. K., Kleinjung, T., & Thomé, E. (2013). *Universal security; from bits and mips to pools, lakes – and beyond*. ePrint 2013/635.** Expresses security levels as the energy needed to boil volumes of water (from prior knowledge). — [ePrint](https://eprint.iacr.org/2013/635)
- On the scarcity of cryptanalytic attention: **Bernstein, D. J. (2020). *Cryptographic competitions*. ePrint 2020/1608; minor revision of the version in *Journal of Cryptology* (2024).** Surveys competition procedures and the extent to which they reduce security risk. — [ePrint](https://eprint.iacr.org/2020/1608)

### Inferences
- Pre-2026 ML cryptanalysis delivered narrow, parameter-specific attacks with training-compute reporting and no human-effort framing. The 2026 HAWK case is the first in which a general model produced a structural reduction on a NIST candidate, with a disclosed dollar cost. That makes it the natural (single) in-domain anchor.

### Gaps
- I did not check pre-2026 reports of LLMs solving crypto-specific CTF categories with cost figures. I also did not check later SALSA-team benchmarking papers (e.g., "Benchmarking attacks on LWE", 2024), which were not searched.
- Venue page numbers for Gohr (LNCS 11693) and the SALSA papers come from prior knowledge, not publisher pages.

---

### Unverified or excluded items (what was tried)
- **Toby Ord, essay on failed-attempt costs in AI math**: only digg.com aggregator summaries found; no primary URL located. Excluded.
- **Carlsmith (2020), Open Philanthropy brain-compute report**: openphilanthropy.org returned 403 to curl. Not retried in the browser. Excluded.
- **"Picante" under arXiv 2302.04981**: that ID is an unrelated paper (AutoNMT). The correct ID is 2303.04178, verified above.
- **Science (Duraisamy ~$6M) and BBC (~$10M) Navier–Stokes cost estimates**: already marked unverified in the YAML. Not re-attempted.
- **LessWrong/Manifold estimates of FrontierMath cost per solution vs. grad-student pay**: forum comments only, not citable.
