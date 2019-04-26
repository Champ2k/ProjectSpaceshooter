def check_crash(bullet_x, bullet_y, enemy_x, enemy_y):
    if enemy_x - 26 < bullet_x < enemy_x + 26 and enemy_y - 33 < bullet_y < enemy_y + 33: 
        return True
    else:
        return False