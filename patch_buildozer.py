#!/usr/bin/env python3
"""Patch buildozer to skip aidl check."""
import sys
import subprocess
import os

# Find android.py via Python
result = subprocess.run(
    [sys.executable, '-c', 'import buildozer.targets.android as m; print(m.__file__)'],
    capture_output=True, text=True, timeout=10
)
if result.returncode != 0:
    print(f"ERROR: {result.stderr}")
    sys.exit(1)

android_py = result.stdout.strip()
print(f"Patching: {android_py}")

with open(android_py, 'r') as f:
    content = f.read()

# Find and replace the entire _check_aidl method
# Match from "def _check_aidl" to the next method or end of class
import re

# Pattern: match the method def + everything until next def at same indent level or end
pattern = r"(    def _check_aidl\(self, v_build_tools\):)\n(        .+?\n)*?(?=\n    def |\n    @|\nclass |\Z)"

replacement = """    def _check_aidl(self, v_build_tools):
        self.buildozer.debug('aidl check skipped - patched')
        return
"""

new_content, count = re.subn(pattern, replacement, content)

if count == 0:
    print("ERROR: Could not find _check_aidl method!")
    sys.exit(1)

with open(android_py, 'w') as f:
    f.write(new_content)

print("Patch applied successfully!")
