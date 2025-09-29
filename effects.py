from abc import ABC, abstractmethod

class Effect(ABC):
    """Абстрактный класс эффекта"""
    
    def __init__(self, power: int, duration: int):
        self.power = power
        self.duration = duration
        self.name = "Эффект"
    
    @abstractmethod
    def apply(self, target: 'Character') -> str:
        """Применение эффекта к цели"""
        pass
    
    def __str__(self):
        return f"{self.name} ({self.duration} ходов)"
    
    def to_dict(self):
        return {
            'class_name': self.__class__.__name__,
            'name': self.name,
            'power': self.power,
            'duration': self.duration
        }

class PoisonEffect(Effect):
    """Эффект отравления - урон каждый ход"""
    
    def __init__(self, power: int, duration: int):
        super().__init__(power, duration)
        self.name = "Отравление"
    
    def apply(self, target: 'Character') -> str:
        damage = self.power
        target.hp -= damage
        return f"{target.name} получает {damage} урона от отравления"

class ShieldEffect(Effect):
    """Эффект щита - поглощение урона"""
    
    def __init__(self, power: int, duration: int):
        super().__init__(power, duration)
        self.name = "Щит"
        self.remaining_shield = power
    
    def apply(self, target: 'Character') -> str:
        # Щит не наносит урон, просто висит на цели
        return f"{target.name} защищен щитом ({self.remaining_shield})"
    
    def absorb_damage(self, damage: int) -> int:
        """Поглощение урона щитом, возвращает непоглощенный урон"""
        if damage <= self.remaining_shield:
            self.remaining_shield -= damage
            return 0
        else:
            remaining_damage = damage - self.remaining_shield
            self.remaining_shield = 0
            self.duration = 0  # Щит разрушен
            return remaining_damage

class SilenceEffect(Effect):
    """Эффект немоты - нельзя использовать навыки"""
    
    def __init__(self, power: int, duration: int):
        super().__init__(power, duration)
        self.name = "Немота"
    
    def apply(self, target: 'Character') -> str:
        return f"{target.name} немой и не может использовать навыки"

class RegenerationEffect(Effect):
    """Эффект регенерации - восстановление HP каждый ход"""
    
    def __init__(self, power: int, duration: int):
        super().__init__(power, duration)
        self.name = "Регенерация"
    
    def apply(self, target: 'Character') -> str:
        heal = self.power
        old_hp = target.hp
        target.hp += heal
        actual_heal = target.hp - old_hp
        return f"{target.name} восстанавливает {actual_heal} HP от регенерации"