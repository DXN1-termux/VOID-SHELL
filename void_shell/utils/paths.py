import os
from pathlib import Path

# The absolute root of the VOID-SHELL project
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Standard Paths
VOID_DIR = PROJECT_ROOT / "void_shell"
CONFIG_PATH = PROJECT_ROOT / "config.json"
DATA_DIR = PROJECT_ROOT / "data"
MEMORY_DB = DATA_DIR / "synapse.db"
VECTOR_INDEX = DATA_DIR / "vectors.json"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
