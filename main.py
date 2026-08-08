import random, sys, time
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# =============================================
# UTILITY FUNCTIONS
# =============================================
def clamp(val, lo=0, hi=100):
    return max(lo, min(hi, val))

def money(val):
    return f"${val:,.0f}"

def colored(text, color):
    colors = {
        "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
        "blue": "\033[94m", "purple": "\033[95m", "cyan": "\033[96m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

# =============================================
# DATA CLASSES
# =============================================
@dataclass
class Skills:
    vocal: float = 30 + random.random()*20
    songwriting: float = 30 + random.random()*20
    production: float = 20 + random.random()*10
    performance: float = 20 + random.random()*15

@dataclass
class Health:
    physical: float = 80 + random.random()*15
    mental: float = 75 + random.random()*15
    voice: float = 90 + random.random()*10

@dataclass
class Personality:
    ambition: float = 60
    anxiety: float = 30
    empathy: float = 50
    hustle: float = 50
    discipline: float = 40

@dataclass
class Hidden:
    drugUse: float = 0.0
    alcohol: float = 0.0
    smoking: float = 0.0
    tendency: float = random.random()*30

@dataclass
class Social:
    subscribers: int = 0
    views: int = 0
    likes: int = 0
    posts: List[dict] = field(default_factory=list)

@dataclass
class Finance:
    cash: float = 200
    bankDebt: float = 0
    labelAdvance: float = 0
    labelRecoupment: float = 0
    monthlyExpenses: float = 50
    taxOwed: float = 0

@dataclass
class Relationships:
    family: float = 60+random.random()*20
    friends: float = 50+random.random()*30
    colleagues: float = 20+random.random()*20
    fans: float = 0
    press: float = 10+random.random()*10

@dataclass
class Career:
    status: str = "unknown"
    reputation: float = 0.0
    producer: Optional[dict] = None
    recorded: List[dict] = field(default_factory=list)
    released: List[dict] = field(default_factory=list)
    contracts: List[dict] = field(default_factory=list)
    legalIssues: List[str] = field(default_factory=list)

@dataclass
class Artist:
    name: str
    genre: str
    age: int = 19
    appearance: float = 50
    skills: Skills = field(default_factory=Skills)
    health: Health = field(default_factory=Health)
    personality: Personality = field(default_factory=Personality)
    hidden: Hidden = field(default_factory=Hidden)
    social: Social = field(default_factory=Social)
    finance: Finance = field(default_factory=Finance)
    relationships: Relationships = field(default_factory=Relationships)
    career: Career = field(default_factory=Career)
    history: List[str] = field(default_factory=list)
    week: int = 1
    alive: bool = True

    def apply_history(self, msg):
        self.history.append(msg)

    def clamp_stats(self):
        self.health.physical = clamp(self.health.physical)
        self.health.mental = clamp(self.health.mental)
        self.health.voice = clamp(self.health.voice)
        self.personality.anxiety = clamp(self.personality.anxiety)
        self.skills.vocal = clamp(self.skills.vocal)
        self.skills.songwriting = clamp(self.skills.songwriting)
        self.skills.production = clamp(self.skills.production)
        self.skills.performance = clamp(self.skills.performance)

# =============================================
# GAME ENGINE
# =============================================
class Game:
    def __init__(self):
        self.artist = None
        self.action_points = 3
        self.running = True

    # ---- CREATE ARTIST ----
    def create_artist(self):
        print("\n🎤 Welcome to APEX MUSIC: ICON")
        name = input("Enter artist name: ").strip() or "Riley Stone"
        genre = input("Genre (Pop/Rock/Hip-Hop/Electronic): ").strip() or "Pop"
        a = Artist(name=name, genre=genre)
        
        # Random backstory
        bg = random.random()
        if bg < 0.15:
            a.finance.cash += 300
            a.finance.monthlyExpenses = 100
            a.apply_history("Born into privilege — $500 allowance.")
        elif bg < 0.35:
            a.finance.bankDebt += 200
            a.apply_history("Student loan debt of $200.")
        elif bg < 0.6:
            a.health.mental -= 20
            a.personality.anxiety += 20
            a.apply_history("Childhood trauma — mental health down, anxiety up.")
        self.artist = a
        self.apply_background_effects()

    def apply_background_effects(self):
        # Example of butterfly: low mental health -> lower discipline
        if self.artist.health.mental < 50:
            self.artist.personality.discipline -= 10
            self.artist.apply_history("Low mental health makes discipline harder.")

    # ---- DISPLAY STATUS ----
    def display_status(self):
        a = self.artist
        print("\n" + "="*55)
        print(f"{colored('ARTIST:', 'cyan')} {a.name} ({a.genre}) | Age {a.age} | Week {a.week}")
        print(f"{colored('FANS:', 'blue')} {a.social.subscribers} | {colored('CASH:', 'green')} {money(a.finance.cash)}")
        print(f"{colored('HEALTH:', 'yellow')} Phys {a.health.physical:.1f} | Ment {a.health.mental:.1f} | Voice {a.health.voice:.1f}")
        print(f"{colored('STATUS:', 'purple')} {a.career.status.upper()} | AP: {'●'*self.action_points}{'○'*(3-self.action_points)}")
        print("="*55)

    def display_stats(self):
        a = self.artist
        print("\n-- SKILLS --")
        for k, v in a.skills.__dict__.items():
            bar = "#" * int(v/2)
            spaces = " " * (50 - len(bar))
            print(f"{k:15} | {bar}{spaces} | {v:.1f}/100")
        print("\n-- HEALTH --")
        for k, v in a.health.__dict__.items():
            print(f"{k:15} | {v:.1f}/100")
        print("\n-- PERSONALITY --")
        for k, v in a.personality.__dict__.items():
            print(f"{k:15} | {v:.1f}/100")
        print("\n-- RELATIONSHIPS --")
        for k, v in a.relationships.__dict__.items():
            print(f"{k:15} | {v:.1f}/100")

    # ---- ACTIONS ----
    def spend_ap(self):
        if self.action_points <= 0:
            print(colored("No action points left! Advance week first.", "red"))
            return False
        self.action_points -= 1
        return True

    def do_practice(self, skill):
        if not self.spend_ap(): return
        if skill not in self.artist.skills.__dict__:
            print("Invalid skill.")
            self.action_points += 1
            return
        gain = 2 + random.random()*3
        old = getattr(self.artist.skills, skill)
        setattr(self.artist.skills, skill, old+gain)
        self.artist.health.mental -= 2
        self.artist.personality.discipline += 1
        self.artist.apply_history(f"Practiced {skill} (+{gain:.1f})")

    def do_upload_video(self):
        if not self.spend_ap(): return
        a = self.artist
        q = (a.skills.vocal + a.skills.performance + a.skills.songwriting) / 3
        views = int((q/50) * random.randint(10, 50))
        if a.social.subscribers > 100:
            views *= a.social.subscribers // 50
        likes = int(views * random.random() * 0.05)
        subs = int(views * 0.005)
        a.social.subscribers += subs
        a.social.views += views
        a.social.likes += likes
        a.social.posts.append({"type":"video", "views":views, "likes":likes, "subs":subs})
        # Revenue
        rev = int(views * 0.0005)
        a.finance.cash += rev
        a.health.mental -= 3
        a.apply_history(f"Uploaded video: +{views} views, +{subs} subs, +${rev}")

    def do_record_track(self):
        if not self.spend_ap(): return
        a = self.artist
        if a.health.voice < 40:
            print(colored("Voice too damaged to record.", "red"))
            self.action_points += 1
            return
        if a.finance.cash < 30:
            print(colored("Need $30 for studio time.", "red"))
            self.action_points += 1
            return
        quality = a.skills.songwriting*0.4 + a.skills.vocal*0.3 + a.skills.production*0.2 + 5 + random.random()*10
        if a.career.producer:
            quality += a.career.producer["boost"]
        a.finance.cash -= 30
        a.health.voice -= 8
        a.health.mental -= 5
        a.career.recorded.append({"title":f"Demo {len(a.career.recorded)+1}", "quality": int(quality)})
        a.apply_history(f"Recorded track (quality: {int(quality)})")

    def do_release_track(self):
        if not self.spend_ap(): return
        a = self.artist
        if not a.career.recorded:
            print("No tracks recorded.")
            self.action_points += 1
            return
        track = a.career.recorded.pop(0)
        fans = int(track["quality"] * (a.social.subscribers/10 if a.social.subscribers > 100 else 1))
        rev = int(track["quality"] * 2)
        a.social.subscribers += fans
        a.finance.cash += rev
        a.career.released.append(track)
        a.relationships.fans += track["quality"]/5
        a.apply_history(f"Released \"{track['title']}\" (+{fans} fans, +${rev})")

    def do_busk(self):
        if not self.spend_ap(): return
        a = self.artist
        earned = int(a.skills.performance*0.2 + a.skills.vocal*0.1 + random.random()*20)
        a.finance.cash += earned
        a.health.voice -= 3
        a.health.mental -= 2
        a.relationships.colleagues += 1
        a.apply_history(f"Bussed: +${earned}")

    def do_rest(self):
        if not self.spend_ap(): return
        a = self.artist
        a.health.physical += 15
        a.health.mental += 10
        a.health.voice += 5
        a.personality.anxiety -= 5
        a.apply_history("Rested and recovered")

    def do_hire_producer(self):
        if not self.spend_ap(): return
        a = self.artist
        if a.career.producer:
            print("Already have a producer.")
            self.action_points += 1
            return
        if a.finance.cash < 100:
            print("Need $100 to hire producer.")
            self.action_points += 1
            return
        a.finance.cash -= 100
        a.career.producer = {"name":"Max Beatz", "boost":15}
        a.apply_history("Hired producer (Max Beatz) +15 track quality")

    def do_promote(self):
        if not self.spend_ap(): return
        a = self.artist
        if a.finance.cash < 50:
            print("Need $50 for promotion.")
            self.action_points += 1
            return
        a.finance.cash -= 50
        boost = random.randint(20, 50)
        a.social.likes += boost
        a.social.subscribers += int(boost*0.5)
        a.apply_history(f"Promoted music: +{boost} likes, +{int(boost*0.5)} subs")

    def do_network(self):
        if not self.spend_ap(): return
        a = self.artist
        a.relationships.colleagues += random.randint(5,15)
        a.personality.hustle += 2
        a.health.mental -= 2
        a.apply_history("Networking at industry event")

    def do_smoke(self):
        if not self.spend_ap(): return
        a = self.artist
        a.hidden.smoking += 5
        a.personality.anxiety -= 8
        a.health.physical -= 3
        a.apply_history("Smoked to calm nerves (-3 physical)")

    # ---- ADVANCE WEEK ----
    def advance_week(self):
        if self.action_points > 0:
            print(colored("You still have action points!", "yellow"))
            return
        a = self.artist
        a.week += 1
        # Month reset every 4 weeks
        if a.week % 4 == 0:
            a.finance.cash -= a.finance.monthlyExpenses
            a.finance.taxOwed += a.finance.cash * 0.05
            if a.finance.bankDebt > 0:
                a.finance.bankDebt *= 1.1
                a.apply_history(f"Bank interest added. Debt: {money(a.finance.bankDebt)}")
            if a.finance.labelRecoupment > 0:
                a.finance.labelRecoupment -= int(a.finance.labelAdvance*0.1)
                a.apply_history(f"Label recouped ${int(a.finance.labelAdvance*0.1)}")
            a.finance.taxOwed = max(0, a.finance.taxOwed - int(a.finance.taxOwed*0.5))  # auto tax half

        # Social decay
        a.social.likes = max(0, int(a.social.likes * 0.95))
        a.relationships.fans *= 0.97

        # Random events
        roll = random.random()
        if roll < 0.05:
            crisis = random.choice([
                "🔥 Scandal: old tweets resurfaced! Press -20",
                "🤒 Vocal cord nodule – voice -30, need surgery ($200)",
                "🏦 Loan shark demands $100",
                "😭 Mother sick – pay $150 or guilt",
                "⚖️ Lawsuit: copyright strike – pay $100 lawyer"
            ])
            if "Scandal" in crisis:
                a.relationships.press -= 20
            elif "Vocal" in crisis:
                a.health.voice = max(10, a.health.voice-30)
            elif "Loan" in crisis:
                a.finance.cash -= 100
            elif "Mother" in crisis:
                a.finance.cash -= 150
                a.relationships.family += 10
            else:
                a.finance.cash -= 100
                a.career.legalIssues.append("Copyright lawsuit")
            a.apply_history(crisis)
        elif roll < 0.15:
            ev = random.choice([
                "🎯 Met A&R rep (colleagues +15)",
                "💊 Offered drugs (hidden.drug +5, try? maybe)",
                "🎸 Wrote a great song (songwriting +5)",
                "😤 Bad review (press -10)",
                "🧠 Creative burst (songwriting +5, anxiety -5)"
            ])
            if "A&R" in ev:
                a.relationships.colleagues += 15
            elif "drugs" in ev:
                a.hidden.drugUse += 5
                if random.random() < 0.3:
                    a.hidden.drugUse += 10
            elif "great song" in ev:
                a.skills.songwriting += 5
            elif "Bad review" in ev:
                a.relationships.press -= 10
            else:
                a.skills.songwriting += 5
                a.personality.anxiety -= 5
            a.apply_history(ev)

        # Health decay
        a.health.physical -= 0.5
        a.health.mental -= 0.3
        a.health.voice -= 0.2

        # Check for mental collapse or death
        if a.health.mental < 10:
            a.alive = False
            a.apply_history("💀 Mental breakdown ended your life.")
        elif a.health.physical < 0:
            a.alive = False
            a.apply_history("💀 Severe illness ended your life.")

        a.clamp_stats()

        # Apply career phase
        fans = a.social.subscribers
        if fans > 100000: a.career.status = "superstar"
        elif fans > 10000: a.career.status = "mainstream"
        elif fans > 1000: a.career.status = "rising"
        elif fans > 100: a.career.status = "underground"

        # Reset action points
        self.action_points = 3

        # Show new week
        print("\n" + colored(f"--- WEEK {a.week} ---", "cyan"))

    # ---- EVENT LOOP ----
    def run(self):
        self.create_artist()
        print("\nYour journey begins...")

        while self.running:
            self.display_status()
            if not self.artist.alive:
                print(colored("GAME OVER – You died.", "red"))
                break
            print("\nWhat do you do? (type 'help' for commands)")
            cmd = input("> ").strip().lower()
            if cmd in ["quit","exit"]:
                self.running = False
            elif cmd == "help":
                self.show_help()
            elif cmd == "status":
                self.display_stats()
            elif cmd == "practice vocal": self.do_practice("vocal")
            elif cmd == "practice songwriting": self.do_practice("songwriting")
            elif cmd == "practice production": self.do_practice("production")
            elif cmd == "practice performance": self.do_practice("performance")
            elif cmd == "upload": self.do_upload_video()
            elif cmd == "record": self.do_record_track()
            elif cmd == "release": self.do_release_track()
            elif cmd == "busk": self.do_busk()
            elif cmd == "rest": self.do_rest()
            elif cmd == "hire": self.do_hire_producer()
            elif cmd == "promote": self.do_promote()
            elif cmd == "network": self.do_network()
            elif cmd == "smoke": self.do_smoke()
            elif cmd == "next": self.advance_week()
            else:
                print("Unknown command. Try 'help'.")

    def show_help(self):
        print("""
=== COMMANDS ===
  practice <skill>    – Practice vocal/songwriting/production/performance
  upload              – Upload YouTube video
  record              – Record track (costs $30, uses voice)
  release             – Release recorded track
  busk                – Street perform (earn cash)
  rest                – Recover energy
  hire                – Hire producer (costs $100)
  promote             – Boost social media (costs $50)
  network             – Meet industry people
  smoke               – Smoke to calm nerves (dangerous)
  status              – Show detailed stats
  next                – Advance to next week
  quit                – End game
""")

# =============================================
# MAIN
# =============================================
if __name__ == "__main__":
    game = Game()
    game.run()
