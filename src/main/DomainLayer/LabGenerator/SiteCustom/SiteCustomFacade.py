import Template,SiteCustom

class SiteCustomFacade:
    _singleton_instance = None

    def __init__(self):
        if SiteCustomFacade._singleton_instance is not None:
            raise Exception("This is a singleton class!")
        self.sites = []

    @staticmethod
    def get_instance():
        if SiteCustomFacade._singleton_instance is None:
            SiteCustomFacade._singleton_instance = SiteCustomFacade()
        return SiteCustomFacade._singleton_instance

    def create_new_site(self, domain, name, components, template: Template):
        site = SiteCustom(domain, name, components, template)
        self.sites.append(site)

    def change_site_name(self, site_index, new_name):
        """Changes the name of a site."""
        try:
            if not isinstance(new_name, str) or not new_name:
                raise ValueError("Invalid site name provided")

            site = self.sites[site_index]
            site.change_name(new_name)
        except IndexError:
            print("Error: Site index out of range")
        except ValueError as ve:
            print(f"Error changing site name: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def change_site_domain(self, site_index, new_domain):
        """Changes the domain of a site."""
        try:
            if not isinstance(new_domain, str) or not new_domain:
                raise ValueError("Invalid domain provided")

            site = self.sites[site_index]
            site.change_domain(new_domain)
        except IndexError:
            print("Error: Site index out of range")
        except ValueError as ve:
            print(f"Error changing site domain: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def change_site_template(self, site_index, new_template: Template):
        """Changes the template of a site."""
        try:
            if not isinstance(new_template, Template):
                raise ValueError("Invalid template provided")

            site = self.sites[site_index]
            site.change_template(new_template)
        except IndexError:
            print("Error: Site index out of range")
        except ValueError as ve:
            print(f"Error changing site template: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def add_components_to_site(self, site_index, components):
        """Adds components to a site."""
        try:
            if not isinstance(components, list) or not all(isinstance(c, str) for c in components):
                raise ValueError("Components should be a list of strings")

            site = self.sites[site_index]
            site.add_component(components)
        except IndexError:
            print("Error: Site index out of range")
        except ValueError as ve:
            print(f"Error adding components: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def remove_component_from_site(self, site_index, component):
        """Removes a component from a site."""
        try:
            if not isinstance(component, str):
                raise ValueError("Component should be a string")

            site = self.sites[site_index]
            site.remove_component(component)
        except IndexError:
            print("Error: Site index out of range")
        except ValueError as ve:
            print(f"Error removing component: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")