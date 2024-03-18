import cv2
import dlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance as dist
import requests
from PIL import Image
from io import BytesIO

#Load the dlib face detector and the facial landmarks predictor, shape_predictor_68_face_landmarks.dat file should be in same repo
#https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat
detector = dlib.get_frontal_face_detector()
predictor_path = 'shape_predictor_68_face_landmarks.dat'
predictor = dlib.shape_predictor(predictor_path)

#Load the image from thispersondoesnotexist
url = 'https://thispersondoesnotexist.com/'
response = requests.get(url)
img = Image.open(BytesIO(response.content))
im = np.array(img)

#Convert to grayscale for better readabitity
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

#Detect faces in the image
faces = detector(gray, 1)

#Define functions to calculate EAR and MAR
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[13], mouth[19])
    B = dist.euclidean(mouth[14], mouth[18])
    C = dist.euclidean(mouth[15], mouth[17])
    D = dist.euclidean(mouth[12], mouth[16])
    mar = (A + B + C) / (3.0 * D)
    return mar

#Go through each detected face
for (i, rect) in enumerate(faces):
    # Get the landmarks/parts for the face in rect.
    shape = predictor(gray, rect)
    shape_np = np.array([[p.x, p.y] for p in shape.parts()])

    #Draw the face landmarks with a mesh
    for (x, y) in shape_np:
        cv2.circle(im, (x, y), 1, (0, 255, 0), -1)  # Green dots
    
    #Connect the dots with lines to form the mesh
    mesh_indices = [
        list(range(0, 17)),  # Jaw line
        list(range(17, 22)),  # Left eyebrow
        list(range(22, 27)),  # Right eyebrow
        list(range(27, 31)),  # Nose bridge
        list(range(31, 36)),  # Lower nose
        list(range(36, 42)) + [36],  # Left eye, closing the loop
        list(range(42, 48)) + [42],  # Right eye, closing the loop
        list(range(48, 60)) + [48],  # Outer lip, closing the loop
        list(range(60, 68)) + [60]   # Inner lip, closing the loop
    ]
    for idx_group in mesh_indices:
        points = np.array([shape_np[idx] for idx in idx_group], dtype=np.int32)
        cv2.polylines(im, [points], isClosed=False, color=(0, 255, 0), thickness=1)
    
    #Eye level and distance checks
    left_eye_pts = shape_np[36:42]
    right_eye_pts = shape_np[42:48]
    left_eye_center = left_eye_pts.mean(axis=0).astype(int)
    right_eye_center = right_eye_pts.mean(axis=0).astype(int)
    # Draw line between the eye centers
    cv2.line(im, tuple(left_eye_center), tuple(right_eye_center), (255, 0, 0), 1)  
    
    eye_distance = dist.euclidean(left_eye_center, right_eye_center)
    print(f"Distance between the eyes: {eye_distance:.2f}")
    
    eye_level_diff = abs(left_eye_center[1] - right_eye_center[1])
    print(f"Difference in eye level: {eye_level_diff}")
    
    # Calculate EAR and MAR
    leftEAR = eye_aspect_ratio(left_eye_pts)
    rightEAR = eye_aspect_ratio(right_eye_pts)
    ear = (leftEAR + rightEAR) / 2.0
    mouth_pts = shape_np[48:68]  # Outer and inner lip
    mar = mouth_aspect_ratio(mouth_pts)
    
    print("Eye Aspect Ratio (EAR): {:.2f}".format(ear))
    print("Mouth Aspect Ratio (MAR): {:.2f}".format(mar))

    break  # Process only the first face

#Convert to RGB for matplotlib and display the image
image_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
plt.imshow(image_rgb)
plt.axis('off')
plt.title('Facial Landmarks with Mesh')
plt.show()
