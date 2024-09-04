import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            data.append({
                "chapter_number": row['chapter_number'],
                "chapter_title": row['chapter_title'],
                "chapter_verse": row['chapter_verse'],
                "translation": row['translation']
            })
    
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


csv_file_path = 'gita.csv'
json_file_path = 'gita_data.json'

csv_to_json(csv_file_path, json_file_path)
