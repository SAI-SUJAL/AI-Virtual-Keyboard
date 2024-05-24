import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller
import cvzone as cz

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

# Initialize the hand detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Define the layout of the keys
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["Space", "<-"]]

finaltext = ""
keyboard = Controller()

# Define the Button class
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text
        self.hovered = False

def draw_all(img, button_list):
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        cz.cornerRect(img,(x,y,w,h),20,rt=0)
        if button.hovered:  # Check if the button is hovered
            cv2.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), (0, 255, 255), 2)  # Add corner rectangle
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

# Create button instances based on the layout
button_list = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if key == "Space":
            button_list.append(Button([100 * j + 50, 100 * i + 50], key, [300, 85]))  # Larger button for Space
        elif key == "<-":
            button_list.append(Button([100 * j + 350, 100 * i + 50], key, [200, 85]))  # Larger button for Backspace
        else:
            button_list.append(Button([100 * j + 50, 100 * i + 50], key))

# Debounce mechanism to improve accuracy


while True:
    # Read a frame from the camera
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break

    # Find hands in the frame
    hands, img = detector.findHands(img)

    # Draw buttons on the frame
    img = draw_all(img, button_list)

    # Interact with hand landmarks
    if hands:
        for button in button_list:
            x, y = button.pos
            w, h = button.size
            
            if x < hands[0]["lmList"][8][0] < x + w and y < hands[0]["lmList"][8][1] < y + h:
                
                cv2.rectangle(img, button.pos, (x + w, y + h), (128, 0, 128), cv2.FILLED)  # Dark purple color when hovered
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                if len(hands[0]["lmList"]) >= 13:
                    # Convert lists to tuples with two elements
                    p1 = tuple(hands[0]["lmList"][8][:2])  # Thumb tip landmark
                    p2 = tuple(hands[0]["lmList"][12][:2])  # Index finger tip landmark
                    distance = detector.findDistance(p1, p2)
                    # when clicked
                  
                    if distance is not None and distance[0] < 40: 
                        
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)  # Green color when clicked
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        if button.text == "<-":
                            finaltext = finaltext[:-1]  # Remove the last character
                        else:
                            if button.text == "Space":
                                finaltext += " "
                            else:
                                finaltext += button.text
                        sleep(0.3)
            

    cv2.rectangle(img, (50, 600), (1200, 700), (175, 0, 175), cv2.FILLED)  # Dark purple color when hovered
    cv2.putText(img, finaltext, (60, 680), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # Display the frame
    cv2.imshow("Image", img)

    # Check for key press
    key = cv2.waitKey(1)
    if key == 27:  # Escape key
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
