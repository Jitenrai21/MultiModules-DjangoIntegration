let video = document.getElementById('video');
let stream = null;
let captureInterval = null;

document.getElementById('startBtn').addEventListener('click', async () => {
    if (!stream) {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: {
        width: { ideal: 640 },
        height: { ideal: 480 }
    }
});
            video.srcObject = stream;
            console.log("Eye tracking started.");

            // Start capturing and sending frames every 200ms
            captureInterval = setInterval(sendFrameToBackend, 200);

        } catch (err) {
            console.error("Error accessing webcam:", err);
        }
    }
});

document.getElementById('stopBtn').addEventListener('click', () => {
    if (stream) {
        let tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        video.srcObject = null;
        stream = null;
        console.log("Eye tracking stopped.");

        // Stop sending frames
        clearInterval(captureInterval);
        captureInterval = null;
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'x' || e.key === 'X') {
        document.getElementById('stopBtn').click();
    }
});

// Function to capture current video frame and send to backend
function sendFrameToBackend() {
    if (!video || video.readyState < 2) {  // HAVE_CURRENT_DATA
        return;
    }

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageDataURL = canvas.toDataURL('image/jpeg');

    fetch('/process_frame/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: imageDataURL })
    })
    .then(response => response.json())
    .then(data => {
        // Handle wink detection feedback
        if (data.wink) {
            console.log('🎯 WINK DETECTED:', data.wink);
            showWinkFeedback(data.wink);
        }
        
        // Log all response data for debugging
        console.log('Backend response:', data);
    })
    .catch(err => {
        console.error('Error sending frame to backend:', err);
    });
}

// Function to show visual feedback when a wink is detected
function showWinkFeedback(winkType) {
    // Create or update wink indicator
    let winkIndicator = document.getElementById('wink-feedback');
    if (!winkIndicator) {
        winkIndicator = document.createElement('div');
        winkIndicator.id = 'wink-feedback';
        winkIndicator.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #3B38A0, #7A85C1);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: bold;
            z-index: 1000;
            transition: all 0.3s ease;
            opacity: 0;
            transform: translateX(100px);
        `;
        document.body.appendChild(winkIndicator);
    }
    
    // Update content and show
    winkIndicator.innerHTML = `
        <i class="fas fa-eye${winkType === 'left' ? '-slash' : ''}"></i>
        ${winkType.toUpperCase()} WINK DETECTED!
    `;
    winkIndicator.style.opacity = '1';
    winkIndicator.style.transform = 'translateX(0)';
    
    // Hide after 2 seconds
    setTimeout(() => {
        winkIndicator.style.opacity = '0';
        winkIndicator.style.transform = 'translateX(100px)';
    }, 2000);
}