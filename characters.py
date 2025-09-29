from abc import ABC, abstractmethod
import random
from typing import List, Dict, Any

# Сначала импортируем все необходимые классы
from core import Character, Human
from skills import Skill, DamageSkill, HealSkill, EffectSkill
from effects import PoisonEffect, ShieldEffect, SilenceEffect, RegenerationEffect

class CritMixin:
    """Миксин для критического урона"""
    
    def calculate_crit(self, base_damage: int, crit_chance: float = 0.1) -> tuple[int, bool]:
        """Расчет критического урона"""
        is_crit = random.random() < crit_chance
        if is_crit:
            return int(base_damage * 1.5), True
        return base_damage, False

# Стратегии поведения босса должны быть объявлены ДО класса Boss
class BossStrategy(ABC):
    """Абстрактный класс стратегии босса"""
    
    @abstractmethod
    def choose_action(self, boss: 'Boss', targets: List[Character]) -> str:
        pass

class AggressiveStrategy(BossStrategy):
    """Агрессивная стратегия - атака самого слабого"""
    
    def choose_action(self, boss: 'Boss', targets: List[Character]) -> str:
        alive_targets = [t for t in targets if t.is_alive]
        if not alive_targets:
            return "Нет целей для атаки"
        
        # Атакуем цель с наименьшим HP
        target = min(alive_targets, key=lambda x: x.hp)
        return boss.basic_attack(target)

class AOEStrategy(BossStrategy):
    """Стратегия массовой атаки"""
    
    def choose_action(self, boss: 'Boss', targets: List[Character]) -> str:
        alive_targets = [t for t in targets if t.is_alive]
        if not alive_targets:
            return "Нет целей для атаки"
        
        # Используем AOE навык если доступен
        aoe_skill = next((s for s in boss.skills if "массовая" in s.name.lower()), None)
        if aoe_skill and aoe_skill.name not in boss.cooldowns and boss.mp >= aoe_skill.mp_cost:
            return boss.use_skill(boss.skills.index(aoe_skill), alive_targets)
        
        # Иначе атакуем случайную цель
        target = random.choice(alive_targets)
        return boss.basic_attack(target)

class DebuffStrategy(BossStrategy):
    """Стратегия наложения дебаффов"""
    
    def choose_action(self, boss: 'Boss', targets: List[Character]) -> str:
        alive_targets = [t for t in targets if t.is_alive]
        if not alive_targets:
            return "Нет целей для атаки"
        
        # Ищем навык с эффектом
        debuff_skill = next((s for s in boss.skills if hasattr(s, 'effect_type')), None)
        if debuff_skill and debuff_skill.name not in boss.cooldowns and boss.mp >= debuff_skill.mp_cost:
            target = random.choice(alive_targets)
            return boss.use_skill(boss.skills.index(debuff_skill), [target])
        
        target = random.choice(alive_targets)
        return boss.basic_attack(target)

# Теперь объявляем классы персонажей
class Warrior(Character, CritMixin):
    """Класс воина"""
    
    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self.max_hp = 150 + level * 20
        self.hp = self.max_hp
        self.max_mp = 30 + level * 5
        self.mp = self.max_mp
        self.strength = 15 + level * 2
        self.agility = 8 + level
        self.intelligence = 5 + level
        
        # Навыки воина
        self.skills = [
    DamageSkill("Удар мечом", 10, 5, "strength", 1.2, cooldown=0),
    DamageSkill("Мощный удар", 20, 15, "strength", 2.0, cooldown=2),
    EffectSkill("Боевой клич", 15, "strength", 1.5, 3, effect_type="shield", cooldown=3)  # Изменено с "buff" на "shield"
]
    
    def basic_attack(self, target: Character) -> str:
        damage = self.strength + random.randint(1, 5)
        damage, is_crit = self.calculate_crit(damage, 0.15)
        target.hp -= damage
        crit_text = " КРИТИЧЕСКИЙ УРОН!" if is_crit else ""
        return f"{self.name} атакует {target.name} на {damage} урона{crit_text}"
    
    def use_skill(self, skill_index: int, targets: List[Character]) -> str:
        if skill_index >= len(self.skills):
            return "Неверный навык"
        
        skill = self.skills[skill_index]
        
        if skill.name in self.cooldowns:
            return f"Навык {skill.name} на перезарядке"
        
        if self.mp < skill.mp_cost:
            return "Недостаточно MP"
        
        self.mp -= skill.mp_cost
        if skill.cooldown > 0:
            self.cooldowns[skill.name] = skill.cooldown
        
        return skill.use(self, targets)

