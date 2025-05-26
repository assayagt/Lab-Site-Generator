from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.DAL.DTOs.SiteCustom_dto import siteCustom_dto
import os

class SiteCustom:
    def __init__(self, domain, name, components, template: Template, site_creator_email, logo=None, home_picture=None, generated=False, gallery_path=None):
        self.domain = domain
        self.name = name
        self.components = components
        self.template = template
        self.logo = logo
        self.home_picture = home_picture
        self.generated = generated
        self.site_creator_email = site_creator_email
        self.gallery_path = gallery_path

    def change_template(self, template: Template):
        self.template = template

    def add_component(self, components: list):
        if isinstance(components, list):
            self.components = components  # Adds multiple components at once
            if "Gallery" in components:
                # Create gallery directory in the website's folder
                website_folder = os.path.join("LabWebsitesUploads", self.domain)
                gallery_folder = os.path.join(website_folder, 'gallery')
                
                os.makedirs(gallery_folder, exist_ok=True)
                self.gallery_path = gallery_folder
            else:
                self.gallery_path = None
        else:
            raise TypeError("The input should be a list of components")

    def remove_component(self, component):
        if component in self.components:
            self.components.remove(component)

    def change_name(self, new_name: str):
        self.name = new_name

    def change_domain(self, new_domain: str):
        self.domain = new_domain

    def get_domain(self):
        return self.domain

    def set_generated(self):
        self.generated = True

    def set_logo(self, logo):
        self.logo = logo

    def set_home_picture(self, home_picture):
        self.home_picture = home_picture

    def get_site_creator_email(self):
        return self.site_creator_email

    def set_site_creator_email(self, site_creator_email):
        self.site_creator_email = site_creator_email

    def get_gallery_images(self):
        gallery_images = []
        if self.gallery_path and os.path.exists(self.gallery_path):
            # Get all files in the gallery directory
            for filename in os.listdir(self.gallery_path):
                file_path = os.path.join(self.gallery_path, filename)
                # Check if it's a file and has a valid image extension
                if os.path.isfile(file_path):
                    extension = os.path.splitext(filename)[1].lower()
                    if extension in ['.jpg', '.jpeg', '.png', '.gif']:
                        try:
                            with open(file_path, "rb") as image_file:
                                # Determine the correct MIME type
                                if extension == '.jpg' or extension == '.jpeg':
                                    mime_type = 'image/jpeg'
                                elif extension == '.png':
                                    mime_type = 'image/png'
                                elif extension == '.gif':
                                    mime_type = 'image/gif'
                                else:
                                    mime_type = 'application/octet-stream'

                                # Encode the image
                                image_base64 = base64.b64encode(image_file.read()).decode()
                                image_data_url = f"data:{mime_type};base64,{image_base64}"
                                gallery_images.append({
                                    'filename': filename,
                                    'data_url': image_data_url
                                })
                        except Exception as e:
                            print(f"Error processing image {filename}: {str(e)}")
                            continue
        return gallery_images

    def to_dto(self):
        return siteCustom_dto(
            domain=self.domain,
            name=self.name,
            components_list=self.components,
            template=self.template.value if self.template else None,
            logo=self.logo,
            home_picture=self.home_picture,
            site_creator_email= self.site_creator_email,
            generated=self.generated,
            gallery_path=self.gallery_path if self.gallery_path else None
        )