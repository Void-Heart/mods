name = 'Debug Mode'
class Mod:
    def __init__(self, room_renderer, save_sys, persistant_save_sys, texture_sys):
        room_renderer.debug = True
    def tick(self):
        pass
    def close(self):
        pass
