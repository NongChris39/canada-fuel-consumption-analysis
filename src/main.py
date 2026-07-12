from .config import DATA_PATH, FIGURES_DIR, TABLES_DIR, TARGET_COLUMN
from .data_loader import load_dataset
from .data_quality import evaluate_data_quality, quality_summary_table
from .feature_engineering import clean_and_engineer_features
from .statistical_analysis import run_default_statistical_tests
from .visualization import generate_all_figures

def main():
    FIGURES_DIR.mkdir(parents=True,exist_ok=True)
    TABLES_DIR.mkdir(parents=True,exist_ok=True)

    print("="*72)
    print("CANADIAN VEHICLE FUEL CONSUMPTION ANALYSIS")
    print("="*72)

    raw = load_dataset(DATA_PATH)
    print(f"Rows loaded: {len(raw)} | Columns: {raw.shape[1]}")

    quality = evaluate_data_quality(raw)
    print(f"Completeness: {quality['overall_completeness']:.2%}")
    print(f"Quality score: {quality['overall_quality_score']:.2f}/10")
    print(
        "Highway < combined < city consistency: "
        f"{quality['rule_scores']['highway_combined_city_consistency']:.2%}"
    )
    quality_summary_table(quality).to_csv(
        TABLES_DIR/"data_quality_summary.csv",index=False
    )

    clean = clean_and_engineer_features(raw)
    pairwise, global_tests = run_default_statistical_tests(clean,TARGET_COLUMN)
    pairwise.to_csv(TABLES_DIR/"pairwise_tests.csv",index=False)
    global_tests.to_csv(TABLES_DIR/"global_group_tests.csv",index=False)

    print("\nPAIRWISE WELCH TESTS")
    print(pairwise.to_string(index=False))
    print("\nGLOBAL KRUSKAL-WALLIS TESTS")
    print(global_tests.to_string(index=False))

    generate_all_figures(clean,FIGURES_DIR)
    print("\nAnalysis completed. Results saved in the results directory.")

if __name__ == "__main__":
    main()
