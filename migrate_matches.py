from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///tournament.db")

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE matches ADD COLUMN notes TEXT"))
        conn.commit()
        print("Success: added notes to matches")
    except Exception as e:
        print(f"Error (maybe column exists?): {e}")
