class Transaction:
    def __init__(self, id):
        self.id = id
class LogAnalyzer:
    def analyze_logs(self, logs):
        alerts = []
        for log in logs:
            if "anomalous pattern" in log:
                alerts.append(log)
        return alerts
class System:
    def __init__(self):
        self.logs = []
    def execute_transaction(self, transaction):

        self.logs.append(f"{transaction.id}")
    def generate_log(self, message):

        self.logs.append(message)
    def get_logs(self):

        return self.logs