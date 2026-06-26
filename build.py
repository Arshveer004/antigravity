import os
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader

# Configuration
DIST_DIR = 'dist'
STATIC_DIR = 'static'
TEMPLATES_DIR = 'templates'
DATA_FILE = 'data.yaml'

def load_data(filepath):
    """Load YAML data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def setup_dist():
    """Clean and setup the dist directory."""
    if os.path.exists(DIST_DIR):
        print(f"Removing existing {DIST_DIR}/ directory...")
        shutil.rmtree(DIST_DIR)
    
    print(f"Creating {DIST_DIR}/ directory...")
    os.makedirs(DIST_DIR)
    
    # Create speakers sub-directory
    os.makedirs(os.path.join(DIST_DIR, 'speakers'))
    
    # Copy static files if they exist
    if os.path.exists(STATIC_DIR):
        print(f"Copying {STATIC_DIR}/ to {DIST_DIR}/{STATIC_DIR}/...")
        shutil.copytree(STATIC_DIR, os.path.join(DIST_DIR, STATIC_DIR))
    else:
        print(f"Warning: {STATIC_DIR}/ directory not found. Skipping static files.")

def build_site():
    print("Starting build process...")
    
    # 1. Load Data
    try:
        data = load_data(DATA_FILE)
    except Exception as e:
        print(f"Error loading {DATA_FILE}: {e}")
        return

    # 2. Setup Jinja2 Environment
    if not os.path.exists(TEMPLATES_DIR):
        print(f"Error: {TEMPLATES_DIR}/ directory not found. Please create it and add your templates.")
        return
        
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    # 3. Setup dist folder
    setup_dist()

    # 4. Render standard pages
    standard_pages = ['index', 'about', 'schedule', 'speakers', 'venue', 'register']
    
    for page in standard_pages:
        template_name = f"{page}.html"
        output_path = os.path.join(DIST_DIR, template_name)
        
        try:
            template = env.get_template(template_name)
            rendered_html = template.render(data=data)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
            print(f"Rendered {output_path}")
        except Exception as e:
            print(f"Warning: Could not render {template_name}. ({e})")

    # 5. Render speaker detail pages
    speaker_template_name = "speaker_detail.html"
    try:
        speaker_template = env.get_template(speaker_template_name)
        
        for speaker in data.get('speakers', []):
            slug = speaker.get('slug')
            if not slug:
                continue
                
            output_path = os.path.join(DIST_DIR, 'speakers', f"{slug}.html")
            
            # Pass both the global data and the specific speaker data
            rendered_html = speaker_template.render(data=data, speaker=speaker)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
            print(f"Rendered {output_path}")
            
    except Exception as e:
        print(f"Warning: Could not render speaker pages. Make sure {speaker_template_name} exists. ({e})")

    print("Build complete!")

if __name__ == "__main__":
    build_site()
