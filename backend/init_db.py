from app.db.session import engine, Base
from app.models.job import Job

Base.metadata.create_all(bind=engine)

print("Database tables created!")