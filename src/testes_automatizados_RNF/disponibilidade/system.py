class Component:
    def __init__(self, name):
        self.name = name
        self.active = False

    def set_active(self, state):
        self.active = state

    def is_active(self):
        return self.active

    def fail(self):
        self.set_active(False)

class System:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def is_service_available(self):
        return any(component.is_active() for component in self.components)
