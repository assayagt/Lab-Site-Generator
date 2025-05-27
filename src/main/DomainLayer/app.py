from queue import Queue
import time
from flask import Flask, json, jsonify, render_template, request, send_from_directory
from flask import session
from flask_restful import Api, Resource, reqparse
import os
from flask_cors import CORS
import subprocess
import pandas as pd
from flask_socketio import SocketIO, emit
import threading
from src.main.DomainLayer.socketio_instance import socketio
from google.oauth2 import id_token
from google.auth.transport import requests

def send_test_notifications():
    while True:
        socketio.emit('registration-notification', {'message': 'Test notification'})
        print("Test notification sent")
        time.sleep(60)  # Wait for 60 seconds



from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabGenerator.GeneratorSystemService import GeneratorSystemService
from src.main.DomainLayer.LabWebsites.LabSystemService import LabSystemService
from src.main.DomainLayer.LabWebsites.Website.ContactInfo import ContactInfo

# Create a Flask app
app_secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app = Flask(__name__)
app.config["SECRET_KEY"] = app_secret_key
GOOGLE_CLIENT_ID = "894370088866-4jkvg622sluvf0k7cfv737tnjlgg00nt.apps.googleusercontent.com"
# CORS(app)

CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:3001"]}})  # Allow both frontends
api = Api(app)
socketio.init_app(app)
# Directories for file storage and website generation
UPLOAD_FOLDER = './uploads'
GENERATED_WEBSITES_FOLDER = './LabWebsitesUploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_WEBSITES_FOLDER, exist_ok=True)


generator_system = GeneratorSystemService()
lab_system_service = LabSystemService.get_instance(generator_system.get_lab_system_controller())


TEMPLATE_1_PATH = os.path.join(os.getcwd(), 'Frontend', 'template1')

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# def notify_registration(email):
#     socketio.emit('registration-notification', {'message': f'New registration request from: {email}'})

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    disconnected_sid = request.sid
    response = lab_system_service.disconnect_user_socket(disconnected_sid)


@socketio.on('register_manager')
def handle_register_user(data):
    """
    Expects: { "email": "user@example.com" }
    """
    email = data.get("email")
    domain = data.get("domain")
    if email:
        try:
            sid = request.sid
            response = lab_system_service.connect_user_socket(email, domain, sid)
        except Exception as e:
            print(f"Error: {str(e)}")
            response = None

# Service for uploading file

def read_lab_info(excel_path):
    # Check if the file exists
    if not os.path.exists(excel_path):
        return None, None, "Excel file does not exist."
    try:
        # Load the Excel file
        df = pd.read_csv(excel_path)

        # Assuming columns are named 'Full Name', 'Email', 'Degree', 'Manager', 'Site Creator'
        lab_members = {}
        lab_managers = {}
        site_creator = None
        
        site_creator_count = df['Site Creator'].sum()  # Assuming this column contains boolean True for the site creator

        if site_creator_count != 1:
            return None, None, "There must be exactly one site creator."

        for index, row in df.iterrows():
            person_info = {
                "full_name": row['Full Name'],
                "degree": row['Degree']
            }
            # Add to lab_members dictionary
            lab_members[row['Email']] = person_info
            
            # Check if the person is a manager
            if row['Manager']:  # Assuming this column contains boolean values
                lab_managers[row['Email']] = person_info

            # Identify the site creator
            if row['Site Creator']:
                site_creator = {
                    "email": row['Email'],
                    "full_name": row['Full Name'],
                    "degree": row['Degree']
                }

        return lab_members, lab_managers, site_creator

    except Exception as e:
        return None, None, str(e)


# class UploadFilesAndData(Resource):
#     def post(self):
#         try:
#             # Get the data from the frontend
#             domain = request.form['domain']
#             website_name = request.form['website_name']

#             website_folder = os.path.join(GENERATED_WEBSITES_FOLDER, domain)
#             os.makedirs(website_folder, exist_ok=True)

#             files = request.files
#             for component in files:
#                 file = files[component]
#                 print(component)
#                 if file:
#                     if component == 'logo':
#                         file_path = os.path.join(website_folder, "logo.svg")  # Assuming logo is always a .png
#                     elif component == 'homepage_photo':
#                         file_path = os.path.join(website_folder, "homepage_photo")  # Assuming photo is always a .jpg
#                     else:
#                         print("help")
#                         file_path = os.path.join(website_folder, f"{component}.csv")  # Default case for other files
#                     file.save(file_path)

#             return jsonify({'message': 'Files and data uploaded successfully!'})
#         except Exception as e:
#             return jsonify({"error": f"An error occurred: {str(e)}"})




# class UploadFilesAndData(Resource):
#     def post(self):
#         try:
#             # Get the data from the frontend
#             domain = request.form['domain']
#             website_name = request.form['website_name']

#             website_folder = os.path.join(GENERATED_WEBSITES_FOLDER, domain)
#             os.makedirs(website_folder, exist_ok=True)

#             files = request.files
#             for component in files:
#                 file = files[component]
#                 print(f"Processing {component}")

#                 if file:
#                     # Get file extension
#                     extension = os.path.splitext(file.filename)[1].lower()

#                     # Handle logo upload
#                     if component == 'logo':
#                         if extension in ['.svg', '.png', '.jpg', '.jpeg']:
#                             # Save the logo with the correct extension
#                             file_path = os.path.join(website_folder, f"logo{extension}")  # Save with the original extension
#                         else:
#                             return jsonify({"error": "Invalid file type for logo, only SVG, PNG, JPG are allowed."})

