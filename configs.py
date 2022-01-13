import sys

# Core
token = "TOKEN"
if(token == ""):
    print("Please enter a discord token in the configs.py file.")
    sys.exit(0)

# Basics
prefix = ">"

# Logger
logger = False
logFormat = "log"  # be sure not to put a dot in here

# Misc
statusCycleTimer = 300  # Measured in seconds. Do not make this too fast.
