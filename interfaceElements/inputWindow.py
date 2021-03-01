import pygame


class inputWindow:
    def __init__(self, x, y, width, height, screen, arr, inputs, text='', editable=False):
        self.x = x
        self.y = y
        arr.append(self)
        inputs.append(self)
        self.width = width
        self.height = height
        self.text = text
        self.default_text = 'Введите объект для поиска'
        self.edit = editable
        self.i = 0
        self.active = False
        self.screen = screen
        a = 1
        font = pygame.font.SysFont('calibri', a)
        string = font.render('Test string', True, pygame.Color(255, 255, 255))
        rect = string.get_rect()
        while rect.height < self.height:
            a += 1
            font = pygame.font.SysFont('calibri', a)
            string = font.render('Test string', True, pygame.Color(255, 255, 255))
            rect = string.get_rect()
        a -= 2
        self.font = pygame.font.SysFont('calibri', a)
        string = font.render('D', True, pygame.Color(255, 255, 255))
        self.one_sym = string.get_rect().width
        while self.width % self.one_sym:
            self.width += 1

    def getText(self):
        return self.text

    def checkMouse(self, event):
        x, y = event.pos
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height and self.edit:
            self.active = not self.active
        else:
            self.active = False

    def keyboardButtonPressed(self, event):
        button = event.unicode
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif button:
                self.text += button

    def draw(self):
        x = self.x
        y = self.y

        if self.active:
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (self.x - 3, self.y, self.width + 6,
                              self.height))
            for sym in self.text[-self.width // self.one_sym:]:
                x += self.render(sym, (x, y))
                if x > self.width:
                    self.i += 1
        else:
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (self.x - 3, self.y, self.width + 6,
                              self.height), width=1)
            if self.text:
                for sym in self.text[-self.width // self.one_sym :]:
                    x += self.render(sym, (x, y), (255, 255, 255))
            else:
                for sym in self.default_text[-self.width // self.one_sym - 4:]:
                    x += self.render(sym, (x, y), (255, 255, 255))

    def render(self, sym, coords, color=(0, 0, 0)):
        string = self.font.render(sym, True, pygame.Color(color))
        rect = string.get_rect()
        rect.x = coords[0]
        rect.y = coords[1]
        self.screen.blit(string, rect)
        return rect.width

    def setText(self, text):
        self.text = text
