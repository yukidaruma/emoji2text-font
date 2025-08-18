#!/usr/bin/env python3
"""
Parses Unicode emoji-test.txt data to extract emoji names.
"""

import re
import os
from typing import Dict, List, Tuple, Optional
from unicode_constants import ZWJ, REGIONAL_INDICATOR_A, REGIONAL_INDICATOR_Z
from paths import EMOJI_TEST_FILE


def _normalize_emoji_name(emoji_name: str) -> str:
    """Normalize emoji name to snake_case format."""

    # Handle special cases for flags and keycaps
    if ':' in emoji_name:
        if emoji_name.startswith(('flag:', 'keycap:')):
            _, suffix = emoji_name.split(':', 1)
            emoji_name = f"flag_{suffix.strip().lower()}"
        else:
            emoji_name = emoji_name.split(':')[0].strip()

    name = emoji_name.lower()
    # Normalize 'ñ' in piñata to 'n'
    name = name.replace('ñ', 'n')
    # Convert to snake_case and remove special characters
    # Replace characters not in font with underscores
    name = re.sub(r'[^a-z0-9#()*_]+', '_', name)
    # Clean up multiple underscores
    # e.g. "Congo - Kinshasa": "congo___kinshasa" -> "congo_kinshasa"
    return re.sub(r'_+', '_', name)


def _extract_emoji_name(comment_part: str) -> Optional[str]:
    """Extract emoji name from the comment part of the line."""

    # Extract name part from format: 'emoji E0.6 name'
    parts = comment_part.split(' ', 2)
    return parts[2] if len(parts) >= 3 else None


def _parse_line(line: str) -> Optional[Tuple[List[str], str]]:
    """Parse a single line from emoji-test.txt."""

    # Skip empty lines and comments
    if not line or line.startswith('#'):
        return None

    # Parse format: "codepoints ; status # emoji name"
    if ';' not in line or '#' not in line:
        return None

    # Split on semicolon to get codepoints and the rest
    codepoints_part, rest = line.split(';', 1)
    codepoints_str = codepoints_part.strip()

    # Extract name from the comment part (after #)
    if '#' not in rest:
        return None

    comment_part = rest.split('#', 1)[1].strip()
    emoji_name = _extract_emoji_name(comment_part)

    if not emoji_name:
        return None

    # Parse codepoints
    codepoint_list = codepoints_str.split()
    name = _normalize_emoji_name(emoji_name)

    return codepoint_list, name


def parse_emoji_test(test_file_path: str) -> Tuple[Dict[int, str], List[Tuple[List[int], str]]]:
    """Parse Unicode emoji-test.txt and extract emoji mappings and composition sequences."""

    emoji_mappings: Dict[int, str] = {}
    composition_sequences: List[Tuple[List[int], str]] = []

    with open(test_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parsed = _parse_line(line.strip())
            if not parsed:
                continue

            codepoint_list, name = parsed

            # Handle multi-codepoint sequences vs single codepoints
            if len(codepoint_list) > 1:
                # Multi-codepoint sequence (e.g., keycaps, flags with modifiers)
                # Convert hex strings to integers
                codepoint_ints = [int(cp, 16) for cp in codepoint_list]
                composition_sequences.append((codepoint_ints, name))
                # Don't add individual mappings for components in sequences,
                # as they will be handled by GSUB compositions
            else:
                # Single codepoint emoji
                codepoint = int(codepoint_list[0], 16)
                emoji_mappings[codepoint] = name

    return emoji_mappings, composition_sequences


# Parse the Unicode emoji test file
EMOJI_MAPPINGS, COMPOSITION_SEQUENCES = parse_emoji_test(EMOJI_TEST_FILE)

# Special character mappings for font generation
SPECIAL_MAPPINGS = {
    ZWJ: "_",
}

# Add Regional Indicators to SPECIAL_MAPPINGS
for cp in range(REGIONAL_INDICATOR_A, REGIONAL_INDICATOR_Z + 1):
    letter = chr(cp - REGIONAL_INDICATOR_A + ord('a'))  # Convert to lowercase a-z
    SPECIAL_MAPPINGS[cp] = f"regional_indicator_{letter}"

# Combined mappings for all emoji and special characters
# Characters that does not have mappings
ALL_MAPPINGS = {**EMOJI_MAPPINGS, **SPECIAL_MAPPINGS}
