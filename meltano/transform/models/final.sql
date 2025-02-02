WITH o as (SELECT * FROM orders),

     od as (SELECT * FROM order_details),

     p as (SELECT * FROM products),

     c as (SELECT categories.category_id, category_name, description as category_description, picture FROM categories),

     e as (SELECT employee_id, last_name, first_name, title, concat(last_name, ', ', first_name) as full_name FROM employees),

     cust as (SELECT * FROM customers),

     
     
     final as (SELECT o.order_id,
                      o.customer_id,
                      cust.company_name,
                      o.employee_id,
                      e.full_name,
                      o.order_date,
                      o.ship_city,
                      o.ship_country,
                      od.product_id,
                      p.product_name,
                      c.category_name,
                      c.category_description,
                      od.unit_price,
                      od.quantity,
                      od.discount
               FROM o
                        INNER JOIN od ON o.order_id = od.order_id
                        INNER JOIN p ON od.product_id = p.product_id
                        INNER JOIN c ON p.category_id = c.category_id
                        INNER JOIN e ON o.employee_id = e.employee_id
                        INNER JOIN cust ON o.customer_id = cust.customer_id)


                        
SELECT * FROM final