#                     # Handle homepage photo upload
#                     elif component == 'homepagephoto':
#                         if extension in ['.jpg', '.jpeg', '.png']:
#                             # Save homepage photo with the correct extension
#                             file_path = os.path.join(website_folder, f"homepagephoto{extension}")
#                         else:
#                             return jsonify({"error": "Invalid file type for homepage photo, only JPG, PNG, and JPEG are allowed."})

#                     else:
#                         # Default case for other files (e.g., CSV files)
#                         if extension == '.csv':
#                             file_path = os.path.join(website_folder, f"{component}.csv")
#                         else:
#                             return jsonify({"error": "Invalid file type for component."})

#                     # Check if a file with the same name exists and overwrite it
#                     if os.path.exists(file_path):
#                         print(f"File {component} already exists. Replacing it.")
#                     else:
#                         print(f"Uploading new file: {component}")

#                     # Save or replace the file
#                     file.save(file_path)

#             return jsonify({'message': 'Files and data uploaded successfully!'})
#         except Exception as e:
#             return jsonify({"error": f"An error occurred: {str(e)}"})

class UploadFilesAndData(Resource):
    def post(self):
        try:
            domain = request.form['domain']
            website_name = request.form['website_name']

            website_folder = os.path.join(GENERATED_WEBSITES_FOLDER, domain)
            os.makedirs(website_folder, exist_ok=True)

            files = request.files
            uploaded_files = []

            for component in files:
                file = files[component]
                print(f"Processing: {component}")

                if not file:
                    continue  

                extension = os.path.splitext(file.filename)[1].lower()
                file_path = None

                if component == 'logo':
                    if extension in ['.svg', '.png', '.jpg', '.jpeg']:
                        file_path = os.path.join(website_folder, f"logo{extension}")
                    else:
                        return {
                            "error": "Invalid file type for logo. Allowed: PNG, JPG, JPEG"
                        }, 400

                elif component == 'homepagephoto':
                    if extension in ['.jpg', '.jpeg', '.png']:
                        file_path = os.path.join(website_folder, f"homepagephoto{extension}")
                    else:
                        return {
                            "error": "Invalid file type for homepage photo. Allowed: JPG, JPEG, PNG"
                        }, 400

                else:
                    return {
                        "error": f"Unsupported component: {component}"
                    }, 400

                if file_path is None:
                    return {
                        "error": f"Failed to resolve file path for: {component}"
                    }, 500

                file.save(file_path)
                uploaded_files.append(os.path.basename(file_path))

            return {
                "message": "Files and data uploaded successfully!",
                "uploaded": uploaded_files
            }, 200

        except Exception as e:
            return {
                "error": f"An error occurred: {str(e)}"
            }, 500


class UploadGalleryImages(Resource):
    def post(self):
        try:
            domain = request.form['domain']
            website_folder = os.path.join(GENERATED_WEBSITES_FOLDER, domain)
            gallery_folder = os.path.join(website_folder, 'gallery')

            if not os.path.exists(gallery_folder):
                os.makedirs(gallery_folder)

            # ✅ Use getlist to get all files under the same 'gallery' key
            files = request.files.getlist('gallery')
            uploaded_files = []

            for file in files:
                if not file:
                    continue

                extension = os.path.splitext(file.filename)[1].lower()

                # Only allow image files
                if extension not in ['.jpg', '.jpeg', '.png', '.gif']:
                    return {
                        "error": "Invalid file type for gallery image. Allowed: JPG, JPEG, PNG, GIF"
                    }, 400

                # Generate a unique filename using timestamp
                timestamp = int(time.time() * 1000)
                file_path = os.path.join(gallery_folder, f"gallery_{timestamp}{extension}")

                file.save(file_path)
                uploaded_files.append(os.path.basename(file_path))

            return {
                "message": "Gallery images uploaded successfully!",
                "uploaded": uploaded_files
            }, 200

        except Exception as e:
            return {
                "error": f"An error occurred: {str(e)}"
            }, 500

