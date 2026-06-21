:::center
# Scalable Analytics for Enterprise Decisions

### From MapReduce to Holiday-Aware Demand Forecasting

*Engineering-to-Research Monograph Series, Volume 7 of 10*

**Alan Biju Palayil**

Independent Researcher · Application Development Analyst, Financial Services · Doctoral Researcher, University of the Cumberlands

ORCID: [0009-0004-8302-5090](https://orcid.org/0009-0004-8302-5090)

Version 1.0 · June 2026

DOI: [10.5281/zenodo.20733992](https://doi.org/10.5281/zenodo.20733992)

Companion code: [github.com/AlanP13/Scalable-Analytics-for-Enterprise-Decisions-Vol7](https://github.com/AlanP13/Scalable-Analytics-for-Enterprise-Decisions-Vol7)

License: Text CC BY 4.0 · Companion code MIT

**Keywords:** big data, MapReduce, Spark, demand forecasting, feature engineering, tree ensembles, gradient boosting, extremely randomized trees, tabular data, enterprise analytics, financial operations

---

*Engineering-to-Research Monograph Series · Volume 7 of 10*
:::

[PAGEBREAK]

## Executive Summary

**Problem.** Enterprises do not lack data. They lack a reliable path from data to decisions. That path has two halves that are usually taught and tooled apart: the infrastructure half (how to store and process data at scale) and the modeling half (how to turn features into accurate, trustworthy predictions). When teams optimize the showy parts of each half, large-scale infrastructure and complex models, and under-invest in the quiet parts, feature quality and honest validation, decision quality suffers and models that look good in a notebook fail in production.

**Findings.** For the structured, tabular data on which most enterprise decisions rest, the marginal return on model sophistication is low and the marginal return on feature engineering and validation is high. Deep learning, which transformed vision and language, has repeatedly failed to dominate tree-ensemble methods on tabular problems. Distribution (Spark) earns its cost mainly in the ingest and feature stages, not in the modeling step, because the feature matrices behind most decisions fit in memory after aggregation.

**Framework.** This report offers a five-stage data-to-decision workflow, a stated design principle that for tabular enterprise data better features beat bigger models, and an evaluation of modeling approaches that places interpretable tree ensembles as the rational default. Two implementation studies ground the argument: a holiday-aware retail demand-forecasting pipeline and an Extremely Randomized Trees model for vehicle-price prediction that treats feature importance as a first-class output.

**Recommendations.** Spend scale where it pays, namely on leak-free feature engineering and out-of-period validation with drift monitoring. Keep the model a transparent, well-calibrated tree ensemble whose drivers a decision-maker can see. Adopt newer architectures only when they beat a well-validated tree-ensemble baseline by enough to justify their cost and opacity. Treat reconciliation and exception monitoring in financial operations as the same workflow applied to anomaly detection, which is the bridge to Volume 8 and to the governance and explainability themes of the series.

[PAGEBREAK]

## Table of Contents

1. Introduction .... 4
2. Related Work .... 4
3. A Data-to-Decision Workflow .... 5
4. The Big-Data Foundation: When Scale Actually Matters .... 6
5. From Storage to Signal: Feature Engineering .... 7
6. Modeling for Decisions: Why Tree Ensembles Remain the Default .... 7
7. Case Studies .... 8
8. The Enterprise and Financial-Operations Bridge .... 10
9. Synthesized Contributions .... 10
10. Approach Evaluation .... 10
11. From Accuracy to Trust: Validation, Drift, and Explainability .... 11
12. Limitations .... 12
13. Future Work .... 12
14. Conclusion .... 12

Acknowledgments and References .... 13

Appendix A. Methodology and Implementation Details .... 14

## List of Figures

Figure 1. The Data-to-Decision Workflow .... 6

Figure 2. The Feature-First Thesis for Tabular Enterprise Data .... 8

[PAGEBREAK]

## Abstract

Enterprises do not lack data; they lack the path from data to decisions. That path has two halves usually taught and tooled separately: the infrastructure half (MapReduce, Spark, distributed storage) and the modeling half (turning features into accurate, trustworthy predictions). This report joins the two halves into a single decision-oriented analytics workflow and argues a deliberately unfashionable thesis: for the tabular data on which most enterprise decisions rest, scale should be spent on feature quality and validation, not on model complexity, and tree-ensemble models remain the rational default. The argument is grounded in two implementation studies the author conducted: a holiday-aware retail demand-forecasting pipeline built on a large Walmart dataset with engineered calendar and macroeconomic features, and an Extremely Randomized Trees model for vehicle-price prediction that treats feature importance as a first-class decision output. It situates both against the 2008 to 2026 literature on big-data processing and tabular learning, contributes a five-stage workflow and a feature-first design principle, evaluates modeling approaches for tabular enterprise data, and extends the workflow to financial reconciliation and exception monitoring. It closes with the validation, drift, and explainability concerns that connect this volume to the governance and explainable-AI volumes of the series.

---

## 1. Introduction

A retail planner deciding how much inventory to stock before a holiday, an analyst reconciling millions of daily financial transactions, and an operations team triaging exceptions all face the same problem in different clothing. A large volume of structured data must become a small number of reliable decisions. The data-science curriculum tends to split this problem in two. Courses on big data teach the infrastructure, namely distributed storage, MapReduce, and Spark, while courses on machine learning teach the models. In practice the two are inseparable. Infrastructure choices determine which features can be computed at all, and modeling choices determine whether the infrastructure investment yields better decisions or merely faster ones.

This report integrates the two halves into one decision-oriented workflow and defends a specific, evidence-backed position. For the tabular, structured data that dominates enterprise decision-making, the marginal return on model sophistication is low and the marginal return on feature engineering and validation is high. Deep learning, which transformed vision and language, has repeatedly failed to dominate tree-ensemble methods on tabular problems. The practical consequence is a workflow in which scalable infrastructure is used to build better features and more honest validation, while the model itself stays a well-understood, well-calibrated tree ensemble.

The contributions are stated in Section 9 and evaluated in Section 10. In brief: a five-stage data-to-decision workflow (Section 3), a grounded account of when scale matters (Section 4), two implementation case studies with their evaluation protocols (Section 7), and a treatment of trust through validation, drift, and explainability that bridges to later volumes (Section 11). Limitations are stated plainly in Section 12 and implementation details in Appendix A.

---

## 2. Related Work

Three bodies of work inform this report. Table 1 summarizes their main insight and their limitation for enterprise tabular decisions.

**Big-data processing.** MapReduce established that computation should move to the data and that large jobs can be expressed as map and reduce phases over a distributed file system [8]. Its limitation is that each phase reads from and writes to disk, so iterative workloads, which is the shape of most model training, pay repeated input and output costs [8]. Apache Spark addressed this by keeping working data in memory across iterations, lowering latency for iterative workloads and enabling near-real-time processing [6]. This literature is mature and is the infrastructure backbone of the workflow here, but it is silent on which modeling choices actually improve decisions.

**Demand forecasting.** Retail and demand forecasting is a deep applied literature. Recent work compares deep neural networks for retail forecasting and proposes new architectures [1], while established results show that careful treatment of calendar effects and special days materially improves daily retail forecasts [3]. Scalable probabilistic forecasting with gradient-boosted trees is an actively used practitioner approach for very large retail datasets [2]. The limitation is that much of this literature optimizes a forecasting model in isolation rather than the end-to-end decision pipeline.

**Tabular machine learning.** A growing body of controlled comparison finds that deep-learning models do not reliably beat well-tuned gradient-boosted trees on tabular data, that the trees require far less tuning, and that gains from deep models, where they exist, are modest and often come only in ensemble with trees [4], [5], [7]. The limitation is that tabular deep learning continues to attract effort disproportionate to its measured benefit on enterprise data.

**Table 1. Comparison of the informing literatures.**

| Area | Main insight | Limitation for enterprise tabular decisions |
|---|---|---|
| MapReduce [8] | Move computation to the data; express jobs as map and reduce | High latency from repeated disk input and output; poor for iterative training |
| Spark [6] | In-memory processing speeds iteration and enables near-real-time work | Operational complexity; unnecessary when data fits in memory after aggregation |
| Deep learning [1], [4], [5] | Strong on images, text, and sequences | Does not reliably beat tuned tree ensembles on tabular data; high tuning and opacity cost |
| Tree ensembles [2], [5], [7] | Strong accuracy on tabular data with native feature importance | Less expressive for unstructured data; still requires disciplined feature engineering |

**The gap.** Each literature is strong within its half. Big-data work optimizes infrastructure; forecasting and tabular-ML work optimize models. What is missing is an integrated, decision-oriented account that says where in the pipeline scale actually pays for enterprise tabular problems. This report supplies that account.

---

## 3. A Data-to-Decision Workflow

The workflow has five stages, each with a governing question, shown in Figure 1.

![Figure 1. The Data-to-Decision Workflow. Five stages, each with a governing question. Stages 3 and 5, feature engineering and validation, are where decision quality is won; stages 2 and 4 are where effort is usually over-invested.](figures/vol7_fig1_data_to_decision_workflow.png)

1. **Ingest and store.** Can the data be landed reliably and queried at the needed granularity?
2. **Process at scale.** Does the transformation truly require distribution, or is single-node sufficient?
3. **Engineer features.** What signal does the decision depend on, and can it be computed without leakage?
4. **Model.** What is the simplest model that captures the signal and exposes which features drive it?
5. **Validate and monitor.** Will this hold on data the model has never seen, and will it keep holding?

The recurring mistake in enterprise analytics is to over-invest in Stage 2 (impressive infrastructure) and Stage 4 (impressive models) while under-investing in Stages 3 and 5, which is where decision quality is actually won or lost. The rest of the report follows this workflow.

---

## 4. The Big-Data Foundation: When Scale Actually Matters

**Data types and the case for distribution.** Enterprise data spans structured (transactional tables), semi-structured (logs, JSON), and unstructured (documents, images) forms. The first decision is honest sizing. A great deal of big-data work is performed on datasets that fit on one machine, where distribution adds latency and operational complexity without benefit. Distribution earns its cost when data exceeds single-node memory or storage, when ingestion is continuous, or when many independent transformations can run in parallel.

**MapReduce and its limits.** MapReduce is excellent for large single-pass transformations and aggregations and poor for the iterative inner loops of model training, because each phase reads from and writes to disk [8]. The author worked through the MapReduce programming model directly in ITS-836, which makes this trade-off concrete.

**Spark and in-memory processing.** Spark keeps working data in memory across iterations, lowering latency and enabling near-real-time processing [6]. The practical guidance for this workflow is to use distributed processing for ingest and heavy feature computation when data genuinely exceeds single-node limits, and not to distribute the modeling step unless the feature matrix itself is too large to fit in memory, which for most tabular enterprise problems it is not.

---

**Key Takeaway.** Because the feature matrices behind most enterprise decisions fit in memory after aggregation, the modeling stage rarely needs distribution. Spend distributed compute on ingest and feature computation, not on the model.

---

## 5. From Storage to Signal: Feature Engineering

Feature engineering is where domain knowledge enters the pipeline, and it is the highest-leverage stage. Two patterns from the case studies generalize widely.

**Calendar and event windows.** Demand and financial activity are strongly shaped by the calendar. Rather than encoding only a binary is-holiday flag, the author engineered a holiday window, a two-week band around each holiday-flagged period, to capture the pre-event and post-event dynamics that a single-day flag misses. The forecasting literature is explicit that careful treatment of calendric special days materially improves daily retail forecasts [3].

**Exogenous context.** Decisions depend on conditions outside the immediate series. The Walmart pipeline incorporated macroeconomic indicators (CPI, unemployment) and promotional markdowns as exogenous features, treating them as analogues of the external signals (for example, FRED indicators) that a production model would consume.

Both patterns illustrate the thesis: these features are cheap to compute even at scale, and they move accuracy more than swapping the model would. The discipline is to compute them without leakage. Every feature must be available at prediction time and must not encode the future.

---

## 6. Modeling for Decisions: Why Tree Ensembles Remain the Default

The modeling layer should be the simplest thing that captures the signal and shows what drives it. For tabular enterprise data, that is a tree ensemble. This report states the point as a design principle so later sections can refer to it.

---

**Design Principle 1 (Feature-First Analytics).** For tabular enterprise data, marginal decision quality is gained more cheaply by improving feature engineering and validation than by increasing model complexity. The model should be the simplest one that captures the signal and exposes which features drive it.

---

**The tabular-data evidence.** On tabular data, tree-ensemble methods (random forests, Extremely Randomized Trees, and gradient-boosted trees such as XGBoost) remain the rational default. Controlled comparisons repeatedly find that deep-learning models do not reliably outperform well-tuned gradient-boosted trees on tabular problems, that the trees require far less tuning, and that where deep models help it is usually in ensemble with the trees rather than instead of them [4], [5], [7]. Figure 2 illustrates why the marginal gains from feature engineering and validation exceed the gains from additional model complexity, and names the rational default model for tabular enterprise data.

![Figure 2. The Feature-First Thesis for Tabular Enterprise Data. Marginal return is higher from feature engineering and validation than from model complexity, and the rational default model for tabular enterprise data is an interpretable tree ensemble.](figures/vol7_fig2_feature_first_payoff.png)

**Bagging, boosting, and Extra-Trees.** Bagging methods (random forests, Extremely Randomized Trees) reduce variance by averaging many decorrelated trees; Extra-Trees randomize split thresholds, which lowers variance and training cost at a small bias cost. Boosting methods (XGBoost, LightGBM) reduce bias by fitting trees sequentially to residuals and tend to win accuracy competitions, at the price of more careful tuning and greater overfitting risk [2], [7]. For decision support where stability and feature attribution matter as much as raw accuracy, bagging ensembles are often the safer first choice; for maximal predictive accuracy on a well-validated pipeline, gradient boosting is the stronger tool.

**Interpretability as a decision requirement.** Tree ensembles expose feature importance and support per-prediction attribution. In a decision context this is not a nicety. The planner needs to know which factors drive a forecast in order to act on it and to trust it. This requirement is what makes the choice to keep the model a tree ensemble a decision-quality choice, not merely a convenience.

---

## 7. Case Studies

### 7.1 Holiday-aware demand forecasting (ITS-836)
**Problem.** Forecast weekly sales across stores and departments around major holidays, using a large Walmart dataset as a proxy for hypermarket operations.

**Method.** A single high-volume store-department series is selected and structured as a weekly time series. Features are engineered from the raw panel: a holiday window (a two-week band around each holiday-flagged week), lagged and rolling-window values, a discount-intensity feature derived from markdowns, and the exogenous macroeconomic indicators (CPI, unemployment). The data is split chronologically (80 percent train, 20 percent test) so the evaluation respects time. Four models are compared: a Naive Lag-1 forecast as the baseline, a SARIMA time-series model, a Random Forest, and XGBoost, each scored with RMSE, MAE, and the coefficient of determination (R-squared).

**Results and evaluation.** The directional result, shown in Table 2, is that the tree-ensemble model clearly beat the Naive Lag-1 baseline, with lower RMSE, lower MAE, and higher R-squared, and that a lagged value was the strongest single predictor, followed by the macroeconomic and holiday features. This is consistent with Design Principle 1 (the engineered lag, holiday, and exogenous features carry most of the signal) and with the calendric-special-days literature [3]. The exact RMSE, MAE, and R-squared values for each model are produced by the evaluation script in the companion repository and recorded in its `RESULTS.md`, so the result is reproducible rather than asserted in the body of this report.

**Table 2. Forecasting model performance on the held-out test period (directional, as reported in the source study).**

| Model | RMSE | MAE | R-squared |
|---|---|---|---|
| Naive Lag-1 (baseline) | Higher | Higher | Lower |
| Random Forest | Lower | Lower | Higher |

The full numeric table, including the SARIMA and XGBoost results, is in the companion repository's `RESULTS.md`.

### 7.2 Vehicle-price prediction with Extremely Randomized Trees (MSDS-532)
**Problem.** Predict advertised vehicle price from attributes (age, mileage, fuel type, transmission, body style) and determine which attributes most influence price.

**Method.** The workflow includes data cleaning, filtering to a set of comparable vehicle models, categorical encoding, exploratory analysis, a held-out test split, and an Extremely Randomized Trees regressor. Performance is reported with the coefficient of determination (R-squared) and root-mean-square error (RMSE), and predictor influence is assessed with permutation importance, which is more robust than the default tree-based importance.

**Results and evaluation.** The model fit the held-out data well, with the actual figures shown in Table 3. The test R-squared of 0.91 indicates strong explanatory power, and the gap between the near-perfect training fit and the test fit is the expected signature of a flexible ensemble that still generalizes. Importantly for decision support, the permutation-importance ranking was clear: registration year was by far the strongest predictor of price, followed by vehicle model and gearbox type, while mileage contributed less than expected. The decision value lies as much in that ranking, which tells buyers, sellers, and analysts which characteristics move price, as in the point accuracy.

**Table 3. Vehicle-price model performance (Extremely Randomized Trees).**

| Metric | Training | Test |
|---|---|---|
| R-squared | 0.9991 | 0.9075 |
| RMSE | 300.17 | 2881.55 |

Top predictors by permutation importance: (1) registration year, (2) vehicle model, (3) gearbox type. These figures are reproduced by the evaluation script in the companion repository and recorded in its `RESULTS.md`.

**What the two studies share.** Both spend their effort on features and validation and keep the model a transparent tree ensemble; both treat which features matter as a first-class output; and both are reproducible from a companion script, the property that lets an enterprise trust and re-run them.

---

## 8. The Enterprise and Financial-Operations Bridge

The same workflow underpins financial-operations analytics, the author's domain of professional practice. Daily reconciliation across enterprise systems, vendor platforms, and cloud pipelines is, structurally, a large-scale tabular problem: ingest at scale, engineer comparison and tolerance features, model the normal envelope, and flag exceptions. Casting reconciliation and exception monitoring as anomaly detection over engineered features, rather than as hand-maintained rule sets, makes the process scalable, adaptive, and auditable, and it inherits every lesson above: distribute the ingest, engineer leak-free comparison features, keep the detector interpretable so flagged exceptions can be explained to an operator, and validate against labelled history.

---

**Practitioner Guidance.** Treat reconciliation and exception monitoring as anomaly detection over engineered comparison features, not as a growing pile of hand-maintained rules. Keep the detector interpretable so every flagged exception can be explained to an operator and an auditor. This is the connective tissue between Volume 7 (analytics) and Volume 8 (financial-systems data mining).

---

## 9. Synthesized Contributions

This report synthesizes prior work and the author's practice into four practitioner-oriented contributions. They are integrative rather than novel discoveries, and they are stated here so the reader can locate them.

1. **A data-to-decision workflow.** A five-stage pipeline (Figure 1) that names the governing question at each stage and locates where decision quality is actually won.
2. **The feature-first design principle.** Design Principle 1 states, with supporting evidence from the tabular-ML literature, that for tabular enterprise data better features and validation beat bigger models.
3. **A modeling-approach evaluation for tabular enterprise data.** Section 10 compares rule-based, deep-learning, and tree-ensemble approaches on the criteria that matter for enterprise decisions.
4. **An enterprise and financial-operations mapping.** Section 8 maps the workflow onto reconciliation and exception monitoring as anomaly detection, connecting the analytics method to regulated financial practice. This mapping, drawn from the author's professional work, is the most original of the four.

---

## 10. Approach Evaluation

The table compares four ways to turn enterprise tabular data into decisions, scored on the criteria that matter in practice.

**Table 4. Approaches to turning enterprise tabular data into decisions.**

| Approach | Tabular accuracy | Interpretability | Tuning cost | Scales to large data | Handles drift |
|---|---|---|---|---|---|
| Hand-maintained rules | Low to medium | High | Low | Poor | Poor |
| Deep neural networks | Medium to high | Low | High | Medium | Medium |
| Tree ensembles (default) | High | Medium to high | Low to medium | Medium | Medium |
| Feature-first tree-ensemble workflow (this report) | High | Medium to high | Low to medium | High (scale in ingest and features) | Higher (validation and monitoring built in) |

Two conclusions follow. First, the modeling families are close on tabular accuracy, with tree ensembles ahead of deep networks at far lower tuning cost, while rules alone are brittle and unscalable. Second, what separates the proposed workflow is not a new model but the placement of effort: scale is spent in ingest and feature engineering, interpretability is preserved at the model, and validation with drift monitoring is built into the pipeline rather than bolted on. The evaluation is structured and evidence-grounded rather than a single benchmark number, which suits a decision-oriented report; a head-to-head empirical benchmark on a shared enterprise dataset is named as future work and as a limitation.

---

## 11. From Accuracy to Trust: Validation, Drift, and Explainability

A model that is accurate in a notebook and untrusted in production has failed. Three concerns convert accuracy into trust.

**Honest validation.** For temporal problems, validation must respect time, namely out-of-sample and out-of-period evaluation, never random splits that leak the future. The case studies' use of held-out periods is the minimum bar.

**Drift.** Enterprise data distributions move. Promotions change, macroeconomic regimes shift, transaction formats evolve. A deployed model needs monitoring for data and concept drift, with retraining triggers, or yesterday's accurate model silently becomes today's liability.

**Explainability.** Tree ensembles' native feature importance and per-prediction attribution are a starting point. As automated analytics begin to drive consequential decisions, the demand rises from which features matter on average to why this decision, and under whose accountability. That demand, namely explainable and governable analytics, is the subject of the series governance volume (Volume 6) and explainable-AI capstone (Volume 10). Volume 7's contribution to that arc is the insistence that interpretability be designed in at the modeling stage, not retrofitted.

---

## 12. Limitations

This report is a decision-oriented technical monograph, not an experimental paper, and its claims should be read with four limitations in mind.

First, the approach evaluation in Section 10 is structured and evidence-grounded rather than a single controlled benchmark on a shared dataset; the relative scores summarize the cited literature and the author's studies rather than one head-to-head experiment. Second, the two case studies report their exact metrics in the companion repository rather than in the body of this report, so a reader who wants precise R-squared, MAE, RMSE, or weighted error figures must consult the code. Third, the feature-first thesis is strongest for the structured, tabular, enterprise data that is this report's scope; it does not extend to unstructured vision, language, or audio problems, where deep learning is dominant. Fourth, the financial-operations mapping in Section 8 is drawn from professional practice and is presented at the level of method and architecture; it deliberately contains no proprietary data or employer-specific detail, which limits how concretely it can be demonstrated here.

---

## 13. Future Work

**Probabilistic and hierarchical forecasting.** Moving from point forecasts to calibrated predictive distributions, and reconciling forecasts across the store, department, and company hierarchy, would make the demand pipeline directly usable for inventory and risk decisions; gradient-boosted-tree approaches to scalable probabilistic retail forecasting are an active, practitioner-validated direction [2].

**Foundation and hybrid models, measured against trees.** Newer time-series foundation models and tree-and-deep hybrids should be evaluated, but on the explicit standard set here: do they beat a well-engineered, well-validated gradient-boosted-tree baseline by enough to justify their cost and opacity [1], [5].

**A shared enterprise benchmark.** The approach evaluation in Section 10 is structured rather than empirical. Building a reproducible head-to-head benchmark on a shared enterprise dataset, scoring the whole workflow rather than model accuracy alone, is a concrete next step that would also resolve the first limitation in Section 12.

**Automated, reproducible pipelines.** Packaging the storage, signal, model, and validation workflow as a reusable, parameterized pipeline with drift monitoring and scheduled retraining turns each study into enterprise infrastructure and is the natural extension of the companion code.

---

## 14. Conclusion

Scalable analytics for enterprise decisions is not primarily a contest of model architectures. It is a discipline of spending scale where it pays, on feature quality, honest validation, and monitoring, while keeping the model a transparent, well-calibrated tree ensemble whose drivers a decision-maker can see and trust. The two case studies demonstrate the discipline on real data, the financial-operations bridge shows its enterprise reach, and the trust concerns point forward to the governance and explainable-AI volumes. The feature-first thesis, that for tabular enterprise data better features beat bigger models, is, on the present evidence, simply the rational one.

---

## Acknowledgments

The implementation studies underlying this report originated in graduate coursework at the University of the Cumberlands: Data Science and Big Data Analytics (ITS-836) and Data Science Programming (MSDS-532). The author thanks the instructors and the program. All synthesis, analysis, framework development, and writing are the author's own and were written from scratch for publication, and contain no confidential employer information.

## References

[1] G. Theodoridis and A. Tsadiras, "Retail Demand Forecasting: A Comparative Analysis of Deep Neural Networks and the Proposal of LSTMixer," Information, vol. 16, no. 7, art. 596, 2025. doi: 10.3390/info16070596.

[2] X. Long, Q. Bui, G. Oktavian, D. F. Schmidt, C. Bergmeir, R. Godahewa, et al., "Scalable Probabilistic Forecasting in Retail with Gradient Boosted Trees: A Practitioner's Approach," arXiv:2311.00993, 2023. doi: 10.48550/arXiv.2311.00993.

[3] R. Huber and H. Stuckenschmidt, "Daily retail demand forecasting using machine learning with emphasis on calendric special days," International Journal of Forecasting, vol. 36, no. 4, pp. 1420-1438, 2020. doi: 10.1016/j.ijforecast.2020.02.005.

[4] R. Shwartz-Ziv and A. Armon, "Tabular Data: Deep Learning is Not All You Need," Information Fusion, vol. 81, pp. 84-90, 2022. doi: 10.1016/j.inffus.2021.11.011.

[5] V. Borisov, T. Leemann, K. Sessler, J. Haug, M. Pawelczyk, and G. Kasneci, "Deep Neural Networks and Tabular Data: A Survey," IEEE Transactions on Neural Networks and Learning Systems, vol. 35, no. 6, pp. 7499-7519, 2024. doi: 10.1109/TNNLS.2022.3229161.

[6] M. Zaharia, R. S. Xin, P. Wendell, T. Das, M. Armbrust, A. Dave, et al., "Apache Spark: A Unified Engine for Big Data Processing," Communications of the ACM, vol. 59, no. 11, pp. 56-65, 2016. doi: 10.1145/2934664.

[7] T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System," in Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining (KDD), 2016, pp. 785-794. doi: 10.1145/2939672.2939785.

[8] J. Dean and S. Ghemawat, "MapReduce: Simplified Data Processing on Large Clusters," Communications of the ACM, vol. 51, no. 1, pp. 107-113, 2008. doi: 10.1145/1327452.1327492.

*Primary sources, author coursework, rewritten and synthesized for this report: A. Palayil, "Forecasting Hypermarket Sales Around Major Holidays" (ITS-836, University of the Cumberlands, 2026); "Vehicle Price Prediction Using Extremely Randomized Trees Regression" (MSDS-532, University of the Cumberlands, 2026); time-series, linear-, and logistic-regression labs (ITS-836).*

[PAGEBREAK]

## Appendix A. Methodology and Implementation Details

This appendix records the methodological choices behind the workflow and the two case studies so that the results are reproducible from the companion repository.

**Data and environment.** The demand-forecasting study uses a large public Walmart sales dataset (weekly sales by store and department, with store features, markdowns, CPI, and unemployment) as a proxy for hypermarket operations. The vehicle-price study uses a tabular dataset of advertised vehicles with mixed numeric and categorical attributes. Both studies are implemented in Python with the standard scientific stack (pandas, NumPy, scikit-learn), and are organized so that ingestion, feature engineering, modeling, and evaluation are separable stages, mirroring the workflow of Section 3.

**Feature engineering.** The forecasting study constructs a holiday-window feature (a two-week band around each holiday-flagged week), lagged and rolling-window values, and a discount-intensity feature, and joins exogenous macroeconomic features (CPI, unemployment), taking care that every feature is available at prediction time to avoid leakage. The vehicle-price study cleans missing and inconsistent records, filters to comparable vehicle models, encodes categorical attributes, and retains registration year, which proved the dominant predictor.

**Modeling.** The forecasting study compares a Naive Lag-1 baseline against a SARIMA time-series model, a Random Forest, and XGBoost. The vehicle-price study uses an Extremely Randomized Trees regressor, chosen for low variance, low tuning cost, and a permutation-importance ranking that is robust for decision support.

**Validation protocol.** The forecasting study uses a chronological train and test split (80 percent train, 20 percent test) so that the evaluation respects time and does not leak future information, and scores each model with RMSE, MAE, and R-squared. The vehicle-price study uses a held-out test split and reports R-squared and RMSE with permutation feature importance. The exact metric values are produced by the evaluation scripts and recorded in `RESULTS.md` in the companion repository.

**Reproducibility.** Random seeds, dependency versions, and the train and test split definitions are fixed and recorded in the companion repository so that the reported results can be regenerated.

---

*Note on references: all eight references carry full author lists, venue, year, and DOI in IEEE format. This version (1.0) is prepared for Zenodo deposit.*
