from pathlib import Path
import json

CONFIG_DIR = Path.home() / ".kleep"
CONFIG_FILE = CONFIG_DIR / "config.json"

def get_config():
    """Load configuration from file, or return default if not exists"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save configuration to file"""
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_output_dir():
    """Get the output directory from config, or prompt user if not set"""
    config = get_config()
    output_dir = config.get('output_dir')
    
    if not output_dir:
        import click
        output_dir = click.prompt(
            "Where would you like to save your downloaded files?",
            default=str(Path.home() / "Music"),
            type=click.Path(exists=False, dir_okay=True, writable=True)
        )
        config['output_dir'] = output_dir
        save_config(config)
    
    return Path(output_dir)
