"""
Artist character model
"""
from config.constants import STAT_MIN, STAT_MAX, STARTING_MONEY, STARTING_AGE


class Artist:
    """Main artist character class"""
    
    def __init__(self, name: str):
        """Initialize a new artist
        
        Args:
            name: Artist's stage name
        """
        self.name = name
        self.age = STARTING_AGE
        self.created_at = None
        
        # CORE TALENT STATS (0-100)
        self.vocal_ability = 50
        self.songwriting = 40
        self.stage_presence = 45
        self.creativity = 50
        
        # PHYSICAL & MENTAL STATS (0-100)
        self.health = 80
        self.stress = 20
        self.integrity = 75
        self.appearance = 60
        
        # PERSONALITY STATS (0-100)
        self.ambition = 60
        self.empathy = 50
        self.work_ethic = 55
        
        # CAREER STATUS
        self.fame_level = 0
        self.money = STARTING_MONEY
        self.debt = 0
        self.contracts = []
        
        # Career tracking
        self.songs_released = 0
        self.concerts_performed = 0
        self.current_month = 0
        
    def __repr__(self):
        return f"Artist({self.name}, Fame: {self.fame_level}, Money: ${self.money})"
    
    def get_all_stats(self) -> dict:
        """Get all artist stats as a dictionary"""
        return {
            "name": self.name,
            "age": self.age,
            "vocal_ability": self.vocal_ability,
            "songwriting": self.songwriting,
            "stage_presence": self.stage_presence,
            "creativity": self.creativity,
            "health": self.health,
            "stress": self.stress,
            "integrity": self.integrity,
            "appearance": self.appearance,
            "ambition": self.ambition,
            "empathy": self.empathy,
            "work_ethic": self.work_ethic,
            "fame_level": self.fame_level,
            "money": self.money,
            "debt": self.debt,
            "contracts": len(self.contracts),
        }
    
    def clamp_stat(self, value: float, stat_min: int = STAT_MIN, stat_max: int = STAT_MAX) -> float:
        """Clamp a stat value between min and max
        
        Args:
            value: The stat value
            stat_min: Minimum allowed value
            stat_max: Maximum allowed value
            
        Returns:
            Clamped value
        """
        return max(stat_min, min(stat_max, value))
    
    def modify_stat(self, stat_name: str, change: float) -> bool:
        """Modify any stat with bounds checking
        
        Args:
            stat_name: Name of the stat to modify
            change: Amount to change (can be positive or negative)
            
        Returns:
            True if successful, False if stat doesn't exist
        """
        if not hasattr(self, stat_name):
            return False
        
        current_value = getattr(self, stat_name)
        
        if stat_name in ["money", "debt", "songs_released", "concerts_performed"]:
            # These can go higher than 100
            new_value = current_value + change
        else:
            # Regular stats are clamped 0-100
            new_value = self.clamp_stat(current_value + change)
        
        setattr(self, stat_name, new_value)
        return True
    
    def add_contract(self, contract):
        """Add a contract to artist's portfolio
        
        Args:
            contract: Contract object to add
        """
        self.contracts.append(contract)
    
    def get_monthly_income(self) -> float:
        """Calculate monthly income based on fame and other factors
        
        Returns:
            Monthly income amount
        """
        from config.constants import BASE_SALARY, FAME_MULTIPLIER
        
        base = BASE_SALARY
        fame_bonus = self.fame_level * FAME_MULTIPLIER
        
        # Stress and health can affect income
        if self.stress > 80:
            fame_bonus *= 0.8  # 20% penalty if too stressed
        if self.health < 40:
            fame_bonus *= 0.6  # 40% penalty if unhealthy
            
        return base + fame_bonus
