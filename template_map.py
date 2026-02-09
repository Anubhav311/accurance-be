TEMPLATE_MAP = {
    "Board Meeting": {
        "NOTICE": "BM_NOTICE.docx",
        "AGENDA": "BM_AGENDA.docx",
        "MINUTES": "BM_MINUTES.docx",
        "ATTENDANCE": "BM_ATTENDANCE_SHEET.docx",
        "CTC": "BM_CTC.docx",
        "SNC": "BM_SHORTER_NOTICE_CONSENT.docx",
    },
    "Annual General Meeting": {
        "NOTICE": "AGM_NOTICE.docx",
        "AGENDA": "AGM_AGENDA.docx",
        "MINUTES": "AGM_MINUTES.docx",
        "PROXY": "AGM_PROXY_FORM.docx",
        "SNC": "AGM_SHORTER_NOTICE_CONSENT.docx",
        "ATTENDANCE": "AGM_ATTENDANCE_SHEET.docx",
        "CTC": "AGM_CTC.docx",
        "AUTHORITY": "AGM_AUTHORITY_LETTER.docx"
    },
    "Extraordinary General Meeting": {
        "NOTICE": "EGM_NOTICE.docx",
        "AGENDA": "EGM_AGENDA.docx",
        "MINUTES": "EGM_MINUTES.docx",
        "SNC": "EGM_SHORTER_NOTICE_CONSENT.docx",
        "ATTENDANCE": "EGM_ATTENDANCE_SHEET.docx",
        "CTC": "EGM_CTC.docx",
        "AUTHORITY": "EGM_AUTHORITY_LETTER.docx"
    }
}

MULTI_OUTPUT_DOCS = {"SNC"}      # one template → many files
SINGLE_OUTPUT_DOCS = {"NOTICE", "AGENDA", "MINUTES", "ATTENDANCE", "CTC"}
