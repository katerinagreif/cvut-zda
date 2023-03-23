DROP SCHEMA IF EXISTS dvdrental_dwh;
CREATE schema dvdrental_dwh;


/* Creating Dimensions table */

CREATE TABLE dvdrental_dwh.customer_dim
(
    customer_id INT PRIMARY KEY,
    first_name  VARCHAR(50),
    last_name   VARCHAR(50),
    email       VARCHAR(255),
    address_id  INT,
    create_date DATE,
    last_update TIMESTAMP
);

CREATE TABLE dvdrental_dwh.store_dim
(
    store_id         INT PRIMARY KEY,
    manager_staff_id INT,
    address_id       INT,
    last_update      TIMESTAMP
);


CREATE TABLE dvdrental_dwh.date_dim
(
    date_id     SERIAL PRIMARY KEY,
    date        DATE,
    year        INT,
    quarter     INT,
    month       INT,
    day         INT,
    day_of_week INT,
    day_name    VARCHAR(10),
    is_weekend  BOOLEAN
);

DROP TABLE IF EXISTS dvdrental_dwh.address_dim CASCADE;
CREATE TABLE dvdrental_dwh.address_dim
(
    address_id   INT PRIMARY KEY,
    address      TEXT      NOT NULL,
    district     TEXT      NOT NULL,
    city_id      INT       NOT NULL,
    city_name    TEXT      NOT NULL,
    country_id   INT       NOT NULL,
    country_name TEXT      NOT NULL,
    postal_code  TEXT      NOT NULL,
    phone        TEXT      NOT NULL,
    last_update  TIMESTAMP NOT NULL
);


CREATE TABLE dvdrental_dwh.staff_dim
(
    staff_id   INT PRIMARY KEY,
    first_name TEXT,
    last_name  TEXT,
    email      TEXT,
    active     BOOLEAN,
    store_id   INT,
    address_id INT REFERENCES dvdrental_dwh.address_dim (address_id),
    CONSTRAINT staff_store_fk FOREIGN KEY (store_id) REFERENCES store (store_id)
);


/* Create fact table*/
CREATE TABLE dvdrental_dwh.rental_fact
(
    customer_id      INT,
    store_id         INT,
    date_id          INT,
    rental_count     INT,
    rental_revenue   DECIMAL(5, 2),
    late_fee_revenue DECIMAL(5, 2)
);


/* Populating Dimension tables*/

INSERT INTO dvdrental_dwh.customer_dim
SELECT customer_id,
       first_name,
       last_name,
       email,
       address_id,
       create_date,
       last_update
FROM dvdrental.public.customer;



INSERT INTO dvdrental_dwh.store_dim
SELECT store_id,
       manager_staff_id,
       address_id,
       last_update
FROM dvdrental.public.store;

INSERT INTO dvdrental_dwh.date_dim (date, year, quarter, month, day, day_of_week, day_name, is_weekend)
SELECT distinct DATE(rental_date)                 AS date,
                EXTRACT(year FROM rental_date)    AS year,
                EXTRACT(quarter FROM rental_date) AS quarter,
                EXTRACT(month FROM rental_date)   AS month,
                EXTRACT(day FROM rental_date)     AS day,
                EXTRACT(dow FROM rental_date)     AS day_of_week,
                to_char(rental_date, 'Day')       AS day_name,
                CASE
                    WHEN EXTRACT(dow FROM rental_date) IN (0, 6) THEN TRUE
                    ELSE FALSE
                    END                           AS is_weekend
FROM dvdrental.public.rental;

INSERT INTO dvdrental_dwh.address_dim (address_id, address, district, city_id, city_name, country_id, country_name,
                                       postal_code, phone, last_update)
SELECT address_id,
       address,
       district,
       city.city_id,
       city.city,
       country.country_id,
       country.country,
       postal_code,
       phone,
       address.last_update
FROM dvdrental.public.address
         JOIN dvdrental.public.city ON address.city_id = city.city_id
         JOIN dvdrental.public.country ON city.country_id = country.country_id;

INSERT INTO dvdrental_dwh.staff_dim (staff_id, first_name, last_name, email, active, store_id, address_id)
SELECT staff_id,
       first_name,
       last_name,
       email,
       active,
       store_id,
       address.address_id
FROM dvdrental.public.staff
         JOIN dvdrental.public.address ON staff.address_id = address.address_id;


INSERT INTO dvdrental_dwh.rental_fact (customer_id, store_id, date_id, rental_count, rental_revenue, late_fee_revenue)
SELECT rental.customer_id,
       store.store_id,
       date_dim.date_id,
       COUNT(rental.rental_id) AS rental_count,
       SUM(payment.amount)     AS rental_revenue,
       SUM(CASE
               WHEN rental.return_date > rental.rental_date + INTERVAL '1 day' * film.rental_duration THEN
                       EXTRACT(day FROM
                               (rental.return_date - rental.rental_date - INTERVAL '1 day' * film.rental_duration)) *
                       film.rental_rate
               ELSE 0 END)     AS late_fee_revenue
FROM dvdrental.public.rental
         LEFT JOIN dvdrental.public.payment
                   ON rental.rental_id = payment.rental_id
         LEFT JOIN dvdrental.public.inventory
                   ON rental.inventory_id = inventory.inventory_id
         LEFT JOIN dvdrental.public.film
                   ON inventory.film_id = film.film_id
         LEFT JOIN dvdrental.public.store
                   ON inventory.store_id = store.store_id
         LEFT JOIN dvdrental_dwh.date_dim
                   ON DATE(rental.rental_date) = date_dim.date
GROUP BY rental.customer_id,
         store.store_id,
         date_dim.date_id

