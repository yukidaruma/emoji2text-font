#!/usr/bin/env python3
"""
Centralized path definitions for the project.
"""

import os

_script_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(_script_dir)

# Input paths
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
SOURCE_FONTS_DIR = os.path.join(PROJECT_ROOT, "source-fonts")

EMOJI_TEST_FILE = os.path.join(DATA_DIR, "emoji-test.txt")
DEFAULT_SOURCE_FONT_FILE = os.path.join(SOURCE_FONTS_DIR, "SourceCodePro-Regular.otf")

# Output pathts
OUTPUT_DIR = os.path.join(os.getcwd(), "fonts")
