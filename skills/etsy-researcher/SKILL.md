---
name: etsy-researcher
description: Research Etsy listings at scale, classify products into tactical demand tiers, and report under-saturated niches and reusable text angles. Use when analyzing Etsy search result URLs, scraping competitor listings, clustering Etsy sub-niches, or producing niche research reports from structured listing data.
---

# Etsy Researcher

Run repeatable Etsy market research without storing raw research data inside the skill folder.

## Overview

Use this skill to turn Etsy search-result data into a tactical niche report.
Keep the skill stateless: store raw research data outside the skill directory and use the skill only for workflow, classification logic, scripts, and report templates.

## Workflow

1. Clarify the research target.
   - Confirm the seed keyword or Etsy search URL.
   - Confirm the user's goal: niche discovery, competitor mapping, text-angle mining, or saturation analysis.

2. Collect listing data.
   - Use the best available browsing or web-research tool for the current environment.
   - Prefer multi-page Etsy search results when available.
   - Capture structured fields when possible: title, price, review count, badges, shipping signals, recent-sales signals if visible, and listing URL.
   - If Etsy blocks direct access, use the strongest available fallback and state the limitations.

3. Save raw data outside the skill.
   - Never store raw crawl data inside the skill folder.
   - Save research CSV files under `~/etsy/research_data/`.
   - Use descriptive names such as `<keyword>_<YYYY_MM_DD>.csv`.

4. Classify the market.
   - Read `references/tactical-classification.md` before assigning tiers.
   - Classify listings into tactical groups using observed signals only.
   - Exclude dead patterns, policy-risk patterns, and unsupported guesses.

5. Analyze with scripts when available.
   - Use `scripts/matrix_generator.py` to convert raw CSV data into a Markdown research matrix.
   - If the script is missing or incomplete, perform the equivalent analysis manually and say so.

6. Deliver the report.
   - Read `assets/report-template.md` before writing the final answer.
   - Follow that structure closely.
   - End with actionable niche recommendations and a watchlist of promising text angles.

## Data Handling

- Keep the skill stateless.
- Store raw research outputs outside the skill folder.
- Keep only reusable logic, templates, and scripts inside the skill.
- Do not claim sales velocity or saturation conclusions unless supported by observed data.

## Guardrails

- Exclude listings with clear IP or trademark risk.
- Exclude dead patterns as defined in `references/tactical-classification.md`.
- Base tactical classification on extracted evidence, not intuition.
- State missing data clearly when Etsy or the browsing environment limits extraction.

## References

- Read `references/tactical-classification.md` for the tiering model and exclusion rules.
- Read `assets/report-template.md` before delivering the final report.
- Use `scripts/matrix_generator.py` when structured CSV analysis is available.
