"""Automatic clean code refactoring script."""
import os
import re
from pathlib import Path

# Define replacement mappings
REPLACEMENTS = {
    # Constants
    'SZELESSEG': 'SCREEN_WIDTH',
    'MAGASSAG': 'SCREEN_HEIGHT',
    'RACS_MERET': 'GRID_SIZE',
    'FEKETE': 'BLACK',
    'SZURKE': 'DARK_GRAY',
    'ZOLD': 'GREEN',
    'FEHER': 'WHITE',
    'KEK': 'BLUE',
    'NARANCS': 'ORANGE',
    'AR_BANYASZ': 'MINER_COST',
    'AR_TORONY': 'TOWER_COST',
    
    # Class names
    'Palya': 'Map',
    'Gazdasag': 'Economy',
    
    # Method/variable names
    'rajzol': 'draw',
    'ablak': 'surface',
    'palya': 'map',
    'ellensegek': 'enemies',
    'tornyok': 'towers',
    'hullam': 'wave',
    'sebzes': 'damage',
    'hatotav': 'range',
    'tuzelesi_sebesseg': 'fire_speed',
    'szin': 'color',
    'szoveg': 'text',
    'pozicio': 'position',
    'sebesseg': 'speed',
    'elet': 'health',
    'nev': 'name',
    'kristaly': 'crystal',
    'epulet': 'building',
    'repo': 'path',
    'koord': 'coords',
    'esemenyek': 'handle_events',
    'update': 'update',
    'utolso_spawn': 'last_spawn_time',
    'ora': 'clock',
    'futo': 'running',
    'ellenseg': 'enemy',
    'torony': 'tower',
    'vasarlas': 'purchase',
    'rajzol_ui': 'draw_ui',
    'epulet_nev': 'building_name',
    'epulet_szin': 'building_color',
    'szoveg_penz': 'text_money',
}

def refactor_file(filepath):
    """Refactor a single Python file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements, being careful with word boundaries
        for old, new in REPLACEMENTS.items():
            # Use word boundaries for variable names
            pattern = r'\b' + re.escape(old) + r'\b'
            content = re.sub(pattern, new, content)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error refactoring {filepath}: {e}")
        return False

def main():
    """Refactor all Python files in the project."""
    project_root = Path(__file__).parent
    python_files = list(project_root.rglob('*.py'))
    
    # Exclude the refactor script itself
    python_files = [f for f in python_files if f.name != 'refactor.py']
    
    refactored_count = 0
    for filepath in python_files:
        if refactor_file(filepath):
            refactored_count += 1
            print(f"✓ {filepath.relative_to(project_root)}")
    
    print(f"\nRefactored {refactored_count} files")

if __name__ == '__main__':
    main()
