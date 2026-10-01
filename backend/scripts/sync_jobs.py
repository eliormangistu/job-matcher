from app.db.session import SessionLocal
from app.ingestion.service import ingest_jobs
from app.services.cv_match import refresh_all_cv_matches
from scripts.import_jobs import import_jobs


def sync_jobs():
    print("Starting job sync...")

    ingest_jobs()
    print("Ingestion completed.")

    print("Importing jobs into PostgreSQL...")
    import_jobs()
    print("Job import completed.")

    print("Refreshing CV matches...")
    db = SessionLocal()

    try:
        refresh_all_cv_matches(
            db=db,
        )
    finally:
        db.close()

    print("CV matches refreshed.")
    print("Job sync completed successfully.")


if __name__ == "__main__":
    sync_jobs()
