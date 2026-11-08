"""Applique les couleurs marque Simple Icons aux SVG locaux (usage ponctuel)."""
from pathlib import Path

COLORS = {
    "openai.svg": "#10A37F",
    "anthropic.svg": "#D97757",
    "google.svg": "#8E75B2",
    "ollama.svg": "#000000",
    "demo.svg": "#6E9F18",
}

def main() -> None:
    root = Path(__file__).resolve().parents[2] / "docs" / "assets" / "icons" / "llm"
    for name, color in COLORS.items():
        path = root / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if 'fill="' in text:
            continue
        text = text.replace("<path d=", f'<path fill="{color}" d=', 1)
        if name == "ollama.svg":
            text = text.replace(
                "<svg ",
                '<svg style="background:#fff;border-radius:6px" ',
                1,
            )
        path.write_text(text, encoding="utf-8")
        print(f"OK {name}")


if __name__ == "__main__":
    main()
