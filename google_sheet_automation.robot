*** Settings ***
Library           google_sheets_lib.py
Library           OperatingSystem
Library           postgres_lib.py

*** Variables ***
${SPREADSHEET_ID}    15LziGkhsTY-GvGRAW-Q5OCXy7znuJhVJE8RZjKdltL8  # Replace with actual Spreadsheet ID


*** Test Cases ***
Copy Data From Google Sheets And Insert Into PostgreSQL
    [Documentation]     Copies data from Sheet1 to Sheet2 and inserts it into PostgreSQL
    Run Keyword         copy_sheet_data
    
*** Keywords ***
get_sheet_data
    [Arguments]         ${sheet_name}
    ${service}=         Get Service
    ${sheet}=           Call Method               ${service}.spreadsheets().values().get
    ...                 spreadsheetId=${SPREADSHEET_ID}
    ...                 range=${sheet_name}
    ${result}=          Call Method               ${sheet}.execute()
    ${values}=          Set Variable              ${result['values']}
    RETURN              ${values}
