"""
Contract and record deal management
"""
from enum import Enum
from typing import Optional


class ContractType(Enum):
    """Types of contracts available"""
    RECORDING = "recording"
    ENDORSEMENT = "endorsement"
    TOUR = "tour"
    PUBLISHING = "publishing"


class Contract:
    """Represents a contract or record deal"""
    
    def __init__(
        self,
        name: str,
        contract_type: ContractType,
        advance: float = 0,
        royalty_rate: float = 0,
        duration_months: int = 12,
        requirements: Optional[dict] = None
    ):
        """Initialize a contract
        
        Args:
            name: Name/label of the contract
            contract_type: Type of contract
            advance: Upfront payment
            royalty_rate: Percentage of sales (0-100)
            duration_months: How long the contract lasts
            requirements: Dict of requirements (e.g., {"songs_per_year": 4})
        """
        self.name = name
        self.type = contract_type
        self.advance = advance
        self.royalty_rate = royalty_rate
        self.duration_months = duration_months
        self.requirements = requirements or {}
        self.active = True
        self.months_remaining = duration_months
        
    def __repr__(self):
        return f"Contract({self.name}, {self.type.value}, Advance: ${self.advance})"
    
    def is_active(self) -> bool:
        """Check if contract is still active"""
        return self.active and self.months_remaining > 0
    
    def tick_month(self) -> None:
        """Decrease contract duration by one month"""
        if self.months_remaining > 0:
            self.months_remaining -= 1
        
        if self.months_remaining == 0:
            self.active = False
    
    def check_requirements(self, artist_stats: dict) -> bool:
        """Check if artist is meeting contract requirements
        
        Args:
            artist_stats: Dictionary of artist stats
            
        Returns:
            True if all requirements are met
        """
        for requirement, value in self.requirements.items():
            # Add specific requirement checks here
            if requirement == "min_fame" and artist_stats.get("fame_level", 0) < value:
                return False
            if requirement == "min_health" and artist_stats.get("health", 0) < value:
                return False
        
        return True


class RecordingContract(Contract):
    """Record label contract"""
    
    def __init__(self, label_name: str, advance: float, royalty_rate: float, duration_months: int = 36):
        super().__init__(
            name=f"{label_name} Records",
            contract_type=ContractType.RECORDING,
            advance=advance,
            royalty_rate=royalty_rate,
            duration_months=duration_months,
            requirements={"min_fame": 10}
        )


class EndorsementContract(Contract):
    """Brand endorsement contract"""
    
    def __init__(self, brand_name: str, payment: float, duration_months: int = 12):
        super().__init__(
            name=f"{brand_name} Endorsement",
            contract_type=ContractType.ENDORSEMENT,
            advance=payment,
            royalty_rate=0,
            duration_months=duration_months,
            requirements={"min_fame": 20}
        )


class TourContract(Contract):
    """Concert tour contract"""
    
    def __init__(self, promoter_name: str, advance: float, duration_months: int = 6):
        super().__init__(
            name=f"{promoter_name} Tour",
            contract_type=ContractType.TOUR,
            advance=advance,
            royalty_rate=0,
            duration_months=duration_months,
            requirements={"min_fame": 30, "min_health": 60}
        )
