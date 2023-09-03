'''
案例一：奥特曼打小怪兽
author：dong
主要学习的参数：
    1）通过from abc import ABCMeta,abstractmethod 引入抽象类，用来子类的继承和多态
    2）通过__slots__限制类的可引入属性名称
    3）关于属性的安全性，通过@property修饰的setter和getter来进行属性的获取和命名，代替以__开头表示私有属性
    （安全差）：example：
        class Test:
                def __init__(self, foo):
                    self.__foo = foo
                def __bar(self):
                    print(self.__foo)
                    print('__bar')
                def main():
                    test = Test('hello')
                    test._Test__bar()
                    print(test._Test__foo)
                if __name__ == "__main__":
                    main()
    4）静态方法staticmethod和类方法classmethod
设计思路：
'''

# 定义一个抽象类
from abc import ABCMeta, abstractmethod
from random import randint, randrange


class Fighter(object, metaclass=ABCMeta):
    # 限定属性名字,生命，
    __slots__ = ('_name', '_hp')

    def __init__(self, name, hp):
        self._name = name
        self._hp = hp

    @property
    def name(self):
        return self._name

    # 生命直可以修改
    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, hp):
        self._hp = hp if hp >= 0 else 0

    @property
    def alive(self):
        return self._hp

    # 战斗,other是其他
    def fight(self, other):
        pass


# 定义奥特曼继承自Fighter
class Aoteman(Fighter):
    # 生命，魔法
    __slots__ = ('_name', '_hp', '_mp')

    def __init__(self, name, hp, mp):
        super().__init__(name, hp)
        self._mp = mp

    # 重写fight
    def fight(self, other):
        other.hp -= randint(15, 20)

    def huge_fight(self, other):
        if self._mp > 50:
            self._mp -= 50
            injury = other.hp * 3 / 4
            injury = injury if injury > 50 else 50
            other.hp -= injury
            return True
        else:
            self.fight(other)
            return False

    def magic_fight(self, others):
        if self._mp > 20:
            self._mp -= 20
            for i in others:
                if i.alive:
                    i.hp -= randint(10, 20)
            return True

    def resume(self):
        a = randint(10, 20)
        self._mp += a
        return a

    def __str__(self):
        return '~~~%s奥特曼~~~\n' % self._name + \
            '生命值: %d\n' % self._hp + \
            '魔法值: %d\n' % self._mp


class Xiao(Fighter):
    __slots__ = ('_name', '_hp')

    def attack(self, other):
        other.hp -= randint(10, 20)

    def __str__(self):
        return '~~~%s小怪兽~~~\n' % self._name + \
            '生命值: %d\n' % self._hp


def is_any_alive(monsters):
    """判断有没有小怪兽是活着的"""
    for monster in monsters:
        if monster.alive > 0:
            return True
    return False


def select_alive_one(monsters):
    """选中一只活着的小怪兽"""
    monsters_len = len(monsters)
    while True:
        index = randrange(monsters_len)
        monster = monsters[index]
        if monster.alive > 0:
            return monster


def display_info(ultraman, monsters):
    """显示奥特曼和小怪兽的信息"""
    print(ultraman)
    for monster in monsters:
        print(monster, end='')


def main():
    aoteman = Aoteman('aoteman', 1000, 100)
    xiao1 = Xiao('x1', 400)
    xiao2 = Xiao('x2', 400)
    xiao3 = Xiao('x3', 400)
    xiao = [xiao1, xiao2, xiao3]
    fight_round = 1
    while aoteman.alive and is_any_alive(xiao):
        m = select_alive_one(xiao)
        skill = randint(1, 10)
        if skill <= 6:
            print('%s使用普通攻击打了%s.' % (aoteman.name, m.name))
            aoteman.fight(m)
            print('%s的魔法值恢复了%d点.' % (aoteman.name, aoteman.resume()))
        elif skill <= 9:
            print('%s使用普通攻击打了%s.' % (aoteman.name, m.name))
            aoteman.magic_fight(xiao)
            print('%s的魔法值恢复了%d点.' % (aoteman.name, aoteman.resume()))
        else:
            if aoteman.huge_fight(m):
                print('%s使用究极必杀技虐了%s.' % (aoteman.name, m.name))
            else:
                print('%s使用普通攻击打了%s.' % (aoteman.name, m.name))
                print('%s的魔法值恢复了%d点.' % (aoteman.name, aoteman.resume()))

        if m.alive > 0:
            print('%s回击了%s.' % (m.name, aoteman.name))
            m.attack(aoteman)
        display_info(aoteman, xiao)  # 每个回合结束后显示奥特曼和小怪兽的信息
        fight_round += 1

    print('\n========战斗结束!========\n')
    if aoteman.alive > 0:
        print('%s奥特曼胜利!' % aoteman.name)
    else:
        print('小怪兽胜利!')


if __name__ == '__main__':
    main()
