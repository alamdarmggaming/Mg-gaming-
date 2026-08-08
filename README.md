# MG Gaming - Music Career Simulation

A Python-based music career simulation game where you manage an artist's journey from unknown to superstar.

## Features
- **Artist Management**: Track vocal ability, songwriting, stage presence, and more
- **Career Progression**: Gain fame, earn money, manage contracts
- **Dynamic Events**: Face challenges, opportunities, and random events
- **Stat System**: Monitor health, stress, integrity, and other attributes
- **Decision Making**: Make choices that affect your artist's career path

## Project Structure
```
Mg-gaming-/
├── main.py              # Game entry point
├── models/
│   ├── artist.py        # Artist class definition
│   ├── event.py         # Game events system
│   └── contract.py      # Contract management
├── mechanics/
│   ├── game.py          # Core game loop
│   ├── progression.py   # Career progression logic
│   └── decisions.py     # Decision-making system
├── config/
│   └── constants.py     # Game constants and settings
└── utils/
    └── helpers.py       # Utility functions
```

## Getting Started
```bash
python main.py
```

## Requirements
- Python 3.8+
- No external dependencies (pure Python)
