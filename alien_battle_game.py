import random
from playsound import playsound
import threading


# 定义玩家飞船类
class PlayerShip:
    def __init__(self):
        self.health = 100
        self.attack_power = 20
        self.level = 1
        self.weapons = {
            "普通激光": {"min_damage": self.attack_power - 5, "max_damage": self.attack_power + 5},
            "离子炮": {"min_damage": self.attack_power, "max_damage": self.attack_power + 10}
        }
        self.current_weapon = "普通激光"

    def level_up(self):
        self.level += 1
        self.attack_power += 5
        for weapon in self.weapons:
            self.weapons[weapon]["min_damage"] += 5
            self.weapons[weapon]["max_damage"] += 5
        print(f"你升级到了 {self.level} 级，攻击力提升到了 {self.attack_power}！")
        self.play_sound('level_up_sound.wav')

    def change_weapon(self, weapon_name):
        if weapon_name in self.weapons:
            self.current_weapon = weapon_name
            print(f"你切换到了 {self.current_weapon}。")
            self.play_sound('weapon_switch_sound.wav')
        else:
            print("没有这种武器！")

    def attack(self, alien):
        weapon = self.weapons[self.current_weapon]
        damage = random.randint(weapon["min_damage"], weapon["max_damage"])
        alien.health -= damage
        print(f"你使用 {self.current_weapon} 发动了攻击，对外星人造成了 {damage} 点伤害！外星人还剩 {alien.health} 点生命值。")
        self.play_sound('player_attack_sound.wav')
        if alien.health <= 0:
            self.level_up()

    def play_sound(self, sound_file):
        def play():
            try:
                playsound(sound_file)
            except Exception as e:
                print(f"播放音效 {sound_file} 时出错: {e}")
        threading.Thread(target=play).start()


# 定义外星人类
class Alien:
    def __init__(self):
        self.health = 80
        self.attack_power = 15

    def attack(self, player):
        damage = random.randint(self.attack_power - 3, self.attack_power + 3)
        player.health -= damage
        print(f"外星人发动了攻击，对你造成了 {damage} 点伤害！你还剩 {player.health} 点生命值。")
        self.play_sound('alien_attack_sound.wav')

    def play_sound(self, sound_file):
        def play():
            try:
                playsound(sound_file)
            except Exception as e:
                print(f"播放音效 {sound_file} 时出错: {e}")
        threading.Thread(target=play).start()


# 播放背景音乐
def play_background_music():
    def play():
        try:
            playsound('background_music.wav')
        except Exception as e:
            print(f"播放背景音乐时出错: {e}")
    threading.Thread(target=play).start()


# 游戏主循环
def main():
    play_background_music()
    player = PlayerShip()
    alien = Alien()

    print("外星人大战开始！")
    while player.health > 0 and alien.health > 0:
        # 玩家回合
        print("请选择操作：1. 攻击  2. 切换武器")
        choice = input()
        if choice == "1":
            player.attack(alien)
        elif choice == "2":
            print("可用武器：", list(player.weapons.keys()))
            weapon_choice = input("请输入要切换的武器名称：")
            player.change_weapon(weapon_choice)
            continue
        if alien.health <= 0:
            print("你击败了外星人，取得了胜利！")
            break
        # 外星人回合
        alien.attack(player)
        if player.health <= 0:
            print("你被外星人击败了，游戏失败！")
            break


if __name__ == "__main__":
    main()
    