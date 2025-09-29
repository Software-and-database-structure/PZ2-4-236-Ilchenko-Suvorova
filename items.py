from typing import List

class Item:
    """Базовый класс предмета"""
    
    def __init__(self, name: str, description: str, consumable: bool = True):
        self.name = name
        self.description = description
        self.consumable = consumable
    
    def use(self, user: 'Character', target: 'Character' = None) -> str:
        """Использование предмета"""
        if target is None:
            target = user
        return f"{user.name} использует {self.name} на {target.name}"
    
    def __str__(self):
        return f"{self.name}: {self.description}"

class HealthPotion(Item):
    """Зелье здоровья"""
    
    def __init__(self, heal_amount: int = 50):
        super().__init__("Зелье здоровья", f"Восстанавливает {heal_amount} HP")
        self.heal_amount = heal_amount
    
    def use(self, user: 'Character', target: 'Character' = None) -> str:
        if target is None:
            target = user
        
        old_hp = target.hp
        target.hp += self.heal_amount
        actual_heal = target.hp - old_hp
        
        return f"{user.name} использует {self.name} на {target.name} и восстанавливает {actual_heal} HP"

class ManaPotion(Item):
    """Зелье маны"""
    
    def __init__(self, mana_amount: int = 30):
        super().__init__("Зелье маны", f"Восстанавливает {mana_amount} MP")
        self.mana_amount = mana_amount
    
    def use(self, user: 'Character', target: 'Character' = None) -> str:
        if target is None:
            target = user
        
        old_mp = target.mp
        target.mp += self.mana_amount
        actual_mana = target.mp - old_mp
        
        return f"{user.name} использует {self.name} на {target.name} и восстанавливает {actual_mana} MP"

class Inventory:
    """Инвентарь персонажа"""
    
    def __init__(self):
        self.items: List[Item] = []
    
    def add_item(self, item: Item):
        """Добавление предмета в инвентарь"""
        self.items.append(item)
    
    def remove_item(self, item: Item):
        """Удаление предмета из инвентаря"""
        if item in self.items:
            self.items.remove(item)
    
    def use_item(self, item_index: int, user: 'Character', target: 'Character' = None) -> str:
        """Использование предмета по индексу"""
        if item_index >= len(self.items):
            return "Неверный предмет"
        
        item = self.items[item_index]
        result = item.use(user, target)
        
        if item.consumable:
            self.remove_item(item)
        
        return result
    
    def __str__(self):
        if not self.items:
            return "Инвентарь пуст"
        
        return "\n".join([f"{i}. {item}" for i, item in enumerate(self.items)])