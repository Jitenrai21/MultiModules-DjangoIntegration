# 🚀 JKR Modules Galore - AI-Powered Multi-Module Application

<div align="center">

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

*A comprehensive Django web application showcasing cutting-edge AI technologies with modern UI/UX design*

[View Demo](#demo) • [Features](#features) • [Installation](#installation) • [Usage](#usage) • [API Reference](#api-reference)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

**JKR Modules Galore** is a sophisticated Django web application that integrates multiple AI-powered modules into a single, cohesive platform. The application features a modern glass-morphism UI design with a beautiful blue/purple color palette, providing users with an intuitive interface to interact with various AI technologies.

### 🎯 Core Modules

1. **🤖 Gemini AI Chat** - Interactive conversations with historical figures
2. **🎙️ Jarvis Voice Assistant** - Voice-controlled AI assistant 
3. **👁️ Real-time Eye Tracker** - Advanced computer vision for gaze tracking and wink detection

---

## ✨ Features

### 🤖 **Gemini AI Chat Module**
- **Historical Figure Personas**: Chat with Einstein, Shakespeare, Gandhi, and more
- **Real-time Conversations**: Powered by Google's Gemini AI
- **Voice Integration**: Speech-to-text input and text-to-speech output
- **Modern Chat UI**: Glass-morphism design with typing indicators
- **Persona Switching**: Seamlessly switch between different historical characters

### 🎙️ **Jarvis Voice Assistant**
- **Voice Activation**: Spacebar or click-to-activate voice recognition
- **Natural Language Processing**: Understand and respond to voice commands
- **Visual Feedback**: Real-time status indicators and listening animations
- **Cross-browser Compatibility**: Works with modern web browsers supporting Speech API
- **Accessibility**: Keyboard shortcuts and visual cues

### 👁️ **Eye Tracking System**
- **Real-time Gaze Detection**: Track eye movement using computer vision
- **Wink Detection**: Advanced algorithms to detect eye winks
- **Cursor Control**: Move mouse cursor with eye gaze (experimental)
- **Live Video Feed**: Real-time camera processing with overlay indicators
- **Computer Vision**: Powered by OpenCV and MediaPipe technologies

### 🎨 **Modern UI/UX Design**
- **Glass Morphism**: Frosted glass aesthetic with backdrop blur effects
- **Responsive Design**: Mobile-first approach using Tailwind CSS
- **Blue/Purple Theme**: Cohesive color palette across all modules
- **Smooth Animations**: CSS transitions and JavaScript-powered interactions
- **Accessibility**: WCAG compliant with focus states and keyboard navigation

---

## 🎥 Demo

### Screenshots

| Home Page | Chat Interface | Voice Assistant |
|-----------|----------------|-----------------|
| ![Home](docs/screenshots/home.png) | ![Chat](docs/screenshots/chat.png) | ![Voice](docs/screenshots/jarvis.png) |

| Eye Tracker | Mobile View | Glass Effects |
|-------------|-------------|---------------|
| ![Tracker](docs/screenshots/tracker.png) | ![Mobile](docs/screenshots/mobile.png) | ![Glass](docs/screenshots/glass.png) |

---

## 🛠️ Technology Stack

### Backend
- **Django 5.2.4** - Python web framework
- **Python 3.x** - Core programming language
- **Google Generative AI** - Gemini AI integration
- **OpenCV** - Computer vision processing
- **MediaPipe** - Face and eye detection
- **PyAutoGUI** - System automation

### Frontend
- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first CSS framework
- **JavaScript ES6+** - Modern JavaScript features
- **FontAwesome** - Icon library
- **Web Speech API** - Voice recognition and synthesis

### Development Tools
- **SQLite** - Development database
- **CORS Headers** - Cross-origin resource sharing
- **Environment Variables** - Configuration management
- **Static Files** - Asset management

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)
- Webcam (for eye tracking module)
- Microphone (for voice assistant)

### 1. Clone the Repository

```bash
git clone https://github.com/Jitenrai21/MultiModules-DjangoIntegration.git
cd MultiModules-DjangoIntegration
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Google Gemini AI API Key
GOOGLE_API_KEY=your_gemini_api_key_here

# Django Secret Key
SECRET_KEY=your_django_secret_key_here

# Debug Mode (set to False in production)
DEBUG=True

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup

```bash
cd MultiModuleProject
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

---

## ⚙️ Configuration

### Google Gemini AI Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the API key to your `.env` file:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

### Camera Permissions

For the eye tracking module to work properly:
- Grant camera permissions to your browser
- Ensure good lighting conditions
- Position camera at eye level for best results

### Voice Assistant Setup

