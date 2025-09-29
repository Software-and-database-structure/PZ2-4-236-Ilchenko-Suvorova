import random
from typing import List
from characters import Warrior, Mage, Healer, Boss
def create_party(party_config: List[dict]) -> List:
    """Создание пати по конфигурации"""
    party = []
    class_map = {
        'warrior': Warrior,
        'mage': Mage, 
        'healer': Healer
    }
    
    for config in party_config:
        char_class = class_map[config['class']]
        character = char_class(config['name'], config.get('level', 1))
        party.append(character)
    
    return party

def create_default_party() -> List:
    """Создание пати по умолчанию"""
    return [
        Warrior("Боромир", 5),
        Mage("Гэндальф", 5),
        Healer("Элронд", 5)
    ]

def select_difficulty() -> str:
    """Выбор сложности через CLI"""
    print("Выберите сложность:")
    print("1. Легкая")
    print("2. Нормальная") 
    print("3. Сложная")
    
    while True:
        choice = input("Ваш выбор (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return ['easy', 'normal', 'hard'][int(choice) - 1]
        print("Неверный выбор. Попробуйте снова.")

def show_party_status(party: List):
    """Показать статус пати"""
    print("\n=== СОСТАВ ПАТИ ===")
    for i, char in enumerate(party, 1):
        status = "❤️" if char.is_alive else "💀"
        print(f"{i}. {status} {char}")
        if char.skills:
            print("   Навыки:", ", ".join([f"{skill.name} ({skill.mp_cost} MP)" for skill in char.skills]))

def show_boss_status(boss: Boss):
    """Показать статус босса"""
    print(f"\n=== БОСС ===")
    status = "❤️" if boss.is_alive else "💀"
    print(f"{status} {boss}")
    hp_percent = boss.hp / boss.max_hp * 100
    print(f"HP: {'█' * int(hp_percent / 10)}{'░' * (10 - int(hp_percent / 10))} {hp_percent:.1f}%")

def create_custom_party():
    """Создание кастомной пати"""
    party = []
    classes = {
        '1': ('Warrior', Warrior),
        '2': ('Mage', Mage),
        '3': ('Healer', Healer)
    }
    
    print("\nСоздание кастомной пати (3 персонажа):")
    
    for i in range(3):
        print(f"\nПерсонаж {i+1}:")
        print("1. Воин (высокий HP, сила)")
        print("2. Маг (магия, интеллект)") 
        print("3. Лекарь (лечение, поддержка)")
        
        while True:
            class_choice = input("Выберите класс (1-3): ").strip()
            if class_choice in classes:
                break
            print("Неверный выбор. Попробуйте снова.")
        
        name = input("Введите имя персонажа: ").strip()
        if not name:
            name = f"{classes[class_choice][0]}{i+1}"
        
        character = classes[class_choice][1](name, 5)
        party.append(character)
        print(f"Добавлен: {character}")
    
    return party