"""
Advocate Portfolio — Flask Backend
Handles contact form submissions and serves frontend.
"""

import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ✅ IMPORTANT: Serve frontend files
app = Flask(__name__, static_folder="../", template_folder="../")
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# In-memory storage (use DB in production)
contact_submissions = []


# ===============================
# 🔥 FRONTEND ROUTES (IMPORTANT)
# ===============================

# Serve index.html
@app.route("/")
def serve_home():
    return send_from_directory("../", "index.html")


# Serve static files (css, js, images, sections)
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("../", path)


# ===============================
# 🔥 API ROUTES
# ===============================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'Advocate Portfolio API',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'message']
        for field in required_fields:
            if not data.get(field, '').strip():
                return jsonify({'error': f'{field} is required'}), 400

        # Validate email
        email = data['email'].strip()
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email address'}), 400

        # Create submission
        submission = {
            'id': len(contact_submissions) + 1,
            'firstName': data['firstName'].strip(),
            'lastName': data['lastName'].strip(),
            'email': email,
            'phone': data.get('phone', '').strip(),
            'caseType': data.get('caseType', '').strip(),
            'message': data['message'].strip(),
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'new'
        }

        contact_submissions.append(submission)

        print(f"\n{'='*50}")
        print(f"NEW CONTACT SUBMISSION")
        print(f"{'='*50}")
        print(f"Name: {submission['firstName']} {submission['lastName']}")
        print(f"Email: {submission['email']}")
        print(f"Phone: {submission['phone'] or 'Not provided'}")
        print(f"Case Type: {submission['caseType'] or 'Not specified'}")
        print(f"Message: {submission['message'][:100]}...")
        print(f"Time: {submission['timestamp']}")
        print(f"{'='*50}\n")

        return jsonify({
            'success': True,
            'message': 'Your message has been received. We will contact you within 24 hours.',
            'id': submission['id']
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    return jsonify({
        'total': len(contact_submissions),
        'submissions': contact_submissions
    }), 200


# ===============================
# 🚀 RUN APP (LOCAL ONLY)
# ===============================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
