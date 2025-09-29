#!/usr/bin/env python3
import os
import sys

# Добавляем путь для импорта модулей
sys.path.append(os.path.dirname(__file__))

from utils import create_default_party, select_difficulty, show_party_status, show_boss_status, create_custom_party
from characters import Boss
from battle import Battle

def main():
    print("🐉 МИНИ-ИГРА 'ПАТИ ПРОТИВ БОССА' 🐉")
    print("=" * 40)
    
    # Выбор типа пати
    print("Выберите тип пати:")
    print("1. Стандартная пати")
    print("2. Кастомная пати")
    
    party_choice = input("Ваш выбор (1-2): ").strip()
    if party_choice == "2":
        party = create_custom_party()
    else:
        party = create_default_party()
    
    show_party_status(party)
    
    # Выбор сложности
    difficulty = select_difficulty()
    
    # Создание босса
    boss_name = input("Введите имя босса (или нажмите Enter для имени по умолчанию): ").strip()
    if not boss_name:
        boss_name = "Саурон"
    
    boss_level = 5
    boss = Boss(boss_name, boss_level, difficulty)
    
    print(f"\n⚔️  Босс создан: {boss_name} (Уровень {boss_level}, Сложность: {difficulty})")
    show_boss_status(boss)
    
    # Настройка сида для повторяемости
    seed_input = input("Введите seed для случайной генерации (или нажмите Enter для случайного): ").strip()
    seed = int(seed_input) if seed_input and seed_input.isdigit() else None
    
    # Запуск боя
    input("\nНажмите Enter чтобы начать бой...")
    
    battle = Battle(party, boss, seed)
    result = battle.run_battle()
    
    # Показ итогов
    if result == "party":
        print("\n🎊 Поздравляем с победой! 🎊")
    else:
        print("\n😞 Не повезло в этот раз... Попробуйте снова!")
    
    # Предложение сохранить результат
    save = input("\nСохранить результат боя? (y/n): ").strip().lower()
    if save == 'y':
        battle.save_state("final_battle_result.json")
        print("Результат сохранен в 'final_battle_result.json'")

if __name__ == "__main__":
    main()