# 📊 Batch Data Pipeline Assignment

## 🎯 Goal

Your task is to complete a **batch data pipeline** for an e-commerce platform.

The pipeline should:

```text
read raw data → transform with PySpark → store in Parquet → run via Airflow
```

---

## 🧠 Business Context

An e-commerce company needs daily analytics:

```text
daily revenue by country
```

This dataset is used by:

* analysts
* dashboards
* data science teams

---

## 🧩 Your Task

You are given a **production-like pipeline with missing core logic**.

Your job is to implement the transformation so that the pipeline works correctly.

---

## ✅ What Is Already Implemented

You do NOT need to implement or modify:

* Airflow DAG
* Docker setup
* config loader
* input validation
* output validation
* Spark session creation

---

## 📁 Project Structure

```text
.
├── dags/                 # Airflow DAG (already implemented)
├── src/
│   ├── jobs/             # PySpark job (you must complete)
│   └── utils/            # config + validation (already implemented)
├── config/               # config.yaml
├── data/
│   ├── raw/              # input data
│   └── curated/          # output data
├── tests/                # unit tests
├── Dockerfile.airflow
├── docker-compose.yml
└── README.md
```

---

## 📥 Input Data

Located in:

```text
data/raw/
```

### users.csv

```text
user_id, country, registration_date
```

### orders.csv

```text
order_id, user_id, order_date, amount, status
```

---

## 📤 Expected Output

```text
data/curated/daily_revenue_by_country/
```

Partitioned by:

```text
order_date=YYYY-MM-DD/
```

### Expected columns

```text
order_date
country
total_revenue
completed_orders_count
unique_customers_count
avg_order_value
```

---

## ⚙️ What You Need to Implement

File:

```text
src/jobs/daily_revenue_by_country.py
```

### Required function

```python
def transform(users_df, orders_df):
    """
    Implement the transformation:

    1. filter only completed orders
    2. join orders with users on user_id
    3. group by order_date and country
    4. calculate:
       - total_revenue
       - completed_orders_count
       - unique_customers_count
       - avg_order_value

    avg_order_value = total_revenue / completed_orders_count
    """
    pass
```

---

## 🚀 How to Run

### 1. Start the system

```bash
docker compose up --build
```

---

### 2. Open Airflow

```text
http://localhost:8080
```

Credentials:

```text
admin / admin
```

---

### 3. Run the pipeline

* Find DAG: `ecommerce_daily_revenue_pipeline`
* Trigger DAG

---

## 🧪 Run Tests

Run tests inside Docker:

```bash
docker compose exec airflow-scheduler bash -c "cd /opt/airflow && PYTHONPATH=/opt/airflow pytest tests/"
```

---

## 🧪 What Will Be Checked

Autograder will verify:

* only completed orders are included
* cancelled orders are excluded
* revenue is calculated correctly
* users are joined correctly
* country is present in output
* unique customers are counted correctly
* avg_order_value is correct
* output is written as Parquet
* all tests pass

---

## ✔ Success Criteria

Your solution is correct if:

```text
✔ all tests pass
✔ Airflow DAG runs successfully (all tasks are green)
✔ output folder is created
✔ Parquet files exist
✔ data is correct
```

---

## ❌ Common Mistakes

* using pandas instead of PySpark
* not filtering cancelled orders
* incorrect join
* wrong aggregations
* missing partitioning
* modifying DAG or infrastructure instead of job logic

---

## 🧠 Important Notes

* Do NOT modify:

  * Airflow DAG
  * Docker configuration
  * validation utilities
  * tests

* Focus only on:

```text
transform() function
```

---

## 🟡 Bonus (Optional)

Implement a simple API:

```text
GET /revenue?date=YYYY-MM-DD
```

Requirements:

* read Parquet output
* return JSON

This does NOT affect the core assignment grading.

---

## 🏁 Final Result

You will build a **production-like batch data pipeline** using:

```text
PySpark + Airflow + Parquet
```
