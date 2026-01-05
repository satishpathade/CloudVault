const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const progress = document.getElementById("progress");
const progressBar = document.getElementById("progressBar");
const statusText = document.getElementById("status");
const dropZone = document.getElementById("dropZone");

let selectedFile = null;

// File selection
fileInput.addEventListener("change", () => {
    selectedFile = fileInput.files[0];
    if (selectedFile) {
        fileName.style.display = "block";
        fileName.textContent = selectedFile.name;
    }
});

// Drag & drop
dropZone.addEventListener("dragover", e => {
    e.preventDefault();
    dropZone.style.borderColor = "#38bdf8";
});

dropZone.addEventListener("dragleave", () => {
    dropZone.style.borderColor = "#334155";
});

dropZone.addEventListener("drop", e => {
    e.preventDefault();
    dropZone.style.borderColor = "#334155";
    selectedFile = e.dataTransfer.files[0];
    fileInput.files = e.dataTransfer.files;
    fileName.style.display = "block";
    fileName.textContent = selectedFile.name;
});

async function uploadFile() {
    if (!selectedFile) {
        alert("Please select a file");
        return;
    }

    statusText.style.display = "none";
    progress.style.display = "block";
    progressBar.style.width = "0%";

    // STEP 1: Request presigned URL
    const res = await fetch("/api/uploads/presigned-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            filename: selectedFile.name,
            content_type: selectedFile.type || "application/octet-stream"
        })
    });

    if (!res.ok) {
        const errorText = await res.text();
        showStatus(
            `Backend error ❌
Status: ${res.status}
Response: ${errorText}`,
            false
        );
        return;
    }

    const data = await res.json();

    // STEP 2: Upload to S3 with progress
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", data.uploadUrl, true);
    xhr.setRequestHeader(
        "Content-Type",
        selectedFile.type || "application/octet-stream"
    );

    xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
            const percent = (e.loaded / e.total) * 100;
            progressBar.style.width = percent + "%";
        }
    };

    xhr.onload = () => {
        if (xhr.status === 200) {
            showStatus("Upload completed successfully ✅", true);
        } else {
            showStatus(
                `Upload failed ❌
Status: ${xhr.status}
Response: ${xhr.responseText || "No response from S3"}`,
                false
            );
        }
    };

    xhr.onerror = () => {
        showStatus("Network error ❌ Unable to reach S3", false);
    };

    xhr.send(selectedFile);
}

function showStatus(message, success) {
    statusText.textContent = message;
    statusText.className = "status " + (success ? "success" : "error");
    statusText.style.display = "block";
}
