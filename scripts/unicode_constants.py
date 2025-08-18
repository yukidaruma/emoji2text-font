#!/usr/bin/env python3
"""
Unicode constants for emoji processing.
"""

# ASCII constants
ASCII_DIGIT_0 = 0x30
ASCII_DIGIT_9 = 0x39
ASCII_SMALL_A = 0x61
ASCII_SMALL_Z = 0x7A

# Regional Indicator Symbols (A-Z)
REGIONAL_INDICATOR_A = 0x1F1E6
REGIONAL_INDICATOR_Z = 0x1F1FF

# Other special emoji characters
ZWJ = 0x200D  # Zero Width Joiner


# Below are codepoints that appear in emoji-test.txt but are not used in scripts

# Combining and control characters used in emoji sequences
VARIATION_SELECTOR_16 = 0xFE0F  # Forces sequence in emoji style
COMBINING_KEYCAP = 0x20E3
CANCEL_TAG = 0xE007F

# Tag Latin Small Letters
TAG_LATIN_SMALL_A = 0xE0061
TAG_LATIN_SMALL_Z = 0xE007A
