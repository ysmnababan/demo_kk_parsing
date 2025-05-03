import json
from openpyxl import load_workbook

# Load your JSON file
with open('./output/processed_data.json') as f:
    data = json.load(f)

SheetName = "Input Form"
# Define the mapping of JSON keys to cell locations
cell_mapping = {
    'no': (SheetName, 'J3'),
    'keluarga': (SheetName, 'D4'),
    'kelurahan': (SheetName, 'Q4'),
    'alamat': (SheetName, 'D5'),
    'kecamatan': (SheetName, 'Q5'),
    'rw': (SheetName, 'D6'),
    'kota': (SheetName, 'Q6'),
    'pos': (SheetName, 'D7'),
    'provinsi': (SheetName, 'Q7'),
    'keluarga': (SheetName, 'H39'),
    'officer_name': (SheetName, 'N39'),
    'nip': (SheetName, 'O40'),
    'father_names': (SheetName, 'N24'),  # starting cell for the array
    'mother_names': (SheetName, 'Q24'),  # starting cell for the array
    'kitas_no': (SheetName, 'K24')  # starting cell for the array
}

# Load your Excel workbook
workbook = load_workbook('./src/template.xlsx')

# Fill the cells with data
for key, (sheet_name, cell) in cell_mapping.items():
    if key in data:
        sheet = workbook[sheet_name]
        value = data[key]
        
        # Check if it's a list (array)
        if isinstance(value, list):
            # Get the starting row and column
            col = ''.join(filter(str.isalpha, cell))
            start_row = int(''.join(filter(str.isdigit, cell)))
            
            # Fill down the column
            for i, item in enumerate(value):
                target_cell = f"{col}{start_row + i}"
                sheet[target_cell] = item
        else:
            # Single value
            sheet[cell] = value

# Save to a new file (or overwrite)
workbook.save('./output/final.xlsx')