For optimal voice assistant performance:
- Grant microphone permissions
- Use Chrome or Edge for best compatibility
- Ensure stable internet connection for speech recognition

---

## 🎯 Usage

### 🏠 **Home Page**
- Navigate through different AI modules
- View feature highlights and statistics
- Access quick links to each module

### 💬 **Chat Module (`/chat/`)**
1. Select a historical figure persona
2. Type your message or use voice input
3. Receive AI-generated responses in character
4. Switch personas for different conversation styles

### 🎙️ **Voice Assistant (`/jarvis/`)**
1. Press and hold spacebar or click the microphone button
2. Speak your command clearly
3. Release to process and receive response
4. View conversation history in real-time

### 👁️ **Eye Tracker (`/tracker/`)**
1. Click "Start Tracking" to begin
2. Allow camera permissions when prompted
3. Look around to see gaze detection in action
4. Wink to trigger click events (experimental)
5. Click "Stop Tracking" to end session

---

## 🔌 API Reference

### Chat API Endpoint

```http
POST /chat/
Content-Type: application/json

{
    "message": "Hello, Einstein!",
    "persona": "einstein",
    "session_id": "unique_session_id"
}
```

**Response:**
```json
{
    "response": "Hello! I'm delighted to discuss the mysteries of the universe with you.",
    "persona": "einstein",
    "timestamp": "2025-08-24T10:30:00Z"
}
```

### Voice Assistant Integration

The voice assistant uses the Web Speech API for:
- **Speech Recognition**: Convert speech to text
- **Speech Synthesis**: Convert text to speech
- **Real-time Processing**: Live audio processing

### Eye Tracking Data

```javascript
// Eye tracking events
window.addEventListener('gazeUpdate', (event) => {
    const { x, y, confidence } = event.detail;
    // Handle gaze coordinates
});

window.addEventListener('winkDetected', (event) => {
    const { eye, timestamp } = event.detail;
    // Handle wink events
});
```

---

## 📁 Project Structure

```
MultiModules-DjangoIntegration/
├── 📁 MultiModuleProject/           # Django project root
│   ├── 📁 MultiModuleApp/           # Main Django app
│   │   ├── 📁 modules/              # AI module implementations
│   │   │   ├── 📄 app.py           # Main application logic
│   │   │   ├── 📄 controller.py    # System control functions
│   │   │   ├── 📄 detector.py      # Face/eye detection
│   │   │   ├── 📄 gaze_tracker.py  # Gaze tracking algorithms
│   │   │   └── 📄 wink_detector.py # Wink detection logic
│   │   ├── 📁 migrations/          # Database migrations
│   │   ├── 📄 admin.py            # Django admin configuration
│   │   ├── 📄 apps.py             # App configuration
│   │   ├── 📄 models.py           # Database models
│   │   ├── 📄 urls.py             # URL routing
│   │   └── 📄 views.py            # View functions
│   ├── 📁 MultiModuleProject/       # Django project settings
│   │   ├── 📄 settings.py         # Project settings
│   │   ├── 📄 urls.py             # Main URL configuration
│   │   └── 📄 wsgi.py             # WSGI configuration
│   ├── 📁 static/                   # Static assets
│   │   ├── 📁 css/                 # Stylesheets
│   │   │   └── 📄 style.css       # Main styles
│   │   ├── 📁 images/              # Image assets
│   │   ├── 📄 chat.js             # Chat functionality
│   │   ├── 📄 chat-enhanced.js    # Enhanced chat features
│   │   ├── 📄 jarvis.js           # Voice assistant logic
│   │   ├── 📄 main.js             # Main JavaScript
│   │   └── 📄 script.js           # Additional scripts
│   ├── 📁 templates/               # HTML templates
│   │   └── 📁 MultiModuleApp/      # App templates
│   │       ├── 📄 base.html       # Base template
│   │       ├── 📄 chat.html       # Chat interface
│   │       ├── 📄 index.html      # Home page
│   │       ├── 📄 jarvis.html     # Voice assistant
│   │       └── 📄 tracker.html    # Eye tracking
│   ├── 📄 db.sqlite3              # SQLite database
│   └── 📄 manage.py               # Django management script
├── 📁 env/                         # Virtual environment
├── 📄 .env                        # Environment variables
├── 📄 .gitignore                  # Git ignore rules
├── 📄 README.md                   # Project documentation
└── 📄 requirements.txt            # Python dependencies
```

---

## 🎨 UI/UX Design System

### Color Palette
```css
:root {
    --primary-dark: #1A2A80;      /* Deep blue */
    --primary-medium: #3B38A0;    /* Medium blue */
    --primary-light: #7A85C1;     /* Light blue */
    --primary-lightest: #B2B0E8;  /* Pale blue */
}
```

