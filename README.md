# ♻️ San Francisco Recycling Cost-Benefit Analysis

A Python data analysis project evaluating whether San Francisco's recycling and composting programs generate greater economic and environmental value than landfilling.

This project combines financial costs, greenhouse gas emissions, and the Social Cost of Carbon (SCC) to estimate the net social value of different municipal waste streams.

---

## Background

San Francisco is recognized as one of the leading U.S. cities in recycling and waste diversion through its Zero Waste initiative. While recycling programs require significant operational investment, they also reduce greenhouse gas emissions, conserve natural resources, and decrease landfill dependence.

This project evaluates whether those environmental benefits outweigh the additional processing costs.

---

## Research Question

**Is San Francisco's recycling program more cost-effective than landfilling when both financial costs and environmental benefits are considered?**

---

## Hypothesis

Recycling and composting provide greater overall social and environmental benefits than landfilling, even after accounting for higher processing costs.

---

## Data Sources

- San Francisco RY2022 tipping-fee data
- EPA Waste Reduction Model (WARM)
- Social Cost of Carbon (SCC): **$190 per metric ton of CO₂e**

The cleaned dataset includes:

- Waste stream
- Tons recycled
- Tons disposed
- Recycling cost per ton
- Landfill cost per ton
- Emissions saved per ton
- Social Cost of Carbon

---

## Methodology

The program calculates:

- Environmental Benefit per Ton
- Cost Advantage Compared to Landfilling
- Net Social Value per Ton
- Total Net Social Value
- Percentage Share of Total Net Social Value

The analysis is performed using Python and visualized with Matplotlib.

---

## Key Findings

- All analyzed waste streams generated positive net social value.
- **Recyclables (MRF)** produced the largest environmental and economic benefit.
- Compostables also produced substantial positive value because of their high recycling volume.
- Lower-quality waste streams generated smaller climate benefits but remained net-positive overall.

---

## Visualizations

The program automatically generates:

- Environmental Benefit vs. Cost Advantage
- Total Net Social Value by Waste Stream
- Share of Total Net Social Value

Generated figures are saved to the `figures/` directory.

---

## Technologies

- Python
- pandas
- Matplotlib

---

## Repository Structure

```
san-francisco-recycling-analysis/
│
├── data/
│   └── sf_stream_analysis.csv
│
├── figures/
│
├── recycling_analysis.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## How to Run

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the analysis:

```bash
python recycling_analysis.py
```

---

## Future Improvements

- Sensitivity analysis using different Social Cost of Carbon values
- Interactive dashboard for exploring waste streams
- Support for additional municipalities
- Geographic visualization of recycling performance

---

## Author

**Zuwairiyah Bari**

California State Polytechnic University, Pomona
