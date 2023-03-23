CREATE MATERIALIZED VIEW dvdrental_dwh.rental_cube AS
SELECT customer_dim.first_name,
       customer_dim.last_name,
       store_dim.store_id,
       date_dim.year,
       date_dim.quarter,
       SUM(rental_fact.rental_count)     AS rental_count,
       SUM(rental_fact.rental_revenue)   AS rental_revenue,
       SUM(rental_fact.late_fee_revenue) AS late_fee_revenue
FROM dvdrental_dwh.rental_fact
         LEFT JOIN
     dvdrental_dwh.customer_dim ON rental_fact.customer_id = customer_dim.customer_id
         LEFT JOIN
     dvdrental_dwh.store_dim ON rental_fact.store_id = store_dim.store_id
         LEFT JOIN
     dvdrental_dwh.date_dim ON rental_fact.date_id = date_dim.date_id
GROUP BY customer_dim.first_name,
         customer_dim.last_name,
         store_dim.store_id,
         date_dim.year,
         date_dim.quarter
WITH DATA;
