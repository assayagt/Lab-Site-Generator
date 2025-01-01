from flask import Flask, json, jsonify, render_template, request, send_from_directory
from flask import session
from flask_restful import Api, Resource, reqparse
import os
from flask_cors import CORS

from src.main.DomainLayer.LabGenerator import GeneratorSystemService


# Create a Flask app
app_secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app = Flask(__name__)
app.config["SECRET_KEY"] = app.secret_key
CORS(app)
api = Api(app)

# Directories for file storage and website generation
UPLOAD_FOLDER = './uploads'
GENERATED_WEBSITES_FOLDER = './LabWebsites'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_WEBSITES_FOLDER, exist_ok=True)


generator_system = GeneratorSystemService.GeneratorSystemService.get_instance()


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
        parser.add_argument('user_id', type=str, required=True, help="User id is required")
        parser.add_argument('old_domain', type=str, required=True, help=" Old Domain is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()


        user_id = args['user_id']
        old_domain = args['old_domain']
        domain = args['domain']

        try:
            response = generator_system.change_website_domain(user_id, domain, old_domain)
            if response.is_success():
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
        parser.add_argument('user_id', type=str, required=True, help="User id is required")
        parser.add_argument('components', type=list, required=True, help="Components to be added are required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        # Example: store the chosen components (could be in a database or in-memory)
        user_id = args['user_id']
        domain = args['domain']
        selected_components = args['components']
        try:
            response = generator_system.add_components_to_site(user_id, domain, selected_components)
            if response.is_success():
                return jsonify({"message": "Components selected", "components": selected_components}), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Handles the template selection for the lab website
class ChooseTemplate(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User id is required")
        parser.add_argument('template', type=str, required=True, help="Template name is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        user_id = args['user_id']
        domain = args['domain']
        selected_template = args['template']
        try:
            response = generator_system.change_website_template(user_id, domain, selected_template)
            if response.is_success():
                return jsonify({"message": "Template selected", "template": selected_template}), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Handles setting the name for the lab website
class ChooseName(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User id is required")
        parser.add_argument('website_name', type=str, required=True, help=" name is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        user_id = args['user_id']
        domain = args['domain']
        website_name = args['website_name']
        try:
            response = generator_system.change_website_name(user_id, website_name, domain)
            if response.is_success():
                return jsonify({"message": "Website name set", "website_name": website_name}), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Handles user login with email and password
class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="email is required")
        parser.add_argument('user_id', type=str, required=True, help="User id is required")

        args = parser.parse_args()

        email = args['email']
        user_id = args['user_id']
    

        try:
            response = generator_system.login(email, user_id)
            
            if response.is_success():
                return jsonify({"message": "User logged in successfully","response" : "true" })
            return jsonify({"message": response.get_message(),"response" : "false" })
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}","response" : "false"})

# Handles user logout
class Logout(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User id is required")
        args = parser.parse_args()

        user_id = args['user_id']

        try:
            response = generator_system.logout(user_id)
            if response.is_success():
                return jsonify({"message": "User logged out successfully","response" : "true"})
            return jsonify({"message": "Error","response" : "false" })
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}","response" : "false"})


class StartCustomSite(Resource):
    def post(self):
        """
        Starts a new custom site by setting a name, domain, and components.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User id is required")
        parser.add_argument('website_name', type=str, required=True, help="Website name is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        user_id = args['user_id']
        website_name = args['website_name']
        domain = args['domain']
        try:
            response = generator_system.create_website(user_id, website_name, domain)
            if response.is_success():
                return jsonify({"message": f"Custom site '{website_name}' started successfully", "websiteLink": f"/view/{website_name.replace(' ', '_')}/index.html"}), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Service to fetch all lab websites
class GetAllLabWebsites(Resource):
    def get(self):
        """Fetch all lab websites."""
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User id is required")
        args = parser.parse_args()

        user_id = args['user_id']

        try:
            response = generator_system.get_lab_websites(user_id)
            if response.is_success():
                websites = response.get_data()  # rertun list of <domain>
                # Store the user ID in the session for tracking
                return jsonify({"websites": websites}), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Service to fetch all custom websites
class GetAllCustomWebsites(Resource):
    def get(self):
        """Fetch all lab websites."""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=str, required=True, help="User id is required")
            args = parser.parse_args()

            user_id = args['user_id']

            response = generator_system.get_custom_websites(user_id)
            if response.is_success():
                websites = response.get_data() #rertun map of <domain, site name>
                # Store the user ID in the session for tracking
                return jsonify({"websites": websites}), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500


class EnterGeneratorSystem(Resource):
    def get(self):
        try:
            # Generate a new guest ID via the service
            response = generator_system.enter_generator_system()
            if response.is_success():
                user_id = response.get_data()
                # Store the user ID in the session for tracking
                return jsonify({
                    "user_id": user_id,
                    "message": "New user entered the system successfully"
                })
            else:
                return jsonify({"error": "An internal server error occurred"})
        except Exception as e:
            # Log the exception (consider integrating a logging library)
            return jsonify({"error": "An internal server error occurred"}), 500


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
api.add_resource(GetAllCustomWebsites, '/api/getCustomWebsites')
api.add_resource(GetAllLabWebsites, '/api/getAllLabWebsites')
api.add_resource(EnterGeneratorSystem, '/api/enterGeneratorSystem')

if __name__ == '__main__':
    app.run(debug=True)
