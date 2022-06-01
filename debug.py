name = 'Debug Mode'
class Mod:
    def __init__(self, room_renderer, save_sys, persistant_save_sys, texture_sys):
        room_renderer.debug = True
    def tick(self, room_renderer, save_sys, persistant_save_sys, texture_sys):
        pass
    def close(self, room_renderer, save_sys, persistant_save_sys, texture_sys):
        pass
