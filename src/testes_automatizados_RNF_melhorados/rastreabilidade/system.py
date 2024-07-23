

import datetime

class Transaction:
    def __init__(self, id):
        self.id = id

class LogAnalyzer:
    def analyze_logs(self, logs):
        alerts = []
        for log in logs:
            if "anomalous pattern detected" in log['message']:
                alerts.append(log['message'])
        return alerts

class System:
    def __init__(self):
        self.logs = []

    def execute_transaction(self, transaction):

        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "transaction",
            "message": f"Transaction {transaction.id} executed"
        }
        self.logs.append(log_entry)

    def generate_log(self, message):

        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "system",
            "message": message
        }
        self.logs.append(log_entry)

    def get_logs(self):

        return self.logs
