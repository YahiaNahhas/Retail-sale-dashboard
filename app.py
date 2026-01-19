import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
DB = "retail.db"

def q(sql, params=()):
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(sql, params).fetchall()

@app.route("/")
def index():
    kpis = q("""
        SELECT
          COUNT(*) AS total_orders,
          COUNT(DISTINCT customer_id) AS unique_customers,
          ROUND(SUM(total_sale), 2) AS total_sales,
          ROUND(AVG(total_sale), 2) AS avg_order_value
        FROM retail_sales
    """)[0]

    sales_by_category = q("""
        SELECT category,
               ROUND(SUM(total_sale), 2) AS net_sale,
               COUNT(*) AS total_orders
        FROM retail_sales
        GROUP BY category
        ORDER BY net_sale DESC
    """)

    top_customers = q("""
        SELECT customer_id,
               ROUND(SUM(total_sale), 2) AS total_sales
        FROM retail_sales
        GROUP BY customer_id
        ORDER BY total_sales DESC
        LIMIT 10
    """)

    return render_template(
        "index.html",
        kpis=kpis,
        sales_by_category=sales_by_category,
        top_customers=top_customers
    )

@app.route("/transactions")
def transactions():
    start_month = request.args.get("start_month", "").strip()  # YYYY-MM
    end_month = request.args.get("end_month", "").strip()      # YYYY-MM
    category = request.args.get("category", "").strip()
    search_customer = request.args.get("customer", "").strip()
    limit = min(int(request.args.get("limit", 100)), 500)

    months = q("""
        SELECT DISTINCT substr(sale_date, 1, 7) AS month
        FROM retail_sales
        WHERE sale_date IS NOT NULL AND length(sale_date) >= 7
        ORDER BY month DESC
    """)

    sql = "SELECT * FROM retail_sales WHERE 1=1"
    params = []

    # Month-to-month filtering
    if start_month and end_month:
        sql += " AND substr(sale_date, 1, 7) BETWEEN ? AND ?"
        params.extend([start_month, end_month])
    elif start_month:
        sql += " AND substr(sale_date, 1, 7) >= ?"
        params.append(start_month)
    elif end_month:
        sql += " AND substr(sale_date, 1, 7) <= ?"
        params.append(end_month)

    if category:
        sql += " AND category = ?"
        params.append(category)

    if search_customer:
        sql += " AND CAST(customer_id AS TEXT) LIKE ?"
        params.append(f"%{search_customer}%")

    sql += " ORDER BY sale_date DESC, sale_time DESC LIMIT ?"
    params.append(limit)

    rows = q(sql, tuple(params))
    categories = q("SELECT DISTINCT category FROM retail_sales ORDER BY category")

    return render_template(
        "transactions.html",
        rows=rows,
        months=months,
        start_month=start_month,
        end_month=end_month,
        categories=categories,
        selected_category=category,
        search_customer=search_customer,
        limit=limit
    )



@app.route("/analysis")
def analysis():
    best_month = q("""
      WITH monthly AS (
        SELECT
          substr(sale_date, 1, 4) AS year,
          substr(sale_date, 6, 2) AS month,
          AVG(total_sale) AS avg_sale
        FROM retail_sales
        GROUP BY 1,2
      ),
      ranked AS (
        SELECT *,
               RANK() OVER (PARTITION BY year ORDER BY avg_sale DESC) AS rnk
        FROM monthly
      )
      SELECT year, month, ROUND(avg_sale, 2) AS avg_sale
      FROM ranked
      WHERE rnk = 1
      ORDER BY year;
    """)

    shift_orders = q("""
      WITH hourly AS (
        SELECT
          CASE
            WHEN CAST(substr(sale_time, 1, 2) AS INT) < 12 THEN 'Morning'
            WHEN CAST(substr(sale_time, 1, 2) AS INT) BETWEEN 12 AND 17 THEN 'Afternoon'
            ELSE 'Evening'
          END AS shift
        FROM retail_sales
      )
      SELECT shift, COUNT(*) AS total_orders
      FROM hourly
      GROUP BY shift
      ORDER BY total_orders DESC;
    """)

    sales_by_gender = q("""
      SELECT gender, ROUND(SUM(total_sale), 2) AS total_sales, COUNT(*) AS orders
      FROM retail_sales
      GROUP BY gender
      ORDER BY total_sales DESC;
    """)

    return render_template(
        "analysis.html",
        best_month=best_month,
        shift_orders=shift_orders,
        sales_by_gender=sales_by_gender
    )

if __name__ == "__main__":
    app.run(debug=True)
