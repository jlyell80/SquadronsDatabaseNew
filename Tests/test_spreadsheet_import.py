from src.GoogleTools.SheetsTools import import_sheet_data

sheet_url = 'https://docs.google.com/spreadsheets/d/1tQ6Fvg_jVRny3weLGcrV0vadI9geUe9-_zgSt8HJpLY/'
column_names = ["Match ID", "Result", "Away", "Home", "Season", "Round", "Match", "Group", "Map"]
data = import_sheet_data(sheet_url, "Entry_Check", column_names)

print(data)
