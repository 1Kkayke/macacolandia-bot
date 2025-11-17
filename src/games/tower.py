"""Tower climbing game implementation"""

import random
from typing import Tuple, List


class TowerGame:
    """Tower climbing risk/reward game"""
    
    DIFFICULTIES = {
        'facil': {'tiles_per_level': 3, 'safe_tiles': 2, 'levels': 8},
        'medio': {'tiles_per_level': 3, 'safe_tiles': 2, 'levels': 12},
        'dificil': {'tiles_per_level': 4, 'safe_tiles': 2, 'levels': 10},
        'extremo': {'tiles_per_level': 4, 'safe_tiles': 1, 'levels': 12}
    }
    
    def __init__(self, difficulty: str = 'medio'):
        """Initialize tower game"""
        self.difficulty = difficulty.lower()
        if self.difficulty not in TowerGame.DIFFICULTIES:
            self.difficulty = 'medio'
        
        settings = TowerGame.DIFFICULTIES[self.difficulty]
        self.tiles_per_level = settings['tiles_per_level']
        self.safe_tiles = settings['safe_tiles']
        self.max_levels = settings['levels']
        
        self.current_level = 0
        self.game_over = False
        self.won = False
        
        # Generate tower
        self.tower = self._generate_tower()
        self.revealed = []
    
    def _generate_tower(self) -> List[List[bool]]:
        """Generate tower with safe/unsafe tiles"""
        tower = []
        for _ in range(self.max_levels):
            level = [True] * self.safe_tiles + [False] * (self.tiles_per_level - self.safe_tiles)
            random.shuffle(level)
            tower.append(level)
        return tower
    
    def choose_tile(self, tile_index: int) -> Tuple[bool, float]:
        """
        Choose a tile at current level
        Returns: (is_safe, current_multiplier)
        """
        if self.game_over or tile_index < 0 or tile_index >= self.tiles_per_level:
            return False, 0.0
        
        is_safe = self.tower[self.current_level][tile_index]
        self.revealed.append((self.current_level, tile_index, is_safe))
        
        if is_safe:
            self.current_level += 1
            if self.current_level >= self.max_levels:
                self.game_over = True
                self.won = True
        else:
            self.game_over = True
            self.won = False
        
        return is_safe, self.get_multiplier()
    
    def get_multiplier(self) -> float:
        """Get current multiplier based on level reached"""
        if self.current_level == 0:
            return 0.0
        
        # Calculate multiplier based on difficulty and level
        # Each level increases multiplier exponentially
        base_multiplier = 1.0
        
        if self.difficulty == 'facil':
            multiplier_per_level = 0.3
        elif self.difficulty == 'medio':
            multiplier_per_level = 0.4
        elif self.difficulty == 'dificil':
            multiplier_per_level = 0.6
        else:  # extremo
            multiplier_per_level = 1.2
        
        multiplier = base_multiplier + (self.current_level * multiplier_per_level)
        
        # Exponential bonus for higher levels
        if self.current_level > 5:
            multiplier *= (1.0 + (self.current_level - 5) * 0.1)
        
        return round(multiplier, 2)
    
    def cash_out(self) -> float:
        """Cash out current winnings"""
        if self.current_level == 0:
            return 0.0
        
        self.game_over = True
        self.won = True
        return self.get_multiplier()
    
    def format_level(self, level: int, show_all: bool = False) -> str:
        """Format a level for display"""
        if level >= len(self.tower):
            return ""
        
        tiles = []
        for i in range(self.tiles_per_level):
            # Check if this tile was revealed
            revealed_tile = None
            for rev_level, rev_index, is_safe in self.revealed:
                if rev_level == level and rev_index == i:
                    revealed_tile = is_safe
                    break
            
            if revealed_tile is not None:
                tiles.append('✅' if revealed_tile else '💥')
            elif show_all:
                tiles.append('✅' if self.tower[level][i] else '💥')
            else:
                tiles.append('🟦')
        
        return ' '.join(tiles)
    
    def format_tower(self, show_all: bool = False) -> str:
        """Format entire tower for display"""
        tower_str = ""
        
        # Show from top to bottom
        for level in range(self.max_levels - 1, -1, -1):
            level_num = level + 1
            
            if level == self.current_level and not self.game_over:
                tower_str += f"▶ Nível {level_num:2d}: {self.format_level(level, show_all)}\n"
            elif level < self.current_level:
                tower_str += f"  Nível {level_num:2d}: {self.format_level(level, show_all)}\n"
            else:
                tower_str += f"  Nível {level_num:2d}: {'🟦 ' * self.tiles_per_level}\n"
        
        return tower_str
    
    @staticmethod
    def validate_difficulty(difficulty: str) -> bool:
        """Validate difficulty level"""
        return difficulty.lower() in TowerGame.DIFFICULTIES
    
    @staticmethod
    def get_difficulty_info(difficulty: str) -> str:
        """Get difficulty information"""
        difficulty = difficulty.lower()
        if difficulty not in TowerGame.DIFFICULTIES:
            return ""
        
        settings = TowerGame.DIFFICULTIES[difficulty]
        safe_chance = (settings['safe_tiles'] / settings['tiles_per_level']) * 100
        
        descriptions = {
            'facil': f"🟢 Fácil: {settings['levels']} níveis, {safe_chance:.0f}% chance por nível",
            'medio': f"🟡 Médio: {settings['levels']} níveis, {safe_chance:.0f}% chance por nível",
            'dificil': f"🟠 Difícil: {settings['levels']} níveis, {safe_chance:.0f}% chance por nível",
            'extremo': f"🔴 Extremo: {settings['levels']} níveis, {safe_chance:.0f}% chance por nível"
        }
        
        return descriptions.get(difficulty, '')
