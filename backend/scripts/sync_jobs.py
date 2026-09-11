from app.ingestion.service import ingest_jobs
from scripts.import_jobs import import_jobs


def sync_jobs():
    print("Starting job sync...")

    ingest_jobs()

    print("Ingestion completed.")
    print("Importing jobs into PostgreSQL...")

    import_jobs()

    print("Job sync completed successfully.")


if __name__ == "__main__":
    sync_jobs()
