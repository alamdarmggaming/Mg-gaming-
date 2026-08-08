#!/usr/bin/env python3
"""
MG Gaming - Music Career Simulation Game
Main entry point
"""

from mechanics.game import GameMenu


def main():
    """Main game entry point"""
    menu = GameMenu()
    menu.run()


if __name__ == "__main__":
    main()
