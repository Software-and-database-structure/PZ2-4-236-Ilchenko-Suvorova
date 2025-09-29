import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from effects import PoisonEffect, ShieldEffect, SilenceEffect, RegenerationEffect
from characters import Warrior

class TestPoisonEffect(unittest.TestCase):
    def setUp(self):
        self.warrior = Warrior("Тестовый воин", 3)
        self.poison = PoisonEffect(10, 3)
    
    def test_poison_application(self):
        initial_hp = self.warrior.hp
        self.poison.apply(self.warrior)
        self.assertEqual(self.warrior.hp, initial_hp - 10)
    
    def test_poison_duration(self):
        self.assertEqual(self.poison.duration, 3)
        self.poison.apply(self.warrior)
        self.assertEqual(self.poison.duration, 2)

class TestShieldEffect(unittest.TestCase):
    def setUp(self):
        self.warrior = Warrior("Тестовый воин", 3)
        self.shield = ShieldEffect(50, 2)
    
    def test_shield_creation(self):
        self.assertEqual(self.shield.remaining_shield, 50)
        self.assertEqual(self.shield.duration, 2)
    
    def test_shield_absorb_damage(self):
        # Полное поглощение урона
        remaining_damage = self.shield.absorb_damage(30)
        self.assertEqual(remaining_damage, 0)
        self.assertEqual(self.shield.remaining_shield, 20)
        
        # Частичное поглощение
        remaining_damage = self.shield.absorb_damage(30)
        self.assertEqual(remaining_damage, 10)
        self.assertEqual(self.shield.remaining_shield, 0)
        self.assertEqual(self.shield.duration, 0)  # Щит разрушен

class TestRegenerationEffect(unittest.TestCase):
    def setUp(self):
        self.warrior = Warrior("Тестовый воин", 3)
        self.warrior.hp = 50  # Уменьшаем HP для теста
        self.regen = RegenerationEffect(15, 2)
    
    def test_regeneration_application(self):
        initial_hp = self.warrior.hp
        self.regen.apply(self.warrior)
        self.assertGreater(self.warrior.hp, initial_hp)

class TestSilenceEffect(unittest.TestCase):
    def setUp(self):
        self.warrior = Warrior("Тестовый воин", 3)
        self.silence = SilenceEffect(0, 2)
    
    def test_silence_application(self):
        result = self.silence.apply(self.warrior)
        self.assertIn("немой", result)

if __name__ == '__main__':
    unittest.main()