# Retail Performance Executive Dashboard

An interactive, web-based executive analytics dashboard built using clean, vanilla Python **Dash** and **Plotly**. This application transforms raw retail transactional logging records into a highly visual tool, enabling stakeholders to dynamically track revenue metrics, evaluate categorical spreads, observe timeline trends, and export targeted data partitions.

## 🚀 Live Application
🔗 **Live Demo Link:** (https://retali-data-analysis-project.onrender.com/)

---

## 📊 Business Metrics & Insights Covered
This repository contains both an exploratory analysis notebook and a production script that answers critical business intelligence goals:
* **Total Revenue Architecture:** High-level dynamic tracking of overall corporate sales volume across all product classes.
* **Profit Proxy Modeling:** Real-time visibility into an estimated 40% margin calculation baseline across selected filter states.
* **Temporal Seasonality Spikes:** Line visualization identifying core peak business run rates (such as the high-velocity surges seen historically in May, October, and December).
* **Transaction Value Spreads:** Grouped quartile distribution box plots outlining order sizes across **Electronics**, **Clothing**, and **Beauty** segments.

---

## 🛠️ Project Architecture & Tech Stack
The dashboard pipeline avoids bulky framework templates, leveraging clean web primitives:
* **Data Processing:** Python 3.12, Pandas, NumPy
* **Data Visualization:** Plotly Express (Dynamic HTML5 SVG engine)
* **Dashboard Framework:** Dash (Core HTML & Component libraries wrapper built on React.js)
* **WSGI HTTP Server:** Gunicorn (for production scalability on cloud workers)

---

## 📂 Repository File Structure
Ensure your local folder or GitHub repository maintains the following layout to prevent build pipeline breaks:
```text
├── app.py                      # Main production dashboard script containing layout & callback engines
├── retail_sales_dataset.csv     # Raw tabular comma-separated transaction data
├── requirements.txt            # System dependencies manifest for cloud environment builds
└── README.md                   # Project documentation and architectural blueprint
