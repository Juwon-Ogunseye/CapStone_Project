with sales as (
    select
        p.product_category_name,
        sum(oi.price) as total_sales
    from {{ ref('stg_products') }} as p
    join {{ ref('stg_order_items') }} as oi on p.product_id = oi.product_id
    group by p.product_category_name
)
select * from sales

