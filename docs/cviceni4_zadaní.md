# Cvičení 4 - vyhodnocení procesu - první databázové 

# Příprava:

1. získat databázi
2. získat do ní data



# Kde získat databázi - tj. někam kap nahrát data v SQL

## PostGRE:

### **lokální instalace:**

PostGRE databáze - https://www.postgresql.org/docs/current/tutorial-install.html

*Pro:*

- je to jednouduché a rychlé

*Proti:*

- Postgre se úplně nekamaradí s jinými verzemi na stejném pc


### **Docker - lokální instalace**

Postgre v dockeru - https://hub.docker.com/_/postgres/

Moje instalace je: postgres:15.2-alpine

A docker run zde: 
```
docker run --hostname=24116f7c5ca7 --mac-address=02:42:ac:11:00:02 --env=POSTGRES_PASSWORD=run --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=LANG=en_US.utf8 --env=PG_MAJOR=15 --env=PG_VERSION=15.2 --env=PG_SHA256=99a2171fc3d6b5b5f56b757a7a3cb85d509a38e4273805def23941ed2b8468c7 --env=PGDATA=/var/lib/postgresql/data --volume=//c/dvdrental:/dvdrental --volume=/var/lib/postgresql/data -p 5432:5432 --restart=no --runtime=runc -t -d postgres:15.2-alpine
```

**Pro:**

- izolace Postgre od zbytku systému
- když, to nespustíme, tak to nekonzumuje zdroje.

**Proti:**

- chce to trochu znát docker https://www.docker.com/101-tutorial/ 

### **Cloud**

Zdarma - https://www.dplyr.dev/features/postgresql 
GCP - https://cloud.google.com/sql/postgresql
Azure - https://azure.microsoft.com/en-us/products/postgresql/


# Data

## PostGre SQL
Stáhnout - https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/



testovací MS SQL adventure works databáze
V Azure se dá vytočit v subscripci, případně si napište o přístupy mě.

# Když to nejde nebo nemám čas

napište email a zařídím za vás přístupy do AdventureWroks 2014 od MS.

# Obsah - Data discovery - jak na to
## Power BI
## V databázi samotné

# Úkol na přístí týden

## Dimenzní tabulky

Tabulka customer_dim obsahuje informace o zákaznících s následujícími sloupci:

- `customer_id` - identifikátor zákazníka
- `first_name` - křestní jméno zákazníka
- `last_name` - příjmení zákazníka
- `email` - emailová adresa zákazníka
- `address_id` - identifikátor adresy zákazníka
- `create_date` - datum vytvoření záznamu o zákazníkovi
- `last_update` - datum poslední aktualizace záznamu o zákazníkovi

Tabulka store_dim obsahuje informace o obchodech s následujícími sloupci:

- `store_id` - identifikátor obchodu
- `manager_staff_id` - identifikátor manažera obchodu
- `address_id` - identifikátor adresy obchodu
- `last_update` - datum poslední aktualizace záznamu o obchodu


Tabulka date_dim obsahuje informace o datech s následujícími sloupci:

- `date_id` - identifikátor data
- `date` - datum
- `year` - rok
- `quarter` - čtvrtletí
- `month` - měsíc
- `day` - den
- `day_of_week` - den v týdnu
- `day_name` - název dne v týdnu
- `is_weekend` - příznak, zda se jedná o víkend

```
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


```

## Faktová tabulka
Každý řádek v tabulce `rental_fact` reprezentuje jednu transakci pronájmu a obsahuje informace o zákazníkovi, DVD, datu pronájmu a případných pozdních poplatcích generovaných transakcí pronájmu. Spojením tabulky `rental_fact` s rozměry zákazníka, data a DVD můžeme generovat různé reporty a analýzy, abychom pochopili trendy v pronájmu, chování zákazníků a příjmy generované DVD pronájmem.

- `rental_id:` Tento sloupec je cizím klíčem odkazujícím na sloupec rental_id v tabulce rental. Identifikuje transakci pronájmu, která je spojena s daným řádkem v tabulce.
- `date_id:` Tento sloupec je cizím klíčem odkazujícím na sloupec date_id v tabulce date_dim. Identifikuje rozměr data spojený s daným řádkem v tabulce.
- `customer_id:` Tento sloupec je cizím klíčem odkazujícím na sloupec customer_id v tabulce customer_dim. Identifikuje rozměr zákazníka spojený s daným řádkem v tabulce.
- `inventory_id:` Tento sloupec je cizím klíčem odkazujícím na sloupec inventory_id v tabulce inventory. Identifikuje DVD inventář spojený s daným řádkem v tabulce.
- `rental_count:` Tento sloupec zobrazuje počet zapůjčených filmů.
- `rental_revenue:` Tento sloupec  celkový příjem z pronájmu filmů.
- `late_fee_revenue:` Tento sloupec reprezentuje příjmy generované pozdními poplatky za transakci pronájmu spojenou s daným řádkem v tabulce. Je vypočítán na základě rozdílu mezi datem vrácení a očekávaným datem vrácení pro transakci pronájmu a je vynásobený sazbou pronájmu pro DVD. Pokud DVD ještě nebylo vráceno nebo bylo vráceno včas, bude mít tento sloupec hodnotu 0.


```
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
```