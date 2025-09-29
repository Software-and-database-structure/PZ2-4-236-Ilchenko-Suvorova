import random
import json
from typing import List, Dict, Any, Iterator
from core import Character
from characters import Boss

class TurnOrder:
    """Итератор для определения порядка ходов"""
    
    def __init__(self, characters: List[Character]):
        self.characters = [c for c in characters if c.is_alive]
        # Сортируем по ловкости (в порядке убывания)
        self.characters.sort(key=lambda x: x.agility, reverse=True)
        self.index = 0
    
    def __iter__(self) -> Iterator[Character]:
        return self
    
    def __next__(self) -> Character:
        if not self.characters:
            raise StopIteration
        
        # Убираем мертвых персонажей
        self.characters = [c for c in self.characters if c.is_alive]
        if not self.characters:
            raise StopIteration
        
        if self.index >= len(self.characters):
            self.index = 0
        
        character = self.characters[self.index]
        self.index += 1
        return character
    
    def add_character(self, character: Character):
        """Добавление персонажа в очередь"""
        if character.is_alive and character not in self.characters:
            self.characters.append(character)
            self.characters.sort(key=lambda x: x.agility, reverse=True)

class BattleLogger:
    """Контекстный менеджер для логирования боя"""
    
    def __init__(self, filename: str = "battle_log.txt"):
        self.filename = filename
        self.log_file = None
    
    def __enter__(self):
        self.log_file = open(self.filename, 'w', encoding='utf-8')
        self.log_file.write("=== НАЧАЛО БОЯ ===\n")
        return self
    
    def log(self, message: str):
        """Запись сообщения в лог"""
        if self.log_file:
            self.log_file.write(message + '\n')
        print(message)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.log_file:
            self.log_file.write("=== КОНЕЦ БОЯ ===\n")
            self.log_file.close()

class Battle:
    """Основной класс боя"""
    
    def __init__(self, party: List[Character], boss: Boss, seed: int = None):
        self.party = party
        self.boss = boss
        self.turn_order = TurnOrder(party + [boss])
        self.round = 1
        self.is_battle_over = False
        
        # Настройка генератора случайных чисел
        if seed is not None:
            random.seed(seed)
    
    def save_state(self, filename: str = "battle_save.json"):
        """Сохранение состояния боя в JSON"""
        state = {
            'round': self.round,
            'party': [char.to_dict() for char in self.party],
            'boss': self.boss.to_dict(),
            'is_battle_over': self.is_battle_over
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_state(cls, filename: str = "battle_save.json"):
        """Загрузка состояния боя из JSON"""
        with open(filename, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        # В реальной реализации нужно восстановить объекты из словарей
        # Это упрощенная версия
        return state
    
    def check_battle_end(self) -> bool:
        """Проверка условий окончания боя"""
        party_alive = any(char.is_alive for char in self.party)
        boss_alive = self.boss.is_alive
        
        if not party_alive:
            self.is_battle_over = True
            return True
        elif not boss_alive:
            self.is_battle_over = True
            return True
        
        return False
    
    def apply_start_of_turn_effects(self, character: Character):
        """Применение эффектов в начале хода персонажа"""
        character.apply_effects()
        character.update_cooldowns()
    
    def run_turn(self, character: Character, logger: BattleLogger) -> bool:
        """Выполнение хода одного персонажа"""
        if not character.is_alive:
            return False
        
        logger.log(f"\n--- Ход {character.name} ---")
        self.apply_start_of_turn_effects(character)
        
        if isinstance(character, Boss):
            # Ход босса
            action_result = character.choose_action(self.party)
            logger.log(action_result)
        else:
            # Ход игрока (упрощенная версия - случайное действие)
            if character.skills and random.random() < 0.6 and character.mp > 10:
                # Использование случайного навыка
                available_skills = [i for i, skill in enumerate(character.skills) 
                                  if skill.name not in character.cooldowns and character.mp >= skill.mp_cost]
                if available_skills:
                    skill_index = random.choice(available_skills)
                    action_result = character.use_skill(skill_index, [self.boss])
                    logger.log(action_result)
                else:
                    # Базовая атака если нет доступных навыков
                    action_result = character.basic_attack(self.boss)
                    logger.log(action_result)
            else:
                # Базовая атака
                action_result = character.basic_attack(self.boss)
                logger.log(action_result)
        
        return self.check_battle_end()
    
    def run_battle(self):
        """Основной игровой цикл"""
        with BattleLogger() as logger:
            logger.log(f"Начало боя! Пати против {self.boss.name}")
            logger.log(f"Уровень босса: {self.boss.level}")
            logger.log(f"HP босса: {self.boss.hp}/{self.boss.max_hp}")
            
            while not self.is_battle_over:
                logger.log(f"\n=== Раунд {self.round} ===")
                
                # Показываем статус всех персонажей
                for char in self.party:
                    if char.is_alive:
                        logger.log(f"{char.name}: HP {char.hp}/{char.max_hp}, MP {char.mp}/{char.max_mp}")
                
                logger.log(f"{self.boss.name}: HP {self.boss.hp}/{self.boss.max_hp}, MP {self.boss.mp}/{self.boss.max_mp}")
                
                # Выполняем ходы по очереди
                for character in self.turn_order:
                    if self.run_turn(character, logger):
                        break
                
                if not self.is_battle_over:
                    self.round += 1
                
                # Авто-сохранение каждые 5 раундов
                if self.round % 5 == 0:
                    self.save_state(f"battle_round_{self.round}.json")
            
            # Определяем победителя
            if any(char.is_alive for char in self.party):
                logger.log(f"\n🎉 ПОБЕДА! {self.boss.name} повержен!")
                return "party"
            else:
                logger.log(f"\n💀 ПОРАЖЕНИЕ! {self.boss.name} уничтожил пати!")
                return "boss"