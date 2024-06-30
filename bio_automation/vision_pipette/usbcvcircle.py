import cv2
import numpy as np

# Function to preprocess the image
def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise and improve circle detection
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    return blurred

# Function to detect circles in the image
def detect_circles(image):
    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=100)
    return circles

# Function to capture image from the camera and perform circle detection
def capture_and_detect_circles():
    # Open the camera (0 is the default camera, change if using another one)
    cap = cv2.VideoCapture(2)

    #circle counter
    circounter=0 # counts the circle that fit a criteria
    frameidx=0 # keeps track of the number of frames

    # Variables that will be sent to gcode for movemvent
    distance=5
    speed=100
    axis='Y'

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break
        frameidx+=1
        # Preprocess the image
        preprocessed_image = preprocess_image(frame)

        # Detect circles in the preprocessed image
        circles = detect_circles(preprocessed_image)

        # If some circles are detected, print and draw them
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                circounter = circounter+1 if ((r>25)&(r<50)) else 0
                # Draw the circle in the output image
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                # Draw a rectangle corresponding to the center of the circle
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                print(f"Detected circle: center=({x}, {y}), radius={r}")
        if frameidx%10:
            ratio=circounter/10
            if ratio>0.5:
                print("Circle found! Move away!")
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
    capture_and_detect_circles()
