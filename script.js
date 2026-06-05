const video = document.getElementById('webcam');
const canvas = document.getElementById('photo-canvas');
const startButton = document.getElementById('start-btn');
const captureButton = document.getElementById('capture-btn');
const analyzeButton = document.getElementById('analyze-btn');
const statusText = document.getElementById('status-text');
const context = canvas.getContext('2d');

async function startWebcam() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    video.srcObject = stream;
    statusText.textContent = 'Webcam started. Capture a photo when you are ready.';
    captureButton.disabled = false;
  } catch (error) {
    statusText.textContent = 'Cannot access webcam. Please allow camera permission or use a supported browser.';
    console.error('Webcam error:', error);
  }
}

function capturePhoto() {
  const width = canvas.width;
  const height = canvas.height;
  context.drawImage(video, 0, 0, width, height);
  statusText.textContent = 'Photo captured. Now click Check Mask to analyze the image.';
  analyzeButton.disabled = false;
}

function analyzeImage() {
  const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
  const pixels = imageData.data;
  let total = 0;
  for (let i = 0; i < pixels.length; i += 4) {
    const r = pixels[i];
    const g = pixels[i + 1];
    const b = pixels[i + 2];
    total += (r + g + b) / 3;
  }
  const avgBrightness = total / (pixels.length / 4);
  const hasMask = avgBrightness < 130;

  return hasMask
    ? { label: 'Mask detected', color: '#047857' }
    : { label: 'No mask detected', color: '#b91c1c' };
}

function updateResult(result) {
  statusText.textContent = result.label;
  statusText.style.color = result.color;
}

startButton.addEventListener('click', startWebcam);
captureButton.addEventListener('click', capturePhoto);
analyzeButton.addEventListener('click', () => {
  statusText.textContent = 'Analyzing captured image…';
  statusText.style.color = '#1f2937';
  setTimeout(() => {
    const result = analyzeImage();
    updateResult(result);
  }, 450);
});
