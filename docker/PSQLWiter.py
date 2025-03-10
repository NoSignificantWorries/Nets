import json

import psycopg2
from decimal import Decimal


class PSQLwriter:
    def __init__(self, url, table):
        try:
            self.connection = psycopg2.connect(url)
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            return None
        self.table = table
    
    def quit(self):
        self.cursor.close()
        self.connection.close()
    
    def clear_table(self):
        self.cursor.execute(f"TRUNCATE TABLE {self.table} RESTART IDENTITY;")
        self.connection.commit()

    def write_data(self, data):
        self.cursor.executemany(f"INSERT INTO {self.table} (url) VALUES (%s)", data)
        self.connection.commit()
    
    def write_data_to_json(self, file_path="results.json"):
        self.cursor.execute(f"SELECT * FROM {self.table};")

        column_names = [description[0] for description in self.cursor.description]
        rows = self.cursor.fetchall()

        data = []
        for row in rows:
            row_dict = {}
            for i, column_name in enumerate(column_names):
                value = row[i]
                if isinstance(value, Decimal):
                    value = float(value)
                row_dict[column_name] = value
            data.append(row_dict)

        if file_path is not None:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        
        return json.dumps(data)
