import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from characters import Warrior, Mage, Healer, Boss
from core import Human

class TestHuman(unittest.TestCase):
    def test_human_creation(self):
        human = Human("Тестовый человек", 5)
        self.assertEqual(human.name, "Тестовый человек")
        self.assertEqual(human.level, 5)
        self.assertTrue(human.is_alive)
    
    def test_hp_validation(self):
        human = Human("Тест")
        human.hp = 150
        self.assertEqual(human.hp, 100)  # Не должно превышать max_hp
        human.hp = -10
        self.assertEqual(human.hp, 0)   # Не должно быть меньше 0
    
    def test_is_alive_property(self):
        human = Human("Тест")
        self.assertTrue(human.is_alive)
        human.hp = 0
        self.assertFalse(human.is_alive)

class TestWarrior(unittest.TestCase):
    def setUp(self):
        self.warrior = Warrior("Тестовый воин", 3)
        self.target = Human("Цель")
    
    def test_warrior_stats(self):
        self.assertEqual(self.warrior.max_hp, 150 + 3 * 20)  # 210
        self.assertGreater(self.warrior.strength, 10)
        self.assertEqual(len(self.warrior.skills), 3)
    
    def test_basic_attack(self):
        initial_hp = self.target.hp
        self.warrior.basic_attack(self.target)
        self.assertLess(self.target.hp, initial_hp)
    
    def test_skill_usage(self):
        result = self.warrior.use_skill(0, [self.target])
        self.assertIn("использует", result)
        self.assertLess(self.target.hp, 100)

class TestMage(unittest.TestCase):
    def setUp(self):
        self.mage = Mage("Тестовый маг", 3)
        self.target = Human("Цель")
    
    def test_mage_stats(self):
        self.assertGreater(self.mage.intelligence, 10)
        self.assertGreater(self.mage.max_mp, 50)
    
    def test_skill_mp_cost(self):
        initial_mp = self.mage.mp
        self.mage.use_skill(0, [self.target])
        self.assertLess(self.mage.mp, initial_mp)

class TestBoss(unittest.TestCase):
    def setUp(self):
        self.boss = Boss("Тестовый босс", 5, "normal")
        self.party = [Warrior("Воин", 3), Mage("Маг", 3)]
    
    def test_boss_creation(self):
        self.assertEqual(self.boss.name, "Тестовый босс")
        self.assertGreater(self.boss.max_hp, 500)
        self.assertTrue(self.boss.is_alive)
    
    def test_strategy_changes(self):
        # Фаза 1 (100-70% HP)
        self.boss.hp = self.boss.max_hp * 0.8
        self.boss.update_strategy()
        self.assertEqual(self.boss.current_strategy.__class__.__name__, "AggressiveStrategy")
        
        # Фаза 2 (70-30% HP)
        self.boss.hp = self.boss.max_hp * 0.5
        self.boss.update_strategy()
        self.assertEqual(self.boss.current_strategy.__class__.__name__, "AOEStrategy")
        
        # Фаза 3 (30-0% HP)
        self.boss.hp = self.boss.max_hp * 0.2
        self.boss.update_strategy()
        self.assertEqual(self.boss.current_strategy.__class__.__name__, "DebuffStrategy")
    
    def test_boss_choose_action(self):
        result = self.boss.choose_action(self.party)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()