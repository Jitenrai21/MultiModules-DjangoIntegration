from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import base64
import cv2
import numpy as np
from MultiModuleApp.modules import detector, controller, gaze_tracker, wink_detector
import pyjokes
import datetime
import pyautogui
import google.generativeai as genai
import os
from dotenv import load_dotenv
from MultiModuleApp.services.llm_service import llm_service, LLMServiceError

# Load environment variables
load_dotenv()

# Configure Gemini API (kept for fallback)
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

# In-memory session store for chat
chat_sessions = {}

# Available personas
persona_options = {
    "Isaac Newton": "Mathematician and physicist",
    "Marie Curie": "Pioneering scientist in radioactivity",
    "William Shakespeare": "English playwright and poet",
    "Adam Smith": "Father of modern economics",
    "Alan Turing": "Father of computer science"
}

# Static state to track if Jarvis is activated (shared across requests)
class JarvisState:
    is_jarvis_activated = False

def home(request):
    return render(request, 'MultiModuleApp/index.html')

def tracker_page(request):
    """
    Renders the main tracker.html page.
    This is what the user sees when they first navigate to the URL.
    """
    return render(request, 'MultiModuleApp/tracker.html')

# Global instances to maintain state across requests
wink_detector_instance = None
face_detector_instance = None

def get_face_detector():
    global face_detector_instance
    if face_detector_instance is None:
        face_detector_instance = detector.FaceLandmarkDetector()
    return face_detector_instance

def get_wink_detector():
    global wink_detector_instance
    if wink_detector_instance is None:
        # More sensitive settings for better wink detection
        wink_detector_instance = wink_detector.WinkDetector(
            blink_threshold=0.25,  # Increased from 0.2 for easier detection
            min_wink_duration=0.3  # Reduced from 1.0 seconds for faster response
        )
    return wink_detector_instance

