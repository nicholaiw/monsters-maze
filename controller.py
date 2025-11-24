from pynput import keyboard


class KeyboardController:
    def __init__(self, bindings):
        self.bindings = bindings
        self.direction = None
        self.listener = keyboard.Listener(on_release=self.getKey)
        self.listener.start()

    def getKey(self, key):
        self.direction = self.bindings.get(key, self.direction)

    def getDirection(self):
        return self.direction
