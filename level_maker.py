import uuid
name = 'Level Maker'
class Mod:
    def __init__(self, room_renderer, save_sys, persistant_save_sys, texture_sys):
        self.room_renderer = room_renderer
        self.room_renderer.rooms.append('leveleditor')
        self.room_renderer.room_save_blacklist.append('leveleditor')
        self.display = self.room_renderer.display
        self.pygame = room_renderer.pygame
        self.texture_sys = texture_sys
        self.objects_on_screen = []
        self.blacklisted_game_objects = []
        self.game_objects_detailed = [
            ['platform', 'home', 'test_platform'],
            ['switch', 'lvl2', 'switch', 'lvl2', 'switch_pushed'],
            ['player', 'lvl', 'player'],
            ['portal', 'lvl', 'portal']
        ]
        self.game_objects = []
        for object in self.game_objects_detailed:
            self.game_objects.append([self.texture_sys.get_texture(object[1], object[2]), object[0]])
        self.game_objects_not_drawn = []
        for object in self.game_objects:
            self.game_objects_not_drawn.append([object[0].convert_alpha(), object[1]])
        for object in self.game_objects_not_drawn:
            object[0].set_alpha(127)
        self.current_game_object = 2
        self.mouse_pressed_pf = (0, 0, 0)
    def manage_keydowns(self):
        keydowns = self.room_renderer.keydowns_this_frame
        for key in keydowns:
            if key == self.pygame.K_l:
                if self.room_renderer.room == 'leveleditor':
                    self.room_renderer.change_room(self.room_before_level_editor)
                else:
                    self.room_before_level_editor = self.room_renderer.room
                    self.room_renderer.change_room('leveleditor')
    def manage_clicks(self):
        mouse_pressed = self.pygame.mouse.get_pressed()
        mouse_pos = self.room_renderer.get_mouse_pos()
        if mouse_pressed[2] and not self.mouse_pressed_pf[2]:
            if len(self.game_objects)-1 == self.current_game_object:
                self.current_game_object = 0
            else:
                self.current_game_object += 1
        if mouse_pressed[0] and not self.mouse_pressed_pf[0]:
            if not self.current_game_object in self.blacklisted_game_objects:
                self.objects_on_screen.append([self.current_game_object, mouse_pos])
                if self.current_game_object == 2:
                    self.blacklisted_game_objects.append(self.current_game_object)
        self.mouse_pressed_pf = mouse_pressed
    def draw_current_game_object(self):
        self.display.blit(self.game_objects_not_drawn[self.current_game_object][0], self.room_renderer.get_mouse_pos())
    def draw_all_objects(self):
        for object in self.objects_on_screen:
            self.display.blit(self.game_objects[object[0]][0], object[1])
    def tick(self):
        self.manage_keydowns()
        if self.room_renderer.room == 'leveleditor':
            self.manage_clicks()
            self.draw_all_objects()
            self.draw_current_game_object()
    def generate_code(self):
        code_lines = ["self.stop_music('loadsave')"]
        for object in self.objects_on_screen:
            doi = self.game_objects_detailed[object[0]]+[object[1]]
            if doi[0] == 'player':
                code_lines.append("self.reset_player_x = {}".format(doi[3][0]))
                code_lines.append("self.reset_player_y = {}".format(doi[3][1]))
                code_lines.append('self.player()')
            if doi[0] == 'platform':
                code_lines.append('self.platform({}, {}, self.texture_sys.get_texture({}, {}))'.format(doi[3][0], doi[3][1], doi[1], doi[2]))
            if doi[0] == 'switch':
                code_lines.append('self.switch({}, {}, self.texture_sys.get_texture({}, {}), self.texture_sys.get_texture({}, {}), {})'.format(doi[5][0], doi[5][0], doi[1], doi[2], doi[3], doi[4], str(uuid.uuid4())))
            if doi[0] == 'portal':
                code_lines.append("self.portal({}, {}, '(NEXT LEVEL)')".format(doi[3][0], doi[3][1]))
        code_lines = '\n'.join(code_lines)
        return code_lines
    def close(self):
        print('Level Code Generated: ')
        print(self.generate_code())
