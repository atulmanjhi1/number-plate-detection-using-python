## License Plate Detection and Information Fetch

This is a Streamlit-based web application that detects license plates from uploaded images and fetches the corresponding registration details from a CSV dataset.

## Features
License Plate Detection: Detects text from license plate images using the easyocr library.
Registration Details Lookup: Fetches the vehicle's registration details (e.g., owner name, vehicle type, color) from a CSV file based on the detected license plate.
User-Friendly Interface: Provides a clean and simple UI to upload images and display results.

## Error Handling: Handles cases where:

License plates are not detected.
License plates are not found in the CSV dataset.
CSV file errors occur.

## Prerequisites
Python 3.8 or above
Streamlit library for building the web app.
Pandas for reading and processing the CSV file.
OpenCV for image processing.
EasyOCR for Optical Character Recognition (OCR).


## Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/license-plate-detection.git
cd license-plate-detection

## Install the required Python libraries:

bash
Copy code
pip install -r requirements.txt
Place your CSV dataset (data.csv) in the correct folder or update the csv_file_path in the code. The dataset should have a structure similar to:

Number plate	Owner Name	Vehicle Type	Color	Registration Date
DE29C7060	John Doe	Sedan	Black	2022-03-15
AB12X3456	Jane Smith	SUV	White	2021-11-10

## Run the application:

bash
Copy code
streamlit run app.py
How It Works

## Upload License Plate Image:

Users can upload an image containing a license plate (formats: .jpg, .jpeg, .png).

## Detect License Plate:

The application uses EasyOCR to extract text from the image and identifies license-plate-like text.

## Fetch Registration Details:

The detected license plate is matched against the Number plate column in the CSV dataset.
If a match is found, the app displays the associated registration details.
