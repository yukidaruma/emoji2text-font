#!/usr/bin/env fontforge -lang=py
"""
A FontForge script that generates a font that displays emoji as readable text names.
"""

# fontforge module is available when running under FontForge
# This import is not actually needed but suppresses Pylance warnings
from typing import Dict
import os
import sys
import fontforge  # type: ignore

from emoji_mappings import EMOJI_MAPPINGS, COMPOSITION_SEQUENCES, ALL_MAPPINGS
from unicode_constants import ASCII_DIGIT_0, ASCII_DIGIT_9, ASCII_SMALL_A, ASCII_SMALL_Z
from paths import DEFAULT_SOURCE_FONT_FILE, OUTPUT_DIR

# Configuration
FONT_NAME = "Emoji2Text"
FONT_VERSION = "1.0"

# Characters used in the text representation of emoji
BASE_CHARS = (
    list(range(ASCII_DIGIT_0, ASCII_DIGIT_9 + 1)) +
    list(range(ASCII_SMALL_A, ASCII_SMALL_Z + 1)) +
    [ord(c) for c in '#()*_']
)


def copy_source_glyphs(target_font: fontforge.font, source_font: fontforge.font) -> None:
    """Copy required glyphs used in the text representation from source font to target font."""

    # Bulk select all required characters, then copy/paste all at once for efficiency
    for char_code in BASE_CHARS:
        if char_code in source_font:
            source_font.selection.select(("more",), char_code)

            glyph = target_font.createChar(char_code)
            glyph.glyphname = source_font[char_code].glyphname
            target_font.selection.select(("more",), char_code)

    source_font.copy()
    target_font.paste()


def create_text_glyph(font: fontforge.font, glyph: fontforge.glyph, text: str) -> None:
    """Create a text-based glyph by composing character references."""

    glyph.clear()  # Ensure clean glyph with no default content, resulting in reduced font size

    current_x = 0

    for char in text:
        char_code = ord(char)
        if char_code in font and font[char_code].isWorthOutputting():
            source_glyph = font[char_code]
            char_width = source_glyph.width

            glyph.addReference(source_glyph.glyphname, (1, 0, 0, 1, current_x, 0))
            current_x += char_width

    glyph.width = current_x


def create_emoji_glyphs(font: fontforge.font) -> int:
    """Create text-based glyphs for all standalone emoji characters."""

    count = 0
    for codepoint, name in EMOJI_MAPPINGS.items():
        # Skip characters already copied from source font (0-9, a-z, etc.)
        if codepoint in BASE_CHARS:
            continue

        glyph = font.createChar(codepoint)
        glyph.glyphname = f"uni{codepoint:04X}"
        create_text_glyph(font, glyph, name)
        count += 1

    return count


def create_composition_glyphs(font: fontforge.font, all_mappings: Dict[int, str]) -> int:
    """Create GSUB glyphs and substitution rules for emoji sequences."""

    font.addLookup("ccmp_lookup", "gsub_ligature", None, (("ccmp", (("DFLT", ("dflt",)), ("latn", ("dflt",)))),))
    font.addLookupSubtable("ccmp_lookup", "ccmp_subtable")

    # Pre-create all needed component glyphs once
    # Without this, we'd create the same glyph thousands of times (most notably ZWJ)
    needed_components = set()
    for codepoints, _ in COMPOSITION_SEQUENCES:
        needed_components.update(codepoints)

    for cp in needed_components:
        if cp not in font:
            glyph_name = f"uni{cp:04X}"
            component_glyph = font.createChar(cp, glyph_name)
            if cp in all_mappings:
                text = all_mappings[cp]
            else:
                # Unmapped characters get no visual representation but still need glyph for GSUB
                text = ""
            create_text_glyph(font, component_glyph, text)

    # Create composition glyphs and substitution rules
    count = 0
    for i, (codepoints, name) in enumerate(COMPOSITION_SEQUENCES):
        # Create composition glyph
        comp_glyph = font.createChar(-1, f"comp_{i:04d}")
        create_text_glyph(font, comp_glyph, name)

        # Build component list for substitution rule
        components = []
        for cp in codepoints:
            if cp in font:
                components.append(font[cp].glyphname)
            else:
                components.append(f"uni{cp:04X}")

        # Add substitution rule
        comp_glyph.addPosSub("ccmp_subtable", tuple(components))
        count += 1

    return count


def build_font(source_font_path: str) -> fontforge.font:
    """Build the emoji-to-text font from a source font."""

    source_font = fontforge.open(source_font_path)
    target_font = fontforge.font()

    print(f"Copying necessary glyphs...")
    copy_source_glyphs(target_font, source_font)

    print(f"Creating emoji glyphs...")
    emoji_count = create_emoji_glyphs(target_font)
    print(f"Created {emoji_count} emoji glyphs")

    print(f"Creating compositions...")
    comp_count = create_composition_glyphs(target_font, ALL_MAPPINGS)
    print(f"Created {comp_count} compositions")

    # Set font metadata
    target_font.fontname = target_font.familyname = FONT_NAME
    target_font.fullname = f"{FONT_NAME} Regular"
    target_font.version = FONT_VERSION
    target_font.weight = "Regular"
    target_font.copyright = "© 2025 yukidaruma. All rights reserved, with Reserved Font Name 'Emoji2Text'."
    unique_id = f"{target_font.fullname} {FONT_VERSION} from {source_font.fontname} {source_font.version}"
    target_font.appendSFNTName('English (US)', 'UniqueID', unique_id)
    target_font.appendSFNTName('English (US)', 'License', 'SIL Open Font License')
    target_font.appendSFNTName('English (US)', 'License URL', 'http://scripts.sil.org/OFL')
    target_font.appendSFNTName('English (US)', 'Manufacturer', 'Yuki.games')
    target_font.appendSFNTName('English (US)', 'Vendor URL', 'https://yuki.games')

    source_font.close()

    return target_font


def write_to_files(font: fontforge.font, formats: list[str]) -> None:
    """Write font to files in different formats."""

    # Note: It seems FontForge by default internally uses OTF for WOFF generation
    # For WOFF2, TTF is used internally as Google's woff2 library only supports TTF
    # (see: https://github.com/fontforge/fontforge/issues/5240#issuecomment-1894676034)
    for fmt in formats:
        path = f"{OUTPUT_DIR}/{FONT_NAME}.{fmt}"
        font.generate(path)
        size = os.path.getsize(path) // 1024
        print(f"Generated {fmt.upper()}: {size}KB")


def main() -> int:
    """Main entry point for font generation script."""

    # Parse command line arguments
    source_font_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SOURCE_FONT_FILE
    if not os.path.exists(source_font_path):
        print(f"Error: Source font not found at {source_font_path}")
        print(f"Usage: fontforge -lang=py -script generate_font.py [source_font_path]")
        return 1

    # Generate the font
    generated_font = build_font(source_font_path)

    # Write font to files
    # Note: Extension names in WOFF do not control the actual font format used inside WOFF file
    write_to_files(generated_font, ["otf", "ttf", "otf.woff", "ttf.woff2"])

    generated_font.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
