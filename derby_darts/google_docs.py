import json
import pickle
import os.path
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.credentials import AnonymousCredentials


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

def read_strucutural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            paragraph = value.get('paragraph')
            elements = value.get('paragraph').get('elements')
            bullet = paragraph.get('bullet')
            heading = paragraph.get('paragraphStyle').get("namedStyleType")
            for elem in elements:
                element_text = read_paragraph_element(elem)
                if bullet:
                    indent = "    " * bullet.get("nestingLevel", 0)
                    text += indent + "- "
                if heading.startswith("HEADING") and element_text.strip():
                    text += "\r\n"
                    text += "#" * int(heading[-1]) + " "
                text += element_text
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            text += '<table class="table"><thead><tr>'
            for idx, row in enumerate(table.get('tableRows')):
                cells = row.get('tableCells')
                if (idx == 0):
                    for cell in cells:
                        text += "<th>{}</th>".format(read_strucutural_elements(cell.get('content')))
                    text += "</tr></thead><tbody>"
                else:
                    text += "<tr>"
                    for cell in cells:
                        text += "<td>{}</td>".format(read_strucutural_elements(cell.get('content')))
                    text += "<tr>"
            text += "</tbody></table>"
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
    return text

def google_doc_to_markdown(rules_id, service_account_json_string):
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

    info = json.loads(service_account_json_string)
    creds = service_account.Credentials.from_service_account_info(info)

    service = build('docs', 'v1', credentials=creds)
    document = service.documents().get(documentId=rules_id).execute()
    doc_content = document.get("body").get("content")
    doc_content = read_strucutural_elements(doc_content)

    # Replace phone numbers
    doc_content = re.sub(r"07\d{3}\s?\d{6}", "07--- ------", doc_content)

    return doc_content

def get_calendar_events(calendar_id, service_acc_json, startDate):
    info = json.loads(service_acc_json)
    creds = service_account.Credentials.from_service_account_info(info)
    service = build('calendar', 'v3', credentials=creds)
    events_result = service.events().list(calendarId=calendar_id, singleEvents=True, timeMin=startDate).execute()
    return events_result.get('items', [])
