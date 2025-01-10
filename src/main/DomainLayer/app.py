from flask import Flask, json, jsonify, render_template, request, send_from_directory
from flask import session
from flask_restful import Api, Resource, reqparse
import os
from flask_cors import CORS
import subprocess

from src.main.DomainLayer.LabGenerator import GeneratorSystemService


# Create a Flask app
app_secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app = Flask(__name__)
app.config["SECRET_KEY"] = app.secret_key
CORS(app)
api = Api(app)

# Directories for file storage and website generation
UPLOAD_FOLDER = './uploads'
GENERATED_WEBSITES_FOLDER = './LabWebsitesUploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_WEBSITES_FOLDER, exist_ok=True)


generator_system = GeneratorSystemService.GeneratorSystemService.get_instance()
TEMPLATE_1_PATH = os.path.join(os.getcwd(), 'Frontend', 'template1')

##todo: add email and domain where needed

# Service for uploading file
class UploadFilesAndData(Resource):
    def post(self):
        try:
            # Get the data from the frontend (domain, website_name, content for each component)
            domain = request.form['domain']
            website_name = request.form['website_name']
            about_us_content = request.form.get('aboutus_content')
            contact_us_content = request.form.get('contactus_content')

            # Prepare the directory for the domain
            website_folder = os.path.join(GENERATED_WEBSITES_FOLDER, domain)
            os.makedirs(website_folder, exist_ok=True)

            # Save site data (content) to siteData.json
            site_data = {
                "domain": domain,
                "website_name": website_name,
                "aboutus_content": about_us_content,
                "contactus_content": contact_us_content,
            }
            with open(os.path.join(website_folder, 'siteData.json'), 'w') as json_file:
                json.dump(site_data, json_file)

            # Handle dynamic file uploads for each component (Publications, Participants)
            files = request.files
            for component in files:
                file = files[component]
                if file:
                    # Save each file with the component's name (e.g., "Publications.xlsx")
                    file_path = os.path.join(website_folder, f"{component}.xlsx")
                    file.save(file_path)

            return jsonify({'message': 'Files and data uploaded successfully!'})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})


