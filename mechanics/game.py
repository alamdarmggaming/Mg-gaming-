"""
Core game loop and main game logic
"""
from models.artist import Artist
from models.event import POSITIVE_EVENTS, NEGATIVE_EVENTS, CHOICE_EVENTS
from mechanics.progression import Progression
import random


class GameState:
    """Manages overall game state"""
    
    def __init__(self, artist: Artist):
        """Initialize game state
        
        Args:
            artist: The artist character
        """
        self.artist = artist
        self.current_month = 0
        self.current_year = 0
        self.is_running = True
        self.log = []
        
    def log_event(self, message: str) -> None:
        """Log a game event
        
        Args:
            message: Message to log
        """
        self.log.append(f"Month {self.current_month}: {message}")
    
    def advance_month(self) -> None:
        """Advance game by one month"""
        self.current_month += 1
        self.current_year = self.current_month // 12
        
        # Apply monthly decay
        decay_changes = Progression.monthly_stat_decay(self.artist)
        self.log_event(f"Monthly stat decay: {decay_changes}")
        
        # Monthly income
        income = self.artist.get_monthly_income()
        self.artist.modify_stat("money", income)
        self.log_event(f"Income received: ${income}")
        
        # Update contracts
        for contract in self.artist.contracts:
            contract.tick_month()
        
        # Check for random events
        self.check_random_events()
    
    def check_random_events(self) -> None:
        """Check for and trigger random events"""
        # Check positive events
        for event in POSITIVE_EVENTS:
            if event.should_trigger():
                effects = event.apply_to_artist(self.artist)
                self.log_event(f"✓ {event.title}: {effects}")
                return
        
        # Check negative events
        for event in NEGATIVE_EVENTS:
            if event.should_trigger():
                effects = event.apply_to_artist(self.artist)
                self.log_event(f"✗ {event.title}: {effects}")
                return
        
        # Chance for choice event
        if random.random() < 0.05:  # 5% chance
            event = random.choice(CHOICE_EVENTS)
            self.log_event(f"❓ {event.title}")
    
    def get_status(self) -> dict:
        """Get current game status
        
        Args:
            Returns: Dictionary with current status
        """
        return {
            "month": self.current_month,
            "year": self.current_year,
            "artist": self.artist.get_all_stats(),
            "fame_tier": Progression.calculate_fame_tier(self.artist.fame_level),
        }
    
    def end_game(self) -> None:
        """End the game"""
        self.is_running = False
        self.log_event("Game ended!")
    
    def print_status(self) -> None:
        """Print current game status"""
        status = self.get_status()
        
        print("\n" + "="*60)
        print(f"MONTH {status['month']} (Year {status['year']})")
        print(f"Artist: {status['artist']['name']} - {status['fame_tier']}")
        print("="*60)
        
        print(f"Fame Level: {status['artist']['fame_level']}/100")
        print(f"Money: ${status['artist']['money']:,.0f}")
        print(f"Debt: ${status['artist']['debt']:,.0f}")
        print()
        
        print("CORE TALENT:")
        print(f"  Vocal Ability: {status['artist']['vocal_ability']}")
        print(f"  Songwriting: {status['artist']['songwriting']}")
        print(f"  Stage Presence: {status['artist']['stage_presence']}")
        print(f"  Creativity: {status['artist']['creativity']}")
        print()
        
        print("PHYSICAL & MENTAL:")
        print(f"  Health: {status['artist']['health']}")
        print(f"  Stress: {status['artist']['stress']}")
        print(f"  Integrity: {status['artist']['integrity']}")
        print(f"  Appearance: {status['artist']['appearance']}")
        print()
        
        print("PERSONALITY:")
        print(f"  Ambition: {status['artist']['ambition']}")
        print(f"  Empathy: {status['artist']['empathy']}")
        print(f"  Work Ethic: {status['artist']['work_ethic']}")
        print()
        
        print("CAREER:")
        print(f"  Songs Released: {status['artist']['songs_released']}")
        print(f"  Concerts Performed: {status['artist']['concerts_performed']}")
        print(f"  Active Contracts: {status['artist']['contracts']}")
        print("="*60)


class GameMenu:
    """Main game menu and interaction"""
    
    def __init__(self):
        self.game = None
    
    def create_game(self) -> None:
        """Create a new game"""
        print("\n" + "="*60)
        print("WELCOME TO MG GAMING - MUSIC CAREER SIMULATOR")
        print("="*60)
        
        artist_name = input("\nEnter your artist name: ").strip()
        
        if not artist_name:
            artist_name = "Artist"
        
        self.game = GameState(Artist(artist_name))
        print(f"\nWelcome, {artist_name}! Your music career starts now...\n")
    
    def show_main_menu(self) -> str:
        """Show main menu and get player choice
        
        Returns:
            Player's choice
        """
        print("\n" + "-"*60)
        print("WHAT WOULD YOU LIKE TO DO?")
        print("-"*60)
        print("1. Practice Singing")
        print("2. Write Songs")
        print("3. Perform Concert")
        print("4. Rest")
        print("5. Therapy Session")
        print("6. View Status")
        print("7. View Log")
        print("8. Next Month")
        print("9. Quit Game")
        print("-"*60)
        
        return input("Choose action (1-9): ").strip()
    
    def handle_action(self, choice: str) -> bool:
        """Handle player action
        
        Args:
            choice: Player's menu choice
            
        Returns:
            False if game should end, True otherwise
        """
        if choice == "1":
            changes = Progression.practice_activity(self.game.artist)
            self.game.log_event(f"Practiced singing: {changes}")
            print("\n✓ You practiced singing!")
            
        elif choice == "2":
            changes = Progression.write_songs_activity(self.game.artist, 1)
            self.game.log_event(f"Wrote 1 song: {changes}")
            print("\n✓ You wrote a song!")
            
        elif choice == "3":
            changes = Progression.perform_concert_activity(self.game.artist)
            self.game.log_event(f"Performed concert: {changes}")
            print("\n✓ You performed an amazing concert!")
            
        elif choice == "4":
            changes = Progression.rest_activity(self.game.artist)
            self.game.log_event(f"Took rest: {changes}")
            print("\n✓ You took a well-deserved break!")
            
        elif choice == "5":
            changes = Progression.therapy_session(self.game.artist)
            self.game.log_event(f"Attended therapy: {changes}")
            print("\n✓ Therapy session complete!")
            
        elif choice == "6":
            self.game.print_status()
            
        elif choice == "7":
            print("\n" + "="*60)
            print("GAME LOG")
            print("="*60)
            for entry in self.game.log[-20:]:  # Show last 20 entries
                print(entry)
            
        elif choice == "8":
            self.game.advance_month()
            print(f"\n✓ Month advanced to {self.game.current_month}")
            
        elif choice == "9":
            print("\nThanks for playing MG Gaming!")
            return False
        
        else:
            print("\n✗ Invalid choice. Please try again.")
        
        return True
    
    def run(self) -> None:
        """Run the main game loop"""
        self.create_game()
        
        while self.game.is_running:
            try:
                choice = self.show_main_menu()
                if not self.handle_action(choice):
                    break
            except KeyboardInterrupt:
                print("\n\nGame interrupted!")
                break
            except Exception as e:
                print(f"\nError: {e}")
        
        print("\nGame Over!")
