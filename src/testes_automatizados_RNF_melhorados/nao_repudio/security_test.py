import unittest
from system import System, DigitalSignature, IntrusionDetection

class TestSecurity(unittest.TestCase):

    def setUp(self):
        self.system = System()
        self.digital_signature = DigitalSignature()
        self.intrusion_detection = IntrusionDetection()

    def test_digital_signature(self):

        transaction = 'transaction data'
        signed_transaction = self.digital_signature.sign(transaction)
        self.assertTrue(self.digital_signature.validate(signed_transaction, transaction))

    def test_intrusion_detection(self):

        self.system.simulate_intrusion('malicious activity')
        alerts = self.intrusion_detection.detect_intrusion(self.system.get_activity_log())
        self.assertIn('malicious activity detected', alerts)

if __name__ == '__main__':
    unittest.main()
