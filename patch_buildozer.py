#!/usr/bin/env python3
"""Patch buildozer to skip aidl check.
New Android build-tools (34+) removed aidl, but buildozer still checks for it.
This patches the _check_aidl method to simply return without checking.
"""
import sys

# Find android.py path
import os
import glob

# Search common site-packages locations
possible_paths = [
    os.path.expanduser('~/.local/lib/python*/site-packages/buildozer/targets/android.py'),
    'lib/python*/site-packages/buildozer/targets/android.py',
]

android_py = None
for pattern in possible_paths:
    found = glob.glob(pattern)
    if found:
        android_py = found[0]
        break

# Also try via pip
if not android_py:
    import subprocess
    result = subprocess.run(
        ['python3', '-c', 'import buildozer.targets.android as m; print(m.__file__)'],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode == 0 and result.stdout.strip():
        android_py = result.stdout.strip()

if not android_py:
    print("ERROR: Could not find buildozer/targets/android.py")
    sys.exit(1)

print(f"Patching: {android_py}")

with open(android_py, 'r') as f:
    lines = f.readlines()

new_lines = []
patched = False
in_check_aidl = False

for line in lines:
    if "def _check_aidl(self" in line:
        new_lines.append(line)
        new_lines.append("    self.buildozer.debug('aidl check skipped - patched')\n")
        new_lines.append("    return\n")
        in_check_aidl = True
        patched = True
        continue

    if in_check_aidl:
        # Skip all lines until we hit the next method or class-level code
        # Method body lines are indented with 8+ spaces
        if line.strip() == '' or line.startswith('        '):
            continue  # skip old method body
        else:
            in_check_aidl = False
            new_lines.append(line)
            continue

    new_lines.append(line)

if not patched:
    print("ERROR: Could not find _check_aidl method!")
    sys.exit(1)

with open(android_py, 'w') as f:
    f.writelines(new_lines)

print("Patch applied successfully!")
