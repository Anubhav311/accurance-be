from pydantic import BaseModel, field_validator, Field, HttpUrl
from typing import Literal, List, Optional
from datetime import date, time
from enum import Enum
from .director import Director

# class Address(BaseModel):
#     line1: str
#     line2: str
#     city: str
#     state: str
#     pinCode: str
#     country: str = "India"

#     @field_validator("pinCode")
#     @classmethod
#     def validate_pin(cls, v):
#         if not re.match(r"^[1-9][0-9]{5}$", v):
#             raise ValueError("Invalid Indian PIN code")
#         return v

class MeetingType(str, Enum):
    BM = "BM"
    AGM = "AGM"
    EGM = "EGM"
    CSR = "CSR"


class AttendanceMode(str, Enum):
    physical = "physical"
    virtual = "virtual"


class MeetingDay(str, Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"


class Meeting(BaseModel):
    meetingType: MeetingType
    attendanceMode: AttendanceMode
    serialNumber: str
    financialYear: str
    signatory: str
    meetingLink: Optional[HttpUrl]
    meetingId: Optional[str]
    meetingPasscode: Optional[str]
    meetingDay: MeetingDay
    meetingDate: date
    meetingTime: time
    venue: str
    shorterNotice: bool = False

class CompanyCreateRequest(BaseModel):
    companyName: str
    companyType: Literal[
        "One Person Company",
        "Private Limited",
        "Public Limited",
        "Listed Company",
    ]
    incorporationDate: date
    registeredOffice: str = Field(..., min_length=10)
    directors: List[Director] = Field(..., min_items=2)
    meeting: Meeting

    @field_validator("incorporationDate")
    @classmethod
    def must_be_in_past(cls, v: date):
        if v >= date.today():
            raise ValueError("Date of incorporation must be before today")
        return v

class CompanyCreateResponse(BaseModel):
    companyName: str
    companyType: str
    id: int

