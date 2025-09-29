import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from characters import Warrior, Mage, Boss
from battle import Battle, TurnOrder
from core import Human

class TestTurnOrder(unittest.TestCase):
    def setUp(self):
        self.warrior = Warrior("Воин", 3)
        self.mage = Mage("Маг", 3)
        self.boss = Boss("Босс", 5, "normal")
        self.characters = [self.warrior, self.mage, self.boss]
    
    def test_turn_order_creation(self):
        turn_order = TurnOrder(self.characters)
        self.assertEqual(len(turn_order.characters), 3)
    
    def test_turn_order_sorting(self):
        # Устанавливаем разную ловкость
        self.warrior.agility = 20
        self.mage.agility = 15
        self.boss.agility = 25
        
        turn_order = TurnOrder(self.characters)
        # Должны быть отсортированы по убыванию ловкости
        self.assertEqual(turn_order.characters[0], self.boss)  # Ловкость 25
        self.assertEqual(turn_order.characters[1], self.warrior)  # Ловкость 20
        self.assertEqual(turn_order.characters[2], self.mage)   # Ловкость 15
    
    def test_turn_order_iteration(self):
        turn_order = TurnOrder(self.characters)
        characters_in_order = list(turn_order)
        self.assertEqual(len(characters_in_order), 3)
    
    def test_dead_characters_removed(self):
        self.warrior.hp = 0
        turn_order = TurnOrder(self.characters)
        self.assertEqual(len(turn_order.characters), 2)  # Только живые персонажи

class TestBattle(unittest.TestCase):
    def setUp(self):
        self.party = [Warrior("Воин", 3), Mage("Маг", 3)]
        self.boss = Boss("Босс", 5, "normal")
        self.battle = Battle(self.party, self.boss, seed=42)
    
    def test_battle_creation(self):
        self.assertEqual(len(self.battle.party), 2)
        self.assertEqual(self.battle.boss.name, "Босс")
        self.assertEqual(self.battle.round, 1)
        self.assertFalse(self.battle.is_battle_over)
    
    def test_check_battle_end(self):
        # Бой не должен закончиться при создании
        self.assertFalse(self.battle.check_battle_end())
        
        # Бой должен закончиться когда все персонажи мертвы
        for char in self.party:
            char.hp = 0
        self.boss.hp = 0
        self.assertTrue(self.battle.check_battle_end())
    
    def test_save_load_state(self):
        # Тест сохранения состояния
        self.battle.save_state("test_save.json")
        
        # Проверяем что файл создан
        self.assertTrue(os.path.exists("test_save.json"))
        
        # Тест загрузки состояния
        state = Battle.load_state("test_save.json")
        self.assertEqual(state['round'], 1)
        self.assertEqual(len(state['party']), 2)
        
        # Убираем тестовый файл
        os.remove("test_save.json")
    
    def test_apply_effects(self):
        warrior = self.party[0]
        initial_hp = warrior.hp
        
        # Симулируем применение эффектов
        self.battle.apply_start_of_turn_effects(warrior)
        
        # HP не должен измениться без эффектов
        self.assertEqual(warrior.hp, initial_hp)

if __name__ == '__main__':
    unittest.main()