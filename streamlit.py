import streamlit as st
import pandas as pd
import cv2
import numpy as np
import easyocr

# Path to the CSV file
csv_file_path = r"C:\Users\atul manjhi\Downloads\Desktop\number plate detection\data.csv"
# Function to fetch registration details based on license plate
def fetch_registration_details(plate_text):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)

        # Clean the column names by stripping any leading/trailing spaces
        df.columns = df.columns.str.strip()

        # Check if "Number plate" column exists
        if "Number plate" not in df.columns:
            raise ValueError("'Number plate' column not found in the CSV file.")

        # Convert 'Number plate' to string to avoid matching issues
        df["Number plate"] = df["Number plate"].astype(str)

        # Search for the plate_text in the 'Number plate' column
        result = df.loc[df['Number plate'].str.strip() == plate_text.strip()]
        
        if not result.empty:
            # Return the full row with matching registration details
            return result
        else:
            return None  # No match found
    except Exception as e:
        st.error(f"Error reading CSV file or finding license plate: {e}")
        return None

# Function to detect license plate from an image
def detect_license_plate(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    for (_, text, _) in results:
        if len(text) > 5:  # Filter for license plate-like text
            return text
    return None

# Streamlit app
st.title("License Plate Detection and Information Fetch")

# Upload the image
uploaded_file = st.file_uploader("Upload a license plate image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read and display the uploaded image
    file_bytes = uploaded_file.read()
    image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Save the uploaded image temporarily
    temp_image_path = "temp_license_plate.jpg"
    cv2.imwrite(temp_image_path, image)

    # Detect license plate text
    st.write("Detecting license plate...")
    plate_text = detect_license_plate(temp_image_path)

    if plate_text:
        st.write(f"Detected License Plate: {plate_text}")

        # Fetch registration details
        st.write("Fetching registration details...")
        details = fetch_registration_details(plate_text)

        if details is not None and not details.empty:
            st.write(f"Registration details for License Plate {plate_text}:")
            st.dataframe(details)
        else:
            st.error("No matching registration details found.")
    else:
        st.error("No valid license plate detected.")
