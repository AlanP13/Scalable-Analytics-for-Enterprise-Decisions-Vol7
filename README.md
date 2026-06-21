# Scalable Analytics for Enterprise Decisions

### From MapReduce to Holiday-Aware Demand Forecasting

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20733992.svg)](https://doi.org/10.5281/zenodo.20733992)
[![Paper License: CC BY 4.0](https://img.shields.io/badge/Paper-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)

Companion repository for **Volume 7 of 10** in the **Engineering-to-Research Monograph Series** by **Alan Biju Palayil**.

> Enterprises do not lack data; they lack the path from data to decisions. This monograph joins the infrastructure half (MapReduce, Spark) and the modeling half (tree ensembles) into one decision-oriented workflow, and argues that for tabular enterprise data, better features and validation beat bigger models.

---

## Contents

- [About this repository](#about-this-repository)
- [The monograph](#the-monograph)
- [Framework at a glance](#framework-at-a-glance)
- [Repository structure](#repository-structure)
- [Companion code](#companion-code)
- [Figures](#figures)
- [How to cite](#how-to-cite)
- [The Engineering-to-Research series](#the-engineering-to-research-series)
- [Versioning](#versioning)
- [License](#license)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

---

## About this repository

This repository is the reproducible companion to the technical report *Scalable Analytics for Enterprise Decisions: From MapReduce to Holiday-Aware Demand Forecasting*. It holds the published paper, the source figures, and the coursework-derived code behind the paper's two implementation studies. The archival record of the paper lives on Zenodo with a permanent DOI; this repository is where the supporting artifacts and code live and evolve.

The paper is a synthesis and framework contribution. Its value is in placing effort correctly across the analytics pipeline: spend scale on feature engineering and validation, keep the model an interpretable tree ensemble, and treat reconciliation and exception monitoring in financial operations as the same workflow applied to anomaly detection.

---

## The monograph

- **Title:** Scalable Analytics for Enterprise Decisions: From MapReduce to Holiday-Aware Demand Forecasting
- **Series:** Engineering-to-Research Monograph Series, Volume 7 of 10
- **Type:** Technical report / research monograph
- **Version:** 1.0 (June 2026)
- **DOI:** [10.5281/zenodo.20733992](https://doi.org/10.5281/zenodo.20733992) (version 1.0)
- **Paper:** [`paper/04_Monograph_7_Scalable_Analytics_for_Enterprise_Decisions.pdf`](paper/04_Monograph_7_Scalable_Analytics_for_Enterprise_Decisions.pdf)

**Abstract.** Enterprises do not lack data; they lack the path from data to decisions. That path has two halves that are usually taught and tooled separately: the infrastructure half (MapReduce, Spark, distributed storage) and the modeling half (turning features into accurate, trustworthy predictions). This report joins the two halves into a single decision-oriented analytics workflow and argues that for the tabular data on which most enterprise decisions rest, scale should be spent on feature quality and validation, not on model complexity, and tree-ensemble models remain the rational default. The argument is grounded in two implementation studies: a holiday-aware retail demand-forecasting pipeline with engineered calendar and macroeconomic features, and an Extremely Randomized Trees model for vehicle-price prediction emphasizing feature importance for decision support.

---

## Framework at a glance

**The data-to-decision workflow.** Five stages, each with a governing question: ingest and store, process at scale, engineer features, model, validate and monitor. Decision quality is won in feature engineering and validation, not in raw model complexity.

**Design Principle 1 (Feature-First Analytics).** For tabular enterprise data, marginal decision quality is gained more cheaply by improving feature engineering and validation than by increasing model complexity. The model should be the simplest one that captures the signal and exposes which features drive it.

**Original contributions.**

1. A five-stage data-to-decision workflow that names where decision quality is won.
2. The feature-first design principle, with supporting evidence from the tabular-ML literature.
3. A modeling-approach evaluation for tabular enterprise data (rules, deep networks, tree ensembles, the feature-first workflow).
4. An enterprise and financial-operations mapping, casting reconciliation and exception monitoring as anomaly detection.

---

## Repository structure

```text
scalable-analytics-for-enterprise-decisions-vol7/
├── README.md
├── LICENSE                      # MIT, applies to /code only
├── LICENSE-CC-BY-4.0.txt        # CC BY 4.0, applies to /paper and /figures
├── CITATION.cff
├── RESULTS.md                   # quantitative metrics referenced by the paper
├── .zenodo.json                 # Zenodo deposit metadata (root-level name required)
├── paper/
│   ├── 04_Monograph_7_Scalable_Analytics_for_Enterprise_Decisions.pdf
│   └── 04_Monograph_7_Scalable_Analytics_for_Enterprise_Decisions.docx
├── figures/
│   ├── vol7_fig1_data_to_decision_workflow.svg / .png
│   └── vol7_fig2_feature_first_payoff.svg / .png
└── code/
    ├── its836-holiday-forecasting/   # holiday-aware demand forecasting (Python)
    └── msds532-vehicle-price/        # Extremely Randomized Trees regression (Python)
```

---

## Companion code

- **`code/its836-holiday-forecasting/`** A demand-forecasting pipeline over a large Walmart dataset: merges weekly sales with store features, engineers a holiday-window feature, adds markdowns and macroeconomic indicators (CPI, unemployment), models with tree-based regression, and validates on held-out periods (Section 7).
- **`code/msds532-vehicle-price/`** An Extremely Randomized Trees regressor for vehicle-price prediction with cleaning, exploratory analysis, categorical encoding, and a feature-importance ranking used as a first-class decision output (Section 7).

> Code is provided for reproducibility and study. Some artifacts originated as graduate coursework and have been cleaned for release. Each subfolder's README states its dependencies and how to run it.

---

## Figures

1. **Figure 1, The Data-to-Decision Workflow.** Five stages with governing questions, highlighting where decision quality is won.
2. **Figure 2, The feature-first thesis.** Where to spend scale, and the rational default model for tabular enterprise data.

Both are provided as editable SVG and rendered PNG.

---

## How to cite

A machine-readable [`CITATION.cff`](CITATION.cff) is included; GitHub renders a "Cite this repository" button from it. The DOI 10.5281/zenodo.20733992 is embedded in `CITATION.cff`, the paper, and the citation blocks below.

**IEEE.** A. B. Palayil, "Scalable Analytics for Enterprise Decisions: From MapReduce to Holiday-Aware Demand Forecasting," Engineering-to-Research Monograph Series, vol. 7, 2026. doi: 10.5281/zenodo.20733992.

**BibTeX.**

```bibtex
@techreport{palayil2026scalable,
  author      = {Palayil, Alan Biju},
  title       = {Scalable Analytics for Enterprise Decisions: From MapReduce to Holiday-Aware Demand Forecasting},
  institution = {Engineering-to-Research Monograph Series},
  number      = {Volume 7 of 10},
  year        = {2026},
  version     = {1.0},
  doi         = {10.5281/zenodo.20733992},
  url         = {https://doi.org/10.5281/zenodo.20733992}
}
```

---

## The Engineering-to-Research series

This is Volume 7 of a ten-volume program that turns a decade of engineering and research training into one coherent research identity, ending in explainable-AI governance. Volume 1 (Securing Connected Systems) is published at [10.5281/zenodo.20733453](https://doi.org/10.5281/zenodo.20733453).

| Vol | Title | Theme |
|----|----|----|
| 1 | Securing Connected Systems | Network and edge security |
| 2 | Computer Architecture for Security Engineers | Hardware security |
| 3 | Secure Systems Engineering | Secure coding and concurrency |
| 4 | Embedded-to-Edge-AI Reference Architecture | Edge AI |
| 5 | Teaching Offensive Security | Pedagogy and leadership |
| 6 | ERM and Cybersecurity Governance | Governance |
| 7 | Scalable Analytics for Enterprise Decisions | Big data |
| 8 | Data Mining for Financial Systems | Financial technology |
| 9 | Research Methods for Applied Computing | Methodology |
| 10 | From Embedded Systems to Explainable AI Governance | Synthesis capstone |

---

## Versioning

This repository follows the monograph version. Version 1.0 corresponds to the first Zenodo deposit. Future revisions will be released as new Zenodo versions under the same concept DOI, and tagged here with matching GitHub releases.

---

## License

- **Paper and figures** (`/paper`, `/figures`): Creative Commons Attribution 4.0 International (CC BY 4.0). See `LICENSE-CC-BY-4.0.txt`.
- **Code** (`/code`): MIT License. See `LICENSE`.

---

## Author

**Alan Biju Palayil**
Independent Researcher; Application Development Analyst, Financial Services; Doctoral Researcher, University of the Cumberlands.
ORCID: [0009-0004-8302-5090](https://orcid.org/0009-0004-8302-5090)
GitHub: [@AlanP13](https://github.com/AlanP13)

---

## Acknowledgments

The implementation studies originated in graduate coursework at the University of the Cumberlands: Data Science and Big Data Analytics (ITS-836) and Data Science Programming (MSDS-532). All synthesis, analysis, framework development, and writing are the author's own and were written from scratch for publication, and contain no confidential employer information.
