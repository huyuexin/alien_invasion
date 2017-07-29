import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""

    def __init__(self, ai_settings, screen, ship):
        """在飞船所处位置创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = screen

        # 在 （0，0）处创建一个子弹，并设置位置

        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 存储小数点
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上的子弹"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上画子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
