"""
Dark Web Marketplace System
Complete illegal track marketplace, cryptocurrency, and criminal activities
"""
from dataclasses import dataclass, field
from typing import List, Optional
import random

@dataclass
class DarkTrack:
    """Stolen/illegal track on dark web"""
    id: str
    title: str
    quality: int
    price_btc: float
    price_usd: float
    seller: str
    category: str  # "stolen", "bootleg", "unreleased", "sample_pack"
    heat_level: int  # 1-10, how likely to get caught buying this
    
    def __repr__(self):
        return f"🕸️ {self.title} | Q:{self.quality} | {self.price_btc:.3f} BTC | Heat:{self.heat_level}/10"

@dataclass
class DarkWebMarket:
    """Dark web marketplace"""
    available_tracks: List[DarkTrack] = field(default_factory=list)
    user_purchases: List[dict] = field(default_factory=list)
    reputation: float = 0.0  # Street cred (0-100)
    heat_level: int = 0  # FBI/DEA attention
    
    def add_heat(self, amount: int):
        """Increase heat"""
        self.heat_level = min(100, self.heat_level + amount)
    
    def reduce_heat(self, amount: int):
        """Reduce heat (through bribes, etc)"""
        self.heat_level = max(0, self.heat_level - amount)

@dataclass
class Cryptocurrency:
    """Bitcoin and crypto wallet"""
    bitcoin: float = 0.0
    ethereum: float = 0.0
    monero: float = 0.0  # Most private
    total_value: float = 0.0
    
    def add_bitcoin(self, amount: float):
        self.bitcoin += amount
        self.recalc_total()
    
    def spend_bitcoin(self, amount: float) -> bool:
        if self.bitcoin >= amount:
            self.bitcoin -= amount
            self.recalc_total()
            return True
        return False
    
    def recalc_total(self):
        """Recalculate total value"""
        # Simplified rates
        self.total_value = self.bitcoin * 50000 + self.ethereum * 3000 + self.monero * 40000

@dataclass
class CriminalRecord:
    """Track criminal history and consequences"""
    arrests: int = 0
    convictions: int = 0
    jail_time: int = 0  # weeks served
    current_sentence: int = 0  # weeks remaining
    
    crimes_committed: dict = field(default_factory=dict)  # {crime_type: count}
    
    # Federal charges
    dea_charges: int = 0  # Drug charges
    fbi_charges: int = 0  # Identity theft, hacking
    irs_charges: int = 0  # Tax evasion
    
    # Bounties
    undercover_cops: int = 0  # Number tracking you
    syndicate_enemy: bool = False  # Made enemy of crime org
    
    def add_crime(self, crime_type: str):
        """Log a crime"""
        if crime_type not in self.crimes_committed:
            self.crimes_committed[crime_type] = 0
        self.crimes_committed[crime_type] += 1
    
    def get_wanted_status(self) -> str:
        if self.dea_charges >= 5 and self.fbi_charges >= 3:
            return "FEDERAL FUGITIVE"
        elif self.dea_charges >= 3:
            return "WANTED BY DEA"
        elif self.fbi_charges >= 2:
            return "WANTED BY FBI"
        elif self.arrests >= 3:
            return "HABITUAL CRIMINAL"
        return "CLEAN"

@dataclass
class UndergroundNetwork:
    """Connect with criminal organizations"""
    connected_to_cartel: bool = False
    connected_to_hacker_collective: bool = False
    connected_to_money_laundering_ring: bool = False
    
    cartel_missions: int = 0
    hacker_jobs: int = 0
    money_laundering_jobs: int = 0
    
    # Relationships
    cartel_reputation: float = 0.0
    hacker_reputation: float = 0.0
    launderer_trust: float = 0.0
