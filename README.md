# Bill Data Extractor

This project is a Bill Data Extractor built for the Adobe challenge. It extracts data from PDF invoices and outputs the extracted data in a CSV file.

## Getting Started

Follow the instructions below to set up and run the Bill Data Extractor.

### Prerequisites

- Python 3.8
- API credentials provided by Adobe Extract

### Installation

1. Create a new environment using Python 3.8.
```shell
conda create --name bill-data-extractor python=3.8
```

2. Activate the newly created environment.
```shell
conda activate bill-data-extractor
```

3. Navigate to the project directory where `main.py` is located.
```shell
cd /path/to/bill-data-extractor
```

4. Install the required libraries using `requirements.txt`.
```shell
python -m pip install -r requirements.txt
```

### Usage

1. Ensure that your current working directory is the same as the location of `main.py`.

2. Place the input PDF files in the `input` folder.

3. Run the following command to start the data extraction process.
```shell
python main.py
```

4. Provide your API credentials when prompted. These credentials should be obtained from Adobe Extract.

5. The extraction process will begin, and once completed, the extracted data will be saved in `output.csv` in the same directory as `main.py`.

### Contact

For any questions, details, or issues, please contact patwarinavin3@gmail.com.

### Acknowledgments

This project was developed as a submission for the Adobe challenge.

**Note**: Remember to handle the API credentials securely and avoid sharing them publicly or committing them to version control systems.
