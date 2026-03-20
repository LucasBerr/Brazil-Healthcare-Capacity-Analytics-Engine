import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from analyzer import get_large_cities

# =========================
# PATH HELPERS
# =========================

def get_output_dir(subfolder: str) -> Path:
    base_dir = Path(__file__).resolve().parent.parent
    output_dir = base_dir / "outputs" / subfolder
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

# =========================
# PLOTTING
# =========================

def plot_barh(df, y_col, x_col, title, xlabel, filename, show=False):
    output_dir = get_output_dir("plots")
    output_path = output_dir / filename

    plt.figure()
    plt.barh(df[y_col], df[x_col])
    plt.xlabel(xlabel)
    plt.ylabel("City")
    plt.title(title)
    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.savefig(output_path)

    if show:
        plt.show()

    plt.close()
    return output_path

def plot_worst_large_cities(df, min_population=100_000, top_n=10, show=False):
    df_worst = get_large_cities(df, min_population, top_n)

    return plot_barh(
        df=df_worst,
        y_col="LABEL",
        x_col="LEITOS_TOTAL_PER_THOUSAND",
        title=f"Worst {top_n} Cities (> {min_population:,} inhabitants)",
        xlabel="Hospital beds per thousand",
        filename=f"worst_{top_n}_cities_over_{min_population}_bed.png",
        show=show
    )

def plot_best_large_cities(df, min_population=100_000, top_n=10, show=False):
    df_best = get_large_cities(df, min_population, top_n, worst=False)

    return plot_barh(
        df=df_best,
        y_col="LABEL",
        x_col="LEITOS_TOTAL_PER_THOUSAND",
        title=f"Best {top_n} Cities (> {min_population:,} inhabitants)",
        xlabel="Hospital beds per thousand",
        filename=f"best_{top_n}_cities_over_{min_population}_bed.png",
        show=show
    )

# =========================
# EXPORT - EXCEL
# =========================

def format_excel_sheet(worksheet):
    worksheet.freeze_panes = "A2"

    for col in worksheet.columns:
        max_length = 0
        col_letter = col[0].column_letter

        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))

        worksheet.column_dimensions[col_letter].width = max_length + 2

    worksheet.auto_filter.ref = worksheet.dimensions


def export_excel_report(df, filename="bed_report.xlsx", min_population=100_000):
    output_dir = get_output_dir("excel")
    output_path = output_dir / filename

    df_sorted = df.sort_values("LEITOS_TOTAL_PER_THOUSAND", ascending=False)
    df_top_10 = df_sorted.head(10)
    df_worst_10 = get_large_cities(df, min_population, 10)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_sorted.to_excel(writer, sheet_name="Full Data", index=False)
        df_top_10.to_excel(writer, sheet_name="Top 10 Best", index=False)
        df_worst_10.to_excel(writer, sheet_name="Top 10 Worst (>100k)", index=False)

        for sheet in writer.sheets.values():
            format_excel_sheet(sheet)

    return output_path


# =========================
# EXPORT - CSV
# =========================

def export_csv_report(df, filename="bed_report.csv", top_n=None):
    output_dir = get_output_dir("csv")

    df_sorted = df.sort_values("LEITOS_TOTAL_PER_THOUSAND", ascending=False)

    output_path = output_dir / filename
    df_sorted.to_csv(output_path, index=False, encoding="utf-8-sig")

    top_path = None
    if top_n:
        top_path = output_dir / f"top_{top_n}_cities_hospital_beds_per_capita.csv"
        df_sorted.head(top_n).to_csv(top_path, index=False, encoding="utf-8-sig")

    return output_path, top_path