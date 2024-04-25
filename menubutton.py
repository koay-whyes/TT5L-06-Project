import pygame

class DrawMenu():
    def __init__(self,x, y, image,scale):
        img_width=image.get_width()
        img_height = image.get_height()
        self.image=pygame.transform.scale(image,(int(img_width* scale),(img_height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked = False
        
    def draw(self,surface):
        action=False
        #mouse position
        pos=pygame.mouse.get_pos()
        #if play button clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked= False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action