import pygame


class pyButton:
    def __init__(self, x, y, text, screen, arr, buttons, width=None, height=None, toggle=False):
        self.handler = None
        self.mouse = 0
        arr.append(self)
        buttons.append(self)
        self.x = x
        self.width = width - 3
        self.height = height - 3
        self.mode = 0
        self.key = None
        self.y = y
        self.toggle = toggle
        if self.toggle:
            self.pressed = False
        self.text = text
        self.screen = screen
        self.font = pygame.font.SysFont('calibri', 26)
        self.string = self.font.render(self.text, True, pygame.Color(255, 255, 255))
        if not width:
            self.width = self.intro_rect.width
        if not height:
            self.height = self.intro_rect.height
        self.intro_rect = self.string.get_rect()
        self.intro_rect.x = self.x + (self.width // 2) - (self.intro_rect.width // 2)
        self.intro_rect.y = self.y + (self.height // 2) - (self.intro_rect.height // 2)
        self.timer = 100000
        self.anim = 0

    def setEventHandler(self, handler):
        self.handler = handler

    def timerCheck(self):
        if self.timer < 15:
            self.timer += 1
            self.anim = 1
            return
        self.anim = 0
        return

    def draw(self):
        self.timerCheck()
        if self.anim == 1:
            pygame.draw.rect(self.screen, (45, 45, 45),
                             (self.x, self.y, self.width, self.height))
            self.string = self.font.render(self.text, True, pygame.Color(0, 0, 0))
            self.screen.blit(self.string, self.intro_rect)
        elif self.toggle and self.mode and self.mouse:
            pygame.draw.rect(self.screen, (120, 120, 120),
                             (self.x, self.y, self.width, self.height))
            self.string = self.font.render(self.text, True, pygame.Color(0, 0, 0))
            self.screen.blit(self.string, self.intro_rect)
        elif self.mouse == 1:
            self.string = self.font.render(self.text, True, pygame.Color(120, 120, 120))
            self.screen.blit(self.string, self.intro_rect)
            pygame.draw.rect(self.screen, (120, 120, 120),
                             (self.x, self.y, self.width, self.height),
                             width=1)
        elif self.mode == 1:
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (self.x, self.y, self.width, self.height))
            self.string = self.font.render(self.text, True, pygame.Color(0, 0, 0))
            self.screen.blit(self.string, self.intro_rect)
        else:
            self.string = self.font.render(self.text, True, pygame.Color(255, 255, 255))
            self.screen.blit(self.string, self.intro_rect)
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (self.x, self.y, self.width, self.height),
                             width=1)

    def checkMouse(self, event):
        x, y = event.pos
        if self.toggle:
            if self.x <= x <= self.x + self.width and self.y <= y <= self.y \
                    + self.height:
                self.mode = (self.mode + 1) % 2
                self.timer = 0
                self.pressed = self.mode
                if self.handler:
                    self.handler(self.pressed)
            return
        else:
            if self.x <= x <= self.x + self.width and self.y<= y <= self.y \
                    + self.height:
                self.timer = 0
                if self.handler:
                    self.handler()

    def checkKeyboard(self, event):
        if self.toggle:
            if event.key == self.key:
                self.mode = (self.mode + 1) % 2
                self.timer = 0
                if self.handler:
                    self.handler(self.pressed)
            return
        else:
            if event.key == self.key:
                self.timer = 0
                if self.handler:
                    self.handler()

    def mouseonButton(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y \
                + self.height:
            self.mouse = 1
        else:
            self.mouse = 0

    def setCheckKey(self, key):
        self.key = key
