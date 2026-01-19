# Retail Sales Dashboard (SQL + Flask + SQLite)

A SQL-backed analytics dashboard that loads a retail transactions dataset into SQLite and exposes business insights through a clean HTML UI. The goal of this project is to demonstrate practical SQL skills (schema design, data cleaning, aggregation, window functions) paired with a lightweight web interface for exploring data.

## What This App Does

### 1) Dashboard (KPIs + Executive Summary)
- **Total Sales** (SUM of `total_sale`)
- **Total Orders** (COUNT of transactions)
- **Unique Customers** (COUNT DISTINCT `customer_id`)
- **Average Order Value** (AVG of `total_sale`)
- **Sales by Category** summary table
- **Top Customers** by total spend

### 2) Transactions Explorer (UI Filters)
A browseable transactions table for validation and ad-hoc exploration:
- **Month-to-month range filtering** (Start Month → End Month)
- Category filter
- Customer ID filter
- Row limit control
- Sorted by date/time (most recent first)

### 3) Analysis (SQL Business Questions)
A dedicated analysis view that answers common stakeholder questions using SQL:
- **Best Month per Year** (ranked by average sale)
- **Orders by Shift** (Morning/Afternoon/Evening based on sale time)
- **Sales by Gender** summary

## Tech Stack
- **Python 3** + **Flask** (server + routing)
- **SQLite** (local relational database)
- **SQL** (aggregation, grouping, window functions)
- **HTML + CSS** (UI)
- **Git/GitHub** (version control)

## Project Structure
```text
retail-sales-dashboard/
  app.py
  requirements.txt
  scripts/
    init_db.py
    load_csv.py
  sql/
    schema.sql
  templates/
    base.html
    index.html
    transactions.html
    analysis.html
  static/
    styles.css
    store.png
  data/
    retail_sales.csv   (gitignored)
  retail.db            (gitignored)
