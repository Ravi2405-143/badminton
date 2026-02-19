from sqlalchemy import create_engine, inspect
engine = create_engine("sqlite:///tournament.db")
inspector = inspect(engine)
for table_name in ["scores"]:
    print(f"--- {table_name} ---")
    columns = inspector.get_columns(table_name)
    for column in columns:
        print(column["name"])
