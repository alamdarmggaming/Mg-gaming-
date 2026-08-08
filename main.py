import random, sys, os
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# =============================================
# UTILITY
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
# YOUTUBE DEEP SYSTEM
# =============================================
@dataclass
class YouTubeStats:
    channelCreated: bool = False
    channelName: str = ""
    description: str = ""
    profilePic: str = "default"
    banner: str = "default"

    # Video settings
    editingSkill: float = 0.0   # Influence of editing on quality
    thumbQuality: float = 0.0   # Thumbnail clickability
    tags: List[str] = field(default_factory=list)

    # Performance
    totalViews: int = 0
    totalWatchTime: float = 0.0
    avgViewDuration: float = 0.0
    likes: int = 0
    comments: List[dict] = field(default_factory=list)  # {text, sentiment, author}
    clickRate: float = 0.0

    # Monetization
    revenue: float = 0.0
    rpm: float = 0.5  # Revenue per 1000 views in USD

    # Video library
    videos: List[str] = field(default_factory=list)

# =============================================
# INDUSTRY SYSTEM
# =============================================
@dataclass
class RecordLabel:
    name: str
    advance: float
    recoupment: float
    royaltyRate: float
    marketing: float
    status: str = "interested"  # interested, negotiating, signed, dropped

@dataclass
class Industry:
    labels: List[RecordLabel] = field(default_factory=list)
    activeLabel: Optional[RecordLabel] = None
    reputation: float = 0.0     # Industry gatekeepers opinion of you
    chartPosition: int = 0
    streamingMonthly: float = 0.0  # Monthly revenue from streaming platforms

# =============================================
# ARTIST CLASS (Extended)
# =============================================
@dataclass
class Artist:
    name: str
    genre: str
    age: int = 19
    appearance: float = 50

    skills: 'Skills' = field(default_factory=lambda: Skills())
    health: 'Health' = field(default_factory=lambda: Health())
    personality: 'Personality' = field(default_factory=lambda: Personality())
    hidden: 'Hidden' = field(default_factory=lambda: Hidden())

    youtube: YouTubeStats = field(default_factory=YouTubeStats)
    industry: Industry = field(default_factory=Industry)

    social: 'Social' = field(default_factory=lambda: Social())
    finance: 'Finance' = field(default_factory=lambda: Finance())
    relationships: 'Relationships' = field(default_factory=lambda: Relationships())
    career: 'Career' = field(default_factory=lambda: Career())

    history: List[str] = field(default_factory=list)
    week: int = 1
    alive: bool = True
    action_points: int = 3

    def clamp_stats(self):
        self.health.physical = clamp(self.health.physical)
        self.health.mental = clamp(self.health.mental)
        self.health.voice = clamp(self.health.voice)
        self.personality.anxiety = clamp(self.personality.anxiety)
        self.skills.vocal = clamp(self.skills.vocal)
        self.skills.songwriting = clamp(self.skills.songwriting)
        self.skills.production = clamp(self.skills.production)
        self.skills.performance = clamp(self.skills.performance)
        self.youtube.editingSkill = clamp(self.youtube.editingSkill)

    def apply_history(self, msg):
        self.history.append(msg)

# =============================================
# BASIC SKILLS, HEALTH, PERSONALITY ETC
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

