import json
from zipfile import ZipFile
import re

class Business:

    """
    Extracts business details from a JSON file within a zip folder.
    """

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def business_details(zip_file_path):

        """
        Extracts business details from a JSON file within a zip folder.

        Args:
            zip_file_path (str): Path to the zip file.

        Returns:
            tuple: A tuple containing the extracted business details in the following order:
                - name (str): Business name.
                - city (str): City of the business.
                - country (str): Country of the business.
                - desc (str): Business description.
                - street_add (str): Street address of the business.
                - zip_code (str): Zip code of the business.
        """

        json_file = 'structuredData.json'
        
        # Initializing member variables
        city = None
        country = None
        desc = None
        name = None
        street_add = None
        zip_code = None

        with ZipFile(zip_file_path, 'r') as zip_ref:
            # Extract the JSON file from the zip folder
            zip_ref.extract(json_file)
        
        with open(json_file, 'r') as file:
            data = json.load(file)
            c = 0
            for item in data['elements']:
                
                # Title is often followed by description
                if item.get('Text') and c==1:
                    c = 0
                    desc = item.get('Text')

                    
                # Name is always same as title of the json 
                if item.get('TextSize') and  int(item.get('TextSize')) > 20 :
                    name = item.get('Text')
                    c = 1

            for item in data['elements']:
                
                # Search for zip_code as the first occurence of a 5-digit number
                if item.get('Text'):
                    match = re.search(r'^\d{5}\s*$', item.get('Text'))
                    if match:
                        zip_code = match.group()
                        path = item['Path']
                        last_slash_index = path.rfind('[')
                        modified_path = path[:last_slash_index] if last_slash_index != -1 else path
                        path = modified_path
                        
                        # Extract texts with same path
                        texts_with_same_path = [element.get('Text') for element in data['elements'] if path in element.get('Path')]
                        if texts_with_same_path:
                            for i, text in enumerate(texts_with_same_path):
                                if text == zip_code:
                                    break
                        break
                        
            start = 0
            end = 0
            for i, text in enumerate(texts_with_same_path):
                if text == name:
                    start = i
                if text == zip_code:
                    end = i
            
            s = ''.join(texts_with_same_path[start:end+1])
            tokens = s.split(',')
                
            country, zip_code = tokens[-1].split()
            country = tokens[-2] + ', ' + country
            city = tokens[-3]
            tokens = tokens[:-3]
                    
            street_add = ''.join(tokens)
            if not name:
                name = texts_with_same_path[0]
            street_add = street_add.strip().replace(name, '')
        
        return city, country, desc, name, street_add, zip_code
        