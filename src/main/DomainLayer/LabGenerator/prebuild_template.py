import os
import json
import shutil
import subprocess

def create_base_template():
    """
    Creates a base template from template1 that can be used for faster website generation.
    The base template will have a placeholder domain that can be replaced during generation.
    """
    TEMPLATE_PATH = "/home/admin/project/Lab-Site-Generator/Frontend/template1"
    BASE_TEMPLATE_PATH = "/home/admin/project/Lab-Site-Generator/Frontend/base_template"

    try:
        # Create base template directory if it doesn't exist
        if os.path.exists(BASE_TEMPLATE_PATH):
            shutil.rmtree(BASE_TEMPLATE_PATH)
        os.makedirs(BASE_TEMPLATE_PATH)

        # Copy template files
        shutil.copytree(TEMPLATE_PATH, BASE_TEMPLATE_PATH, dirs_exist_ok=True)

        # Remove any existing build directory
        build_dir = os.path.join(BASE_TEMPLATE_PATH, 'build')
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        # Update package.json with placeholder domain
        package_json_path = os.path.join(BASE_TEMPLATE_PATH, 'package.json')
        with open(package_json_path, 'r+') as f:
            pkg = json.load(f)
            pkg['homepage'] = "/labs/{domain}"  # Placeholder that will be replaced during generation
            f.seek(0)
            json.dump(pkg, f, indent=2)
            f.truncate()

        print("Base template created successfully!")
        return True

    except Exception as e:
        print(f"Error creating base template: {str(e)}")
        # Clean up on error
        if os.path.exists(BASE_TEMPLATE_PATH):
            shutil.rmtree(BASE_TEMPLATE_PATH)
        return False

if __name__ == "__main__":
    create_base_template() 