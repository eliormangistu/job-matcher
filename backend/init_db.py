from app.db.session import engine, Base
from app.models import Job

Base.metadata.create_all(bind=engine)

print("Database tables created!")