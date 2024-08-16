with orders_by_state as (
    select
        c.customer_state,
        count(o.order_id) as total_orders
    from {{ ref('stg_orders') }} as o
    join {{ ref('stg_customers') }} as c on o.customer_id = c.customer_id
    group by c.customer_state
)
select * from orders_by_state
