import hashlib
class DigitalSignature:
    def sign(self, data):
        return hashlib.sha256(data.encode()).hexdigest()
    def validate(self, signature):

        return True
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