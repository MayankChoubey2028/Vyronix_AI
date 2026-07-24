// ================================
// Backend URL
// ================================

const API = "http://127.0.0.1:8000";

// ================================
// HTML Elements
// ================================

const camera = document.getElementById("camera");
const canvas = document.getElementById("canvas");

const cameraBtn = document.getElementById("cameraBtn");
const captureBtn = document.getElementById("captureBtn");

const sendBtn = document.getElementById("sendBtn");
const question = document.getElementById("question");
const chatBox = document.getElementById("chatBox");

const uploadBtn = document.getElementById("uploadBtn");
const pdfFile = document.getElementById("pdfFile");

const websiteBtn = document.getElementById("websiteBtn");
const websiteUrl = document.getElementById("websiteUrl");

const micBtn = document.getElementById("micBtn");
const voiceStatus = document.getElementById("voiceStatus");

// ================================
// Start Camera (browser preview only)
// ================================

cameraBtn.onclick = async () => {

    try {

        const stream = await navigator.mediaDevices.getUserMedia({
            video: true
        });

        camera.srcObject = stream;

    } catch (err) {

        alert("Camera access denied.");

        console.log(err);

    }

};

// ================================
// Live Vision Polling
// The backend camera runs continuously and updates scene_memory in the
// background - we just poll for the latest result every couple seconds.
// No button click needed anymore.
// ================================

const VISION_POLL_INTERVAL_MS = 2000;

async function pollVisionLive() {

    try {

        const response = await fetch(API + "/vision/live");
        const data = await response.json();

        updateObjects(data.objects);
        updateOCR(data.text && data.text.length > 0 ? data.text : "No text detected.");

    } catch (err) {

        console.log(err);
        updateOCR("Backend not running.");

    }

}

// Start polling as soon as the page loads
setInterval(pollVisionLive, VISION_POLL_INTERVAL_MS);
pollVisionLive();

// Capture button now just freezes a snapshot on the browser preview canvas
// for visual reference - it does not trigger the backend (which is always scanning)
captureBtn.onclick = () => {

    const ctx = canvas.getContext("2d");

    canvas.width = camera.videoWidth;
    canvas.height = camera.videoHeight;

    ctx.drawImage(
        camera,
        0,
        0,
        canvas.width,
        canvas.height
    );

    console.log("Snapshot taken (browser preview only)");

};

// ================================
// Chat
// ================================

sendBtn.onclick = async () => {

    const msg = question.value.trim();

    if (msg === "")
        return;

    addMessage("You", msg);

    question.value = "";

    try {

        const response = await fetch(API + "/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                question: msg

            })

        });

        const data = await response.json();

        addMessage("Vyronix", data.answer);

    }

    catch (err) {

        addMessage("Vyronix", "Backend not running.");

        console.log(err);

    }

};

// ================================
// Upload File
// ================================

uploadBtn.onclick = async () => {

    if (!pdfFile.files.length) {

        alert("Select a file.");

        return;

    }

    const formData = new FormData();

    formData.append(
        "file",
        pdfFile.files[0]
    );

    try {

        const response = await fetch(API + "/upload", {

            method: "POST",

            body: formData

        });

        const data = await response.json();

        alert("Uploaded : " + data.file);

    }

    catch (err) {

        console.log(err);

    }

};

// ================================
// Website Loader
// ================================

websiteBtn.onclick = async () => {

    const url = websiteUrl.value.trim();

    if (url === "")
        return;

    try {

        const response = await fetch(API + "/website", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                url: url

            })

        });

        const data = await response.json();

        alert("Website Added.");

        console.log(data);

    }

    catch (err) {

        console.log(err);

    }

};

// ================================
// Voice Assistant (record -> /voice/ask -> play response)
// ================================

let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;

micBtn.onclick = async () => {

    if (!isRecording) {

        try {

            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = (e) => {
                audioChunks.push(e.data);
            };

            mediaRecorder.onstop = async () => {

                const audioBlob = new Blob(audioChunks, { type: "audio/webm" });

                voiceStatus.textContent = "Processing...";

                await sendVoice(audioBlob);

                voiceStatus.textContent = "Click to Speak";

            };

            mediaRecorder.start();
            isRecording = true;

            voiceStatus.textContent = "Listening... click again to stop";
            micBtn.textContent = "⏹️";

        } catch (err) {

            alert("Microphone access denied.");
            console.log(err);

        }

    } else {

        mediaRecorder.stop();
        isRecording = false;
        micBtn.textContent = "🎤";

    }

};

async function sendVoice(audioBlob) {

    const formData = new FormData();
    formData.append("file", audioBlob, "voice.webm");

    try {

        const response = await fetch(API + "/voice/ask", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            addMessage("Vyronix", data.error);
            return;
        }

        addMessage("You", data.question);
        addMessage("Vyronix", data.answer);

        const audio = new Audio("data:audio/mpeg;base64," + data.audio_base64);
        audio.play();

    } catch (err) {

        addMessage("Vyronix", "Voice request failed.");
        console.log(err);

    }

}

// ================================
// Add Chat Bubble
// ================================

function addMessage(sender, text) {

    const div = document.createElement("div");

    div.className = "message";

    div.innerHTML = `

        <strong>${sender}</strong>

        <p>${text}</p>

    `;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;

}

// ================================
// Press Enter
// ================================

question.addEventListener("keypress", function (e) {

    if (e.key === "Enter") {

        sendBtn.click();

    }

});

// ================================
// Update OCR Panel
// ================================

function updateOCR(text) {

    document.getElementById("ocr").innerHTML = text;

}

// ================================
// Update Object Detection Panel
// ================================

function updateObjects(objects) {

    const panel = document.getElementById("objects");

    panel.innerHTML = "";

    if (!objects || objects.length === 0) {
        panel.innerHTML = `<div class="empty">No objects detected.</div>`;
        return;
    }

    objects.forEach(obj => {

        const item = document.createElement("div");

        item.className = "object";

        item.innerHTML = obj;

        panel.appendChild(item);

    });

}