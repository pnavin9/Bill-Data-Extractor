# This file is to extract the information of invoice from the givenBill
# ExtractTable class is to extract the bill table in the pdf

from zipfile import ZipFile
import pandas as pd
class InvoiceTable:

    """
    Extracts the table data from an Excel file within a zip folder.
    """

    def __init__(self):
        pass
    
    @staticmethod
    def create_database(zip_file_path):

        """
        Extracts the table data from an Excel file within a zip folder.

        Args:
            zip_file_path (str): Path to the zip file.

        Returns:
            pandas.DataFrame: A DataFrame containing the extracted table data.
        """

        data_file, header_file = None, None

        with ZipFile(zip_file_path,'r') as zf:
            
            # Fetch all the files in the zip folder
            file_names = sorted(zf.namelist())
            
            for file_name in file_names:
                
                # Extract the Files to make a dataframe
                if file_name.endswith('.xlsx'):
                    zf.extract(file_name)
                    df = pd.read_excel(file_name)
                    num_columns = df.shape[1]
                    
                    # Four columns suggest the right tables to extract
                    if num_columns == 4 :
                        if header_file == None:
                            header_file = file_name
                        else:
                            data_file = file_name
                            break
            if header_file is None or data_file is None:
                raise ValueError("Failed to load header or data table")
            
            # File consisting of headers
            table_header = zf.extract(header_file)
            
            # File consisting of data
            excel_file = zf.extract(data_file)
        
        
        columns = pd.read_excel(table_header, header=None).replace(to_replace=r'_x000D_', value='', regex=True)
        
        # Creating a dataframe
        df = pd.read_excel(excel_file,header = None)
        columns = list(columns.iloc[0,:])
        
        # Setting up the dataframe
        df.columns = columns
        df = df.replace(to_replace=r'_x000D_', value='', regex=True)

        # Drop the Amount Column
        df = df.drop(df.columns[-1], axis=1)

        # Rename table columns
        new_column_names = {'ITEM ':'Invoice__BillDetails__Name','QTY ':'Invoice__BillDetails__Quantity','RATE ':'Invoice__BillDetails__Rate'}
        df = df.rename(columns= new_column_names)
        return df

