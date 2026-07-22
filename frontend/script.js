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

// ================================
// Start Camera
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
// Capture Frame
// ================================

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

    console.log("Frame Captured");

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
// Placeholder for OCR
// ================================

function updateOCR(text) {

    document.getElementById("ocr").innerHTML = text;

}

// ================================
// Placeholder for Object Detection
// ================================

function updateObjects(objects) {

    const panel = document.getElementById("objects");

    panel.innerHTML = "";

    objects.forEach(obj => {

        const item = document.createElement("div");

        item.className = "object";

        item.innerHTML = obj;

        panel.appendChild(item);

    });

}