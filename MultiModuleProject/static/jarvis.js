// --- Speech Recognition Setup ---
const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition;
if (!SpeechRecognitionAPI) {
    alert("Speech Recognition is not supported in this browser. Please use Chrome on HTTPS or localhost.");
}

const recognition = SpeechRecognitionAPI ? new SpeechRecognitionAPI() : null;
const synth = window.speechSynthesis;
let isListening = false;

if (recognition) {
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
}

// --- Speak Function ---
function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.voice = synth.getVoices().find(voice => voice.lang === 'en-US') || synth.getVoices()[0];
    synth.speak(utterance);
}

// --- UI Update Functions ---
function updateStatus(message) {
    console.log("[STATUS]", message);
    document.getElementById('status').textContent = message;
}

function updateOutput(message) {
    console.log("[OUTPUT]", message);
    document.getElementById('output').textContent = message;
}

// --- Command Processing ---
async function processCommand(command) {
    console.log("[COMMAND RECOGNIZED]", command);
    const response = await fetch('/process_command/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command })
    });
    const data = await response.json();

    updateOutput(`Recognized: ${command}`);
    updateStatus(data.status);
    if (data.speak) speak(data.message);
    if (data.open_url) window.open(data.open_url, '_blank');
    if (data.stop_recognition && recognition) {
        recognition.stop();
        isListening = false;
        updateStatus('Press and hold the spacebar to speak to Jarvis');
    }
}

// --- Recognition Event Handlers ---
if (recognition) {
    recognition.onresult = (event) => {
        const command = event.results[0][0].transcript.toLowerCase();
        isListening = false;
        processCommand(command);
    };

    recognition.onerror = (event) => {
        isListening = false;
        console.error("[RECOGNITION ERROR]", event.error);
        updateStatus('Error in recognition: ' + event.error);
    };

    recognition.onend = () => {
        isListening = false;
        console.log("[RECOGNITION ENDED]");
        updateStatus('Press and hold the spacebar to speak to Jarvis');
    };
}

// --- Spacebar Controls ---
document.addEventListener('keydown', (event) => {
    // Detect spacebar (works across browsers)
    if ((event.code === 'Space' || event.key === ' ') && !isListening && !event.repeat) {
        event.preventDefault();
        console.log("[KEYDOWN] Spacebar pressed");

        if (!recognition) {
            console.warn("Speech Recognition API not available");
            return;
        }

        try {
            recognition.start();
            isListening = true;
            updateStatus('Listening...');
        } catch (err) {
            console.error("Error starting recognition:", err);
            updateStatus("Unable to start recognition. Check console for details.");
        }
    }
});

document.addEventListener('keyup', (event) => {
    if ((event.code === 'Space' || event.key === ' ') && isListening) {
        console.log("[KEYUP] Spacebar released - stopping recognition");
        recognition.stop();
        isListening = false;
        updateStatus('Press and hold the spacebar to speak to Jarvis');
    }
});

// --- Initial Greeting ---
window.onload = async () => {
    console.log("[WINDOW ONLOAD] Initializing...");
    try {
        const response = await fetch('/initialize/');
        const data = await response.json();
        updateStatus(data.status);
        updateOutput(data.message);
        if (data.speak) speak(data.message);
    } catch (err) {
        console.error("Error during initialization:", err);
        updateStatus("Initialization failed. Check console for details.");
    }
};
