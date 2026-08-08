"""
Career progression logic and stat changes
"""
from config.constants import (
    HEALTH_DECAY, STRESS_GROWTH, VOCAL_DECAY_NO_PRACTICE,
    VOCAL_GROWTH_PRACTICE, SONGWRITING_GROWTH, STAGEPRESENCE_GROWTH,
    CREATIVITY_GROWTH, BASE_SALARY, FAME_MULTIPLIER
)


class Progression:
    """Handles artist career progression"""
    
    @staticmethod
    def monthly_stat_decay(artist) -> dict:
        """Apply monthly stat decay
        
        Args:
            artist: Artist object
            
        Returns:
            Dictionary of changes applied
        """
        changes = {}
        
        # Health naturally decays
        artist.modify_stat("health", -HEALTH_DECAY)
        changes["health"] = -HEALTH_DECAY
        
        # Stress naturally increases
        artist.modify_stat("stress", STRESS_GROWTH)
        changes["stress"] = STRESS_GROWTH
        
        # Vocal ability decays without practice
        artist.modify_stat("vocal_ability", -VOCAL_DECAY_NO_PRACTICE)
        changes["vocal_ability"] = -VOCAL_DECAY_NO_PRACTICE
        
        return changes
    
    @staticmethod
    def practice_activity(artist, hours: int = 10) -> dict:
        """Artist practices singing
        
        Args:
            artist: Artist object
            hours: Hours spent practicing
            
        Returns:
            Dictionary of changes
        """
        changes = {}
        
        # Vocal ability increases with practice
        vocal_gain = (VOCAL_GROWTH_PRACTICE * hours) / 10
        artist.modify_stat("vocal_ability", vocal_gain)
        changes["vocal_ability"] = vocal_gain
        
        # Health slightly improves (exercise)
        artist.modify_stat("health", hours * 0.5)
        changes["health"] = hours * 0.5
        
        # Stress slightly decreases
        artist.modify_stat("stress", -hours * 0.3)
        changes["stress"] = -hours * 0.3
        
        return changes
    
    @staticmethod
    def write_songs_activity(artist, songs: int = 1) -> dict:
        """Artist writes new songs
        
        Args:
            artist: Artist object
            songs: Number of songs to write
            
        Returns:
            Dictionary of changes
        """
        changes = {}
        
        # Songwriting improves
        songwriting_gain = SONGWRITING_GROWTH * songs
        artist.modify_stat("songwriting", songwriting_gain)
        changes["songwriting"] = songwriting_gain
        
        # Creativity improves
        creativity_gain = CREATIVITY_GROWTH * songs
        artist.modify_stat("creativity", creativity_gain)
        changes["creativity"] = creativity_gain
        
        # Track songs
        artist.songs_released += songs
        changes["songs_released"] = songs
        
        # Mental strain
        artist.modify_stat("stress", songs * 2)
        changes["stress"] = songs * 2
        
        return changes
    
    @staticmethod
    def perform_concert_activity(artist) -> dict:
        """Artist performs a concert
        
        Args:
            artist: Artist object
            
        Returns:
            Dictionary of changes
        """
        changes = {}
        
        # Stage presence improves
        artist.modify_stat("stage_presence", STAGEPRESENCE_GROWTH * 2)
        changes["stage_presence"] = STAGEPRESENCE_GROWTH * 2
        
        # Health decreases (physical toll)
        artist.modify_stat("health", -15)
        changes["health"] = -15
        
        # Stress increases before performance
        artist.modify_stat("stress", 10)
        changes["stress"] = 10
        
        # Money earned
        income = artist.get_monthly_income() * 2
        artist.modify_stat("money", income)
        changes["money"] = income
        
        # Fame increases if health is good
        if artist.health > 60:
            fame_gain = 5
            artist.modify_stat("fame_level", fame_gain)
            changes["fame_level"] = fame_gain
        
        artist.concerts_performed += 1
        changes["concerts_performed"] = 1
        
        return changes
    
    @staticmethod
    def rest_activity(artist, days: int = 7) -> dict:
        """Artist takes a break to rest
        
        Args:
            artist: Artist object
            days: Days of rest
            
        Returns:
            Dictionary of changes
        """
        changes = {}
        
        # Health recovers
        health_gain = days * 2
        artist.modify_stat("health", health_gain)
        changes["health"] = health_gain
        
        # Stress decreases significantly
        stress_reduction = days * 1.5
        artist.modify_stat("stress", -stress_reduction)
        changes["stress"] = -stress_reduction
        
        # Money spent on vacation
        vacation_cost = 5000 * (days / 7)
        artist.modify_stat("money", -vacation_cost)
        changes["money"] = -vacation_cost
        
        return changes
    
    @staticmethod
    def therapy_session(artist) -> dict:
        """Artist attends therapy
        
        Args:
            artist: Artist object
            
        Returns:
            Dictionary of changes
        """
        changes = {}
        
        # Stress significantly reduces
        artist.modify_stat("stress", -25)
        changes["stress"] = -25
        
        # Integrity improves (self-care)
        artist.modify_stat("integrity", 5)
        changes["integrity"] = 5
        
        # Empathy improves (through reflection)
        artist.modify_stat("empathy", 3)
        changes["empathy"] = 3
        
        # Cost
        therapy_cost = 2000
        artist.modify_stat("money", -therapy_cost)
        changes["money"] = -therapy_cost
        
        return changes
    
    @staticmethod
    def calculate_fame_tier(fame_level: int) -> str:
        """Get fame tier description
        
        Args:
            fame_level: Current fame level
            
        Returns:
            Fame tier description
        """
        from config.constants import (
            FAME_UNKNOWN, FAME_LOCAL, FAME_REGIONAL,
            FAME_NATIONAL, FAME_INTERNATIONAL, FAME_SUPERSTAR
        )
        
        if fame_level < FAME_LOCAL:
            return "Unknown Artist"
        elif fame_level < FAME_REGIONAL:
            return "Local Celebrity"
        elif fame_level < FAME_NATIONAL:
            return "Regional Star"
        elif fame_level < FAME_INTERNATIONAL:
            return "National Star"
        elif fame_level < FAME_SUPERSTAR:
            return "International Star"
        else:
            return "SUPERSTAR"