# =============================================
# GAME ENGINE
# =============================================
class Game:
    def __init__(self):
        self.artist = None
        self.running = True

    # ---- CREATE ARTIST ----
    def create_artist(self):
        print("\n🎤 Welcome to APEX MUSIC: ICON")
        name = input("Artist name: ").strip() or "Riley Stone"
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

        # Generate some starting labels
        self.generate_labels()

    def generate_labels(self):
        names = ["HitForge Records", "IndieSoul", "MainStrike Music", "UrbanBeat"]
        for n in random.sample(names, 2):
            adv = random.randint(500, 5000)
            rec = random.randint(2, 5)  # multiplier
            roy = random.randint(5, 15)
            mkt = random.randint(100, 1000)
            label = RecordLabel(name=n, advance=adv, recoupment=rec, royaltyRate=roy, marketing=mkt)
            self.artist.industry.labels.append(label)

    # ---- DISPLAY ----
    def display_status(self):
        a = self.artist
        print("\n" + "="*60)
        print(f"{colored('ARTIST:', 'cyan')} {a.name} ({a.genre}) | Age {a.age} | Week {a.week}")
        print(f"{colored('FANS:', 'blue')} {a.social.subscribers} | SubsYT: {a.youtube.totalViews if a.youtube.channelCreated else 0} views | {colored('CASH:', 'green')} {money(a.finance.cash)}")
        print(f"{colored('HEALTH:', 'yellow')} Phys {a.health.physical:.1f} | Ment {a.health.mental:.1f} | Voice {a.health.voice:.1f}")
        print(f"{colored('STATUS:', 'purple')} {a.career.status.upper()} | Label: {a.industry.activeLabel.name if a.industry.activeLabel else 'None'} | Chart: #{a.industry.chartPosition}")
        print(f"AP: {'●'*a.action_points}{'○'*(3-a.action_points)}")
        print("="*60)

    def display_full_stats(self):
        a = self.artist
        print("\n-- SKILLS --")
        for k, v in a.skills.__dict__.items():
            bar = "#" * int(v/2)
            print(f"{k:15} | {bar:50.50} | {v:.1f}/100")
        print("\n-- YOUTUBE --")
        if a.youtube.channelCreated:
            print(f"Channel: {a.youtube.channelName}")
            print(f"Videos: {len(a.youtube.videos)} | Total Views: {a.youtube.totalViews}")
            print(f"Avg Click Rate: {a.youtube.clickRate:.2f}%")
            print(f"Editing Skill: {a.youtube.editingSkill:.1f} | Thumbnail: {a.youtube.thumbQuality:.1f}")
            print(f"Revenue: {money(a.youtube.revenue)}")
        else:
            print("No channel created yet (use 'create_channel')")
        print("\n-- INDUSTRY --")
        if a.industry.activeLabel:
            print(f"Label: {a.industry.activeLabel.name} | Advance: {money(a.industry.activeLabel.advance)} | Royalty: {a.industry.activeLabel.royaltyRate}%")
            print(f"Recoupment: x{a.industry.activeLabel.recoupment} | Marketing: {money(a.industry.activeLabel.marketing)}")
        else:
            print("No active label")
        print(f"Streaming Monthly: {money(a.industry.streamingMonthly)}")
        # Show available labels if any
        if a.industry.labels:
            print("\nLabels interested in you:")
            for lab in a.industry.labels:
                print(f"  - {lab.name} (Advance: {money(lab.advance)}, Royalty: {lab.royaltyRate}%)")
        print("\n-- HEALTH --")
        for k, v in a.health.__dict__.items():
            print(f"{k:15} | {v:.1f}/100")
        print("\n-- PERSONALITY --")
        for k, v in a.personality.__dict__.items():
            print(f"{k:15} | {v:.1f}/100")

    # ---- YOUTUBE SPECIFIC ACTIONS ----
    def create_channel(self):
        if self.artist.youtube.channelCreated:
            print("Channel already exists.")
            return
        a = self.artist
        a.youtube.channelCreated = True
        a.youtube.channelName = f"{a.name} Official"
        a.youtube.description = f"Music from {a.name}"
        print(f"Channel created: {a.youtube.channelName}")

    def upload_video(self):
        a = self.artist
        if not a.youtube.channelCreated:
            print("Create channel first!")
            return
        if a.action_points <= 0:
            print("No AP!")
            return

        # Choose quality
        print("\nUpload Video Options:")
        print("1. 720p (Cheap, low quality)")
        print("2. 1080p (Standard, moderate)")
        print("3. 1440p (4K, expensive but high quality)")
        res = input("Choose resolution (1/2/3): ").strip()
        res_cost = {"1": 10, "2": 30, "3": 100}
        res_name = {"1": "720p", "2": "1080p", "3": "1440p"}
        if res not in res_cost:
            print("Invalid choice.")
            return
        cost = res_cost[res]
        if a.finance.cash < cost:
            print("Not enough cash for video production.")
            return

        # Editing quality investment
        print("\nEditing quality: how much do you want to spend?")
        print("0. No editing (free, low quality)")
        print("1. Basic ($20)")
        print("2. Professional ($50)")
        edit_choice = input("Choose (0/1/2): ").strip()
        editing_cost = {"0": 0, "1": 20, "2": 50}
        edit_name = {"0": "raw", "1": "basic", "2": "professional"}
        if edit_choice not in editing_cost:
            edit_choice = "0"
        edit_cost = editing_cost[edit_choice]

        # Time: each upload takes a week
        a.finance.cash -= (cost + edit_cost)

        # Determine quality
        base_quality = (a.skills.vocal + a.skills.performance + a.skills.songwriting)/3
        editing_bonus = 0
        if edit_choice == "1": editing_bonus += 5 + random.random()*5
        elif edit_choice == "2": editing_bonus += 15 + random.random()*10
        if res == "1": quality = base_quality * 0.8
        elif res == "2": quality = base_quality
        else: quality = base_quality * 1.2
        quality += editing_bonus

        # Generate views based on subscribers, tags, click rate
        subscribers = a.social.subscribers if a.social.subscribers > 0 else 1
        views = int((quality / 100) * (50 + random.random()*100) * (1 + subscribers/5000))
        if a.youtube.clickRate < 2:
            views = int(views * 0.5)
        elif a.youtube.clickRate > 6:
            views = int(views * 1.5)
        likes = int(views * random.random() * 0.04)
        comments = self.generate_comments(views, quality, a.career.status)

        # Update stats
        a.youtube.totalViews += views
        a.youtube.likes += likes
        a.youtube.videos.append(f"Video #{len(a.youtube.videos)+1} ({res_name[res]}, {edit_name[edit_choice]})")
        a.social.views += views
        a.social.likes += likes
        a.social.subscribers += int(views*0.01)

        # Revenue
        revenue = int(views * 0.0003)  # Base
        if res == "3":
            revenue *= 1.2
        a.youtube.revenue += revenue
        a.finance.cash += revenue
        a.finance.monthlyExpenses += revenue * 0.1  # taxes

        # Track watch time (for algorithm)
        watch_time = views * (0.5 + random.random()) * (0.7 if res == "1" else 1.2)
        a.youtube.totalWatchTime += watch_time
        a.youtube.avgViewDuration = a.youtube.totalWatchTime / a.youtube.totalViews if a.youtube.totalViews else 0

        # Comments to display
        print(f"\nVideo uploaded: {res_name[res]} | {edit_name[edit_choice]} | ${edit_cost} editing")
        print(f"Views: {views} | Likes: {likes} | Subscribers gained: +{int(views*0.01)}")
        print(f"Revenue: +${revenue}")
        if comments:
            print("\nComments:")
            for c in comments[:3]:
                print(f"  {c['author']}: {c['text']} ({c['sentiment']})")

        a.action_points -= 1
        a.health.mental -= 5
        a.health.voice -= 3 if res != "1" else 1

    def generate_comments(self, views, quality, status):
        comments = []
        if views < 50: return comments
        # Positive comments if quality high
        if quality > 50:
            positive = [
                "AMAZING VOICE!🔥", "This is going on repeat!", 
                "How does this not have more views?",
                "The editing is top notch! 👏",
                "You deserve more recognition!"
            ]
            for i in range(random.randint(0,3)):
                comments.append({"author": f"fan{i+1}", "text": random.choice(positive), "sentiment": "positive"})
        else:
            negative = [
                "I've seen better.", "This is mid.",
                "Fake voice?", "You need more practice."
            ]
            for i in range(random.randint(0,2)):
                comments.append({"author": f"hater{i+1}", "text": random.choice(negative), "sentiment": "negative"})

        # Some neutral
        neutrals = ["Nice melody", "Kinda good", "Interesting vibe"]
        for i in range(random.randint(0,4)):
            comments.append({"author": f"user{i+1}", "text": random.choice(neutrals), "sentiment": "neutral"})

        return comments

    def optimize_thumbnail(self):
        a = self.artist
        if a.action_points <= 0:
            print("No AP")
            return
        if not a.youtube.channelCreated:
            print("Create channel first")
            return
        # Simulate A/B testing
        if a.finance.cash < 10:
            print("Need $10 for thumbnail tools")
            return
        a.finance.cash -= 10
        improvement = random.randint(1,10)
        a.youtube.thumbQuality += improvement
        a.youtube.clickRate += improvement * 0.1
        a.apply_history(f"Optimized thumbnail: +{improvement} click rate")
        a.action_points -= 1
        print(f"Thumbnail improved! Click rate now {a.youtube.clickRate:.1f}%")

    # ---- INDUSTRY ACTIONS ----
    def sign_label(self, label):
        a = self.artist
        if a.industry.activeLabel:
            print("Already signed.")
            return
        if not label in a.industry.labels:
            print("Label not available")
            return
        a.industry.activeLabel = label
        a.industry.labels.remove(label)
        a.finance.cash += label.advance
        a.finance.labelAdvance = label.advance
        a.finance.labelRecoupment = label.advance * label.recoupment
        a.apply_history(f"Signed with {label.name} received advance ${label.advance}")
        print(f"Signed with {label.name}! Advance: {money(label.advance)}")
        a.action_points -= 1

    def release_song_to_industry(self):
        a = self.artist
        if a.action_points <= 0:
            print("No AP")
            return
        if not a.career.recorded:
            print("No tracks to release.")
            return
        track = a.career.recorded.pop(0)
        quality = track["quality"]

        # Streaming revenue calculation
        streams = int(quality * 500 * (1.5 if a.industry.activeLabel else 1))
        rev = streams * a.industry.activeLabel.royaltyRate/100  # Only if label
        if not a.industry.activeLabel:
            rev = streams * 0.01  # no label = less exposure
        a.industry.streamingMonthly += rev
        a.finance.cash += rev
        a.social.subscribers += int(streams*0.001)
        a.career.released.append(track)

        # Chart position update
        old = a.industry.chartPosition
        a.industry.chartPosition = int((a.social.subscribers/1000) * (quality/100))
        if a.industry.chartPosition > 0 and old == 0:
            a.apply_history(f"Entered charts at #{a.industry.chartPosition}!")

        a.apply_history(f"Released '{track['title']}' -> +{streams} streams, +${rev}")
        print(f"Released to streaming: {streams} streams, +${rev}")
        a.action_points -= 1

    # ---- GENERAL ACTIONS ----
    def spend_ap(self):
        if self.artist.action_points <= 0:
            print(colored("No action points left!", "red"))
            return False
        self.artist.action_points -= 1
        return True

    def do_practice(self, skill):
        if not self.spend_ap(): return
        a = self.artist
        if skill not in a.skills.__dict__: print("Invalid"); self.artist.action_points += 1; return
        gain = 2 + random.random()*3
        setattr(a.skills, skill, getattr(a.skills, skill) + gain)
        a.health.mental -= 2
        a.apply_history(f"Practiced {skill} (+{gain:.1f})")

    def do_rest(self):
        if not self.spend_ap(): return
        a = self.artist
        a.health.physical += 15
        a.health.mental += 10
        a.health.voice += 5
        a.personality.anxiety -= 5
        a.apply_history("Rested")

    def do_record(self):
        if not self.spend_ap(): return
        a = self.artist
        if a.health.voice < 40: print("Voice damaged"); self.artist.action_points += 1; return
        if a.finance.cash < 40: print("Need $40 for studio"); self.artist.action_points += 1; return
        quality = a.skills.songwriting*0.4 + a.skills.vocal*0.3 + a.skills.production*0.2 + 5 + random.random()*10
        if a.career.producer: quality += a.career.producer["boost"]
        a.finance.cash -= 40
        a.health.voice -= 8
        a.career.recorded.append({"title": f"Track {len(a.career.recorded)+1}", "quality": int(quality)})
        a.apply_history(f"Recorded track (q:{int(quality)})")
        print(f"Recorded a track! Quality: {int(quality)}")

    def do_busk(self):
        if not self.spend_ap(): return
        a = self.artist
        earned = int(a.skills.performance*0.2 + a.skills.vocal*0.1 + random.random()*20)
        a.finance.cash += earned
        a.health.voice -= 3
        a.relationships.colleagues += 1
        a.apply_history(f"Bussed, +${earned}")

    def do_hire_producer(self):
        if not self.spend_ap(): return
        a = self.artist
        if a.career.producer: print("Already have"); self.artist.action_points += 1; return
        if a.finance.cash < 150:
            print("Need $150 for producer")
            self.artist.action_points += 1
            return
        a.finance.cash -= 150
        a.career.producer = {"name":"Max", "boost":20}
        a.apply_history("Hired producer Max (+20 quality)")
        print("Hired producer!")

    # ---- ADVANCE WEEK ----
    def advance_week(self):
        a = self.artist
        if a.action_points > 0:
            print("You still have AP. Use them or type 'skip'")
            return
        a.week += 1
        # Month reset
        if a.week % 4 == 0:
            a.finance.cash -= a.finance.monthlyExpenses
            if a.finance.cash < 0:
                a.finance.bankDebt += abs(a.finance.cash)
                a.finance.cash = 0
            if a.finance.bankDebt > 0:
                a.finance.bankDebt *= 1.1
            # Taxes
            a.finance.taxOwed += a.finance.cash * 0.05
            if a.finance.taxOwed > 0:
                a.finance.taxOwed -= int(a.finance.taxOwed*0.5)
            # Label recoupment
            if a.industry.activeLabel and a.finance.labelRecoupment > 0:
                recoup = int(a.finance.labelAdvance*0.1)
                a.finance.labelRecoupment -= recoup
                a.apply_history(f"Label deducts ${recoup} from margin")

        # Social media decay
        a.youtube.clickRate = max(0.5, a.youtube.clickRate - 0.1)
        a.relationships.fans = max(0, a.relationships.fans - 1)

        # Random events (expand)
        roll = random.random()
        if roll < 0.04:
            msg = "🔥 Scandal! Press relations down 20"
            a.relationships.press -= 20
            a.apply_history(msg)
        elif roll < 0.08:
            msg = "📈 Viral moment! Subscribers +1000, views +5000"
            a.social.subscribers += 1000
            a.youtube.totalViews += 5000
            a.apply_history(msg)
        elif roll < 0.15:
            msg = "💪 Got a feature with a big artist!"
            a.relationships.colleagues += 10
            a.social.subscribers += 200
            a.apply_history(msg)

        # Health decay
        a.health.physical -= 0.5
        a.health.mental -= 0.3
        a.health.voice -= 0.2
        if a.health.mental < 10:
            a.alive = False
        if a.health.physical < 0:
            a.alive = False

        a.clamp_stats()
        a.action_points = 3

        # Career status update
        fans = a.social.subscribers
        if fans > 100000: a.career.status = "superstar"
        elif fans > 10000: a.career.status = "mainstream"
        elif fans > 1000: a.career.status = "rising"
        elif fans > 100: a.career.status = "underground"

        print(f"\n{colored('--- WEEK '+str(a.week)+' ---','cyan')}")
        # Show label offers if any
        if a.industry.labels and not a.industry.activeLabel:
            print("New label offers!")
            for lab in a.industry.labels:
                print(f"  {lab.name} offers {money(lab.advance)} advance, {lab.royaltyRate}% royalty, recoupment x{lab.recoupment}")

    # ---- HELP ----
    def show_help(self):
        print("""
=== GENERAL ACTIONS ===
 practice <skill>   – vocal, songwriting, production, performance
 record             – Record vocal track (needs $40)
 release            – Release recorded track to streaming
 busk               – Street perform for cash
 rest               – Recover health & energy
 hire               – Hire producer ($150)
 create_channel     – Create YouTube channel
 upload             – Upload video with quality options
 thumbnail          – Improve thumbnail/click rate
 sign label <name>  – Sign with interested label (use exact name)
 status             – Show full stats
 next               – Advance to next week
 quit               – End game
""")

    # ---- RUN ----
    def run(self):
        self.create_artist()
        print("\nYour journey begins...")
        while self.running:
            self.display_status()
            if not self.artist.alive:
                print(colored("GAME OVER – You died.", "red"))
                break
            cmd = input("> ").strip().lower()
            if cmd in ["quit", "exit"]:
                self.running = False
            elif cmd == "help": self.show_help()
            elif cmd == "status": self.display_full_stats()
            elif cmd == "create_channel": self.create_channel()
            elif cmd == "upload": self.upload_video()
            elif cmd == "thumbnail": self.optimize_thumbnail()
            elif cmd.startswith("sign label "):
                name = cmd[11:].strip().lower()
                label = next((l for l in self.artist.industry.labels if l.name.lower() == name), None)
                if label: self.sign_label(label)
                else: print("Label not found. Use 'status' to see labels.")
            elif cmd == "release": self.release_song_to_industry()
            elif cmd.startswith("practice "): self.do_practice(cmd[9:].strip())
            elif cmd == "record": self.do_record()
            elif cmd == "busk": self.do_busk()
            elif cmd == "rest": self.do_rest()
            elif cmd == "hire": self.do_hire_producer()
            elif cmd == "next": self.advance_week()
            else:
                print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    game = Game()
    game.run()
