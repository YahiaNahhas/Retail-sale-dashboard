cat > README.md <<'EOF'
# Retail Sales Dashboard (Flask + SQLite)

A SQL-backed web dashboard that loads the Retail Sales dataset into SQLite and provides:
- KPI overview (total sales, orders, unique customers, AOV)
- Filterable Transactions view (month-to-month range, category, customer)
- Analysis page (best month per year, orders by shift, sales by gender)

## Tech Stack
- Python (Flask)
- SQLite
- SQL (aggregations, window functions)
- HTML/CSS

## Setup (macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

python3 scripts/init_db.py
python3 scripts/load_csv.py

python3 app.py
