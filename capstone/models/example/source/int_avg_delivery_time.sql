WITH delivery_times AS (
    SELECT
        order_id,
        DATE_DIFF(
            DATE(SAFE_CAST(order_delivered_customer_date AS TIMESTAMP)),
            DATE(SAFE_CAST(order_purchase_timestamp AS TIMESTAMP)),
            DAY
        ) AS delivery_time_days
    FROM {{ ref('stg_orders') }}
    WHERE order_delivered_customer_date IS NOT NULL
      AND order_purchase_timestamp IS NOT NULL
      AND SAFE_CAST(order_delivered_customer_date AS TIMESTAMP) IS NOT NULL
      AND SAFE_CAST(order_purchase_timestamp AS TIMESTAMP) IS NOT NULL
)

SELECT
    AVG(delivery_time_days) AS avg_delivery_time_days
FROM delivery_times
