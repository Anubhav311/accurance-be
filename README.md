# Meeting Document Generator API

FastAPI backend to generate meeting-related documents
(Board Meetings, AGM, EGM) using Excel inputs and DOCX templates.

## Tech Stack
- FastAPI
- Python
- openpyxl
- docxtpl

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
