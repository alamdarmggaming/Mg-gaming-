"""
Game constants and configuration
"""

# Stat ranges
STAT_MIN = 0
STAT_MAX = 100

# Money ranges
STARTING_MONEY = 10000
MAX_DEBT = 100000

# Fame thresholds
FAME_UNKNOWN = 0
FAME_LOCAL = 20
FAME_REGIONAL = 40
FAME_NATIONAL = 60
FAME_INTERNATIONAL = 80
FAME_SUPERSTAR = 100

# Stat decay rates (per game month)
HEALTH_DECAY = 2
STRESS_GROWTH = 1.5
VOCAL_DECAY_NO_PRACTICE = 0.5

# Stat growth rates (per game month with activity)
VOCAL_GROWTH_PRACTICE = 2
SONGWRITING_GROWTH = 1.5
STAGEPRESENCE_GROWTH = 1
CREATIVITY_GROWTH = 0.5

# Money generation
BASE_SALARY = 500  # Monthly base income
FAME_MULTIPLIER = 100  # Money per fame level

# Stress relief
VACATION_STRESS_REDUCTION = 20
THERAPY_STRESS_REDUCTION = 15

# Game settings
GAME_MONTHS_PER_YEAR = 12
STARTING_AGE = 20
MAX_CAREER_LENGTH = 40  # years
