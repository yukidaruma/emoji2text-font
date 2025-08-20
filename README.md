# Emoji2Text Font

A font that transforms emojis into their names rather than representing them graphically. Built using FontForge and its Python scripting API, it supports the complete emoji set up to Unicode 17.0.

## Overview

Emoji2Text transforms standard emoji characters into their human-readable text representations. This font shows emojis as their names instead of the pictograph. For example, "😀" becomes "grinning_face" and "🔥" becomes "fire".

This project provides both pre-built font files and the scripts to generate custom versions using your preferred base font.

## Features

- Supports emojis up to Unicode 17.0
- Handles complex emoji sequences including but not limited to:
  - Skin tone modifiers
  - Zero-width joiner (ZWJ) sequences
  - National flags and regional indicators
- Multiple font formats: OTF, TTF, WOFF, and WOFF2
- Customizable base font for consistent typography
- Optimized file sizes through glyph composition

## Demo

Try the font in action: [Live Demo](https://yukidaruma.github.io/emoji2text-font/demo.html)

## How It Works

The font operates by mapping emoji codepoints to text representations composed from a limited character set:
`#()*0123456789_abcdefghijklmnopqrstuvwxyz`

### Technical Implementation

1. **Character Mapping**: Each emoji codepoint is mapped to its corresponding text name based on Unicode annotations
2. **Glyph Composition** (ccmp): Text representations are created by referencing existing glyphs from the base font
3. **GSUB Tables**: Emojis that consist of multiple codepoints are handled through OpenType GSUB (Glyph Substitution) tables

| Emoji | Codepoint | Description | Fully-Qualified? | Compatible? |
| - | - | - | - | - |
| 😀 | `U+1F600` | grinning face | Yes | ✅ |
| ❤️ | `U+2764` | red heart | No | ✅ |
| ❤️ | `U+2764 U+FE0F` | red heart with VS-16 | Yes | ❌ |

## Application Compatibility

I have tested this font across different applications on Windows 11:

| Application | Compatible? |
| - | - |
| Google Chrome | ✅ (\*1) |
| Visual Studio Code | ✅ |
| Microsoft Excel/Word | ✅ |
| Microsoft PowerPoint | ❌ (\*2) |
| Windows Terminal | ✅ (\*3) |

\*1: The OTF version of the font may cause rendering issues on Google Chrome (#1). For stability, I recommend using the TTF version.
\*2: It appears impossible to change the emoji font in PowerPoint.
\*3: This is not particularly useful because the font does not fit within a two-column layout.

## Installation

Download the latest font from the [fonts/](fonts/) directory.

### Using on Websites

#### Option 1: Self-host the Font

Download the font files and add the following to your CSS:

```css
@font-face {
  font-family: 'Emoji2Text';
  src: url('path/to/Emoji2Text.ttf.woff2') format('woff2'),
       url('path/to/Emoji2Text.otf.woff') format('woff');
  font-display: block; /* Blocks rendering of text using this font until it loads */
}

.emoji2text {
  font-family: 'Emoji2Text', monospace;
  font-variant-emoji: text;
}
```

#### Option 2: Load from my GitHub Pages

Simply add this `<link>` tag to your HTML:

```html
<link href="https://yukidaruma.github.io/emoji2text-font/fonts/emoji2text.css" rel="stylesheet">
```

Then use the font in your CSS:

```css
.emoji2text {
  font-family: 'Emoji2Text', monospace;
  font-variant-emoji: text;
}
```

## Building from Source

### Prerequisites

- FontForge (20230101 or newer)
  - Python bundled in FontForge (3.11.2 or newer)
- A base font containing glyphs for `a-z`, `0-9`, `#`, `(`, `)`, `*`, `_`

### Build the Font

```bash
# Clone the repository
git clone https://github.com/yukidaruma/emoji2text-font.git
cd emoji2text-font

# Generate using the default Source Code Pro base font
fontforge -lang=py -script scripts/generate_font.py

# Or specify your own base font
fontforge -lang=py -script scripts/generate_font.py /path/to/your/base-font.otf
```

The generated fonts will be placed in the `fonts/` directory in multiple formats.

## Development

You will most likely want to modify one of the following:

- [`data/emoji-test.txt`](data/emoji-test.txt)
  - Update with the latest Unicode emoji data
- [`emoji_mappings.py`](scripts/emoji_mappings.py) 
  - Change `_normalize_emoji_name` and `parse_emoji_test` to determine how the font is represented in text
- [`generate_font.py`](scripts/generate_font.py)
  - Edit `build_font` to update font metadata

After tweaking the code, rebuild the font by running the `fontforge` command.

## Known Issues and Limitations

*See also: the [Issue tracker](https://github.com/yukidaruma/emoji2text-font/issues) and [Known Issues](https://yukidaruma.github.io/emoji2text-font/known-issues.html) page.*

- Most applications prioritize system emoji fonts over text fonts for emoji with Variation Selector-16 (`U+FE0F`), which results in emoji like ❤️ (`U+2764 U+FE0F`) always rendered in emoji form.
  - Variation Selector-16 (`U+FE0F`) is an invisible codepoint that specifies the preceding character should be displayed as an emoji. While my font includes glyphs for emoji sequences containing VS-16, most applications prioritize rendering fully-qualified emojis using graphical emoji fonts over text fonts, regardless of your font selection.
    A potential workaround would be to configure my font to identify itself as an emoji font, but I have not figured out how to do so yet (#4).
- Emojis with long names can be visually broken (#1), likely capped at 16-bit signed integer limit (`32767 / 600 ~= 54 letters`).

## Licenses

This project contains files released under different licenses:

- **Generated Font Files** (`fonts/*`): [SIL Open Font License 1.1](fonts/LICENSE-OFL)
- **Source Font Files** (`source-fonts/*`): [SIL Open Font License 1.1](source-fonts/LICENSE-OFL)
- **Unicode Data** (`data/emoji-test.txt`): [UNICODE LICENSE V3](data/LICENSE-UNICODE-V3)
- **Other files** (including source code and documentation): [MIT License](scripts/LICENSE-MIT)

## Acknowledgments

- FontForge for providing an excellent tool to work with fonts programmatically
- Adobe for Source Code Pro font used as the default base
- Google Noto project for emoji reference implementation

----

Last but not least, if you enjoyed this project, please consider giving it a *`star`*!  
-- *Made with `snow` by yukidaruma `snowman`*
