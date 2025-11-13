"""
Factory Method Pattern - RPG Weapons

>>> # Test Warrior creates Sword
>>> warrior = Warrior("Conan")
>>> weapon = warrior.create_weapon()
>>> weapon.get_name()
'Sword'
>>> weapon.get_damage()
50

>>> # Test Mage creates Staff
>>> mage = Mage("Gandalf")
>>> weapon = mage.create_weapon()
>>> weapon.get_name()
'Staff'
>>> weapon.get_damage()
30

>>> # Test Archer creates Bow
>>> archer = Archer("Legolas")
>>> weapon = archer.create_weapon()
>>> weapon.get_name()
'Bow'
>>> weapon.get_damage()
40

>>> # Test character uses weapon
>>> warrior = Warrior("Conan")
>>> warrior.attack()
'Conan attacks with Sword for 50 damage!'
"""

# %% About
# - Name: Factory Method - RPG Weapons
# - Focus: Factory Method pattern - subclasses decide what to create

# %% Description
"""
Factory Method Pattern - RPG Weapons

Wzorzec Factory Method deleguje tworzenie obiektów do podklas.
Każda klasa postaci (Warrior, Mage, Archer) tworzy swoją unikalną broń.
"""

from abc import ABC, abstractmethod


# %% STEP 1: Product Interface (Weapon) - GOTOWE

class Weapon(ABC):
    """Interfejs broni - używaj tego w swoim rozwiązaniu"""

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_damage(self) -> int:
        pass


# %% STEP 2: Concrete Products (Sword, Staff, Bow) - GOTOWE

class Sword(Weapon):
    """Miecz - broń wojownika"""

    def get_name(self) -> str:
        return "Sword"

    def get_damage(self) -> int:
        return 50


class Staff(Weapon):
    """Laska - broń maga"""

    def get_name(self) -> str:
        return "Staff"

    def get_damage(self) -> int:
        return 30


class Bow(Weapon):
    """Łuk - broń łucznika"""

    def get_name(self) -> str:
        return "Bow"

    def get_damage(self) -> int:
        return 40


# %% STEP 3: Creator (Character) - zawiera Factory Method

# TODO: Zaimplementuj klasę Character (ABC)
# Konstruktor przyjmuje name: str
# Abstrakcyjna metoda create_weapon() -> Weapon (FACTORY METHOD)
# Metoda attack() -> str:
#   - Wywołuje self.create_weapon() aby stworzyć broń
#   - Zwraca: "{name} attacks with {weapon_name} for {damage} damage!"

class Character(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def create_weapon(self): ...

    def attack(self):
        weapon = self.create_weapon()

        return f'{self.name} attacks with {weapon.get_name()} for {weapon.get_damage()} damage!'


# %% STEP 4: Concrete Creators (Warrior, Mage, Archer)

# TODO: Zaimplementuj klasę Warrior
# Dziedziczy po Character
# Nadpisz create_weapon() - zwraca Sword()

class Warrior(Character):
    def create_weapon(self):
        return Sword()


# TODO: Zaimplementuj klasę Mage
# Dziedziczy po Character
# Nadpisz create_weapon() - zwraca Staff()

class Mage(Character):
    def create_weapon(self):
        return Staff()


# TODO: Zaimplementuj klasę Archer
# Dziedziczy po Character
# Nadpisz create_weapon() - zwraca Bow()

class Archer(Character):
    def create_weapon(self):
        return Bow()


# %% Run
# - Terminal: `python -m doctest -f -v starter.py`
# - Tests: `python -m pytest test_factory.py -v`

# %% Example
# Odkomentuj gdy zaimplementujesz:
# if __name__ == "__main__":
#     warrior = Warrior("Conan")
#     print(warrior.attack())
#
#     mage = Mage("Gandalf")
#     print(mage.attack())
