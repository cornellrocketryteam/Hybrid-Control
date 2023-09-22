"""
main.py: The entry point for the hybrid control program
"""

from test_stand import TestStand
from controller import Controller

if __name__ == "__main__":
    controller = Controller()
    controller.run()