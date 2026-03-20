import argparse
from pathlib import Path

from analyzer import hospital_bed_per_capita_in_city
from data_loader import load_data, validate_data_hosp, validate_data_popul
from cleaner import clean_data_hosp, clean_data_popul
from visualization import (
    export_excel_report,
    export_csv_report,
    plot_best_large_cities,
    plot_worst_large_cities
)


# =========================
# DATA PIPELINE
# =========================

def load_and_process_data():
    BASE_DIR = Path(__file__).resolve().parent.parent

    data_path_hosp = BASE_DIR / "data" / "Leitos_2026.csv"
    data_path_popul = BASE_DIR / "data" / "POP2025_20251031(Municípios).csv"

    df_hosp = load_data(data_path_hosp)
    df_popul = load_data(data_path_popul, skip_rows=1, encod="utf-8")

    validate_data_popul(df_popul)
    validate_data_hosp(df_hosp)

    df_hosp = clean_data_hosp(df_hosp)
    df_popul = clean_data_popul(df_popul)

    return hospital_bed_per_capita_in_city(df_hosp, df_popul)


# =========================
# CLI SETUP
# =========================

def parse_args():
    parser = argparse.ArgumentParser(
        description="ICU Analytics Pipeline"
    )

    parser.add_argument(
        "mode",
        nargs="?",
        default="all",
        choices=["all", "csv", "plot", "excel"],
        help="What to run"
    )

    parser.add_argument(
        "--type",
        choices=["icu", "all", "best", "worst"],
        help="Type of operation"
    )

    parser.add_argument(
        "--min_population",
        type=int,
        default=100_000,
        help="Minimum population filter (default: 100000)"
    )

    parser.add_argument(
        "--top_n",
        type=int,
        default=10,
        help="Number of cities (default: 10)"
    )

    return parser.parse_args()

def main():
    args = parse_args()
    df = load_and_process_data()

    COMMANDS = {
        "all": run_all_reports,
        "csv": run_csv_report,
        "plot": run_plot_report,
        "excel": run_excel_report
    }
    # Check if the mode is valid and run the corresponding function
    command = COMMANDS.get(args.mode)
    if command:
        command(df, args)
    
def run_all_reports(df, args):
    export_excel_report(df, min_population=args.min_population)
    export_csv_report(df, top_n=args.top_n)
    plot_worst_large_cities(df, args.min_population, args.top_n)
    plot_best_large_cities(df, args.min_population, args.top_n)
    print("All reports generated.")

def run_csv_report(df, args):
    if args.type == "icu":
        export_csv_report(df)
        print("CSV ICU report generated.")

    elif args.type == "all":
        export_csv_report(df, top_n=args.top_n)
        print("All CSV reports generated.")

    else:
        print("Specify --type icu or --type all")
     
def run_plot_report(df, args):
    if args.type == "best":
        plot_best_large_cities(df, args.min_population, args.top_n)

    elif args.type == "worst":
        plot_worst_large_cities(df, args.min_population, args.top_n)

    else:
        print("Use --type | best | worst")


def run_excel_report(df, args):
    export_excel_report(df, min_population=args.min_population)
    print("Excel report generated.")
    

if __name__ == "__main__":
    main()