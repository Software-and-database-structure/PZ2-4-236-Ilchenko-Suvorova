from abc import ABC, abstractmethod
import json
from typing import Dict, List, Optional, Any

class BoundedStat:
    """Дескриптор для валидации характеристик"""
    def __init__(self, min_val: int = 0, max_val: int = 100):
        self.min_val = min_val
        self.max_val = max_val
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, self.min_val)
    
    def __set__(self, instance, value):
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"{self.name} must be between {self.min_val} and {self.max_val}")
        instance.__dict__[self.name] = value

class Human:
    """Базовый класс для всех персонажей"""
    _hp = BoundedStat(0, 1000)
    _mp = BoundedStat(0, 500)
    _strength = BoundedStat(1, 100)
    _agility = BoundedStat(1, 100)
    _intelligence = BoundedStat(1, 100)
    
    def __init__(self, name: str, level: int = 1):
        self.name = name
        self.level = level
        self._hp = 100
        self._mp = 50
        self._strength = 10
        self._agility = 10
        self._intelligence = 10
        self.max_hp = 100
        self.max_mp = 50
        self.effects: List['Effect'] = []
    
    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, value: int):
        self._hp = max(0, min(value, self.max_hp))
    
    @property
    def mp(self) -> int:
        return self._mp
    
    @mp.setter
    def mp(self, value: int):
        self._mp = max(0, min(value, self.max_mp))
    
    @property
    def strength(self) -> int:
        return self._strength
    
    @strength.setter
    def strength(self, value: int):
        self._strength = value
    
    @property
    def agility(self) -> int:
        return self._agility
    
    @agility.setter
    def agility(self, value: int):
        self._agility = value
    
    @property
    def intelligence(self) -> int:
        return self._intelligence
    
    @intelligence.setter
    def intelligence(self, value: int):
        self._intelligence = value
    
    @property
    def is_alive(self) -> bool:
        return self.hp > 0
    
    def __str__(self) -> str:
        return f"{self.name} (Lvl {self.level}) - HP: {self.hp}/{self.max_hp}, MP: {self.mp}/{self.max_mp}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}', level={self.level})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Сериализация в словарь"""
        return {
            'class_name': self.__class__.__name__,
            'name': self.name,
            'level': self.level,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'mp': self.mp,
            'max_mp': self.max_mp,
            'strength': self.strength,
            'agility': self.agility,
            'intelligence': self.intelligence,
            'effects': [effect.to_dict() for effect in self.effects]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Human':
        """Десериализация из словаря"""
        # Этот метод будет переопределен в дочерних классах
        raise NotImplementedError

class Character(Human, ABC):
    """Абстрактный класс для игровых персонажей"""
    
    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self.skills: List['Skill'] = []
        self.cooldowns: Dict[str, int] = {}
    
    @abstractmethod
    def basic_attack(self, target: 'Character') -> str:
        pass
    
    @abstractmethod
    def use_skill(self, skill_index: int, targets: List['Character']) -> str:
        pass
    
    def update_cooldowns(self):
        """Обновление кулдаунов навыков"""
        for skill_name in list(self.cooldowns.keys()):
            self.cooldowns[skill_name] -= 1
            if self.cooldowns[skill_name] <= 0:
                del self.cooldowns[skill_name]
    
    def apply_effects(self):
        """Применение эффектов в начале хода"""
        for effect in self.effects[:]:
            effect.apply(self)
            effect.duration -= 1
            if effect.duration <= 0:
                self.effects.remove(effect)
    
    def add_effect(self, effect: 'Effect'):
        """Добавление эффекта персонажу"""
        self.effects.append(effect)