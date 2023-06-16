import logging
import os.path
import pandas as pd
import re
from tqdm import tqdm


from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation

from src.extract import PDFTableExtractor
from src.invoice_table import InvoiceTable
from src.invoice_details import InvoiceDetails
from src.customer import Customer
from src.business import Business

# Configure logging
logging.basicConfig(level=os.environ.get("LOGLEVEL"))


class InvoiceProcessor:
    """
    InvoiceProcessor is responsible for processing invoice PDF files,
    extracting information, and merging the data into a CSV file.
    """

    def __init__(self, base_path, input_folder_path, output_path):
        """
        Initialize InvoiceProcessor.

        Args:
            base_path (str): Base path of the working directory.
            input_folder_path (str): Path to the folder containing input PDF files.
            output_path (str): Path to the output CSV file.
        """
        self.base_path = base_path
        self.input_folder_path = input_folder_path
        self.output_path = output_path
        self.pdfTableExtractor = PDFTableExtractor(base_path=self.base_path)

    def process_invoices(self):
        """
        Process the invoices in the input folder, extract information,
        and merge the data into a CSV file.
        """
        # Get a list of PDF files in the input folder and sort them
        input_files = [file for file in os.listdir(self.input_folder_path) if file.endswith('.pdf')]
        input_files = sorted(input_files, key=lambda x: (int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else x[:-4], x))

        # Initialize merged DataFrame
        merged_data = pd.DataFrame()

        # Process each input file
        for file in tqdm(input_files, desc="Processing invoices", unit="file"):
            # Check the extension of the file
            if file.endswith('.pdf'):
                file = file.split('.')[0]  # Extract file name without extension
                try:
                    
                    # Extract the PDF as JSON along with the tables
                    zip_file_path = self.pdfTableExtractor.extract_table(file)

                    df = pd.DataFrame()
                    
                    # Extract the invoice information from tables
                    df = InvoiceTable.create_database(zip_file_path) # Name, Qty, rate

                    # Extract business details and assign to columns
                    df[['Bussiness__City', 'Bussiness__Country', 'Bussiness__Description', 'Bussiness__Name', 'Bussiness__StreetAddress', 'Bussiness__Zipcode']] = Business.business_details(zip_file_path)

                    # Extract customer details and assign to columns
                    df[['Customer__Address__line1', 'Customer__Address__line2', 'Customer__Email', 'Customer__Name', 'Customer__PhoneNumber']] = Customer.customer_details(zip_file_path)

                    # Extract invoice details and assign to columns
                    df[['Invoice__Description', 'Invoice__DueDate', 'Invoice__IssueDate', 'Invoice__Number', 'Invoice__Tax']] = InvoiceDetails.invoice_columns(zip_file_path)
                    
                    #df['file_name'] = file

                    # Rearrange the columns
                    df = df[['Bussiness__City', 'Bussiness__Country', 'Bussiness__Description', 'Bussiness__Name',
                             'Bussiness__StreetAddress', 'Bussiness__Zipcode', 'Customer__Address__line1',
                             'Customer__Address__line2', 'Customer__Email', 'Customer__Name', 'Customer__PhoneNumber',
                             'Invoice__BillDetails__Name','Invoice__BillDetails__Quantity','Invoice__BillDetails__Rate',
                             'Invoice__Description', 'Invoice__DueDate', 'Invoice__IssueDate', 'Invoice__Number',
                             'Invoice__Tax']]
                    
                    # Append the DataFrame to the final DataFrame
                    merged_data = pd.concat([merged_data, df], ignore_index=True)
                    
                    # Remove the temporary zip file
                    os.remove(zip_file_path)
                except Exception as e:
                    print("############## ERROR IN", file, "###################")
                    logging.error(str(e))

        # Save the merged DataFrame to CSV
        merged_data.to_csv(self.output_path, index=False)


# Get the current working directory
base_path = os.getcwd()

# Define input and output paths
input_folder_path = os.path.join(base_path, 'input')
output_path = os.path.join(base_path, 'output.csv')

# Create an instance of InvoiceProcessor
processor = InvoiceProcessor(base_path, input_folder_path, output_path)

# Process the invoices and generate the merged CSV
processor.process_invoices()
