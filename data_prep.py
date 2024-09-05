import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    chapters = {}
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            chapter_number = row['chapter_number']
            if chapter_number not in chapters:
                chapters[chapter_number] = {
                    "chapter_number": chapter_number,
                    "chapter_text": ""
                }
            
            # Append to the combined chapter text
            chapters[chapter_number]["chapter_text"] += f"{row['chapter_verse']}: {row['translation']} "
    
    data = list(chapters.values())
    
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

csv_file_path = 'gita.csv'
json_file_path = 'gita_data.json'

csv_to_json(csv_file_path, json_file_path)