from flask import Flask, request, jsonify
import requests
import re
import json
from uuid import uuid4
import datetime

app = Flask(__name__)

# Constants
STATUS_1 = 'STATUS~1'
STATUS_2 = 'STATUS~2'
STATUS_3 = 'STATUS~3'
W = 'XMLHttpRequest'
V = '936619743392459'
U = 'same-origin'
T = 'cors'
S = 'empty'
R = '*/*'
Q = 'x-requested-with'
P = 'x-ig-www-claim'
O = 'x-ig-app-id'
N = 'sec-fetch-site'
M = 'sec-fetch-mode'
L = 'sec-fetch-dest'
K = 'referer'
J = 'accept-language'
I = 'accept'
H = 'email_or_username'
F = 'csrftoken'
G = 'User-Agent'

def method_x(email_or_username):
    """First method for password reset"""
    url = 'https://www.instagram.com/accounts/account_recovery_send_ajax/'
    headers = {
        G: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.instagram.com/accounts/password/reset/',
        'X-CSRFToken': F
    }
    data = {
        H: email_or_username,
        'recaptcha_challenge_field': ''
    }
    try:
        response = requests.post(url, headers=headers, data=data, timeout=30)
        return response
    except requests.exceptions.RequestException as e:
        return type('Response', (), {'status_code': 500, 'text': str(e)})()

def extract_email(response_text):
    """Extract email from response text"""
    match = re.search('<b>(.*?)</b>', response_text)
    if match:
        return match.group(1)
    else:
        return 'Unknown'

def method_z(username):
    """Second method for password reset"""
    try:
        username = username.split('@gmail.com')[0]
    except:
        pass
    
    # Get user ID
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        I: R,
        'accept-encoding': 'gzip',
        J: 'en-US;q=0.9,en;q=0.7',
        K: f"https://www.instagram.com/{username}",
        L: S,
        M: T,
        N: U,
        O: V,
        P: '0',
        Q: W
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response_json = response.json()
        
        try:
            user_id = response_json['data']['user']['id']
        except:
            return {
                "status": STATUS_2,
                "success": False,
                "message": f"FAILED TO SEND THE PASSWORD RESET TO @{username}",
                "error": "Could not get user ID"
            }
        
        # Send password reset
        url = 'https://i.instagram.com/api/v1/accounts/send_password_reset/'
        headers = {
            G: 'Instagram 6.12.1 Android (30/11; 480dpi; 1080x2004; HONOR; ANY-LX2; HNANY-Q1; qcom; ar_EG_#u-nu-arab)',
            'Cookie': 'mid=YwsgcAABAAGsRwCKCbYCaUO5xej3; csrftoken=u6c8M4zaneeZBfR5scLVY43lYSIoUhxL',
            'Cookie2': '$Version=1',
            'Accept-Language': 'ar-EG, en-US',
            'X-IG-Connection-Type': 'MOBILE(LTE)',
            'X-IG-Capabilities': 'AQ==',
            'Accept-Encoding': 'gzip'
        }
        data = {
            'user_id': user_id,
            'device_id': str(uuid4())
        }
        
        response = requests.post(url, headers=headers, data=data, timeout=30)
        response_json = response.json()
        
        try:
            obfuscated_email = response_json['obfuscated_email']
            return {
                "status": STATUS_2,
                "success": True,
                "message": f"PASSWORD RESET LINK SENT TO @{username}",
                "obfuscated_email": obfuscated_email
            }
        except:
            return {
                "status": STATUS_2,
                "success": False,
                "message": f"FAILED TO SEND THE PASSWORD RESET TO @{username}"
            }
    except Exception as e:
        return {
            "status": STATUS_2,
            "success": False,
            "message": f"FAILED TO SEND THE PASSWORD RESET TO @{username}",
            "error": str(e)
        }

