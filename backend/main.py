from fastapi import FastAPI

app = FastAPI(title="Job Matcher API")


@app.get("/")
def root():
    return {"message": "Job Matcher API is running!"}


@app.get("/jobs")
def get_jobs():
    return [
        {
            "id": 1,
            "title": "Full Stack Developer",
            "company": "Example Tech",
            "location": "Tel Aviv",
            "remote": True
        },
        {
            "id": 2,
            "title": "Backend Developer",
            "company": "AI Startup",
            "location": "Tel Aviv",
            "remote": False
        }
    ]