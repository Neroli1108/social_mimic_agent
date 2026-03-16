#!/usr/bin/env python3
"""Social Simulation Engine — Pygame UI entry point."""
from game.engine import GameEngine


def main():
    engine = GameEngine()
    engine.run()


if __name__ == '__main__':
    main()
