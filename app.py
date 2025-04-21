import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Simulated deepfake detection function
def detect_deepfake(image_path):
    # This is a placeholder for actual model inference
    # For now, simulate detection with random results
    import random
    is_fake = random.random() > 0.7
    confidence = random.uniform(0.5, 1.0)
    indicators = {
        'Face Consistency': random.choice([True, False]),
        'Texture Analysis': random.choice([True, False]),
        'Color Artifacts': random.choice([True, False]),
        'Blink Pattern': random.choice([True, False]),
    }
    result = {
        'is_fake': is_fake,
        'confidence': round(confidence, 2),
        'indicators': indicators,
        'source': 'AI-Generated (Likely Deepfake)' if is_fake else 'Authentic Image',
        'summary': 'This image shows multiple signs of AI manipulation' if is_fake else 'No significant signs of manipulation detected'
    }
    return result

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        detection_result = detect_deepfake(filepath)
        # Map indicators keys to user expected keys
        indicators_mapped = {
            'face_consistency': detection_result['indicators']['Face Consistency'],
            'texture_analysis': detection_result['indicators']['Texture Analysis'],
            'color_artifacts': detection_result['indicators']['Color Artifacts']
        }
        response = {
            'status': 'success',
            'filename': filename,
            'results': {
                'is_fake': detection_result['is_fake'],
                'confidence': detection_result['confidence'],
                'indicators': indicators_mapped,
                'likely_source': detection_result['source']
            }
        }
        # Optionally delete the file after processing
        os.remove(filepath)
        return jsonify(response)
    else:
        return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
