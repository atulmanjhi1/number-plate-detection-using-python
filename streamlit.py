import streamlit as st
import cv2
import numpy as np  # Import numpy
import easyocr
import asyncio
import platform
from playwright.sync_api import sync_playwright


# Set asyncio event loop policy for Windows
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Function to fetch registration details using Playwright
def fetch_registration_details(plate_text):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the website for registration details
        page.goto("https://example-registration-check.com")

        # Input the license plate number
        page.fill("input#plate_number", plate_text)

        # Submit the form
        page.click("button#submit")

        # Wait for the page to load results
        page.wait_for_selector("div#results")

        # Scrape the registration details
        status = page.text_content("div#status")
        details = page.text_content("div#details")

        browser.close()
        return status, details

# Function to detect license plate from image
def detect_license_plate(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    plate_text = ""
    for (bbox, text, prob) in results:
        if len(text) > 5:  # Basic filter for potential license plate
            plate_text = text
            break
    return plate_text

# Streamlit app
st.title("License Plate Detection and Registration Details")

# File uploader
uploaded_file = st.file_uploader("Upload an image of the license plate", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load the uploaded image
    file_bytes = uploaded_file.read()
    image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Save the uploaded image temporarily
    temp_image_path = "temp_license_plate.jpg"
    cv2.imwrite(temp_image_path, image)

    # Detect the license plate
    st.write("Detecting license plate...")
    plate_text = detect_license_plate(temp_image_path)
    st.write(f"Detected Plate: {plate_text}")

    # Fetch registration details
    if plate_text:
        st.write("Fetching registration details...")
        try:
            status, details = fetch_registration_details(plate_text)
            st.write(f"Status: {status}")
            st.write(f"Details: {details}")
        except Exception as e:
            st.error(f"Error fetching details: {e}")
    else:
        st.error("Could not detect a valid license plate.")
