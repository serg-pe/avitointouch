# Avito Scraper


Scraper for Avito website.

# List of environment variables used in project
- *DB_NAME* - sqlite database name
- *TG_BOT_TOKEN* - token for telegram bot

# How to guides

Init database with Alembic
1. Initialize alembic database using Terminal

```bash
alembic init alembic
```
2. In *alembic.ini* find *sqlalchemy.url* variable and set its value to connection string of your database
3. Open *alembic/env.py* and change *target_metadata = None* to *target_metadata = Base* from *models/models.py* given from *declarative_base()* 
4. Make migration using Terminal
```bash
alembic upgrade head
```