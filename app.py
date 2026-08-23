from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time
import hashlib

app = Flask(__name__)
CORS(app)

organizations = {

    "TF001": {
        "name": "सरकारी सेवा केंद्र",
        "url": "https://example.gov.in",
        "verified": True,
        "risk": "LOW"
    },

    "TF002": {
        "name": "सामुदायिक डिजिटल केंद्र",
        "url": "https://example.org",
        "verified": True,
        "risk": "LOW"
    },

    "FAKE001": {
        "name": "Unknown Service",
        "url": "unknown.example",
        "verified": False,
        "risk": "HIGH"
    }
}

otp_store = {}


@app.route("/")
def home():

    return jsonify({
        "application": "TrustForge",
        "status": "running"
    })


@app.route("/api/check", methods=["POST"])
def check_service():

    data = request.get_json()

    service_id = data.get(
        "serviceId",
        ""
    ).strip()

    service = organizations.get(
        service_id
    )

    if service is None:

        return jsonify({

            "verified": False,

            "risk": "HIGH",

            "message":
            "सावधान। इस सेवा की पहचान प्रमाणित नहीं है।"
        })


    if not service["verified"]:

        return jsonify({

            "verified": False,

            "risk": "HIGH",

            "message":
            "सावधान। यह सेवा प्रमाणित नहीं है।"
        })


    return jsonify({

        "verified": True,

        "risk": service["risk"],

        "name": service["name"],

        "url": service["url"],

        "message":
        "यह प्रमाणित संस्था है। आप सुरक्षित रूप से आगे बढ़ सकते हैं।"
    })


@app.route("/api/send-otp", methods=["POST"])
def send_otp():

    data = request.get_json()

    phone = data.get(
        "phone",
        ""
    ).strip()

    if len(phone) < 10:

        return jsonify({

            "success": False,

            "message":
            "कृपया सही मोबाइल नंबर दर्ज करें।"

        }), 400


    otp = str(
        random.randint(
            100000,
            999999
        )
    )


    otp_store[phone] = {

        "otp": otp,

        "expires":
        time.time() + 300

    }


    # DEMO ONLY
    print(
        "DEMO OTP:",
        otp
    )


    return jsonify({

        "success": True,

        "message":
        "OTP भेज दिया गया है।",

        "demoOtp":
        otp
    })


@app.route("/api/verify-otp", methods=["POST"])
def verify_otp():

    data = request.get_json()

    phone = data.get(
        "phone",
        ""
    ).strip()

    otp = data.get(
        "otp",
        ""
    ).strip()


    record = otp_store.get(
        phone
    )


    if not record:

        return jsonify({

            "verified": False,

            "message":
            "OTP उपलब्ध नहीं है।"
        })


    if time.time() > record["expires"]:

        del otp_store[phone]

        return jsonify({

            "verified": False,

            "message":
            "OTP की समय सीमा समाप्त हो गई।"
        })


    if otp != record["otp"]:

        return jsonify({

            "verified": False,

            "message":
            "OTP गलत है।"
        })


    del otp_store[phone]


    return jsonify({

        "verified": True,

        "message":
        "आपकी पहचान सफलतापूर्वक सत्यापित हो गई।"
    })


@app.route("/api/hash", methods=["POST"])
def create_hash():

    data = request.get_json()

    identity = data.get(
        "identity",
        ""
    )

    salt = data.get(
        "salt",
        ""
    )


    if not identity or not salt:

        return jsonify({

            "error":
            "Identity और salt आवश्यक हैं।"

        }), 400


    value = (
        identity +
        salt
    )


    digest = hashlib.sha256(
        value.encode()
    ).hexdigest()


    return jsonify({

        "hash":
        digest
    })


if __name__ == "__main__":

    print(
        "TrustForge Python Server Started"
    )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )