import time
import logging

logger = logging.getLogger(__name__)

class WinkDetector:
    def __init__(self, blink_threshold=0.25, min_wink_duration=0.3):
        self.blink_threshold = blink_threshold # Threshold for EAR below which the eye is considered closed
        self.min_wink_duration = min_wink_duration # Minimum duration (in seconds) the eye must stay closed to count as a wink
        self.left_eye_closed_since = None
        self.right_eye_closed_since = None
        self.last_detected_wink = None
        self.last_wink_time = 0
        
    def eye_aspect_ratio(self, eye_landmarks, frame_width, frame_height):
        """Calculate Eye Aspect Ratio (EAR) for wink detection"""
        try:
            # Get vertical distances (top and bottom of eye)
            y1 = eye_landmarks[1].y * frame_height  # Top eyelid
            y2 = eye_landmarks[5].y * frame_height  # Bottom eyelid
            y3 = eye_landmarks[2].y * frame_height  # Top eyelid (middle)
            y4 = eye_landmarks[4].y * frame_height  # Bottom eyelid (middle)
            
            # Get horizontal distance (left and right corners)
            x1 = eye_landmarks[0].x * frame_width   # Left corner
            x2 = eye_landmarks[3].x * frame_width   # Right corner
            
            # Calculate vertical distances
            vertical_1 = abs(y1 - y2)
            vertical_2 = abs(y3 - y4)
            
            # Calculate horizontal distance  
            horizontal = abs(x1 - x2)
            
            if horizontal == 0:
                return 0
                
            # EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
            ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
            return ear
            
        except (IndexError, AttributeError) as e:
            logger.warning(f"Error calculating EAR: {e}")
            return 0

    def detect_wink(self, landmarks, frame_width, frame_height):
        """
        Detect winks using Eye Aspect Ratio (EAR)
        MediaPipe face mesh landmark indices for eyes:
        Left eye: [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        Right eye: [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        """
        # More accurate eye landmark indices for MediaPipe face mesh
        LEFT_EYE = [33, 160, 158, 133, 153, 144]    # Key points for left eye EAR calculation
        RIGHT_EYE = [362, 385, 387, 263, 373, 380]  # Key points for right eye EAR calculation

        try:
            # Extract eye landmarks
            left_eye_points = [landmarks[i] for i in LEFT_EYE]
            right_eye_points = [landmarks[i] for i in RIGHT_EYE]
            
            # Calculate Eye Aspect Ratios
            left_ear = self.eye_aspect_ratio(left_eye_points, frame_width, frame_height)
            right_ear = self.eye_aspect_ratio(right_eye_points, frame_width, frame_height)
            
            # Debug logging
            logger.debug(f"Left EAR: {left_ear:.3f}, Right EAR: {right_ear:.3f}, Threshold: {self.blink_threshold}")
            
            now = time.time()
            wink_detected = None
            
            # Prevent too frequent wink detections
            if now - self.last_wink_time < 0.5:  # 500ms cooldown
                return None

            # Check left eye wink (left eye closed, right eye open)
            if left_ear < self.blink_threshold and right_ear >= self.blink_threshold:
                if self.left_eye_closed_since is None:
                    self.left_eye_closed_since = now
                    logger.debug("Left eye closed")
                elif now - self.left_eye_closed_since >= self.min_wink_duration:
                    if self.last_detected_wink != 'left':
                        wink_detected = 'left'
                        self.last_detected_wink = 'left'
                        self.last_wink_time = now
                        logger.info("LEFT WINK DETECTED!")
            else:
                self.left_eye_closed_since = None

            # Check right eye wink (right eye closed, left eye open)
            if right_ear < self.blink_threshold and left_ear >= self.blink_threshold:
                if self.right_eye_closed_since is None:
                    self.right_eye_closed_since = now
                    logger.debug("Right eye closed")
                elif now - self.right_eye_closed_since >= self.min_wink_duration:
                    if self.last_detected_wink != 'right':
                        wink_detected = 'right'
                        self.last_detected_wink = 'right'
                        self.last_wink_time = now
                        logger.info("RIGHT WINK DETECTED!")
            else:
                self.right_eye_closed_since = None

            # Reset last detected wink when both eyes are open
            if left_ear >= self.blink_threshold and right_ear >= self.blink_threshold:
                self.last_detected_wink = None

            return wink_detected
            
        except (IndexError, AttributeError) as e:
            logger.error(f"Error in wink detection: {e}")
            return None