# Service for generating a website from templates
class GenerateWebsiteResource(Resource):
    def post(self):
        try:  
            if not os.path.exists(TEMPLATE_1_PATH):
                return jsonify({"error": f"Path {TEMPLATE_1_PATH} does not exist."})


            ##TODO: take all the xlxs files and make them as dictionaries
            ##TODO: call generate site
            command = ['start', 'cmd', '/K', 'npm', 'start']  # Command to open a new terminal and run npm start
            process = subprocess.Popen(command, cwd=TEMPLATE_1_PATH, shell=True)
    
            return jsonify({"message": "Website generated successfully!"})
        
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})
        

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
                return jsonify({"message": "Domain updated successfully", "domain": domain})

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
                return jsonify({"message": "Components selected", "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

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
                return jsonify({"message": "Template selected", "template": selected_template})
            return jsonify({"message": response.get_message(), "response": "false"})
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
                return jsonify({"message": "Website name set", "website_name": website_name})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

class CreateNewSiteManagerFromGenerator(Resource):
    """
    Define and add new manager to a specific website, from generator site.
    The given nominated_manager_email must be associated with a Lab Member of the given website.
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nominator_manager_userId', type=str, required=True, help="Nominator manager user id is required")
        parser.add_argument('nominated_manager_email', type=str, required=True, help="Nominated manager email is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        nominator_manager_userId = args['nominator_manager_userId']
        nominated_manager_email = args['nominated_manager_email']
        domain = args['domain']
        try:
            response = generator_system.create_new_site_manager(nominator_manager_userId, nominated_manager_email, domain)
            if response.is_success():
                return jsonify({"message": "New site manager created", "manager_email": nominated_manager_email})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

    def remove_site_manager_from_generator(self, nominator_manager_userId, manager_toRemove_email, domain):

class RemoveSiteManagerFromGenerator(Resource):
    """
    Remove a manager from a specific website, from generator site.
    nomintator_manager_userId is the user that removes the manager.
    The given removed_manager_email must be associated with a manager of the given website.
    The permissions of the lab creator cannot be removed, it must always remain a Lab Manager
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nominator_manager_userId', type=str, required=True, help="Nominator manager user id is required")
        parser.add_argument('manager_toRemove_email', type=str, required=True, help="Manager to remove email is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        nominator_manager_userId = args['nominator_manager_userId']
        manager_toRemove_email = args['manager_toRemove_email']
        domain = args['domain']
        try:
            response = generator_system.remove_site_manager_from_generator(nominator_manager_userId, manager_toRemove_email, domain)
            if response.is_success():
                return jsonify({"message": "Site manager removed", "manager_email": manager_toRemove_email})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

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
            return jsonify({"message": response.get_message(),"response" : "false" })
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
        parser.add_argument('components', type=str, required=True, help="components is required")
        parser.add_argument('template', type=str, required=True, help="template is required")
        args = parser.parse_args()

        user_id = args['user_id']
        website_name = args['website_name']
        domain = args['domain']
        components = args['components'].split(", ")  # Split the string back into a list
        template = args['template']
        print(components)
        try:
            response = generator_system.create_website(user_id, website_name, domain,components,template)
            if response.is_success():
                return jsonify({"message": f"Custom site '{website_name}' started successfully", "websiteLink": f"/view/{website_name.replace(' ', '_')}/index.html","response": "true"})
            return jsonify({"message": response.get_message(),"response": "false"})

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

# Service to fetch all custom websites
class GetAllCustomWebsitesOfManager(Resource):
    def get(self):
        """Fetch all custom website details for specific manager (both generated and not generated sites).
        The details contain the domain, site name, and generated status"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=str, required=True, help="User id is required")
            args = parser.parse_args()

            user_id = args['user_id']

            response = generator_system.get_all_custom_websites_of_manager(user_id)
            if response.is_success():
                websites = response.get_data() #rertun map of {domain: {site name, generated status}}
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

class GetCustomSite(Resource):
    """ Get a custom website dto for specific manager and domain"""
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=str, required=True, help="User id is required")
            parser.add_argument('domain', type=str, required=True, help="Domain is required")
            args = parser.parse_args()

            user_id = args['user_id']
            domain = args['domain']

            response = generator_system.get_custom_website(user_id, domain)
            if response.is_success():
                #the returned value is website name, template, components
                website_data = response.get_data()
                return jsonify({'data': website_data,"response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

<<<<<<< Updated upstream
class GetHomepageDetails(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('domain', type=str, required=True, help="Domain is required")
            args = parser.parse_args()

            domain = args['domain']

            # Fetch the site data from the siteData.json file
            response_1 = generator_system.get_custom_website(domain)
            if response_1.is_success():
                # the returned value is website name, template, components
                response_2 = lab_system_service.get_about_us(domain)
                if response_2.is_success():
                    website_data = response_1.get_data()
                    about_us_data = response_2.get_data()
                    website_data['about_us'] = about_us_data
                    return jsonify({'data': website_data, "response": "true"})

                return jsonify({"message": response_2.get_message(), "response": "false"})
            return jsonify({"message": response_1.get_message(), "response": "false"})

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})
        
=======
>>>>>>> Stashed changes


class EnterLabWebsite(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        domain = args['domain']
        try:
            response = lab_system_service.enter_lab_website(domain)
            if response.is_success():
                return jsonify({"message": response.get_message(), "user_id": response.get_data()})
            return jsonify({"message": response.get_message()}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

class LoginWebsite(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('email', type=str, required=True, help="Email is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.login(args['domain'], args['user_id'], args['email'])
            if response.is_success():
                return jsonify({"message": response.get_message()})
            return jsonify({"message": response.get_message()}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
class LogoutWebsite(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.logout(args['domain'], args['user_id'])
            if response.is_success():
                return jsonify({"message": response.get_message()})
            return jsonify({"message": response.get_message()}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
class GetApprovedPublications(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.get_all_approved_publications(args['domain'])
            if response.is_success():
                return jsonify({"publications": response.get_data()})
            return jsonify({"message": response.get_message()}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

class AddPublication(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('publication_dto', type=dict, location='json', required=True, help="Publication data is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('authors_emails', type=list, location='json', required=True, help="Authors' emails are required")
        args = parser.parse_args()

        try:
            response = lab_system_service.add_publication_manually(
                args['user_id'], args['publication_dto'], args['domain'], args['authors_emails']
            )
            if response.is_success():
                return jsonify({"message": response.get_message()})
            return jsonify({"message": response.get_message()}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

class SetPublicationVideoLink(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('publication_id', type=str, required=True, help="Publication ID is required")
        parser.add_argument('video_link', type=str, required=False, help="Video link")
        args = parser.parse_args()

        try:
            
            response = lab_system_service.set_publication_video_link(
                    args['user_id'], args['domain'], args['publication_id'], args['video_link']
                )
         
            if response.is_success():
                return jsonify({"message": response.get_message()})
            return jsonify({"message": response.get_message()}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        

class SetPublicationGitLink(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=str, required=True, help="User ID is required")
            parser.add_argument('domain', type=str, required=True, help="Domain is required")
            parser.add_argument('publication_id', type=str, required=True, help="Publication ID is required")
            parser.add_argument('git_link', type=str, required=False, help="Git link")
            args = parser.parse_args()

            try:
               
                response = lab_system_service.set_publication_git_link(
                    args['user_id'], args['domain'], args['publication_id'], args['git_link']
                )
        
                if response.is_success():
                    return jsonify({"message": response.get_message()})
                return jsonify({"message": response.get_message()}), 400
            except Exception as e:
                return jsonify({"error": f"An error occurred: {str(e)}"}), 500

class SetPublicationPttxLink(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('publication_id', type=str, required=True, help="Publication ID is required")
    
        parser.add_argument('presentation_link', type=str, required=False, help="Presentation link")
        args = parser.parse_args()

        try:
           
           
            response = lab_system_service.set_publication_presentation_link(
                    args['user_id'], args['domain'], args['publication_id'], args['presentation_link']
                )
            
            if response.is_success():
                return jsonify({"message": response.get_message()})
            return jsonify({"message": response.get_message()}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Add resources to the API of lab
api.add_resource(EnterLabWebsite, '/api/enterLabWebsite')
api.add_resource(LoginWebsite, '/api/loginWebsite')
api.add_resource(LogoutWebsite, '/api/logoutWebsite')
api.add_resource(GetApprovedPublications, '/api/getApprovedPublications')
api.add_resource(AddPublication, '/api/addPublication')
api.add_resource(SetPublicationVideoLink, '/api/setPublicationVideoLink')
api.add_resource(SetPublicationGitLink, '/api/setPublicationGitLink')
api.add_resource(SetPublicationPttxLink, '/api/setPublicationPttxLink')


# Add the resources to API
api.add_resource(UploadFilesAndData, '/api/uploadFile')
api.add_resource(GenerateWebsiteResource, '/api/generateWebsite')
api.add_resource(ChooseComponents, '/api/chooseComponents')
api.add_resource(ChooseTemplate, '/api/chooseTemplate')
api.add_resource(ChooseName, '/api/chooseName')
api.add_resource(Login, '/api/Login')
api.add_resource(Logout, '/api/Logout')
api.add_resource(ChooseDomain, '/api/chooseDomain')
api.add_resource(StartCustomSite, '/api/startCustomSite')  # New endpoint to start custom site
api.add_resource(GetAllCustomWebsites, '/api/getCustomWebsites')
api.add_resource(GetAllLabWebsites, '/api/getAllLabWebsites')
api.add_resource(EnterGeneratorSystem, '/api/enterGeneratorSystem')
api.add_resource(GetCustomSite, '/api/getCustomSite')

##TODO: add members
##TODO: add managers

if __name__ == '__main__':
    app.run(debug=True)
