from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_FILE = Path("data/sf_stream_analysis.csv")
FIGURES_DIR = Path("figures")


def load_and_validate_data(file_path: Path) -> pd.DataFrame:
    """Load the waste-stream dataset and verify that required data are present."""

    required_columns = {
        "material",
        "tons_recycled",
        "tons_disposed",
        "recycle_cost_per_ton",
        "landfill_cost_per_ton",
        "emissions_saved_tCO2_per_ton",
        "scc_usd_per_tCO2",
    }

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    data = pd.read_csv(file_path)

    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_columns)}"
        )

    if data[list(required_columns)].isnull().any().any():
        raise ValueError("Dataset contains missing values.")

    numeric_columns = required_columns.difference({"material"})

    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="raise")

    if (data[list(numeric_columns)] < 0).any().any():
        raise ValueError("Numeric values cannot be negative.")

    return data


def calculate_social_value(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate environmental and economic value for each waste stream."""

    results = data.copy()

    results["environmental_benefit_per_ton"] = (
        results["emissions_saved_tCO2_per_ton"]
        * results["scc_usd_per_tCO2"]
    )

    results["cost_advantage_per_ton"] = (
        results["landfill_cost_per_ton"]
        - results["recycle_cost_per_ton"]
    )

    results["net_social_value_per_ton"] = (
        results["environmental_benefit_per_ton"]
        + results["cost_advantage_per_ton"]
    )

    results["total_net_social_value"] = (
        results["net_social_value_per_ton"]
        * results["tons_recycled"]
    )

    results["share_of_total_value"] = (
        results["total_net_social_value"]
        / results["total_net_social_value"].sum()
        * 100
    )

    return results


def format_material_names(data: pd.DataFrame) -> pd.Series:
    """Convert database-style material names into readable labels."""

    return data["material"].str.replace("_", " ").str.title()


def create_per_ton_chart(data: pd.DataFrame) -> None:
    """Compare climate benefits and cost advantages per ton."""

    chart_data = data.set_index(format_material_names(data))[
        ["environmental_benefit_per_ton", "cost_advantage_per_ton"]
    ]

    chart_data.columns = [
        "Environmental Benefit",
        "Cost Advantage vs. Landfill",
    ]

    ax = chart_data.plot(kind="bar", figsize=(11, 6))

    ax.set_title("Environmental Benefit and Cost Advantage per Ton")
    ax.set_xlabel("Waste Stream")
    ax.set_ylabel("Value per Ton (USD)")
    ax.tick_params(axis="x", rotation=30)
    ax.axhline(0, linewidth=0.8)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "per_ton_cost_benefit.png", dpi=300)
    plt.close()


def create_total_value_chart(data: pd.DataFrame) -> None:
    """Create a bar chart of total net social value by waste stream."""

    chart_data = data.copy()
    chart_data["material_label"] = format_material_names(chart_data)
    chart_data = chart_data.sort_values(
        "total_net_social_value",
        ascending=False,
    )

    ax = chart_data.plot(
        kind="bar",
        x="material_label",
        y="total_net_social_value",
        legend=False,
        figsize=(11, 6),
    )

    ax.set_title("Total Net Social Value by Waste Stream")
    ax.set_xlabel("Waste Stream")
    ax.set_ylabel("Total Net Social Value (USD)")
    ax.tick_params(axis="x", rotation=30)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "total_net_social_value.png", dpi=300)
    plt.close()


def create_value_share_chart(data: pd.DataFrame) -> None:
    """Create a pie chart showing each stream's share of total value."""

    labels = format_material_names(data)

    plt.figure(figsize=(9, 7))
    plt.pie(
        data["total_net_social_value"],
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Share of Total Net Social Value by Waste Stream")

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "net_social_value_share.png", dpi=300)
    plt.close()


def display_results(data: pd.DataFrame) -> None:
    """Print the main analysis results in a readable table."""

    display_columns = [
        "material",
        "tons_recycled",
        "environmental_benefit_per_ton",
        "cost_advantage_per_ton",
        "net_social_value_per_ton",
        "total_net_social_value",
        "share_of_total_value",
    ]

    print("\nSan Francisco Recycling Cost-Benefit Analysis\n")
    print(
        data[display_columns].to_string(
            index=False,
            formatters={
                "environmental_benefit_per_ton": "${:,.2f}".format,
                "cost_advantage_per_ton": "${:,.2f}".format,
                "net_social_value_per_ton": "${:,.2f}".format,
                "total_net_social_value": "${:,.2f}".format,
                "share_of_total_value": "{:,.1f}%".format,
            },
        )
    )

    total_value = data["total_net_social_value"].sum()

    print(f"\nCombined net social value: ${total_value:,.2f}")


def main() -> None:
    """Run the complete recycling cost-benefit analysis."""

    FIGURES_DIR.mkdir(exist_ok=True)

    waste_data = load_and_validate_data(DATA_FILE)
    results = calculate_social_value(waste_data)

    results.to_csv("recycling_analysis_results.csv", index=False)

    display_results(results)
    create_per_ton_chart(results)
    create_total_value_chart(results)
    create_value_share_chart(results)

    print("\nAnalysis complete.")
    print("Results saved to recycling_analysis_results.csv")
    print(f"Figures saved in the {FIGURES_DIR}/ folder.")


if __name__ == "__main__":
    main()
