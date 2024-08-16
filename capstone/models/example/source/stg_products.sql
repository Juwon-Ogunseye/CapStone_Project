with products as (
    select
        product_id,
        product_category_name,
        product_name_lenght,  -- Note the correct column names
        product_description_lenght,  -- Correct the column names
        product_photos_qty,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm
    from {{ source('raw', 'olist_products_dataset') }}
)
select * from products
