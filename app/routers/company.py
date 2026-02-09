from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from app.models.company import CompanyCreateRequest, CompanyCreateResponse
from gen_meeting_docs import gen_meeting_docs
# from app.services.meeting_service import MeetingService
from app.services.excel_writer import write_company_with_directors_and_meeting

router = APIRouter(prefix="/company", tags=["Company"])

# service = MeetingService()

@router.post(
    "/create",
    response_model=CompanyCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_company(company: CompanyCreateRequest):
    company_id = write_company_with_directors_and_meeting(company)

    try:
        return {
            "id": company_id,
            "companyName": company.companyName,
            "companyType": company.companyType,
        }
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid company")
        # return {"error": str(e)}
