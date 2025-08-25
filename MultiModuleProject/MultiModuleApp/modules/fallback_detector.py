import cv2
import logging

logger = logging.getLogger(__name__)

class SimpleFaceDetector:
    """Fallback face detector using OpenCV Haar Cascades"""
    
    def __init__(self):
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            logger.info("OpenCV face detector initialized")
        except Exception as e:
            logger.error(f"Failed to initialize OpenCV detector: {e}")
            raise
    
    def detect_faces_and_eyes(self, frame):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            results = []
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                
                results.append({
                    'face': (x, y, w, h),
                    'eyes': [(x+ex, y+ey, ew, eh) for (ex, ey, ew, eh) in eyes]
                })
            
            return results
        except Exception as e:
            logger.error(f"Error in face detection: {e}")
            return []
