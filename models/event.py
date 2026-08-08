"""
Game events and random occurrences
"""
from enum import Enum
from typing import Callable, Optional
import random


class EventType(Enum):
    """Types of game events"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    CHOICE = "choice"


class Event:
    """Represents a game event"""
    
    def __init__(
        self,
        title: str,
        description: str,
        event_type: EventType,
        effects: dict,
        probability: float = 1.0
    ):
        """Initialize an event
        
        Args:
            title: Event title
            description: Event description
            event_type: Type of event
            effects: Dictionary of stat changes {stat_name: change_amount}
            probability: Chance of event occurring (0.0-1.0)
        """
        self.title = title
        self.description = description
        self.type = event_type
        self.effects = effects
        self.probability = probability
        
    def __repr__(self):
        return f"Event({self.title}, {self.type.value})"
    
    def should_trigger(self) -> bool:
        """Determine if this event should trigger"""
        return random.random() < self.probability
    
    def apply_to_artist(self, artist) -> dict:
        """Apply event effects to an artist
        
        Args:
            artist: Artist object to affect
            
        Returns:
            Dictionary of applied effects
        """
        applied = {}
        
        for stat, change in self.effects.items():
            if artist.modify_stat(stat, change):
                applied[stat] = change
        
        return applied


class ChoiceEvent(Event):
    """Event that requires player choice"""
    
    def __init__(
        self,
        title: str,
        description: str,
        choices: list,  # List of (choice_text, effects_dict) tuples
    ):
        """Initialize a choice event
        
        Args:
            title: Event title
            description: Event description
            choices: List of (choice_text, effects_dict) tuples
        """
        self.title = title
        self.description = description
        self.type = EventType.CHOICE
        self.choices = choices
        self.probability = 1.0
    
    def get_choice_options(self) -> list:
        """Get available choice options"""
        return [choice[0] for choice in self.choices]
    
    def apply_choice(self, artist, choice_index: int) -> dict:
        """Apply effects of a chosen option
        
        Args:
            artist: Artist object
            choice_index: Index of the chosen option
            
        Returns:
            Dictionary of applied effects
        """
        if choice_index < 0 or choice_index >= len(self.choices):
            return {}
        
        _, effects = self.choices[choice_index]
        applied = {}
        
        for stat, change in effects.items():
            if artist.modify_stat(stat, change):
                applied[stat] = change
        
        return applied


# Predefined events
POSITIVE_EVENTS = [
    Event(
        title="Hit Song Released",
        description="Your latest song went viral! Fans love it.",
        event_type=EventType.POSITIVE,
        effects={"fame_level": 15, "money": 50000, "stress": -10},
        probability=0.3
    ),
    Event(
        title="Award Nomination",
        description="You've been nominated for a major music award!",
        event_type=EventType.POSITIVE,
        effects={"fame_level": 10, "integrity": 5, "stress": -5},
        probability=0.2
    ),
    Event(
        title="Sold Out Concert",
        description="Your concert sold out in minutes!",
        event_type=EventType.POSITIVE,
        effects={"fame_level": 8, "money": 100000, "stage_presence": 2},
        probability=0.25
    ),
]

NEGATIVE_EVENTS = [
    Event(
        title="Vocal Injury",
        description="You've strained your voice. Recovery needed.",
        event_type=EventType.NEGATIVE,
        effects={"vocal_ability": -20, "health": -30, "stress": 15},
        probability=0.15
    ),
    Event(
        title="Leaked Private Content",
        description="Private content leaked online. Public backlash incoming.",
        event_type=EventType.NEGATIVE,
        effects={"fame_level": -10, "integrity": -20, "stress": 30},
        probability=0.1
    ),
    Event(
        title="Contract Dispute",
        description="Your label is claiming breach of contract.",
        event_type=EventType.NEGATIVE,
        effects={"money": -50000, "stress": 25, "integrity": -15},
        probability=0.12
    ),
]

CHOICE_EVENTS = [
    ChoiceEvent(
        title="Major Record Deal Offer",
        description="A top label is offering you a recording contract. Do you sign?",
        choices=[
            ("Sign the deal", {"fame_level": 20, "money": 200000, "stress": 10}),
            ("Decline - stay independent", {"fame_level": 5, "integrity": 10, "stress": -5}),
        ]
    ),
    ChoiceEvent(
        title="Tour Opportunity",
        description="An opportunity to go on a world tour. It will be grueling.",
        choices=[
            ("Go on tour", {"fame_level": 25, "money": 150000, "health": -20, "stress": 15}),
            ("Stay home", {"fame_level": 0, "health": 10, "stress": -10}),
        ]
    ),
]