class GenerateWebsiteResource(Resource):
    def post(self):
        try:
            # Parse JSON request body
       # Parse incoming JSON data
            data = request.get_json()

            # Ensure required fields exist
            required_fields = ['domain', 'about_us', 'lab_address', 'lab_mail', 'lab_phone_num', 'participants', 'creator_scholar_link']
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}", "response": "false"})

            domain = data['domain']
            about_us = data['about_us']
            lab_address = data['lab_address']
            lab_mail = data['lab_mail']
            lab_phone_num = data['lab_phone_num']
            participants = data['participants']
            creator_scholar_link = data['creator_scholar_link']
            contact_info = ContactInfo(lab_address, lab_mail, lab_phone_num)
            # Extract lab members, managers, and site creator
            lab_members = {}
            lab_managers = {}
            site_creator = None
            print(participants)

            for participant in participants:
                email = participant.get("email", "").strip()
                full_name = participant.get("fullName", "").strip()
                degree = participant.get("degree", "").strip()
                is_lab_manager = participant.get("isLabManager", False)

                if not email or not full_name or not degree:
                    return jsonify({"error": "All participants must have an email, full name, and degree.", "response": "false"})

                # Add to lab members
                lab_members[email] = {"full_name": full_name, "degree": degree}

                # Add to lab managers if applicable
                if is_lab_manager:
                    lab_managers[email] = {"full_name": full_name, "degree": degree}

            # Set the site creator (there is exactly one due to check above)
            site_creator = {
                "email": participants[0]["email"],
                "full_name": participants[0]["fullName"],
                "degree": participants[0]["degree"]
            }


            # Call generator system to create a new lab website
            response = generator_system.create_new_lab_website(domain, lab_members, lab_managers, site_creator, creator_scholar_link)

            if response.is_success():
                response2 = generator_system.set_site_about_us_on_creation_from_generator(domain, about_us)
                if response2.is_success():
                    response3 = generator_system.set_site_contact_info_on_creation_from_generator(domain, contact_info)
                    if response3.is_success():
                        # Start npm server in a new terminal
                        command = ['start', 'cmd', '/K', 'npm', 'start']
                        process = subprocess.Popen(command, cwd=TEMPLATE_1_PATH, shell=True)

                        return jsonify({"message": "Website generated successfully!", "response": "true"})
                    return jsonify({"error1": f"An error occurred: {response3.get_message()}", "response": "false"})
                return jsonify({"error2": f"An error occurred: {response2.get_message()}", "response": "false"})
            return jsonify({"error3": f"An error occurred: {response.get_message()}", "response": "false"})

        except Exception as e:
            return jsonify({"error4": f"An error occurred: {str(e)}", "response": "false"})
        
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
        parser.add_argument('components', type=str, required=True, help="Components to be added are required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        # Example: store the chosen components (could be in a database or in-memory)
        user_id = args['user_id']
        domain = args['domain']
        selected_components = args['components'].split(", ") 
        print(selected_components)
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
        template_str = args['template']
        selected_template = Template(template_str)

        try:
            response = generator_system.change_website_template(user_id, domain, selected_template)
            if response.is_success():
                return jsonify({"message": "Template selected", "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})


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
                return jsonify({"message": "New site manager created", "manager_email": nominated_manager_email,"response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

class CreateNewSiteManagerFromLabWebsite(Resource):
    """
    Define and add new manager to a specific website, from specific lab website.
    The given nominated_manager_email must be associated with a Lab Member of the given website.
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID of the nominating manager is required")
        parser.add_argument('email', type=str, required=True, help="Email of the new manager is required")
        parser.add_argument('domain', type=str, required=True, help="Domain of the lab is required")
        args = parser.parse_args()

        try:
            response1 = lab_system_service.create_new_site_manager_from_labWebsite(args['user_id'], args['domain'],
                                                                                   args['email'])
            if response1.is_success():
                response2 = generator_system.create_new_site_manager_from_lab_website(args['email'], args['domain'])
                if response2.is_success():
                    return jsonify({"message": "Lab manager added successfully", "response": "true"})
                return jsonify({"message": response2.get_message(), "response": "false"})
            return jsonify({"message": response1.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})


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
                return jsonify({"message": "Site manager removed", "manager_email": manager_toRemove_email, "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

# Handles user login with email and password
class Login(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        google_token = data.get('google_token')
    

        try:
            if google_token:
                try:
                    # Verify the token
                    print("request token")
                    idinfo = id_token.verify_oauth2_token(google_token, requests.Request(), GOOGLE_CLIENT_ID, clock_skew_in_seconds=2)
                    print("token verified")
                    email = idinfo['email']
                    
                except ValueError as e:
                    print("Token verification failed:", str(e))
                    return jsonify({"error": "Invalid Google token", "response": "false"})

            response = generator_system.login(user_id, email)
            
            if response.is_success():
                return jsonify({"message": "User logged in successfully","response" : "true", "email": email })
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

class ChangeSiteHomePictureByManager(Resource):
    def post(self):
        """
        Change the home picture of a site by a manager.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User id is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        user_id = args['user_id']
        domain = args['domain']

        try:
            response = generator_system.change_site_home_picture_by_manager(user_id, domain)
            if response.is_success():
                return jsonify({"message": "Home picture changed successfully"})
            return jsonify({"message": response.get_message()})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

class ChangeSiteLogoByManager(Resource):
    def post(self):
        """
        Change the logo of a site by a manager.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User id is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        user_id = args['user_id']
        domain = args['domain']

        try:
            response = generator_system.change_site_logo_by_manager(user_id, domain)
            if response.is_success():
                return jsonify({"message": "Logo changed successfully"})
            return jsonify({"message": response.get_message()})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

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
        

            user_id = request.args.get("user_id")

            response = generator_system.get_all_custom_websites_of_manager(user_id)
            if response.is_success():
                websites = response.get_data() #rertun map of {domain: {site name, generated status}}
                # Store the user ID in the session for tracking
                return jsonify({"websites": websites , "response": "true"})
            return jsonify({"message": response.get_message(),"response": "false"})
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
        
            user_id = request.args.get('user_id')
            domain = request.args.get('domain')
            response = generator_system.get_custom_website(user_id, domain)
            if response.is_success():
                #the returned value is website name, template, components
                website_data = response.get_data()
                return jsonify({'data': website_data,"response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

class GetHomepageDetails(Resource):
    def get(self):
        try:
            domain = request.args.get('domain')
           
            # Fetch the site data from the siteData.json file
            response_1 = generator_system.get_site_by_domain(domain)
            if response_1.is_success():
                # the returned value is website name, template, components
                response_2 = lab_system_service.get_about_us(domain)
                if response_2.is_success():
                    response_3 = lab_system_service.get_news(domain)
                    if response_3.is_success():
                        news_data = response_3.get_data()
                        website_data = response_1.get_data()
                        about_us_data = response_2.get_data()
                        website_data['about_us'] = about_us_data
                        website_data['news'] = news_data
                        return jsonify({'data': website_data, "response": "true"})

                return jsonify({"message1": response_2.get_message(), "response": "false"})
            return jsonify({"message2": response_1.get_message(), "response": "false"})

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})



class EnterLabWebsite(Resource):
    def get(self):
        domain = request.args.get('domain')
        try:
            response = lab_system_service.enter_lab_website(domain)
            if response.is_success():
                return jsonify({"message": response.get_message(), "user_id": response.get_data() , "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500



class LoginWebsite(Resource):
    def post(self):
        data = request.get_json()
        domain = data.get('domain')
        user_id = data.get('user_id')
        google_token = data.get('google_token')
                
        try:
            if google_token:
                try:
                    # Verify the token
                    idinfo = id_token.verify_oauth2_token(google_token, requests.Request(), GOOGLE_CLIENT_ID, clock_skew_in_seconds=2)
                    
                    # Check if the email from token matches the provided email
                    email = idinfo['email']
                except ValueError as e:
                    print("Token verification failed:", str(e))
                    return jsonify({"error": "Invalid Google token", "response": "false"})
            response = lab_system_service.login(domain, user_id, email)
            if response.is_success():
                if response.get_data():
                    return jsonify({"message": response.get_message(), "response": "true", "email": email})
                else:
                    #notify_registration(email, domain)
                    return jsonify({"message": response.get_message(), "response": "false"})
            #notify_registration(email, domain)
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})
        
class LogoutWebsite(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.logout(args['domain'], args['user_id'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
class GetApprovedPublications(Resource):
    def get(self):
        domain = request.args.get('domain')

        try:
            response = lab_system_service.get_all_approved_publications(domain)
            if response.is_success():
                return jsonify({"publications": response.get_data(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

class AddPublication(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('publication_link', type=str, location='json', required=True, help="Publication link is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('git_link', type=str, required=False , default="")
        parser.add_argument('video_link', type=str, required=False, default="")
        parser.add_argument('presentation_link', type=str, required=False, default="")
        args = parser.parse_args()

        user_id = args['user_id']
        domain = args['domain']
        publication_link = args['publication_link']
        git_link = args['git_link']
        video_link = args['video_link']
        presentation_link = args['presentation_link']

        try:
            response = lab_system_service.add_publication_manually(user_id, domain, publication_link, git_link, video_link, presentation_link)
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message() , "response": "false"})
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
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "true"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})
        
        

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
                    return jsonify({"message": response.get_message(), "response": "true"})
                return jsonify({"message": response.get_message(), "response": "false"})
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
                    return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500


class AddLabMemberFromWebsite(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID of the manager adding the member is required")
        parser.add_argument('email', type=str, required=True, help="Email of the new member is required")
        parser.add_argument('full_name', type=str, required=True, help="Full name of the new member is required")
        parser.add_argument('degree', type=str, required=True, help="Degree of the new member is required")
        parser.add_argument('domain', type=str, required=True, help="Domain of the lab is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.register_new_LabMember_from_labWebsite(args['user_id'], args['email'], args['full_name'], args['degree'], args['domain'])
            if response.is_success():
                    return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class GetAllCustomWebsites(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User id is required")
        args = parser.parse_args()

        user_id = args['user_id']

        try :
            response = generator_system.get_custom_websites(user_id)
            if response.is_success():
                websites = response.get_data() # Return map of <domain, site name>
                return jsonify({"websites": websites, "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e :
            return jsonify({"error": f"An error occurred: {str(e)}"})
        
class GetCustomSite(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        domain = request.args.get('domain')

        try :
            response = generator_system.get_custom_website(user_id, domain)
            if response.is_success():
                website_data = response.get_data() # Returned value is website name, template, components
                return jsonify({'data': website_data, "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})
        

class GetMemberPublications(Resource):
    def get(self):
        domain = request.args.get('domain')
        user_id = request.args.get('user_id')
        try:
            response = lab_system_service.get_all_approved_publications_of_member(domain, user_id)
            if response.is_success():
                return jsonify({"publications": response.get_data(), "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class ApproveRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('domain', required=True, help="Domain is required.")
        parser.add_argument('manager_userId', required=True, help="Manager User ID is required.")
        parser.add_argument('requested_full_name', required=True)
        parser.add_argument('requested_degree', required=True)
        parser.add_argument('notification_id', required=False)
        args = parser.parse_args()

        try:
            response = lab_system_service.approve_registration_request(args['domain'], args['manager_userId'], args['requested_full_name'], args['requested_degree'], args['notification_id'])
            if response.is_success():
                return jsonify({"message": "Registration approved successfully.", "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class RejectRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('domain', required=True, help="Domain is required.")
        parser.add_argument('manager_userId', required=True, help="Manager User ID is required.")
        parser.add_argument('notification_id', required=True, help="Requested user email is required.")
        args = parser.parse_args()

        try:
            response = lab_system_service.reject_registration_request(args['domain'], args['manager_userId'], args['notification_id'])
            if response.is_success():
                return jsonify({"message": "Registration rejected successfully.", "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})
        

class GetAllLabManagers(Resource):
    def get(self):
        domain = request.args.get('domain')

        try:
            response = lab_system_service.get_all_lab_managers_details(domain)
            if response.is_success():
                return jsonify({"managers": response.get_data(), "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class GetAllLabMembers(Resource):
    def get(self):
        domain = request.args.get('domain')

        try:
            response = lab_system_service.get_all_lab_members_details(domain)
            if response.is_success():
                return jsonify({"members": response.get_data(), "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})


class GetAllAlumni(Resource):
    def get(self):
        domain = request.args.get('domain')

        try:
            response = lab_system_service.get_all_alumnis_details(domain)
            if response.is_success():
                return jsonify({"alumni": response.get_data(), "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class GetUserDetails(Resource):
    def get(self):
        domain = request.args.get('domain')
        user_id = request.args.get('user_id')

        try:
            response = lab_system_service.get_user_details(user_id, domain)
            if response.is_success():
                return jsonify({"user": response.get_data(), "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})


class SetSecondEmail(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', required=True, help="User ID is required")
        parser.add_argument('secondEmail', required=True, help="Second email is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.set_secondEmail_by_member(args['userid'], args['secondEmail'], args['domain'])
            if response.is_success():
                return jsonify({"message": "Second email added successfully", "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class SetLinkedInLink(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', required=True, help="User ID is required")
        parser.add_argument('linkedin_link', required=True, help="LinkedIn link is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.set_linkedin_link_by_member(args['userid'], args['linkedin_link'], args['domain'])
            if response.is_success():
                return jsonify({"message": "LinkedIn link added successfully", "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class SetFullName(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', required=True, help="User ID is required")
        parser.add_argument('fullName', required=True, help="Full name is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.set_fullName_by_member(args['userid'], args['fullName'], args['domain'])
            if response.is_success():
                return jsonify({"message": "Full name updated successfully", "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class SetDegree(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', required=True, help="User ID is required")
        parser.add_argument('degree', required=True, help="Degree is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.set_degree_by_member(args['userid'], args['degree'], args['domain'])
            if response.is_success():
                return jsonify({"message": "Degree updated successfully", "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class SetBio(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', required=True, help="User ID is required")
        parser.add_argument('bio', required=True, help="Bio is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.set_bio_by_member(args['userid'], args['bio'], args['domain'])
            if response.is_success():
                return jsonify({"message": "Bio updated successfully", "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class SetMedia(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', required=True, help="User ID is required")
        parser.add_argument('media', required=True, help="Media link is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.set_media_by_member(args['userid'], args['media'], args['domain'])
            if response.is_success():
                return jsonify({"message": "Media updated successfully", "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class AddLabMemberFromGenerator(Resource):
    """
    Define and add new manager to a specific website, from generator site.
    The given nominated_manager_email must be associated with a Lab Member of the given website.
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('manager_userId', required=True, help="Manager User ID is required")
        parser.add_argument('email_to_register', required=True, help="Email to register is required")
        parser.add_argument('lab_member_fullName', required=True, help="Lab member full name is required")
        parser.add_argument('lab_member_degree', required=True, help="Lab member degree is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        args = parser.parse_args()


        try:
            response = generator_system.register_new_LabMember_from_generator(args['manager_userId'], args['email_to_register'], args['lab_member_fullName'], args['lab_member_degree'], args['domain'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class InitialApprovePublicationByAuthor(Resource):
    """
    Approve a publication by its author in the initial review stage.
    If the publication has not yet been final approved by a lab manager,
    the system sends a notification to lab managers requesting final approval.
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, help="User ID is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        parser.add_argument('notification_id', required=True, help="Notification ID is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.initial_approve_publication_by_author(args['user_id'], args['domain'], args['notification_id'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class FinalApprovePublicationByManager(Resource):
    """
    Approve a publication by a lab manager in the final review stage.
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, help="User ID is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        parser.add_argument('notification_id', required=True, help="Notification ID is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.final_approve_publication_by_manager(args['user_id'], args['domain'], args['notification_id'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})


class RemoveManagerPermission(Resource):
    """A Lab Manager(manager_userId) removes the administrative permissions of another Lab Manager,
    reverting their role to a Lab Member.
    The permissions of the lab creator cannot be removed, it must always remain a Lab Manager
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('manager_userId', type=str, required=True, help="Manager user id is required")
        parser.add_argument('manager_toRemove_email', type=str, required=True, help="Manager to remove email is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        manager_userId = args['manager_userId']
        manager_toRemove_email = args['manager_toRemove_email']
        domain = args['domain']
        try:
            response = lab_system_service.remove_manager_permission(manager_userId, manager_toRemove_email, domain)
            if response.is_success():
                return jsonify({"message": "Site manager removed", "manager_email": manager_toRemove_email})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})


class GetAllMembersNames(Resource):
    '''
    returns all lab members + managers + site creator + alumnis names
    '''
    def get(self):
        domain = request.args.get('domain')

        try:
            response = lab_system_service.get_all_members_names(domain)
            if response.is_success():
                return jsonify({"members": response.get_data(), "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})


class GetPendingRegistrationEmails(Resource):
    '''
    Registration Notifications! returns all pending registration emails
    '''
    def get(self):

        domain = request.args.get('domain')
        user_id = request.args.get('userid')

        try:
            response = lab_system_service.get_pending_registration_emails(user_id, domain)
            if response.is_success():
                return jsonify({"emails": response.get_data(), "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class RejectPublication(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('notification_id', type=str, required=True, help="Notification ID is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.reject_publication(args['user_id'], args['domain'], args['notification_id'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class SetSiteAboutUsByManagerFromGenerator(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('about_us', type=str, required=True, help="About us is required")
        args = parser.parse_args()

        try:
            response = generator_system.set_site_about_us_by_manager_from_generator(args['user_id'], args['domain'], args['about_us'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class SetSiteContactInfoByManagerFromGenerator(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('lab_address', type=str, required=True, help="Lab address is required")
        parser.add_argument('lab_mail', type=str, required=True, help="Lab mail is required")
        parser.add_argument('lab_phone_num', type=str, required=True, help="Lab phone number is required")
        args = parser.parse_args()

        user_id = args['user_id']
        domain = args['domain']
        lab_address = args['lab_address']
        lab_mail = args['lab_mail']
        lab_phone_num = args['lab_phone_num']
        contact_info = ContactInfo(lab_address, lab_mail, lab_phone_num)

        try:
            response = generator_system.set_site_contact_info_by_manager_from_generator(user_id, domain, contact_info)
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class SetSiteAboutUsByManagerFromLabWebsite(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('about_us', type=str, required=True, help="About us is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.set_site_about_us_from_labWebsite(args['user_id'], args['domain'], args['about_us'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})


class SetSiteContactInfoByManagerFromLabWebsite(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('lab_address', type=str, required=True, help="Lab address is required")
        parser.add_argument('lab_mail', type=str, required=True, help="Lab mail is required")
        parser.add_argument('lab_phone_num', type=str, required=True, help="Lab phone number is required")
        args = parser.parse_args()

        user_id = args['user_id']
        domain = args['domain']
        lab_address = args['lab_address']
        lab_mail = args['lab_mail']
        lab_phone_num = args['lab_phone_num']
        contact_info = ContactInfo(lab_address, lab_mail, lab_phone_num)

        try:
            response = lab_system_service.set_site_contact_info_from_labWebsite(user_id, domain, contact_info)
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})


class GetContactUs(Resource):
    def get(self):
        try:
            domain = request.args.get('domain')
           
            response = lab_system_service.get_contact_us(domain)
            if response.is_success():
                # the returned value is website name, template, components
                return jsonify({'data': response.get_data(), "response": "true"})
            return jsonify({"message2": response.get_message(), "response": "false"})

        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})


class SiteCreatorResignationFromGenerator(Resource):
    """
    Resignation of the site creator through GeneratorSystemController.
    new_role is the new role of the current site creator after resignation - can be 'manager' or 'member' or 'alumni'
    email is the mail of the newly nominated member (must be a current lab member/manager)
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, help="User ID is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        parser.add_argument('email', required=True, help="Email is required")
        parser.add_argument('new_role', required=True, help="New role is required")
        args = parser.parse_args()

        try:
            response = generator_system.site_creator_resignation_from_generator(args['user_id'], args['domain'], args['email'], args['new_role'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class SiteCreatorResignationFromLabWebsite(Resource):
    """
    Resignation of the site creator through Lab Website.
    new_role is the new role of the current site creator after resignation - can be 'manager' or 'member' or 'alumni'
    email is the mail of the newly nominated member (must be a current lab member/manager)
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, help="User ID is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        parser.add_argument('email', required=True, help="Email is required")
        parser.add_argument('new_role', required=True, help="New role is required")
        args = parser.parse_args()

        try:
            response1 = lab_system_service.site_creator_resignation_from_lab_website(args['user_id'], args['domain'], args['email'], args['new_role'])
            if response1.is_success():
                response2 = generator_system.site_creator_resignation_from_lab_website(args['domain'], args['email'], args['new_role'])
                if response2.is_success():
                    return jsonify({"message": response2.get_message(), "response": "true"})
                return jsonify({"message": f"An error occurred: {response2.get_message()}", "response": "false"})
            return jsonify({"message": response1.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})


class RemoveAlumniFromGenerator(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('manager_userId', type=str, required=True, help="Manager user id is required")
        parser.add_argument('email_toRemoveAlumni', type=str, required=True, help="Email to remove alumni is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = generator_system.remove_alumni_from_generator(args['manager_userId'], args['email_toRemoveAlumni'], args['domain'])
            if response.is_success():
                return jsonify({"message": "Alumni removed successfully", "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

class AddAlumniFromGenerator(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('manager_userId', type=str, required=True, help="Manager user id is required")
        parser.add_argument('email_toSetAlumni', type=str, required=True, help="Email to set alumni is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = generator_system.add_alumni_from_generator(args['manager_userId'], args['email_toSetAlumni'], args['domain'])
            if response.is_success():
                return jsonify({"message": "Alumni added successfully", "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

class AddAlumniFromLabWebsite(Resource):
    """
    define member (lab manager or lab member) as alumni
    Only managers can perform this operation.
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('manager_user_id', required=True, help="Manager User ID is required")
        parser.add_argument('member_email', required=True, help="Member email is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response1 = lab_system_service.define_member_as_alumni(args['manager_user_id'], args['member_email'], args['domain'])
            if response1.is_success():
                response2 = generator_system.add_alumni_from_lab_website(args['member_email'], args['domain'])
                if response2.is_success():
                    return jsonify({"message": response2.get_message(), "response": "true"})
                return jsonify({"message": response2.get_message(), "response": "false"})
            return jsonify({"message": response1.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class GetAllMembersNotifications(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        domain = request.args.get('domain')

        try:
            response = lab_system_service.get_all_member_notifications(user_id, domain)
            if response.is_success():
                return jsonify({"notifications": response.get_data(), "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})
        
class SetScholarLink(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', required=True, help="User ID is required")
        parser.add_argument('scholar_link', required=True, help="Google Scholar profile link is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.set_scholar_link_by_member(args['userid'], args['scholar_link'], args['domain'])
            if response.is_success():
                return jsonify({"message": "Google Scholar provile link updated successfully", "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class GetNotApprovedMemberPublications(Resource):
    def get(self):
        domain = request.args.get('domain')
        user_id = request.args.get('user_id')
        try:
            response = lab_system_service.get_all_not_approved_publications_of_member(domain, user_id)
            if response.is_success():
                return jsonify({"publications": response.get_data(), "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})
        
class RejectMultiplePublications(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('publication_IDs', type = str, action='append', required=True, help="A list of publication IDs is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.reject_multiple_publications(args['user_id'], args['domain'], args['publication_IDs'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class InitialApproveMultiplePublicationsByAuthor(Resource):
    """
    Approve a publication by its author in the initial review stage.
    If the publication has not yet been final approved by a lab manager,
    the system sends a notification to lab managers requesting final approval.
    """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, help="User ID is required")
        parser.add_argument('domain', required=True, help="Domain is required")
        parser.add_argument('publication_IDs', type=str, required=True, help="A list of publication IDs is required")
        args = parser.parse_args()
        print(args['publication_IDs'].split(", "))
        pubs = args['publication_IDs'].split(", ")
        try:
            response = lab_system_service.initial_approve_multiple_publications_by_author(args['user_id'], args['domain'], pubs)
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})
        
class CrawlPublicationsForMember(Resource):
     def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.crawl_publications_for_labMember(args['user_id'], args['domain'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})


class RemoveAlumniFromLabWebsite(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('manager_user_id', type=str, required=True, help="Manager User ID is required")
        parser.add_argument('alumni_email', type=str, required=True, help="Alumni email is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.remove_alumni_from_labWebsite(args['manager_user_id'], args['alumni_email'], args['domain'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class DeleteWebsite(Resource):
    def delete(self):
        try:
            user_id = request.args.get('user_id')
            domain = request.args.get('domain')
            response = generator_system.delete_website(user_id, domain)
            if response.is_success():
                return jsonify({"message": "Website deleted successfully", "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"})

class GetGalleryImages(Resource):
    def get(self):
        try:
            domain = request.args.get('domain')
            response = generator_system.get_gallery_images(domain)
            if response.is_success():
                return jsonify({"images": response.get_data(), "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class DeleteGalleryImage(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User id is required")
        parser.add_argument('image_name', type=str, required=True, help="Image name is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        args = parser.parse_args()

        try:
            response = generator_system.delete_gallery_image(args['user_id'], args['domain'], args['image_name'])
            if response.is_success():
                return jsonify({"message": "Image deleted successfully", "response": "true"})
            return jsonify({"error": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})

class AddNewsRecord(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('text', type=str, required=True, help="News text is required")
        parser.add_argument('link', type=str, required=False)
        parser.add_argument('date', type=str, required=True, help="Date is required")
        args = parser.parse_args()

        try:
            response = lab_system_service.add_news_record(args['user_id'], args['domain'], args['text'], args['link'], args['date'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e)})


class UploadProfilePicture(Resource):
    def post(self):
        try:
            domain = request.form['domain']
            user_id = request.form['user_id']

            website_folder = os.path.join(GENERATED_WEBSITES_FOLDER, domain)
            profile_pictures_folder = os.path.join(website_folder, 'profile_pictures')

            if not os.path.exists(profile_pictures_folder):
                os.makedirs(profile_pictures_folder)

            file = request.files['profile_picture']
            if not file:
                return {
                    "error": "No file provided"
                }, 400

            extension = os.path.splitext(file.filename)[1].lower()

            # Only allow image files
            if extension not in ['.jpg', '.jpeg', '.png', '.gif']:
                return {
                    "error": "Invalid file type for profile picture. Allowed: JPG, JPEG, PNG, GIF"
                }, 400

            # Generate a unique filename using user_id and timestamp
            timestamp = int(time.time() * 1000)
            file_path = os.path.join(profile_pictures_folder, f"profile_{timestamp}{extension}")

            response = lab_system_service.add_profile_picture(user_id, domain, file_path)

            file.save(file_path)

            return {
                "message": "Profile picture uploaded successfully!",
                "filename": os.path.basename(file_path)
            }, 200

        except Exception as e:
            return {
                "error": f"An error occurred: {str(e)}"
            }, 500

# Add resources to the API of lab
api.add_resource(EnterLabWebsite, '/api/enterLabWebsite')#
api.add_resource(LoginWebsite, '/api/loginWebsite')#
api.add_resource(LogoutWebsite, '/api/logoutWebsite')#
api.add_resource(GetApprovedPublications, '/api/getApprovedPublications')
api.add_resource(AddPublication, '/api/addPublication')
api.add_resource(SetPublicationVideoLink, '/api/setPublicationVideoLink')
api.add_resource(SetPublicationGitLink, '/api/setPublicationGitLink')
api.add_resource(SetPublicationPttxLink, '/api/setPublicationPttxLink')
api.add_resource(InitialApprovePublicationByAuthor, '/api/initialApprovePublicationByAuthor')
api.add_resource(InitialApproveMultiplePublicationsByAuthor, '/api/initialApproveMultiplePublicationsByAuthor')
api.add_resource(FinalApprovePublicationByManager, '/api/finalApprovePublicationByManager')
api.add_resource(AddAlumniFromLabWebsite, '/api/addAlumniFromLabWebsite')
api.add_resource(RemoveAlumniFromLabWebsite, '/api/removeAlumniFromLabWebsite')
api.add_resource(RemoveManagerPermission, '/api/removeManagerPermission')
api.add_resource(GetAllMembersNames, '/api/getAllMembersNames')
api.add_resource(GetPendingRegistrationEmails, '/api/getPendingRegistrationEmails')
api.add_resource(RejectPublication, '/api/RejectPublication')
api.add_resource(RejectMultiplePublications, '/api/rejectMultiplePublications')

# Add the resources to API
api.add_resource(UploadFilesAndData, '/api/uploadFile')#
api.add_resource(GenerateWebsiteResource, '/api/generateWebsite')#
api.add_resource(ChooseComponents, '/api/chooseComponents')#
api.add_resource(ChooseTemplate, '/api/chooseTemplate')#
api.add_resource(ChooseName, '/api/chooseName')#
api.add_resource(Login, '/api/Login')#
api.add_resource(Logout, '/api/Logout')#
api.add_resource(ChooseDomain, '/api/chooseDomain')#
api.add_resource(StartCustomSite, '/api/startCustomSite')  #
api.add_resource(GetAllCustomWebsitesOfManager, '/api/getCustomWebsites')
api.add_resource(EnterGeneratorSystem, '/api/enterGeneratorSystem')#
api.add_resource(GetCustomSite, '/api/getCustomSite')
api.add_resource(CreateNewSiteManagerFromGenerator, '/api/CreateNewSiteManagerFromGenerator')
api.add_resource(RemoveAlumniFromGenerator, '/api/RemoveAlumniFromGenerator')
api.add_resource(AddAlumniFromGenerator, '/api/AddAlumniFromGenerator')
api.add_resource(SiteCreatorResignationFromGenerator, '/api/siteCreatorResignationFromGenerator')

api.add_resource(GetMemberPublications, '/api/getMemberPublications')
api.add_resource(GetNotApprovedMemberPublications, '/api/getNotApprovedMemberPublications')
api.add_resource(ApproveRegistration, '/api/approveRegistration') #
api.add_resource(RejectRegistration, '/api/rejectRegistration') #
api.add_resource(GetAllLabManagers, '/api/getAllLabManagers')#
api.add_resource(GetAllLabMembers, '/api/getAllLabMembers')#
api.add_resource(GetAllAlumni, '/api/getAllAlumni')#
api.add_resource(AddLabMemberFromWebsite, '/api/addLabMemberFromWebsite') #
api.add_resource(AddLabMemberFromGenerator, '/api/addLabMemberFromGenerator')#
api.add_resource(CreateNewSiteManagerFromLabWebsite, '/api/createNewSiteManagerFromLabWebsite')#
api.add_resource(SiteCreatorResignationFromLabWebsite, '/api/siteCreatorResignationFromLabWebsite')#

api.add_resource(SetSecondEmail, '/api/setSecondEmail')#
api.add_resource(SetLinkedInLink, '/api/setLinkedInLink')#
api.add_resource(SetFullName, '/api/setFullName')#
api.add_resource(SetDegree, '/api/setDegree')#
api.add_resource(SetScholarLink, '/api/setScholarLink')#
api.add_resource(SetBio, '/api/setBio')#
api.add_resource(SetMedia, '/api/setMedia')#
api.add_resource(SetSiteAboutUsByManagerFromGenerator, '/api/setSiteAboutUsByManagerFromGenerator')#
api.add_resource(SetSiteAboutUsByManagerFromLabWebsite, '/api/setSiteAboutUsByManagerFromLabWebsite')#
api.add_resource(SetSiteContactInfoByManagerFromGenerator, '/api/setSiteContactInfoByManagerFromGenerator')#
api.add_resource(SetSiteContactInfoByManagerFromLabWebsite, '/api/setSiteContactInfoByManagerFromLabWebsite')#
api.add_resource(GetHomepageDetails, '/api/getHomepageDetails')
api.add_resource(ChangeSiteHomePictureByManager, '/api/ChangeSiteHomePictureByManager')
api.add_resource(ChangeSiteLogoByManager, '/api/ChangeSiteLogoByManager')
api.add_resource(RemoveSiteManagerFromGenerator, '/api/removeSiteManager')
api.add_resource(GetUserDetails, '/api/getUserDetails')
api.add_resource(GetContactUs, '/api/getContactUs')
api.add_resource(GetAllMembersNotifications, '/api/getAllMembersNotifications')
api.add_resource(DeleteWebsite, '/api/deleteWebsite')
api.add_resource(UploadGalleryImages, '/api/uploadGalleryImages')
api.add_resource(GetGalleryImages, '/api/getGallery')
api.add_resource(DeleteGalleryImage, '/api/deleteGalleryImage')
api.add_resource(AddNewsRecord, '/api/addNewsRecord')
##
api.add_resource(CrawlPublicationsForMember, '/api/CrawlPublicationsForMember')

if __name__ == '__main__':
    # notification_thread = threading.Thread(target=send_test_notifications, daemon=True)
    # notification_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=True)    ##app.run(debug=True)


