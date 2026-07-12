# Canadian Vehicle Fuel Consumption Analysis (2015–2024)

Exploratory analysis of the Government of Canada fuel-consumption dataset.

## What this corrected version adds

- corrected consumption consistency rule: highway < combined < city;
- corrected AWD–4WD mean-difference interpretation;
- corrected Diesel–Gasoline manual test calculation;
- Pearson correlations restricted to truly numeric variables;
- global Kruskal–Wallis tests before pairwise conclusions;
- Welch tests with 95% confidence intervals and Hedges' g;
- explicit limitations for drivetrain inference and causal claims;
- modular code, tests, notebook, documentation, and GitHub files.

## Structure

```text
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/README.md
├── notebooks/exploratory_analysis.ipynb
├── results/
│   ├── figures/
│   └── tables/
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── data_quality.py
│   ├── feature_engineering.py
│   ├── statistical_analysis.py
│   ├── visualization.py
│   └── main.py
└── tests/test_feature_engineering.py
```

## Dataset

Place the CSV file at:

```text
data/raw/my2015-2024-fuel-consumption-ratings.csv
```

## Installation

```bash
python -m venv .venv
pip install -r requirements.txt
```

Windows activation:

```bash
.venv\Scripts\activate
```

## Run

```bash
python -m src.main
```

Generated figures and tables are saved in `results/`.

## Methodology and limitations

The analysis uses descriptive statistics, data-quality checks, visualizations, Welch two-sample tests, and Kruskal–Wallis global tests.

Pearson correlation is applied only to genuinely numeric technical variables. Nominal variables such as fuel type, manufacturer country, and transmission category are not interpreted through arbitrary integer encodings.

Pairwise comparisons include:

- sample sizes;
- group means;
- mean differences;
- 95% confidence intervals;
- Welch test statistics;
- p-values;
- Hedges' g effect sizes.

Global Kruskal–Wallis tests are used to determine whether at least one group differs before interpreting selected pairwise comparisons.

Drivetrain is inferred from explicit keywords such as `AWD`, `4WD`, `4X4`, `FWD`, and `RWD` in vehicle model names. Vehicles without a detectable keyword are labelled `Unknown / Other`. Drivetrain findings therefore apply only to vehicles with identifiable labels and may be affected by selection bias.

The dataset is observational. Differences between groups describe statistical associations and do not prove that drivetrain, fuel type, or manufacturer country directly causes the observed fuel-consumption differences. Other factors such as engine size, cylinder count, vehicle class, and vehicle mass may act as confounding variables.

Very small p-values should not be interpreted alone. Confidence intervals and effect sizes are included to assess the practical importance of the observed differences.

## Author

Yves Christian Nonguierma

## License

MIT.
