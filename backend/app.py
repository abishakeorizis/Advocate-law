"""
Advocate Portfolio — Flask Backend
Handles contact form submissions and email notifications.
"""

import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Optional: Flask-Mail config (uncomment when SMTP is configured)
# app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
# app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# In-memory storage for contact submissions (use a database in production)
contact_submissions = []


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Advocate Portfolio API',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/contact', methods=['POST'])
def handle_contact():
    """Process contact form submissions."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'message']
        for field in required_fields:
            if not data.get(field, '').strip():
                return jsonify({'error': f'{field} is required'}), 400

        # Validate email format
        email = data['email'].strip()
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email address'}), 400

        # Create submission record
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

        # Log the submission
        print(f"\n{'='*50}")
        print(f"  NEW CONTACT SUBMISSION")
        print(f"{'='*50}")
        print(f"  Name: {submission['firstName']} {submission['lastName']}")
        print(f"  Email: {submission['email']}")
        print(f"  Phone: {submission['phone'] or 'Not provided'}")
        print(f"  Case Type: {submission['caseType'] or 'Not specified'}")
        print(f"  Message: {submission['message'][:100]}...")
        print(f"  Time: {submission['timestamp']}")
        print(f"{'='*50}\n")

        # TODO: Send email notification using Flask-Mail
        # send_notification_email(submission)

        return jsonify({
            'success': True,
            'message': 'Your message has been received. We will contact you within 24 hours.',
            'id': submission['id']
        }), 200

    except Exception as e:
        print(f"Error processing contact form: {str(e)}")
        return jsonify({'error': 'An internal error occurred. Please try again.'}), 500


@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    """Get all contact submissions (for admin use)."""
    return jsonify({
        'total': len(contact_submissions),
        'submissions': contact_submissions
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    print(f"\n🏛️  Advocate Portfolio API running on http://localhost:{port}")
    print(f"   Health check: http://localhost:{port}/api/health\n")
    app.run(host='0.0.0.0', port=port, debug=debug)
