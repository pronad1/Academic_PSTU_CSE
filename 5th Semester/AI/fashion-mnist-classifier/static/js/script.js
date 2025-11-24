document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();
    predictImage();
});

async function predictImage() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];

    if (!file) {
        showError('Please select an image file.');
        return;
    }

    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        showError('File size too large. Please upload an image smaller than 5MB.');
        return;
    }

    showLoading();

    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.error) {
            showError(result.error);
        } else if (result.success) {
            displayResults(result);
        } else {
            showError('Unexpected response from server.');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

async function predictSample() {
    showLoading();

    try {
        const response = await fetch('/sample_prediction', {
            method: 'POST'
        });

        const result = await response.json();

        if (result.error) {
            showError(result.error);
        } else if (result.success) {
            displayResults(result, true);
        } else {
            showError('Unexpected response from server.');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

function showLoading() {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    resultsSection.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Analyzing image...</p>
        </div>
    `;
}

function showError(message) {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    resultsSection.innerHTML = `
        <div class="prediction-card incorrect">
            <h3>❌ Error</h3>
            <p>${message}</p>
            <button onclick="hideResults()" class="close-btn">Close</button>
        </div>
    `;
}

function hideResults() {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'none';
}

function displayResults(result, isSample = false) {
    const resultsSection = document.getElementById('resultsSection');
    const confidencePercent = (result.confidence * 100).toFixed(1);

    let predictionHTML = `
        <div class="prediction-card ${isSample && result.is_correct !== undefined ? (result.is_correct ? 'correct' : 'incorrect') : ''}">
            <h3>🎯 Prediction Result</h3>
    `;

    if (isSample && result.true_label) {
        predictionHTML += `
            <p><strong>Predicted:</strong> ${result.prediction}</p>
            <p><strong>Actual:</strong> ${result.true_label}</p>
            <p class="result-indicator"><strong>Result:</strong> ${result.is_correct ? '✅ Correct' : '❌ Incorrect'}</p>
        `;
    } else {
        predictionHTML += `
            <p><strong>Detected Item:</strong> ${result.prediction}</p>
        `;
    }

    predictionHTML += `</div>`;

    const confidenceHTML = `
        <div class="confidence-meter">
            <h3>📊 Confidence Level</h3>
            <p><strong>${confidencePercent}%</strong> confident</p>
            <div class="meter-bar">
                <div class="meter-fill" style="width: ${confidencePercent}%"></div>
            </div>
            <p class="confidence-note">Confidence: ${confidencePercent >= 80 ? 'High' : confidencePercent >= 60 ? 'Medium' : 'Low'}</p>
        </div>
    `;

    const chartHTML = `
        <div class="probability-chart">
            <h3>📈 Probability Distribution</h3>
            <img src="data:image/png;base64,${result.plot}" alt="Prediction Probabilities" onerror="this.style.display='none'">
        </div>
    `;

    resultsSection.innerHTML = predictionHTML + confidenceHTML + chartHTML;
}

// Drag and drop functionality
const fileInput = document.getElementById('imageInput');
const fileInputLabel = document.querySelector('.file-input-label');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    fileInputLabel.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    fileInputLabel.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    fileInputLabel.addEventListener(eventName, unhighlight, false);
});

function highlight() {
    fileInputLabel.style.background = '#667eea';
    fileInputLabel.style.color = 'white';
    fileInputLabel.style.borderColor = '#5a6fd8';
}

function unhighlight() {
    fileInputLabel.style.background = 'white';
    fileInputLabel.style.color = 'inherit';
    fileInputLabel.style.borderColor = '#667eea';
}

fileInputLabel.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;

    if (files.length > 0) {
        const file = files[0];

        // Check if it's an image file
        if (!file.type.match('image.*')) {
            showError('Please drop an image file.');
            return;
        }

        // Check file size
        if (file.size > 5 * 1024 * 1024) {
            showError('File size too large. Please use an image smaller than 5MB.');
            return;
        }

        fileInput.files = files;
        fileInputLabel.textContent = `📁 ${file.name}`;
        fileInputLabel.classList.add('file-selected');
    }
}

// Update label when file is selected normally
fileInput.addEventListener('change', function () {
    if (this.files.length > 0) {
        const file = this.files[0];
        fileInputLabel.textContent = `📁 ${file.name}`;
        fileInputLabel.classList.add('file-selected');
    } else {
        fileInputLabel.textContent = '📁 Choose Image File';
        fileInputLabel.classList.remove('file-selected');
    }
});

// Check model status on page load
document.addEventListener('DOMContentLoaded', function () {
    checkModelStatus();
});

async function checkModelStatus() {
    try {
        const response = await fetch('/model_status');
        const status = await response.json();

        if (!status.model_loaded) {
            const warning = document.createElement('div');
            warning.className = 'model-warning';
            warning.innerHTML = `
                <div class="warning-content">
                    <span>⚠️ Model not loaded. </span>
                    <a href="javascript:void(0)" onclick="location.reload()">Refresh</a>
                    <span> or train the model first.</span>
                </div>
            `;
            document.querySelector('.container').prepend(warning);
        }
    } catch (error) {
        console.log('Could not check model status:', error);
    }
}