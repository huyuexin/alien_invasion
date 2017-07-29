import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from pygame.sprite import Sprite
from scoreboard import Scoreboard
def check_keydown_envents(event,ai_settings,screen,ship,bullets):
    #"""相应按键"""
    if event.key ==pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    #创建子弹 加入编组
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
def check_keyup_events(event,ship):
    #"""松开按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_q:
        sys.exit()
def check_events(ai_settings, screen,stats, sb,play_button, ship,aliens,bullets):
    #"相应键盘鼠标事件"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y =pygame.mouse.get_pos()
            check_play_button(ai_settings, screen,stats, sb,play_button, ship,aliens,bullets,mouse_x,mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_envents(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
def check_play_button(ai_settings, screen,stats,sb, play_button, ship,aliens,bullets,mouse_x,mouse_y):
    #点击开始按钮
    button_clicked =play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏
        ai_settings.initialize_dynamic_settings()
        sb.prep_score()
        sb.prep_high_score
        sb.prep_level()
        sb.prep_ships()



        #隐藏光标
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        aliens.empty()
        bullets.empty()

        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    #"更新屏幕上的图像，并切换到新屏幕"
    screen.fill(ai_settings.bg_color)
    sb.show_score()
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):

    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #删除发生碰撞的外星任和子弹
    collisions =pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score +=ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

    if  len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        #提高登记
        stats.level +=1
        sb.prep_level()

        creat_fleet(ai_settings,screen,ship,aliens)
def check_fleet_edges(ai_settings,aliens):
    #到达边缘的措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_feet_direction(ai_settings,aliens)
            break
def change_feet_direction(ai_settings,aliens):
    #下移 改变方向
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)
def get_number_aliens_x(ai_settings,alien_width):
    #计算可放多少飞机
    available_space_x = ai_settings.screen_width - 2* alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))
    return number_aliens_x
def get_number_row(ai_settings,ship_height,alien_height):
    available_space_y = (ai_settings.screen_height -(3*alien_height)-ship_height)
    number_row =int(available_space_y/(2*alien_height))
    return number_row
def creat_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings, screen)
    # 以上这个只是为了获取宽度而生成的。不是编组成员
    alien_width = alien.rect.width
    alien.x =alien_width+2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height +2 * alien.rect.height * row_number
    aliens.add(alien)
def creat_fleet(ai_settings: object, screen: object, ship: object, aliens: object) -> object:
    #创建外星人群

    alien = Alien(ai_settings, screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_row(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_nunber in range(number_aliens_x):
           creat_alien(ai_settings,screen,aliens,alien_nunber,row_number)
def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
    if stats.ship_left>0:
        stats.ship_left -= 1
        sb.prep_ships()
        #命减一

        aliens.empty()
        bullets.empty()


        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active =False
        pygame.mouse.set_visible(True)
def check_aliens_bottom(ai_settings, stats,sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb,screen, ship, aliens, bullets)
            break
def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


