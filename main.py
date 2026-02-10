import openpyxl
from pathlib import Path
from docxtpl import DocxTemplate
from fastapi import FastAPI
from app.routers.meetings import router as meetings_router
from app.routers.company import router as company_router
from app.routers.health import router as health_router
from fastapi.middleware.cors import CORSMiddleware

from table_builder import build_attendance_table
from template_map import TEMPLATE_MAP, MULTI_OUTPUT_DOCS
from utility_helpers.utility_helprs import (
    load_key_value_sheet,
    load_directors_from_excel,
    load_agenda_from_excel,
    safe_filename,
    generate_snc_documents,
    load_resolution_index,
    build_resolution_subdoc
)

from conf import settings

# # ---------------------------
# # Load paths
# # ---------------------------
# BASE_DIR = Path("/Users/marve/Desktop/auto")

# data_path = BASE_DIR / "data" / "data.xlsx"
# output_dir = BASE_DIR / "docs"
# templates_dir = BASE_DIR / "temps" / "BM"
# resolutions_dir = BASE_DIR / "temps" / "BM" / "resolutions"
# resolution_index_path = BASE_DIR / "data" / "resolutions_index.xlsx"

# ctc_template_path = templates_dir / "BM_CTC.docx"
# notice_template_path = templates_dir / "BM_NOTICE.docx"
# agenda_template_path = templates_dir / "BM_AGENDA.docx"
# minutes_template_path = templates_dir / "BM_MINUTES.docx"
# snc_template_path = templates_dir / "BM_SHORTER_NOTICE_CONSENT.docx"
# attendance_sheet_template_path = templates_dir / "BM_ATTENDANCE_SHEET.docx"

# output_dir.mkdir(parents=True, exist_ok=True)


# # --------------------------------------------------
# # Load Excel data
# # --------------------------------------------------
# workbook = openpyxl.load_workbook(data_path)
# meeting_data = load_key_value_sheet(workbook, "Meeting")
# directors = load_directors_from_excel(workbook, "Directors")
# agenda_items = load_agenda_from_excel(workbook, "Agenda")

# meeting_type = meeting_data["MEETING_TYPE"]  # BM / AGM / EGM


# # extract resolution ids from Agenda
# selected_resolution_ids = [
#     item["RESOLUTION_ID"]
#     for item in agenda_items
# ]


# # ==================================================
# # Load resolution index
# # ==================================================
# resolution_index = load_resolution_index(
#     resolution_index_path,
#     meeting_type
# )


# # --------------------------------------------------
# # Load templates
# # --------------------------------------------------
# templates_for_meeting = TEMPLATE_MAP[meeting_type]

# single_docs = {}
# multi_docs = {}

# for doc_type, filename in templates_for_meeting.items():
#     template_path = templates_dir / filename

#     if doc_type in MULTI_OUTPUT_DOCS:
#         multi_docs[doc_type] = template_path   # store PATH only
#     else:
#         single_docs[doc_type] = DocxTemplate(template_path)


# # --------------------------------------------------
# # Build attendance table (subdoc)
# # --------------------------------------------------
# attendance_table_subdoc = build_attendance_table(
#     single_docs["ATTENDANCE"],
#     directors
# )


