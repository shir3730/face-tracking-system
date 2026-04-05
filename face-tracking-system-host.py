import cv2
import serial
import time


def setup_serial(port='COM6', baudrate=9600, timeout=1):
    try:
        arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        time.sleep(2)  # Wait for Arduino to initialize
        print("[INFO] Successfully connected to Arduino")
        return arduino
    except serial.SerialException as e:
        print(f"[ERROR] Connection to Arduino failed: {e}")
        exit(1)


def setup_camera(camera_index=1):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("[ERROR] Camera not available")
        exit(1)
    print("[INFO] Camera initialized")
    return cap


def detect_and_send_face(frame, face_cascade, arduino):
    # Convert frame to Grayscale to optimize processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        # Find the face with the largest area (width * height) to track the closest person
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        (x, y, w, h) = largest_face

        # Draw a green rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate spatial deviation from the center (offset)
        # 220 is an estimated horizontal center for the frame
        offset = x - 220

        # Transmit the offset data to the target microcontroller via UART
        arduino.write(f"{offset}\n".encode())
        print(f"[SEND] Tracking closest person - Offset: {offset}")

    return frame


def read_from_arduino(arduino):
    # Receive feedback or logs from the Target MCU
    if arduino.in_waiting > 0:
        line = arduino.readline().decode('utf-8').strip()
        print(f"[RECV] Arduino says: {line}")


def main():
    # Initialize Host and Target systems
    arduino = setup_serial()
    cap = setup_camera()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    print("[INFO] Starting Face Detection Pipeline")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Issue reading frame from camera")
            break

        # Process frame and communicate with hardware
        frame = detect_and_send_face(frame, face_cascade, arduino)
        read_from_arduino(arduino)

        # Display the visual feedback
        cv2.imshow('Face Detection - Host Side', frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Resource cleanup
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
    print("[INFO] Program terminated")


if __name__ == "__main__":
    main()
