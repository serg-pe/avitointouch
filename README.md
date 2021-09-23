# Avito Scraper


Scraper for Avito website.

Init database with Alembic
2. Initialize alembic database using Terminal

```bash
alembic init alembic
```
2. In *alembic.ini* find *sqlalchemy.url* variable and set its value to connection string of your database
2. Open *alembic/env.py* and change *target_metadata = None* to *target_metadata = Base* from *models/models.py* given from *declarative_base()* 
3. Make migration using Terminal
```bash
alembic upgrade head
```