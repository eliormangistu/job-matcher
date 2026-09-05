from app.db.session import engine, Base
from app.models.job import Job


print("Dropping jobs table...")
Job.__table__.drop(engine, checkfirst=True)

print("Creating jobs table...")
Job.__table__.create(engine, checkfirst=True)

print("Done!")