

import hashlib
import os

class DigitalSignature:
    def __init__(self):
        self.private_key = os.urandom(32)

    def sign(self, data):
        return hashlib.sha256((data + str(self.private_key)).encode()).hexdigest()

    def validate(self, signature, data):
        expected_signature = self.sign(data)
        return signature == expected_signature

class IntrusionDetection:
    def detect_intrusion(self, logs):
        alerts = []
        for log in logs:
            if "malicious" in log:
                alerts.append("malicious activity detected")
        return alerts

class System:
    def __init__(self):
        self.activity_log = []

    def simulate_intrusion(self, activity):
        self.activity_log.append(activity)

    def get_activity_log(self):
        return self.activity_log