class Mage(Character):
    """Класс мага"""
    
    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self.max_hp = 80 + level * 10
        self.hp = self.max_hp
        self.max_mp = 80 + level * 15
        self.mp = self.max_mp
        self.strength = 5 + level
        self.agility = 8 + level
        self.intelligence = 18 + level * 2
        
        self.skills = [
    DamageSkill("Огненный шар", 15, 20, "intelligence", 1.5, cooldown=0),
    DamageSkill("Ледяная стрела", 12, 15, "intelligence", 1.3, cooldown=1),
    EffectSkill("Отравление", 20, "intelligence", 0.5, 3, effect_type="poison", cooldown=3)  # Уже правильно
]
    
    def basic_attack(self, target: Character) -> str:
        damage = self.intelligence // 2 + random.randint(1, 3)
        target.hp -= damage
        return f"{self.name} атакует {target.name} магией на {damage} урона"
    
    def use_skill(self, skill_index: int, targets: List[Character]) -> str:
        if skill_index >= len(self.skills):
            return "Неверный навык"
        
        skill = self.skills[skill_index]
        
        if skill.name in self.cooldowns:
            return f"Навык {skill.name} на перезарядке"
        
        if self.mp < skill.mp_cost:
            return "Недостаточно MP"
        
        self.mp -= skill.mp_cost
        if skill.cooldown > 0:
            self.cooldowns[skill.name] = skill.cooldown
        
        return skill.use(self, targets)

class Healer(Character):
    """Класс лекаря"""
    
    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self.max_hp = 100 + level * 12
        self.hp = self.max_hp
        self.max_mp = 70 + level * 12
        self.mp = self.max_mp
        self.strength = 6 + level
        self.agility = 10 + level
        self.intelligence = 14 + level * 2
        
        self.skills = [
    HealSkill("Лечение", 10, 15, "intelligence", 1.2, cooldown=0),
    HealSkill("Массовое лечение", 25, 30, "intelligence", 0.8, cooldown=3),
    EffectSkill("Щит", 15, "intelligence", 0.5, 2, effect_type="shield", cooldown=2)  # Уже правильно
]
    
    def basic_attack(self, target: Character) -> str:
        damage = self.strength + random.randint(1, 3)
        target.hp -= damage
        return f"{self.name} атакует {target.name} на {damage} урона"
    
    def use_skill(self, skill_index: int, targets: List[Character]) -> str:
        if skill_index >= len(self.skills):
            return "Неверный навык"
        
        skill = self.skills[skill_index]
        
        if skill.name in self.cooldowns:
            return f"Навык {skill.name} на перезарядке"
        
        if self.mp < skill.mp_cost:
            return "Недостаточно MP"
        
        self.mp -= skill.mp_cost
        if skill.cooldown > 0:
            self.cooldowns[skill.name] = skill.cooldown
        
        return skill.use(self, targets)

class Boss(Character, CritMixin):
    """Класс босса с меняющимися фазами"""
    
    def __init__(self, name: str, level: int = 1, difficulty: str = "normal"):
        super().__init__(name, level)
        
        # Настройки сложности
        difficulty_multiplier = {"easy": 0.8, "normal": 1.0, "hard": 1.3}[difficulty]
        
        self.max_hp = int(500 * difficulty_multiplier) + level * 50
        self.hp = self.max_hp
        self.max_mp = 200 + level * 20
        self.mp = self.max_mp
        self.strength = int(20 * difficulty_multiplier) + level * 3
        self.agility = int(15 * difficulty_multiplier) + level * 2
        self.intelligence = int(18 * difficulty_multiplier) + level * 2
        
        self.skills = [
    DamageSkill("Темный удар", 20, 25, "strength", 1.5, cooldown=1),
    DamageSkill("Массовая тьма", 40, 50, "intelligence", 1.0, cooldown=4),
    EffectSkill("Оковы тьмы", 30, "intelligence", 0.3, 2, effect_type="silence", cooldown=3)  # Уже правильно
]
        
        # Стратегии для разных фаз
        self.strategies = {
            "phase1": AggressiveStrategy(),    # 100-70% HP
            "phase2": AOEStrategy(),          # 70-30% HP  
            "phase3": DebuffStrategy()        # 30-0% HP
        }
        self.current_strategy = self.strategies["phase1"]
    
    def basic_attack(self, target: Character) -> str:
        damage = self.strength + random.randint(5, 10)
        damage, is_crit = self.calculate_crit(damage, 0.2)
        target.hp -= damage
        crit_text = " КРИТИЧЕСКИЙ УРОН!" if is_crit else ""
        return f"{self.name} атакует {target.name} на {damage} урона{crit_text}"
    
    def use_skill(self, skill_index: int, targets: List[Character]) -> str:
        if skill_index >= len(self.skills):
            return "Неверный навык"
        
        skill = self.skills[skill_index]
        
        if skill.name in self.cooldowns:
            return f"Навык {skill.name} на перезарядке"
        
        if self.mp < skill.mp_cost:
            return "Недостаточно MP"
        
        self.mp -= skill.mp_cost
        if skill.cooldown > 0:
            self.cooldowns[skill.name] = skill.cooldown
        
        return skill.use(self, targets)
    
    def update_strategy(self):
        """Обновление стратегии в зависимости от HP"""
        hp_percent = self.hp / self.max_hp
        
        if hp_percent > 0.7:
            self.current_strategy = self.strategies["phase1"]
        elif hp_percent > 0.3:
            self.current_strategy = self.strategies["phase2"]
        else:
            self.current_strategy = self.strategies["phase3"]
    
    def choose_action(self, targets: List[Character]) -> str:
        """Выбор действия на основе текущей стратегии"""
        self.update_strategy()
        return self.current_strategy.choose_action(self, targets)