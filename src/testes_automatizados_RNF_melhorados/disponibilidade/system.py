

class Component:
    def __init__(self, name, system=None):
        self.name = name
        self.active = False
        self.system = system

    def set_active(self, state):
        self.active = state

    def is_active(self):
        return self.active

    def fail(self):
        self.set_active(False)

        if self.system:
            self.system.activate_next_available_component(self)

class System:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        component.system = self
        self.components.append(component)

    def activate_next_available_component(self, failed_component):
        next_index = self.components.index(failed_component) + 1

        if next_index < len(self.components):
            self.components[next_index].set_active(True)

    def is_service_available(self):
        return any(component.is_active() for component in self.components)

