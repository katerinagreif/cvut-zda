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