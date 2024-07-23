import unittest
from system import System, Component

class TestAvailability(unittest.TestCase):

    def setUp(self):
        self.system = System()
        self.primary_component = Component('primary')
        self.secondary_component = Component('secondary')
        self.system.add_component(self.primary_component)
        self.system.add_component(self.secondary_component)
        self.primary_component.set_active(True)
        self.secondary_component.set_active(False)

    def test_redundancy(self):

        self.primary_component.set_active(False)
        self.secondary_component.set_active(True)

        self.assertTrue(self.system.is_service_available())

    def test_automated_failover(self):

        self.primary_component.fail()

        self.assertTrue(self.secondary_component.is_active())
        self.assertTrue(self.system.is_service_available())

if __name__ == '__main__':
    unittest.main()