# Program to extract the Json and tables from the given pdf


from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
import logging
import time

class PDFTableExtractor:
    """
    PDFTableExtractor is responsible for extracting tables from PDF files using the Adobe PDF Services API.
    """

    def __init__(self,base_path):
       
        """
        Initialize the PDFTableExtractor.

        Args:
            base_path (str): Base path of the working directory.
        """
        self.base_path = base_path
    
    
    def extract_table(self,file_path):

        """
        Extracts tables from the specified PDF file.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            str: Path to the extracted zip file containing the extracted tables.

        Raises:
            ServiceApiException: If there is an API error during the extraction process.
            ServiceUsageException: If there is an error in the usage of the Adobe PDF Services API.
            SdkException: If there is a general SDK exception.
        """
        MAX_RETRIES = 3
        RETRY_DELAY = 5  # Seconds between retries

        retries = 0
        while retries < MAX_RETRIES:
            try:
                # Initial setup, create credential instance.
                credentials = Credentials.service_account_credentials_builder() \
                    .from_file(self.base_path + "/pdfservices-api-credentials.json") \
                    .build()

                # Create an ExecutionContext using credentials and create a new operation instance.
                execution_context = ExecutionContext.create(credentials)
                extract_pdf_operation = ExtractPDFOperation.create_new()
                # Set operation input from a source file.
                
                source = FileRef.create_from_local_file(self.base_path + '/input/' +file_path+".pdf")
                extract_pdf_operation.set_input(source)
                
                # Build ExtractPDF options and set them into the operation
                extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
                    .with_element_to_extract(ExtractElementType.TEXT) \
                    .with_element_to_extract(ExtractElementType.TABLES) \
                    .build()
                extract_pdf_operation.set_options(extract_pdf_options)

                # Execute the operation.
                result: FileRef = extract_pdf_operation.execute(execution_context)
                
                # Save the result to the specified location.
                save_path = self.base_path + "/temp_output.zip"
                
                result.save_as(save_path)
                return save_path
            except (ServiceApiException, ServiceUsageException, SdkException):
                logging.exception("Exception encountered while extracting file :"+file_path)
                print("API call timed out. Retrying...")
                retries += 1
                time.sleep(RETRY_DELAY)
        raise Exception("Max retries exceeded. Unable to complete API call.")
