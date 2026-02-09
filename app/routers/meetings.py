from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from gen_meeting_docs import gen_meeting_docs
# from app.services.meeting_service import MeetingService

router = APIRouter(prefix="/meetings", tags=["Meetings"])

# service = MeetingService()

@router.get("/generate")
def generate_meeting_doc():
    try:
        gen_meeting_docs()
        return {"message": "Meeting document generated successfully"}
    except ValueError as e:
        print(e)
        return {"error": str(e)}
