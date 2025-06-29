launch: uvicorn app.main:app --reload
create migration: alembic revision --autogenerate -m "migration_description"
apply migrations: alembic upgrade head
