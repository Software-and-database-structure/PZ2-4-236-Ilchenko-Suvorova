from abc import ABC, abstractmethod
from typing import List
import random

class Skill(ABC):
    """Абстрактный класс навыка"""
    
    def __init__(self, name: str, mp_cost: int, cooldown: int = 0):
        self.name = name
        self.mp_cost = mp_cost
        self.cooldown = cooldown
    
    @abstractmethod
    def use(self, caster: 'Character', targets: List['Character']) -> str:
        pass
    
    def __str__(self):
        return f"{self.name} (MP: {self.mp_cost}, CD: {self.cooldown})"

class DamageSkill(Skill):
    """Навык нанесения урона"""
    
    def __init__(self, name: str, mp_cost: int, base_power: int, stat: str, multiplier: float = 1.0, cooldown: int = 0):
        super().__init__(name, mp_cost, cooldown)
        self.base_power = base_power
        self.stat = stat  # "strength", "intelligence", etc.
        self.multiplier = multiplier
    
    def use(self, caster: 'Character', targets: List['Character']) -> str:
        if not targets:
            return "Нет целей для атаки"
        
        target = targets[0]  # Для одиночных атак
        stat_value = getattr(caster, self.stat)
        damage = int((self.base_power + stat_value) * self.multiplier * random.uniform(0.9, 1.1))
        
        target.hp -= damage
        return f"{caster.name} использует {self.name} на {target.name} и наносит {damage} урона"

class HealSkill(Skill):
    """Навык лечения"""
    
    def __init__(self, name: str, mp_cost: int, base_power: int, stat: str, multiplier: float = 1.0, cooldown: int = 0):
        super().__init__(name, mp_cost, cooldown)
        self.base_power = base_power
        self.stat = stat
        self.multiplier = multiplier
    
    def use(self, caster: 'Character', targets: List['Character']) -> str:
        if not targets:
            return "Нет целей для лечения"
        
        if len(targets) == 1:
            # Одиночное лечение
            target = targets[0]
            stat_value = getattr(caster, self.stat)
            heal = int((self.base_power + stat_value) * self.multiplier * random.uniform(0.9, 1.1))
            old_hp = target.hp
            target.hp += heal
            actual_heal = target.hp - old_hp
            return f"{caster.name} использует {self.name} на {target.name} и восстанавливает {actual_heal} HP"
        else:
            # Массовое лечение
            stat_value = getattr(caster, self.stat)
            heal = int((self.base_power + stat_value) * self.multiplier * random.uniform(0.8, 1.0))
            results = []
            for target in targets:
                if target.is_alive:
                    old_hp = target.hp
                    target.hp += heal
                    actual_heal = target.hp - old_hp
                    results.append(f"{target.name} +{actual_heal} HP")
            return f"{caster.name} использует {self.name}: {', '.join(results)}"

class EffectSkill(Skill):
    """Навык наложения эффектов"""
    
    def __init__(self, name: str, mp_cost: int, stat: str, power: float, duration: int, 
                 effect_type: str = "buff", cooldown: int = 0):
        super().__init__(name, mp_cost, cooldown)
        self.stat = stat
        self.power = power
        self.duration = duration
        self.effect_type = effect_type
    
    def use(self, caster: 'Character', targets: List['Character']) -> str:
        if not targets:
            return "Нет целей для навыка"
        
        # Импортируем эффекты внутри метода чтобы избежать циклических импортов
        from effects import PoisonEffect, ShieldEffect, SilenceEffect, RegenerationEffect
        
        effect_map = {
            "poison": PoisonEffect,
            "shield": ShieldEffect, 
            "silence": SilenceEffect,
            "regeneration": RegenerationEffect
        }
        
        effect_class = effect_map.get(self.effect_type)
        if not effect_class:
            return f"Неизвестный тип эффекта: {self.effect_type}"
        
        results = []
        for target in targets:
            if target.is_alive:
                stat_value = getattr(caster, self.stat)
                effect_power = int(stat_value * self.power)
                effect = effect_class(effect_power, self.duration)
                target.add_effect(effect)
                results.append(f"{target.name} получает {effect}")
        
        return f"{caster.name} использует {self.name}: {', '.join(results)}"