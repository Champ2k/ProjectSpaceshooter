def check_crash(bullet_x, bullet_y, enemy_x, enemy_y):
    if enemy_x - 26 < bullet_x < enemy_x + 26 and enemy_y - 33 < bullet_y < enemy_y + 33: 
        return True
    else:
        return False

def check_crash_ship(player_x, player_y, enemy_x, enemy_y):
    if enemy_x - 26 < player_x < enemy_x + 26 and enemy_y - 33 < player_y < enemy_y + 33: 
        return True
    else:
        return False

def check_crash_bonus(player_x, player_y, bonus_x, bonus_y):
    if bonus_x - 26 < player_x < bonus_x + 26 and bonus_y - 25 < player_y < bonus_y + 25: 
        return True
    else:
        return False