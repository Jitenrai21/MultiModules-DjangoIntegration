const API_URL = "/chat/"; // Django endpoint

window.chatAPI = {
    init: function() {
        console.log("chatAPI.init called");
        // Generate UUID for session
        const sessionId = this.generateUUID();
        console.log("Session ID:", sessionId);

        // Clear initial message and add welcome
        const chatOutput = document.getElementById("chat-output");
        if (chatOutput) {
            chatOutput.innerHTML = this.createWelcomeMessage();
        }

        // Check SpeechRecognition support
        const recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let isListening = false;

        if (!recognition) {
            console.log("SpeechRecognition not supported");
            const micBtn = document.getElementById("mic-btn");
            if (micBtn) {
                micBtn.disabled = true;
                micBtn.title = "Voice input not supported in this browser";
                micBtn.classList.add("opacity-50", "cursor-not-allowed");
            }
            this.showStatus("Voice input is not supported in this browser.", "warning");
        } else {
            const recognizer = new recognition();
            recognizer.interimResults = true;
            recognizer.lang = 'en-US';

            recognizer.onresult = (event) => {
                console.log("SpeechRecognition result received");
                const transcript = Array.from(event.results)
                    .map(result => result[0].transcript)
                    .join('');
                const userInput = document.getElementById("user-input");
                if (userInput) userInput.value = transcript;
                this.showStatus("Listening... (Speak clearly)", "info");
            };

            recognizer.onend = () => {
                console.log("SpeechRecognition ended");
                isListening = false;
                const micBtn = document.getElementById("mic-btn");
                if (micBtn) {
                    micBtn.classList.remove("listening");
                    micBtn.innerHTML = '<i class="fas fa-microphone text-white"></i>';
                }
                this.hideStatus();
                const userInput = document.getElementById("user-input");
                if (userInput && userInput.value.trim()) {
                    this.sendMessage(sessionId, userInput.value.trim());
                }
            };

            recognizer.onerror = (event) => {
                console.log("SpeechRecognition error:", event.error);
                isListening = false;
                const micBtn = document.getElementById("mic-btn");
                if (micBtn) {
                    micBtn.classList.remove("listening");
                    micBtn.innerHTML = '<i class="fas fa-microphone text-white"></i>';
                }
                this.hideStatus();
                this.showStatus(`Voice input error: ${event.error}`, "error");
            };

            const micBtn = document.getElementById("mic-btn");
            if (micBtn) {
                micBtn.addEventListener("click", () => {
                    console.log("Mic button clicked");
                    if (!isListening) {
                        isListening = true;
                        micBtn.classList.add("listening");
                        micBtn.innerHTML = '<i class="fas fa-microphone-alt text-white animate-pulse"></i>';
                        this.showStatus("Listening... (Speak clearly)", "info");
                        recognizer.start();
                    }
                });
            }
        }

        // Check SpeechSynthesis support
        if (!window.speechSynthesis) {
            console.log("SpeechSynthesis not supported");
            const enableSpeech = document.getElementById("enable-speech");
            if (enableSpeech) {
                enableSpeech.disabled = true;
                enableSpeech.parentElement.classList.add("opacity-50");
            }
            this.showStatus("Text-to-speech is not supported in this browser.", "warning");
        }

        // Set up event listeners
        const sendBtn = document.getElementById("send-btn");
        if (sendBtn) {
            sendBtn.addEventListener("click", () => {
                console.log("Send button clicked");
                const userInput = document.getElementById("user-input");
                if (userInput && userInput.value.trim()) {
                    this.sendMessage(sessionId, userInput.value.trim());
                }
            });
        }

        const userInput = document.getElementById("user-input");
        if (userInput) {
            userInput.addEventListener("keypress", (e) => {
                if (e.key === "Enter") {
                    console.log("Enter key pressed");
                    if (userInput.value.trim()) {
                        this.sendMessage(sessionId, userInput.value.trim());
                    }
                }
            });
        }
    },

    generateUUID: function() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    },

    createWelcomeMessage: function() {
        return `
            <div class="flex items-start space-x-3 mb-4">
                <div class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0" style="background: linear-gradient(to bottom right, #3B38A0, #7A85C1);">
                    <i class="fas fa-robot text-white text-sm"></i>
                </div>
                <div class="bg-white/10 rounded-2xl px-4 py-3 max-w-xs">
                    <p class="text-white/90 text-sm">Hello! I'm ready to chat as historical figures. Select a persona above and start the conversation!</p>
                </div>
            </div>
        `;
    },

    sendMessage: function(sessionId, message) {
        console.log("sendMessage called with:", message);
        const persona = document.getElementById("persona")?.value || "Isaac Newton";

        if (!message) {
            this.showStatus("Please enter or speak a message.", "error");
            return;
        }

        this.hideStatus();
        this.appendMessage("User", message, "user-message");
        this.showTypingIndicator();
        this.clearInput();

        const data = {
            session_id: sessionId,
            persona: persona,
            message: message
        };

        fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": this.getCSRFToken()
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            this.hideTypingIndicator();
            this.appendMessage(persona, data.response, "bot-message");
            
            // Text-to-speech if enabled
            const enableSpeech = document.getElementById("enable-speech");
            if (enableSpeech && enableSpeech.checked && window.speechSynthesis) {
                this.speak(data.response);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            this.hideTypingIndicator();
            this.appendMessage("System", "Sorry, I encountered an error. Please try again.", "error-message");
            this.showStatus("Failed to send message. Please check your connection.", "error");
        });
    },

    appendMessage: function(sender, message, className) {
        const chatOutput = document.getElementById("chat-output");
        if (!chatOutput) return;

        const isUser = className === "user-message";
        const timestamp = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        const messageHTML = `
            <div class="flex items-start space-x-3 mb-4 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}">
                <div class="w-8 h-8 ${isUser ? 'rounded-full flex items-center justify-center flex-shrink-0' : 'rounded-full flex items-center justify-center flex-shrink-0'}" style="background: ${isUser ? 'linear-gradient(to bottom right, #7A85C1, #B2B0E8)' : 'linear-gradient(to bottom right, #3B38A0, #7A85C1)'};">
                    <i class="fas ${isUser ? 'fa-user' : 'fa-robot'} text-white text-sm"></i>
                </div>
                <div class="${isUser ? 'rounded-2xl px-4 py-3 max-w-lg' : 'bg-white/10 rounded-2xl px-4 py-3 max-w-lg'} ${className === 'error-message' ? 'bg-red-500/20 border border-red-400/30' : ''}" style="${isUser ? 'background: linear-gradient(135deg, #3B38A0, #7A85C1);' : ''}">>
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-white/70 text-xs font-medium">${sender}</span>
                        <span class="text-white/50 text-xs">${timestamp}</span>
                    </div>
                    <p class="text-white/90 text-sm leading-relaxed">${message}</p>
                </div>
            </div>
        `;

        chatOutput.insertAdjacentHTML('beforeend', messageHTML);
        this.scrollToBottom();
    },

    showTypingIndicator: function() {
        const chatOutput = document.getElementById("chat-output");
        if (!chatOutput) return;

        const typingHTML = `
            <div id="typing-indicator-message" class="flex items-start space-x-3 mb-4">
                <div class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0" style="background: linear-gradient(to bottom right, #3B38A0, #7A85C1);">
                    <i class="fas fa-robot text-white text-sm"></i>
                </div>
                <div class="bg-white/10 rounded-2xl px-4 py-3">
                    <div class="flex space-x-1">
                        <div class="w-2 h-2 rounded-full animate-bounce" style="background-color: rgba(122, 133, 193, 0.6);"></div>
                        <div class="w-2 h-2 rounded-full animate-bounce" style="background-color: rgba(122, 133, 193, 0.6); animation-delay: 0.1s;"></div>
                        <div class="w-2 h-2 rounded-full animate-bounce" style="background-color: rgba(122, 133, 193, 0.6); animation-delay: 0.2s;"></div>
                    </div>
                </div>
            </div>
        `;

        chatOutput.insertAdjacentHTML('beforeend', typingHTML);
        this.scrollToBottom();
    },

    hideTypingIndicator: function() {
        const indicator = document.getElementById("typing-indicator-message");
        if (indicator) {
            indicator.remove();
        }
    },

    speak: function(text) {
        if (window.speechSynthesis) {
            // Stop any current speech
            window.speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9;
            utterance.pitch = 1;
            utterance.volume = 0.8;
            
            // Try to use a more natural voice if available
            const voices = window.speechSynthesis.getVoices();
            const preferredVoice = voices.find(voice => 
                voice.name.includes('Google') || 
                voice.name.includes('Natural') ||
                voice.lang.startsWith('en')
            );
            if (preferredVoice) {
                utterance.voice = preferredVoice;
            }
            
            window.speechSynthesis.speak(utterance);
        }
    },

    clearInput: function() {
        const userInput = document.getElementById("user-input");
        if (userInput) {
            userInput.value = "";
            userInput.focus();
        }
    },

    scrollToBottom: function() {
        const chatContainer = document.querySelector('.chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    },

    showStatus: function(message, type = "info") {
        const statusElements = {
            "error": "error-message",
            "warning": "speech-support", 
            "info": "voice-status"
        };
        
        const elementId = statusElements[type] || "voice-status";
        const statusElement = document.getElementById(elementId);
        
        if (statusElement) {
            const span = statusElement.querySelector('span');
            if (span) {
                span.textContent = message;
            } else {
                statusElement.textContent = message;
            }
            statusElement.classList.remove("hidden");
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                statusElement.classList.add("hidden");
            }, 5000);
        }
    },

    hideStatus: function() {
        const statusIds = ["error-message", "voice-status", "speech-support"];
        statusIds.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.classList.add("hidden");
            }
        });
    },

    getCSRFToken: function() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }
};
