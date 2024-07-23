import unittest
from system import System, Transaction, LogAnalyzer

class TestTraceability(unittest.TestCase):

    def setUp(self):
        self.system = System()
        self.log_analyzer = LogAnalyzer()

    def test_log_generation(self):

        transaction1 = Transaction('T1')
        transaction2 = Transaction('T2')
        self.system.execute_transaction(transaction1)
        self.system.execute_transaction(transaction2)
        logs = self.system.get_logs()
        self.assertIn('T1', logs)
        self.assertIn('T2', logs)

    def test_log_analysis(self):

        self.system.generate_log('normal operation')
        self.system.generate_log('anomalous pattern detected')
        alerts = self.log_analyzer.analyze_logs(self.system.get_logs())
        self.assertIn('anomalous pattern detected', alerts)

if __name__ == '__main__':
    unittest.main()