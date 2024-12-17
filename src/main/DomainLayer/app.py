# from flask import Flask, jsonify, request
# from flask_restful import Api, Resource, reqparse
# import os

# app = Flask(__name__)
# api = Api(app)

# # Directories for file storage and website generation
# UPLOAD_FOLDER = './uploads'
# GENERATED_WEBSITES_FOLDER = './LabWebsites'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(GENERATED_WEBSITES_FOLDER, exist_ok=True)

# # Service for uploading file
# class FileUploadResource(Resource):
#     def post(self):
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file part'}), 400
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400
#         filename = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(filename)
#         return jsonify({'message': 'File uploaded successfully', 'file_path': filename})

# # Service for generating a website from templates
# class GenerateWebsiteResource(Resource):
#     def post(self):
#         data = request.json
#         template = data.get('template')
#         lab_name = data.get('lab_name')
#         research_focus = data.get('research_focus')
#         projects = data.get('projects')
        
#         # Here you could call a function to render a template and generate the website
#         html_content = f"<html><head><title>{lab_name}</title></head><body><h1>{lab_name}</h1><p>{research_focus}</p><ul>{''.join([f'<li>{project}</li>' for project in projects])}</ul></body></html>"
        
#         website_folder = os.path.join(GENERATED_WEBSITES_FOLDER, f'{template}_website')
#         os.makedirs(website_folder, exist_ok=True)
#         html_path = os.path.join(website_folder, 'index.html')
#         with open(html_path, 'w') as f:
#             f.write(html_content)

#         return jsonify({'website_link': f"/download/{template}_website/index.html"})
    

# class ChooseComponents(Resource):
#     def post(self):
#         """
#         Handles the selection of components (e.g., text boxes, images, etc.) 
#         for the lab website.
#         """
#         parser = reqparse.RequestParser()
#         parser.add_argument('components', type=list, required=True, help="Components to be added are required")
#         args = parser.parse_args()
        
#         # Example: store the chosen components (could be in a database or in-memory)
#         selected_components = args['components']
        
#         # You can process the components as needed here (e.g., validate, save to database)
        
#         return jsonify({"message": "Components selected", "components": selected_components}), 200

# class ChooseTemplate(Resource):
#     def post(self):
#         """
#         Handles the template selection for the lab website.
#         """
#         parser = reqparse.RequestParser()
#         parser.add_argument('template', type=str, required=True, help="Template name is required")
#         args = parser.parse_args()
        
#         selected_template = args['template']
        
#         # You can process the template selection (e.g., validate, save selection)
        
#         return jsonify({"message": "Template selected", "template": selected_template}), 200

# class ChooseName(Resource):
#     def post(self):
#         """
#         Handles setting the name for the lab website.
#         """
#         parser = reqparse.RequestParser()
#         parser.add_argument('website_name', type=str, required=True, help="Website name is required")
#         args = parser.parse_args()
        
#         website_name = args['website_name']
        
#         # Store or process the website name (e.g., save in a database)
        
#         return jsonify({"message": "Website name set", "website_name": website_name}), 200
    
# class Login(Resource):
#     def post(self):
#         """
#         Handles user login with email and password.
#         """
#         parser = reqparse.RequestParser()
#         parser.add_argument('email', type=str, required=True, help="Email is required")
#         parser.add_argument('password', type=str, required=True, help="Password is required")
#         args = parser.parse_args()
        
#         email = args['email']
#         password = args['password']
        
#         # Authenticate the user (this could involve checking a database)
#         # For now, we'll just simulate the login
#         if email == "test@example.com" and password == "password123":
#             return jsonify({"message": "Login successful", "email": email}), 200
#         else:
#             return jsonify({"message": "Invalid credentials"}), 401
        
# class Logout(Resource):
#     def post(self):
#         """
#         Handles user logout by clearing their session or token.
#         """
#         # Here you would invalidate the user session or token
#         # For now, we'll just simulate a successful logout.
        
#         return jsonify({"message": "Logout successful"}), 200
    

# # Add the resources to API
# api.add_resource(FileUploadResource, '/api/uploadFile')
# api.add_resource(GenerateWebsiteResource, '/api/generateWebsite')
# api.add_resources(ChooseComponents, '/api/chooseComponents')
# api.add_resources(ChooseTemplate, '/api/chooseTemplate')
# api.add_resources(ChooseName, '/api/chooseName')
# api.add_resources(Login, '/api/Login')
# api.add_resources(Logout, '/api/Logout')

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS

import os

app = Flask(__name__)
CORS(app)
# Directory to save generated websites
GENERATED_WEBSITES_FOLDER = './generated_websites'
os.makedirs(GENERATED_WEBSITES_FOLDER, exist_ok=True)

# Endpoint to generate website
@app.route('/generateWebsite', methods=['POST'])
def generate_website():
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
@app.route('/view/<folder_name>/<filename>', methods=['GET'])
def view_website(folder_name, filename):
    website_folder = os.path.join(GENERATED_WEBSITES_FOLDER, folder_name)
    if os.path.exists(website_folder):
        # Read the site data (e.g., title, description, components)
        with open(os.path.join(website_folder, 'siteData.json'), 'r') as json_file:
            site_data = json.load(json_file)

        # Serve React app template (index.html) with injected dynamic data
        return render_template('index.html', site_data=site_data)
    return jsonify({"error": "Website not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)