### Glass Morphism Effects
- **Backdrop Blur**: `backdrop-filter: blur(20px)`
- **Transparency**: `background: rgba(255, 255, 255, 0.1)`
- **Border**: `border: 1px solid rgba(255, 255, 255, 0.2)`
- **Shadow**: `box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.25)`

### Typography
- **Primary Font**: System fonts (sans-serif)
- **Icon Library**: FontAwesome 6.0+
- **Responsive Text**: Tailwind CSS responsive utilities

---

## 🤝 Contributing

We welcome contributions to improve JKR Modules Galore! Here's how you can help:

### Getting Started
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Test all AI modules before submitting
- Update documentation for new features
- Ensure responsive design compatibility

### Areas for Contribution
- 🔧 **Performance Optimization**: Improve AI processing speed
- 🎨 **UI Enhancements**: New themes and animations  
- 🤖 **AI Features**: Additional chat personas or voice commands
- 👁️ **Computer Vision**: Enhanced eye tracking accuracy
- 📱 **Mobile Experience**: Improved mobile responsiveness
- 🧪 **Testing**: Unit tests and integration tests
- 📚 **Documentation**: Tutorials and API docs

---

## 🔒 Security Considerations

### API Key Management
- Store API keys in environment variables
- Never commit sensitive data to version control
- Use different keys for development and production

### CORS Configuration
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]
```

### Camera/Microphone Permissions
- Request permissions appropriately
- Handle permission denials gracefully
- Provide clear privacy information to users

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use production database (PostgreSQL recommended)
- [ ] Set up static file serving
- [ ] Configure HTTPS
- [ ] Set up environment variables
- [ ] Test all modules in production environment

### Recommended Hosting Platforms
- **Heroku**: Easy Django deployment
- **DigitalOcean**: VPS hosting
- **AWS**: Scalable cloud hosting
- **Vercel**: Frontend deployment (static files)

---

## 🐛 Troubleshooting

### Common Issues

#### Camera Not Working
```bash
# Check camera permissions in browser settings
# Ensure HTTPS in production (required for camera access)
# Test with different browsers
```

#### Voice Recognition Fails
```bash
# Verify microphone permissions
# Check internet connection (required for speech-to-text)
# Try different browsers (Chrome/Edge recommended)
```

#### Gemini AI Errors
```bash
# Verify API key is correctly set
# Check API quota and billing
# Ensure stable internet connection
```

#### Styling Issues
```bash
# Clear browser cache
# Check if static files are loading correctly
# Verify Tailwind CSS is included
```

---

## 📊 Performance Metrics

### Optimization Targets
- **Page Load Time**: < 2 seconds
- **Voice Recognition Latency**: < 1 second  
- **AI Response Time**: < 3 seconds
- **Eye Tracking FPS**: 30+ fps
- **Mobile Performance**: 90+ Lighthouse score

### Monitoring
- Use Django Debug Toolbar for development
- Implement logging for production errors
- Monitor API usage and quotas
- Track user interaction metrics

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 JKR Modules Galore

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgments

### Technologies & Libraries
- [Django](https://djangoproject.com/) - The web framework for perfectionists with deadlines
- [Google Gemini AI](https://ai.google.dev/) - Advanced AI language model
- [OpenCV](https://opencv.org/) - Open Source Computer Vision Library
- [Tailwind CSS](https://tailwindcss.com/) - A utility-first CSS framework
- [FontAwesome](https://fontawesome.com/) - The internet's icon library

### Inspiration
- Modern glass-morphism design trends
- AI-powered web applications
- Computer vision accessibility tools
- Voice-controlled interfaces

### Contributors
- **Jitenrai21** - Lead Developer & Project Creator
- Community contributors and testers

---

## 📞 Support & Contact

### Get Help
- 📧 **Email**: [your-email@example.com](mailto:your-email@example.com)
- 💬 **GitHub Issues**: [Report a bug or request a feature](https://github.com/Jitenrai21/MultiModules-DjangoIntegration/issues)
- 📖 **Documentation**: [Wiki & Guides](https://github.com/Jitenrai21/MultiModules-DjangoIntegration/wiki)

### Community
- ⭐ **Star this repository** if you find it helpful
- 🍴 **Fork and contribute** to make it even better
- 📢 **Share** with fellow developers and AI enthusiasts

---

<div align="center">

**Made with ❤️ using Django and AI Technologies**

*JKR Modules Galore - Where AI meets beautiful design*

[⬆️ Back to Top](#-jkr-modules-galore---ai-powered-multi-module-application)

</div>
