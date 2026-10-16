## Grading Hints

Your solution will be checked against the following expectations:

### 1. Completed orders only
Cancelled or non-completed orders must not affect revenue or order counts.

### 2. Correct revenue calculation
`total_revenue` must be the sum of `amount` for completed orders.

### 3. Correct grouping
Data must be grouped by:

- `order_date`
- `country`

### 4. Correct customer metric
`unique_customers_count` must count distinct users, not total rows.

### 5. Correct average order value
`avg_order_value` should represent:

```text
total_revenue / completed_orders_count