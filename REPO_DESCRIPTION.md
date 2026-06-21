# GitHub repository description and setup

## Repository name
```
Scalable-Analytics-for-Enterprise-Decisions-Vol7
```
(Lowercase `scalable-analytics-for-enterprise-decisions-vol7` is equivalent; GitHub resolves case-insensitively. Match whichever capitalization you used for Volume 1's repo for consistency.)

## Short description (the GitHub "About" field, keep under ~350 characters)
```
Companion repo for Volume 7 of the Engineering-to-Research monograph series: a decision-oriented analytics workflow arguing that for tabular enterprise data, better features and validation beat bigger models. Includes the paper (CC BY 4.0), figures, and forecasting and tree-ensemble code. DOI pending Zenodo deposit.
```

## Alternative one-line description (even shorter)
```
A feature-first analytics workflow for enterprise decisions: spend scale on features and validation, keep the model an interpretable tree ensemble. Monograph Vol. 7 of 10.
```

## Website field
Set to the Zenodo DOI URL once minted:
```
https://doi.org/10.5281/zenodo.20733992
```

## Suggested topics
```
data-science, big-data, mapreduce, apache-spark, demand-forecasting,
feature-engineering, tree-ensembles, gradient-boosting, xgboost, tabular-data,
enterprise-analytics, research-monograph, zenodo, reproducible-research
```

## First-release checklist
1. Push all files (README.md, LICENSE, LICENSE-CC-BY-4.0.txt, CITATION.cff, .zenodo.json, paper/, figures/, code/).
2. Set the About description and topics above.
3. DOI 10.5281/zenodo.20733992 is reserved and already embedded in README.md, CITATION.cff, LICENSE-CC-BY-4.0.txt, and the paper PDF/DOCX. Before publishing, fill the `TBD` values in RESULTS.md from the evaluation-script output so the paper's references to it resolve.
4. Create a GitHub release tagged `v1.0`.
5. Add the DOI to your portfolio Publications page and the Publication Status Ledger.

## Note on .zenodo.json
Copy `vol7_zenodo_metadata.json` from the archive into the repo root and rename it exactly `.zenodo.json`. Zenodo reads metadata in this priority order: `.zenodo.json` first, then `CITATION.cff`, then `LICENSE`.

## Publishing reminder
Publish on Zenodo into your "Engineering-to-Research Monograph Series" community (or add the record to it after publishing), the same community used for Volume 1.
