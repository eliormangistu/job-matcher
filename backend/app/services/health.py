@router.get("/")
def health_check():
    return {"message": "Job Matcher API is running!"}