# Rome Municipality Report Submission System

## Project Overview

This web application was originally designed to allow citizens to submit reports to the Municipality of Rome directly from their mobile devices or computers, without the need for a scanner. It was conceived as a solution to the initial reporting system of the Rome Municipality, which only accepted printed PDF forms that had to be hand-delivered or scanned and emailed after being signed.

Users could fill out a form, add a digital signature, and generate a PDF report that could be previewed before submission, streamlining the process significantly.

**Please note:** As of now, the Municipality of Rome has updated its reporting system, making this web application obsolete for its original purpose. However, this project remains as a demonstration of web-based form submission and PDF generation techniques, and could potentially be adapted for similar use cases in other contexts.

## Features

- User-friendly web form for report submission
- Digital signature capture using a signature pad
- PDF generation with form data and signature
- PDF preview functionality
- Responsive design for both desktop and mobile devices

## Technology Stack

- Backend: Python with Flask framework
- Frontend: HTML, CSS (Bootstrap 5), JavaScript
- PDF Generation: FPDF library
- Form Handling: Flask-WTF
- Signature Capture: Signature Pad library

## Setup and Installation

1. Clone the repository:

   ```
   git clone https://github.com/SusannaKay/segnalazione-comune.git
   cd segnalazione-comune
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:

   ```
   FLASK_APP=main.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   ```

5. Run the application:

   ```
   flask run
   ```

6. Open a web browser and navigate to `http://localhost:5000`

## Usage

1. Fill out the form with the required information.
2. Sign the document using the digital signature pad.
3. Click "Save PDF" to generate the report.
4. Use the "Preview PDF" button to review the document before submission.
5. Submit the report.

## Project Structure

- `main.py`: Main Flask application file
- `forms.py`: Form definitions using Flask-WTF
- `pdf_utils.py`: PDF generation utilities
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript, images)

## Contributing

Contributions to improve the project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- Flask and its extensions developers
- Bootstrap team for the responsive design framework
- Signature Pad library developers
