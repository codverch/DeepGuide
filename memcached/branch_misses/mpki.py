# Read each line from mpki.txt and look for branch-misses:  or instructions:
import os
import re

if os.path.exists("BranchMissesCount.txt"):
    os.remove("BranchMissesCount.txt")
if os.path.exists("InstructionsCount.txt"):
    os.remove("InstructionsCount.txt")

with open("mpki.txt", "r"):
    for line in open("mpki.txt", "r"):
        if "branch-misses:" in line:
            # Write this line to "BranchMissesCount.txt"
            with open("BranchMissesCount.txt", "w") as file:
                file.write(line)
        if "instructions:" in line:
            # Write this line to "InstructionsCount.txt"
            with open("InstructionsCount.txt", "w") as file:
                file.write(line)

# ===========================================================================================================================

