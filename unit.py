from __future__ import annotations
from abc import ABC
from equipment import Weapon, Armor
from classes import UnitClass
from random import uniform
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name: str = name
        self.unit_class: UnitClass = unit_class
        self.hp: float = unit_class.max_health
        self.stamina: float = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used: bool = False
        self.text_list = [
            ["используя", "пробивает", "соперника и наносит", "урона."],
            ["используя", "наносит удар, но", "cоперника его останавливает"],
            ["попытался использовать", ", но у него не хватило выносливости."]
        ]

    @property
    def health_points(self) -> float:
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon) -> str:
        # присваиваем нашему герою новое оружие
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        # одеваем новую броню
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        self.stamina -= self.weapon.stamina_per_hit
        unit_damage = self.weapon.damage * self.unit_class.attack
        if target.stamina > target.armor.stamina_per_turn:
            target_armor = target.armor.defence * target.unit_class.armor
            target.stamina -= target.armor.stamina_per_turn
        else:
            target_armor = 0

        damage = unit_damage - target_armor
        target.get_damage(damage)
        return damage

    def get_damage(self, damage: int) -> Optional[int]:
        # получение урона целью
        # присваиваем новое значение для аттрибута self.hp
        if damage > 0:
            self.hp -= damage
            return round(damage, 1)
        return None

    def hit(self, target: BaseUnit) -> str:
        """
        этот метод не будет переопределен ниже
        """
        _name: str = self.name
        _weapon_name: str = self.weapon.name
        _target_armor_name: str = target.armor.name
        text_1 = self.text_list[0]
        text_2 = self.text_list[1]
        text_3 = self.text_list[2]

        if self.stamina >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            damage = round(damage, 1)

            if damage > 0:
                return f"{_name} {text_1[0]} {_weapon_name} {text_1[1]}" \
                       f" {_target_armor_name} {text_1[2]} {damage} {text_1[3]}"
            else:
                return f"{_name} {text_2[0]} {_weapon_name} {text_2[1]} {_target_armor_name} {text_2[2]}"
        else:
            return f"{_name} {text_3[0]} {_weapon_name}{text_3[1]}"

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return "Навык использован"
        else:
            if self.unit_class.skill.is_stamina_enough:
                self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)

    def add_stamina(self, stamina_point) -> None:
        stamina_growth = stamina_point * self.unit_class.stamina
        if self.stamina + stamina_growth > self.unit_class.max_stamina:
            self.stamina = self.unit_class.max_stamina
        else:
            self.stamina += stamina_growth


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        self.text_list = [
            ["используя", "пробивает", "соперника и наносит", "урона."],
            ["используя", "наносит удар, но", "cоперника его останавливает"],
            ["попытался использовать", ", но у него не хватило выносливости."]
        ]

        return super().hit(target)


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """

        if uniform(1, 100) in range(1, 10) and not self._is_skill_used:
            return self.use_skill(target)

        self.text_list = [
            ["используя", "пробивает", "и наносит Вам", "урона."],
            ["используя", "наносит удар, но Ваш(а)", "его останавливает."],
            ["попытался использовать", ", но у него не хватило выносливости."]
        ]

        return super().hit(target)