def method_a(username_or_email):
    """Third method for password reset"""
    csrf_token = 'umwHlWf6r3AGDowkZQb47m'
    url = 'https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/'
    
    cookies = {
        F: csrf_token,
        'datr': '_D1dZ0DhNw8dpOJHN-59ONZI',
        'ig_did': 'C0CBB4B6-FF17-4C4A-BB83-F3879B996720',
        'mid': 'Z109_AALAAGxFePISIe2H_ZcGwTD',
        'wd': '1157x959'
    }
    
    headers = {
        I: R,
        J: 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'priority': 'u=1, i',
        K: 'https://www.instagram.com/accounts/password/reset/?source=fxcal&hl=en',
        'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-full-version-list': '"Brave";v="131.0.0.0", "Chromium";v="131.0.0.0", "Not_A Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        L: S,
        M: T,
        N: U,
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-asbd-id': '129477',
        'x-csrftoken': csrf_token,
        O: V,
        P: '0',
        'x-instagram-ajax': '1018880011',
        Q: W,
        'x-web-session-id': 'ag36cv:1ko17s:9bxl9b'
    }
    
    data = {
        H: username_or_email,
        'flow': 'fxcal'
    }
    
    try:
        response = requests.post(url, cookies=cookies, headers=headers, data=data, timeout=30)
        response_json = response.json()
        
        if response_json.get('status') == 'fail':
            if response_json.get('error_type') == 'rate_limit_error':
                return {
                    "status": STATUS_3,
                    "success": False,
                    "message": "TRY USING VPN. IP LIMITED.",
                    "error_type": "rate_limit"
                }
            elif 'message' in response_json and isinstance(response_json['message'], list):
                return {
                    "status": STATUS_3,
                    "success": False,
                    "message": "Check the username or email again.",
                    "error_type": "invalid_username"
                }
            else:
                return {
                    "status": STATUS_3,
                    "success": False,
                    "message": f"An error occurred: {response_json.get('message', 'Unknown error')}",
                    "error_type": "general_error"
                }
        elif response_json.get('status') == 'ok':
            return {
                "status": STATUS_3,
                "success": True,
                "message": f"Message: {response_json.get('message', 'No message provided')}"
            }
        else:
            return {
                "status": STATUS_3,
                "success": False,
                "message": f"Unexpected response: {response_json}"
            }
    except json.JSONDecodeError:
        return {
            "status": STATUS_3,
            "success": False,
            "message": "Failed to parse the response as JSON.",
            "error_type": "json_decode_error"
        }
    except Exception as e:
        return {
            "status": STATUS_3,
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}",
            "error_type": "unexpected_error"
        }

@app.route('/api/reset-password', methods=['GET'])
def reset_password():
    """API endpoint to send Instagram password reset - GET method"""
    username = request.args.get('username')
    
    if not username:
        return jsonify({
            "success": False,
            "error": "Missing 'username' query parameter",
            "usage": "GET /api/reset-password?username=instagram_username_or_email"
        }), 400
    
    # Execute all three methods
    results = {}
    
    # Method X
    try:
        response_x = method_x(username)
        if response_x.status_code == 200:
            email = extract_email(response_x.text)
            results['method_x'] = {
                "status": STATUS_1,
                "success": True,
                "message": f"PASSWORD RESET LINK SENT TO @{username} TO {email}",
                "obfuscated_email": email
            }
        else:
            results['method_x'] = {
                "status": STATUS_1,
                "success": False,
                "message": f"FAILED TO SEND THE PASSWORD RESET TO @{username}",
                "status_code": response_x.status_code
            }
    except Exception as e:
        results['method_x'] = {
            "status": STATUS_1,
            "success": False,
            "message": f"FAILED TO SEND THE PASSWORD RESET TO @{username}",
            "error": str(e)
        }
    
    # Method Z
    results['method_z'] = method_z(username)
    
    # Method A
    results['method_a'] = method_a(username)
    
    # Check if any method was successful
    overall_success = any(method['success'] for method in results.values())
    
    return jsonify({
        "success": overall_success,
        "username": username,
        "methods": results,
        "timestamp": str(datetime.datetime.now())
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Instagram Password Reset API",
        "timestamp": str(datetime.datetime.now())
    })

@app.route('/api/methods', methods=['GET'])
def available_methods():
    """Get information about available methods"""
    return jsonify({
        "methods": {
            "method_x": "First password reset method using account recovery endpoint",
            "method_z": "Second method using user ID lookup and mobile API",
            "method_a": "Third method using web API with cookies"
        },
        "usage": "GET /api/reset-password?username=instagram_username_or_email"
    })

@app.route('/')
def index():
    """Root endpoint with API information"""
    return jsonify({
        "message": "Instagram Password Reset API",
        "version": "1.0",
        "endpoints": {
            "GET /api/reset-password": "Send password reset to Instagram account",
            "GET /api/health": "Health check",
            "GET /api/methods": "Get information about available methods"
        },
        "usage": {
            "reset-password": "GET /api/reset-password?username=instagram_username_or_email"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
