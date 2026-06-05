# Mask Detection Webpage Requirements

This demo page is designed to let you check whether a person appears to be wearing a mask using a webcam capture interface.

## Functional requirements

- A clean webpage with webcam access.
- Live video feed from the device camera.
- Photo capture button to freeze a frame.
- Analyze button to display a mask / no-mask status.
- Responsive layout for desktop and smaller screens.

## Browser requirements

- Modern browser with `getUserMedia` support.
- Recommended: Google Chrome, Microsoft Edge, Firefox.
- Allow camera permission when prompted.

## Project files

- `index.html` — main user interface.
- `styles.css` — styling for the page.
- `script.js` — webcam control and demo detection logic.
- `requirements.md` — this requirements page.

## Optional integration requirements

For a real mask detection model, add a backend endpoint or integrate an ML model into `script.js`.

Example optional dependencies:

- Python 3.11+ (if you want to serve the page using Flask or another local server)
- Flask: `pip install flask`

## How to run

1. Open `index.html` in your browser.
2. Click **Start Webcam** and allow camera access.
3. Click **Capture Photo**.
4. Click **Check Mask**.

> Note: The current demo uses a simple placeholder image analysis heuristic. Replace the JavaScript detection logic with a trained model for production use.
