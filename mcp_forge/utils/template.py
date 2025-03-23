"""Template utilities for MCP server scaffolding."""

from pathlib import Path


def get_template_dir() -> Path:
    """Get the template directory path."""
    return Path(__file__).parent.parent / "templates"


def list_available_features() -> list[str]:
    """List available feature templates."""
    feature_dir = get_template_dir() / "features"
    if not feature_dir.exists():
        return []

    features = []
    for template in feature_dir.glob("*.j2"):
        if template.name == "tool.py.j2":
            continue
        feature_name = template.stem.replace(".py", "").replace("_", "-")
        features.append(feature_name)

    return sorted(features)
