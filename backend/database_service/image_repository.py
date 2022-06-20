import json
from typing import List
import pyodbc
import uuid
import pandas as pd

from models.symbol import Symbol

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-0P6HV5K\SQLEXPRESS;'
                      'Database=MusicalPlayer;'
                      'Trusted_Connection=yes;')


def jsonify(notes: List[Symbol]):
    normalized_list = []
    for staff in notes:
        norm_staff = []
        for n in staff:
            norm_staff.append(n.to_dict())
        normalized_list.append(norm_staff)
    return json.dumps(normalized_list)


def insert_processed_image(file_name: str, values):
    table = 'ProcessedImage'
    stringified_notes = jsonify(values)

    new_row = [str(uuid.uuid4()), file_name, stringified_notes]
    new_values = f"INSERT INTO {table} VALUES (?,?,?)"

    cursor = conn.cursor()
    cursor.execute(new_values, new_row)
    cursor.commit()
    cursor.close()


def read_processed_image(file_name: str):
    processed_image = pd.read_sql_query(f"SELECT * FROM ProcessedImage WHERE FileName = '{file_name}'", conn)

    return processed_image
