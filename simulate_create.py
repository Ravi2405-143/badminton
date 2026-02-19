from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Tournament, SportType, FormatType, Base

engine = create_engine("sqlite:///tournament.db")
Session = sessionmaker(bind=engine)
db = Session()

try:
    t = Tournament(
        name="Test",
        sport=SportType.CRICKET,
        format=FormatType.LEAGUE,
        num_participants=4,
        points_per_win=2,
        points_per_draw=1,
        is_doubles=False,
        rules="{}"
    )
    db.add(t)
    db.commit()
    print("Success")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
