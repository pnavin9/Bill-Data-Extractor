# This will return the part of invoice other than those found in 
# the bill table

import json
from zipfile import ZipFile
import re

class InvoiceDetails:

    """
    Extracts invoice details from a JSON file within a zip folder
    """
    
    def __init__(self):
        pass

    @staticmethod
    def invoice_columns(zip_file_path):
        
        """
        Extracts invoice details from a JSON file within a zip folder.

        Args:
            zip_file_path (str): Path to the zip file.

        Returns:
            tuple: A tuple containing the extracted invoice details in the following order:
                - due_date (str): Due date of the invoice.
                - issue_date (str): Issue date of the invoice.
                - invoice_num (str): Invoice number.
                - tax (float): Tax value.
                - invoice_desc (str): Invoice description.
        """

        json_file = 'structuredData.json'

        with ZipFile(zip_file_path, 'r') as zip_ref:
            
            # Extract the JSON file from the zip folder
            zip_ref.extract(json_file)
        
        with open(json_file,'r') as jfile:

            data = json.load(jfile)
            
            # Initializing outputs with None
            due_date = None
            issue_date = None
            invoice_num = None
            tax = None
            total_due = None
            subtotal = None
            vertical_Details = None
            vertical_Invoice = None
            invoice_desc = None
            
            # Iterating through the json file
            for item in data['elements']:

                if item.get('Text') and subtotal == -1 and '$' in item.get('Text'):
                    subtotal = item.get('Text')
                if item.get('Text') and 'Subtotal' in item.get('Text'):
                    subtotal = -1    

                if item.get('Text') and total_due == -1 and '$' in item.get('Text'):
                    total_due = item.get('Text')
                if item.get('Text') and 'Total Due' in item.get('Text'):
                    total_due = -1            
                
                if item.get('Text') and 'Due date' in item.get('Text'):
                    
                    # Search for date format i.e. dd-mm-yyyy in due_date
                    match = re.search(r'\d{2}-\d{2}-\d{4}', item.get('Text'))
                    if match:
                        due_date = match.group()

                # Figuring out Issue_date
                if item.get("Text") and issue_date == -1:
                    
                    # Search for date format i.e. dd-mm-yyyy in Issue
                    match = re.search(r'\d{2}-\d{2}-\d{4}', item.get('Text'))
                    if match:
                        issue_date = match.group()
                

                if item.get("Text") and "Issue date" in item.get("Text"):
                    issue_date = -1
                    match = re.search(r'\d{2}-\d{2}-\d{4}', item.get('Text'))
                    if match:
                        issue_date = match.group()
            
                
                # Seach for Invoice through the text "Invoice" and "Issue Date"
                
                if item.get('Text') and invoice_num == None:
                    match = re.search(r"\b[A-Za-z0-9]{15,}\b", item.get('Text'))
                    if match:
                        invoice_num = match.group()
                        vertical_Invoice = item.get('Bounds')[0]
                
                if item.get("Text") and tax == -1:
                    if '$' not in item.get('Text'):
                        tax = item.get('Text')
                if item.get('Text') and 'Tax' in item.get('Text'):
                    tax = -1
                    match = re.search(r"\d+", item.get("Text"))
                    if match:
                        tax = match.group()
                
                if vertical_Details and item.get('Bounds'):

                    if item.get('Bounds')[0] >= vertical_Details and item.get('Bounds')[0] < vertical_Invoice and item.get('Text'):
                        invoice_desc += item.get('Text')
        
                if item.get('Text') and  'DETAILS' in item.get('Text'):

                    if item.get('Bounds'):
                        vertical_Details = item.get('Bounds')[0]
                        invoice_desc = item.get('Text')


            if tax == None and subtotal and total_due:
                subtotal = int(subtotal.replace('$',"").strip())
                total_due = int(total_due.replace('$',"").strip())
                tax = ((total_due - subtotal)/subtotal)*100  

            invoice_desc = ' '.join([word for word in invoice_desc.split() if not (word.isupper() or word.isdigit())])
            return invoice_desc,due_date, issue_date, invoice_num,tax