# # --------------------------------------------------
# # Context for all documents 
# # --------------------------------------------------
# base_context = {
#     "GOVERNING_BODY": meeting_data["GOVERNING_BODY"],
#     "COMPANY_NAME": meeting_data["COMPANY_NAME"],
#     "SR_NO": meeting_data["SR_NO"],
#     "FINANCIAL_YEAR": meeting_data["FINANCIAL_YEAR"],
#     "SHORTER_NOTICE": "AT A SHORTER NOTICE" if meeting_data["SHORTER_NOTICE"] == "Yes" else "",
#     "MEETING_DAY": meeting_data["MEETING_DAY"],
#     "MEETING_DATE": meeting_data["MEETING_DATE"],
#     "MEETING_TIME": meeting_data["MEETING_TIME"],
#     "MEETING_VENUE": meeting_data["MEETING_VENUE"],
#     "ATTENDANCE_MODE": meeting_data["ATTENDANCE_MODE"],
#     "MEETING_TYPE": meeting_data["MEETING_TYPE"],
#     "SIGNATORY_NAME": meeting_data["SIGNATORY_NAME"],
#     "SIGNATORY_DESIGNATION": meeting_data["SIGNATORY_DESIGNATION"],
#     "SIGNATORY_DIN": meeting_data["SIGNATORY_DIN"],
#     "SIGNATORY_ADDRESS": meeting_data["SIGNATORY_ADDRESS"],
#     "REGISTERED_OFFICE_ADDRESS": meeting_data["REGISTERED_OFFICE_ADDRESS"],
#     "MEETING_LINK": meeting_data["MEETING_LINK"],
#     "MEETING_ID": meeting_data["MEETING_ID"],
#     "MEETING_PASSCODE": meeting_data["MEETING_PASSCODE"],
#     "AGENDA_ITEMS": agenda_items,
#     "ATTENDANCE_TABLE": attendance_table_subdoc,
# }


# # ==================================================
# # Attach resolutions to agenda items
# # ==================================================
# for item in agenda_items:
#     resolution_id = item.get("RESOLUTION_ID")

#     # Agenda items like "Leave of Absence" may have no resolution
#     if not resolution_id:
#         continue

#     if resolution_id not in resolution_index:
#         raise ValueError(f"Invalid Resolution ID: {resolution_id}")

#     resolution_meta = resolution_index[resolution_id]
#     resolution_template_path = resolutions_dir / resolution_meta["template"]

#     resolution_subdoc = build_resolution_subdoc(single_docs["AGENDA"], resolution_template_path, base_context)
#     # # ✅ subdoc must be created from the AGENDA document
#     # resolution_subdoc = single_docs["AGENDA"].new_subdoc()

#     # # render the resolution template
#     # resolution_tpl = DocxTemplate(resolution_template_path)
#     # resolution_tpl.render(base_context)

#     # for element in resolution_tpl.docx._body._element:
#     #     if element.tag == qn("w:sectPr"):
#     #         continue
#     #     resolution_subdoc._body._element.append(copy.deepcopy(element))

#     item["RESOLUTION_DOC"] = resolution_subdoc

#     ctc_context = {
#         **base_context,
#         "RESOLUTION_BODY": resolution_subdoc,
#     }

#     ctc_doc = DocxTemplate(ctc_template_path)
#     ctc_doc.render(ctc_context)

#     safe_title = safe_filename(resolution_meta["title"])
#     filename = f"CTC_{resolution_id}_{safe_title}.docx"

#     ctc_doc.save(output_dir / filename)




# # ==================================================
# # FINAL CONTEXT (used for Agenda / Minutes / CTC)
# # ==================================================
# context = {
#     **base_context,
#     "AGENDA_ITEMS": agenda_items,
#     "ATTENDANCE_TABLE": attendance_table_subdoc,
# }


# # --------------------------------------------------
# # Render & save documents
# # --------------------------------------------------
# company_name_safe = safe_filename(context["COMPANY_NAME"])

# for doc_type, doc in single_docs.items():
#     doc.render(context)
#     filename = f"{doc_type}_{company_name_safe}.docx"
#     doc.save(output_dir / filename)



# # --------------------------------------------------
# # Render & Save Shorter Notice Consents (SNC)
# # --------------------------------------------------
# if "SNC" in multi_docs and meeting_data["SHORTER_NOTICE"] == "Yes":
#     generate_snc_documents(
#         template_path=multi_docs["SNC"],
#         output_dir=output_dir,
#         base_context=context,
#         directors=directors,
#         company_name_safe=company_name_safe,
#         safe_filename=safe_filename
#     )




app = FastAPI(title="Meeting Document Generator")

origins = [
    settings.origin_localhost,
    settings.origin_localhost_2
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(meetings_router)
app.include_router(company_router)
app.include_router(health_router)