@csrf_exempt
def process_frame(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    try:
        data = json.loads(request.body)
        print("📸 Frame processing request received")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return HttpResponseBadRequest('Invalid JSON')

    if 'image' not in data:
        print("❌ No image in request data")
        return JsonResponse({'error': 'No image received'}, status=400)

    try:
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        frame = cv2.flip(frame, 1)

        frame_height, frame_width = frame.shape[:2]
        print(f'📏 Frame dimensions - Height:{frame_height}, Width: {frame_width}')

        face_landmark_detector_instance = get_face_detector()
        landmarks = face_landmark_detector_instance.detect_landmarks(frame)
        print(f"👤 Landmarks detected: {len(landmarks) if landmarks else 0}")
        
        response = {
            'gaze': None,
            'wink': None
        }
        SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
        cursor_instance = controller.CursorController(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        if landmarks:
            print("✅ Processing landmarks...")
            gazeTrackerInstance = gaze_tracker.GazeTracker()
            gaze, left_iris, right_iris = gazeTrackerInstance.estimate_gaze(landmarks, frame_width, frame_height)
            if gaze and left_iris and right_iris:
                iris_x_norm = (left_iris[0] + right_iris[0]) / 2 / frame_width
                iris_y_norm = (left_iris[1] + right_iris[1]) / 2 / frame_height
                cursor_instance.move_cursor_to_iris(iris_x_norm, iris_y_norm)
                response['gaze'] = gaze
                print(f"👁️ Gaze processed: {gaze}")
                
            wink_instance = get_wink_detector()
            wink = wink_instance.detect_wink(landmarks, frame_width, frame_height)
            if wink:
                print(f"😉 Wink detected: {wink}")  # Debug logging
                cursor_instance.click_if_wink(wink)
                response['wink'] = wink
            else:
                response['wink'] = None
        else:
            print("❌ No landmarks detected")

        print(f"🔄 Sending response: {response}")
        return JsonResponse(response)
        
    except Exception as e:
        print(f"💥 Error processing frame: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

def voice_assistant_page(request):
    """
    Renders the main tracker.html page.
    This is what the user sees when they first navigate to the URL.
    """
    return render(request, 'MultiModuleApp/jarvis.html')

@csrf_exempt
def initialize(request):
    JarvisState.is_jarvis_activated = False
    return JsonResponse({
        "message": "Hello, I am Jarvis AI, your voice-commanded virtual assistant.",
        "speak": True,
        "open_url": None,
        "stop_recognition": False,
        "status": "Press and hold the spacebar to speak to Jarvis"
    })

@csrf_exempt
def process_command(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    try:
        data = json.loads(request.body)
        command = data.get("command", "").lower()
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    response = {
        "message": "I didn't understand that command.",
        "speak": True,
        "open_url": None,
        "stop_recognition": False,
        "status": "Press and hold the spacebar to speak to Jarvis"
    }

    if not JarvisState.is_jarvis_activated:
        if "jarvis" in command:
            JarvisState.is_jarvis_activated = True
            response["message"] = "I am ready for your command."
            response["status"] = "I am ready for your command."
        else:
            response["message"] = "Activate by calling me by my name Jarvis."
            response["status"] = "Press and hold the spacebar to speak to Jarvis"
        return JsonResponse(response)

    # Process commands when activated
    sites = [
        {"name": "youtube", "url": "https://www.youtube.com/"},
        {"name": "chat gpt", "url": "https://chatgpt.com/"},
        {"name": "github account", "url": "https://github.com/Jitenrai21"}
    ]
    for site in sites:
        if f"open {site['name']}" in command:
            response["message"] = f"Opening {site['name']}"
            response["open_url"] = site["url"]
            return JsonResponse(response)

    if "how are you" in command:
        response["message"] = "I am doing great, How are you?"
    elif "hello" in command:
        response["message"] = "Hello there. How can I help you today?"
    elif "soul mate" in command:
        response["message"] = "I believe her name is Inez."
    elif "your name" in command:
        response["message"] = "It's so silly for you to ask again. My name is Jarvis."
    elif "old are you" in command:
        response["message"] = "I have been created quite a while ago. By Jiten Rai, of course!"
    elif "time now" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        response["message"] = f"The time is {time}"
    elif "swift" in command:
        response["message"] = "Opening Swift video"
        response["open_url"] = "https://www.youtube.com/watch?v=X_e5z_XrlzY&list=PLe9t8KT-SdWXaS4thPTG66mazDoJ2-BJq&index=3"
    elif "joke" in command:
        response["message"] = pyjokes.get_joke(language="en", category="all")
    elif "exit" in command:
        JarvisState.is_jarvis_activated = False
        response["message"] = "I am always at your service. Come again."
        response["stop_recognition"] = True
        response["status"] = "Press and hold the spacebar to speak to Jarvis"

    return JsonResponse(response)

def chatbot(request):
    """
    Renders the chatbot page (index.html from FastAPI).
    """
    return render(request, 'MultiModuleApp/chat.html')

@csrf_exempt
def chat(request):
    """
    Handles chat requests, integrating with Ollama (primary) and Gemini (fallback).
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        persona = data.get('persona')
        message = data.get('message')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not all([session_id, persona, message]):
        return JsonResponse({'error': 'Missing session_id, persona, or message'}, status=400)

    if persona not in persona_options:
        return JsonResponse({'error': 'Invalid persona'}, status=400)

    # Initialize or update session
    if session_id not in chat_sessions:
        chat_sessions[session_id] = {
            "persona": persona,
            "chat_history": []
        }

    # Reset session if persona changed
    if chat_sessions[session_id]["persona"] != persona:
        chat_sessions[session_id]["persona"] = persona
        chat_sessions[session_id]["chat_history"] = []
        # Clear LLM service session as well
        llm_service.clear_session(session_id)

    print(f"Session ID: {session_id}")
    print(f"Chat History: {chat_sessions[session_id]['chat_history']}")
    print(f"Persona: {chat_sessions[session_id]['persona']}")

    try:
        # Load prompt template
        with open('prompt_template.txt', 'r', encoding="utf-8") as file:
            prompt_template = file.read().strip()
    except FileNotFoundError:
        return JsonResponse({'error': 'Prompt template not found'}, status=500)

    # Build the persona-specific prompt
    persona_instruction = prompt_template.format(
        persona_name=persona,
        persona_description=persona_options[persona]
    )
    
    # Combine persona instruction with user message
    full_prompt = persona_instruction + "\n\nUser: " + message

    try:
        # Use the new LLM service with session management
        response_text = llm_service.generate_response(
            prompt=full_prompt,
            session_id=session_id,
            temperature=0.7,
            max_tokens=2000
        )
        
        # Update chat history
        chat_sessions[session_id]["chat_history"].append(("User", message))
        chat_sessions[session_id]["chat_history"].append((persona, response_text))
        
        # Get provider status for debugging
        provider_status = llm_service.get_provider_status()
        print(f"LLM Provider Status: {provider_status}")
        
        return JsonResponse({
            'response': response_text,
            'provider_info': {
                'providers': provider_status,
                'primary': 'ollama'
            }
        })
        
    except LLMServiceError as e:
        # Log the error and return user-friendly message
        print(f"LLM Service Error: {str(e)}")
        return JsonResponse({
            'error': f'AI service temporarily unavailable: {str(e)}',
            'provider_info': llm_service.get_provider_status()
        }, status=503)
    except Exception as e:
        print(f"Unexpected error in chat: {str(e)}")
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

@csrf_exempt
def health_check(request):
    """
    Health check endpoint for monitoring and load balancers
    """
    try:
        # Check LLM service status
        provider_status = llm_service.get_provider_status()
        
        # Basic health info
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'providers': provider_status,
            'services': {
                'django': True,
                'ollama': provider_status.get('ollama', {}).get('available', False),
                'gemini_fallback': provider_status.get('gemini', {}).get('available', False)
            }
        }
        
        # Determine overall health
        if provider_status.get('ollama', {}).get('available', False):
            health_data['primary_llm'] = 'ollama'
        elif provider_status.get('gemini', {}).get('available', False):
            health_data['primary_llm'] = 'gemini'
        else:
            health_data['status'] = 'degraded'
            health_data['primary_llm'] = 'none'
        
        status_code = 200 if health_data['status'] == 'healthy' else 503
        return JsonResponse(health_data, status=status_code)
        
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        }, status=503)