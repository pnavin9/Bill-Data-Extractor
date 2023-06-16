# Finding customer is simplest of all
# Find the phone number though regular expression
# figure out all the members that have similar path

import json
from zipfile import ZipFile
import re

class Customer:

    """
    Extracts customer details from a JSON file within a zip folder.
    """

    def __init__(self):
        pass

    @staticmethod
    def customer_details (zip_file_path):

        """
        Extracts customer details from a JSON file within a zip folder.

        Args:
            zip_file_path (str): Path to the zip file.

        Returns:
            tuple: A tuple containing the extracted customer details in the following order:
                - add_line1 (str): Address line 1.
                - add_line2 (str): Address line 2.
                - mail (str): Email address.
                - name (str): Customer name.
                - phone_number (str): Phone number.
        """

        # Initializing the values to None
        add_line1 = None
        add_line2 = None
        mail = None
        name = None
        phone_number = None

        
        json_file  = 'structuredData.json'
        with ZipFile(zip_file_path, 'r') as zip_ref:
            
            # Extract the JSON file from the zip folder
            zip_ref.extract(json_file)
        
        with open(json_file, 'r') as file:
            data = json.load(file)
            customer_details = None
            vertical_buisness_desc = None
            for item in data['elements']:
                
                if vertical_buisness_desc and item.get('Bounds'):

                    if item.get('Bounds')[0] == vertical_buisness_desc and item.get('Text'):
                        customer_details += item.get('Text')
        
                if item.get('Text') and 'BILL' in item.get('Text'):

                    if item.get('Bounds'):

                        vertical_buisness_desc = item.get('Bounds')[0]
                        customer_details = ""
                
        
                    
        pattern = r'\d{3}-\d{3}-\d{4}'
        phone_numbers = re.findall(pattern, customer_details)
        if phone_numbers:
            phone_number = phone_numbers[0].strip()

        pattern = r'\S+@\S+'
        emails = re.findall(pattern, customer_details)
        if emails:
            mail = emails[0].strip()

        if mail:
            name_tokens = customer_details.split()
            if mail in name_tokens:
                name = " ".join(name_tokens[:name_tokens.index(mail)])

        if phone_number:
            address_tokens = customer_details.split()
            if phone_number in address_tokens:
                phone_index = address_tokens.index(phone_number)
                add_line1 = " ".join(address_tokens[phone_index + 1: phone_index + 4])
                add_line2 = " ".join(address_tokens[phone_index + 4:])

        if mail and not mail.endswith('com'):
            mail += customer_details.split()[customer_details.split().index(mail)+1]


        return add_line1, add_line2, mail, name, phone_number