import pygame
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard



def run_game():
    #初始化游戏 创建一个屏幕
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('外星飞船大战')


    play_button =Button(ai_settings,screen,"Play")
    #创建飞船、子弹编组、外星人编组
    stats =GameStats(ai_settings)

    #积分
    sb = Scoreboard(ai_settings,screen,stats)

    ship = Ship(ai_settings, screen)
    #创建存储子弹编组
    bullets = Group()
    aliens = Group()
    gf.creat_fleet(ai_settings,screen,ship,aliens)





    # 开始游戏循环
    while True:
        # 监控键盘和鼠标
        gf.check_events(ai_settings, screen,stats, sb,play_button, ship,aliens,bullets)

        if stats.game_active:

            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)


        #每次循环都重绘屏幕 用背景色填充屏幕#让最近绘制的屏幕可见
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)



run_game()
