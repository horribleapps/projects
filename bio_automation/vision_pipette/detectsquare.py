import cv2
import numpy as np

def is_square(approx):
    """Check if the contour is a square based on the approximation."""
    if len(approx) == 4:  # Square has 4 sides
        # Check if all angles are ~90 degrees
        (x, y, w, h) = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        return 0.9 <= aspect_ratio <= 1.1
    return False

def detect_squares(frame):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise and improve edge detection
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    
    # Apply edge detection
    edges = cv2.Canny(blurred_frame, 50, 150)
    
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if is_square(approx):
            # Draw the detected square on the frame
            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)
    
    return frame

# Open a connection to the USB camera (usually camera 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    # Detect squares in the frame
    frame_with_squares = detect_squares(frame)

    # Display the resulting frame
    cv2.imshow('Frame', frame_with_squares)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
