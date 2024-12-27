from flask import Flask, json, jsonify, render_template, request, send_from_directory
from flask_restful import Api, Resource, reqparse
import os
from flask_cors import CORS

from main.DomainLayer.LabGenerator import GeneratorSystemService


app = Flask(__name__)
CORS(app)
api = Api(app)

# Directories for file storage and website generation
UPLOAD_FOLDER = './uploads'
GENERATED_WEBSITES_FOLDER = './LabWebsites'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_WEBSITES_FOLDER, exist_ok=True)


generator_system = GeneratorSystemService.get_instance()


##todo: add email and domain where needed

# Service for uploading file
class FileUploadResource(Resource):
    def post(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        return jsonify({'message': 'File uploaded successfully', 'file_path': filename})

# Service for generating a website from templates
class GenerateWebsiteResource(Resource):
    def post(self):
        try:
            # Get data from the frontend (e.g., title, description, components)
            data = request.json
            title = data.get('title', 'Untitled Website')
            description = data.get('description', '')
            components = data.get('components', [])

            # Create a new folder for the generated website
            website_folder = os.path.join(GENERATED_WEBSITES_FOLDER, title.replace(' ', '_'))
            os.makedirs(website_folder, exist_ok=True)

            # Save dynamic data (title, description, components) in a JSON file
            site_data = {
                "title": title,
                "description": description,
                "components": components
            }

            # Save the data to a JSON file for later use
            with open(os.path.join(website_folder, 'siteData.json'), 'w') as json_file:
                json.dump(site_data, json_file)

            return jsonify({"websiteLink": f"/view/{title.replace(' ', '_')}/index.html"}), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Serve the generated website with dynamic data
class ViewWebsite(Resource):
    def get(self, folder_name):
        try:
            website_folder = os.path.join(GENERATED_WEBSITES_FOLDER, folder_name)
            if os.path.exists(website_folder):
                # Read the site data (e.g., title, description, components)
                with open(os.path.join(website_folder, 'siteData.json'), 'r') as json_file:
                    site_data = json.load(json_file)

                # Serve React app template (index.html) with injected dynamic data
                return render_template('index.html', site_data=site_data)
            return jsonify({"error": "Website not found"}), 404
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500


class ChooseDomain(Resource):
    def post(self):
        """
        Handles setting the domain for the lab website.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help=" Email is required")
        parser.add_argument('old_domain', type=str, required=True, help=" Old Domain is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('website_name', type=str, required=True, help="Website name is required")
        args = parser.parse_args()


        email = args['email']
        old_domain = args['old_domain']
        domain = args['domain']
        website_name = args['website_name']

        try:
            generator_system.change_website_domain(domain,old_domain)
            return jsonify({"message": "Domain updated successfully", "domain": domain}), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500


class ChooseComponents(Resource):
    def post(self):
        """
        Handles the selection of components (e.g., text boxes, images, etc.) 
        for the lab website.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('components', type=list, required=True, help="Components to be added are required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()
        
        domain = args['domain']
        selected_components = args['components']
        try:
            generator_system.add_components_to_site(domain,selected_components)
            return jsonify({"message": "Components selected", "components": selected_components}), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
# Handles the template selection for the lab website
class ChooseTemplate(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('template', type=str, required=True, help="Template name is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        domain = args['domain']
        selected_template = args['template']
        try:
            generator_system.change_website_template(domain,selected_template )
            return jsonify({"message": "Template selected", "template": selected_template}), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        

# Handles setting the name for the lab website
class ChooseName(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help=" name is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        domain = args['domain']
        website_name = args['website_name']
        try:
            return jsonify({"message": "Website name set", "website_name": website_name}), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
# Handles user login with email and password
class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="Email is required")
        args = parser.parse_args()
        
        email = args['email']

        try:
            generator_system.login(email)
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
# Handles user logout
class Logout(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="Email is required")
        args = parser.parse_args()
        
        email = args['email']
        try:
            generator_system.logout(email)
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500


class StartCustomSite(Resource):
    def post(self):
        """
        Starts a new custom site by setting a name, domain, and components.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="Email is required")
        parser.add_argument('website_name', type=str, required=True, help="Website name is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        email = args['email']
        website_name = args['website_name']
        domain = args['domain']
        try:
            generator_system.create_website(email,website_name,domain)
            return jsonify({"message": f"Custom site '{website_name}' started successfully", "websiteLink": f"/view/{website_name.replace(' ', '_')}/index.html"}), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

class GetCustomWebsites(Resource):
    def get(self):
        try:
            # Fetch the website by name from the service
            websites = generator_system.get_custom_website()
            return jsonify({"websites": websites}), 200
         
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Service to fetch all lab websites
class GetAllLabWebsites(Resource):
    def get(self):
        """Fetch all lab websites."""
        try:
            # Fetch all lab websites from the service
            websites = generator_system.get_all_lab_websites()
            return jsonify({"websites": websites}), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        

# Add the resources to API
api.add_resource(FileUploadResource, '/api/uploadFile')
api.add_resource(GenerateWebsiteResource, '/api/generateWebsite')
api.add_resource(ChooseComponents, '/api/chooseComponents')
api.add_resource(ChooseTemplate, '/api/chooseTemplate')
api.add_resource(ChooseName, '/api/chooseName')
api.add_resource(Login, '/api/Login')
api.add_resource(Logout, '/api/Logout')
api.add_resource(ViewWebsite, '/view/<folder_name>') 
api.add_resource(ChooseDomain, '/api/chooseDomain') 
api.add_resource(StartCustomSite, '/api/startCustomSite')  # New endpoint to start custom site
api.add_resource(GetCustomWebsite, '/api/getCustomWebsite')
api.add_resource(GetAllLabWebsites, '/api/getAllLabWebsites')

if __name__ == '__main__':
    app.run(debug=True)
