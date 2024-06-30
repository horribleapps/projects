import cv2
import pytesseract
import numpy as np
import re

# Function to preprocess image
def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use adaptive thresholding to binarize the image
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    return thresh

# Function to manually set the DPI
def set_dpi(image):
    dpi = 300
    height, width = image.shape[:2]
    image = cv2.resize(image, (width, height))
    return cv2.copyMakeBorder(image, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])

# Function to correct the orientation of the image
def correct_orientation(image):
    try:
        # Get text orientation using pytesseract
        osd = pytesseract.image_to_osd(image)
        #angle = int(re.search('(?<=Rotate: )\d+', osd).group(0))
        angle=180
        if angle == 90:
            rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif angle == 180:
            rotated_image = cv2.rotate(image, cv2.ROTATE_180)
        elif angle == 270:
            rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        else:
            rotated_image = image
        return rotated_image
    except Exception as e:
        print(f"Error during orientation detection: {e}")
        return image

# Function to capture image from the camera and perform OCR
def capture_and_read_text():
    # Open the camera (0 is the default camera, change if using another one)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Preprocess the image
        preprocessed_image = preprocess_image(frame)
        
        # Set DPI manually
        preprocessed_image = set_dpi(preprocessed_image)

        # Correct the orientation of the image
        corrected_image = correct_orientation(preprocessed_image)

        # Use Tesseract to do OCR on the corrected image
        text = pytesseract.image_to_string(corrected_image)

        # Print the detected text if any
        if text.strip():
            print(f"Detected text: {text.strip()}")

        # Display the resulting frame
        cv2.imshow('Camera', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# Run the function
if __name__ == "__main__":
    capture_and_read_text()
