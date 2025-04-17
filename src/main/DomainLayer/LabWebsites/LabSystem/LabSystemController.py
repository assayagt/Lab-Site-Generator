from datetime import datetime
import re
from src.main.DomainLayer.LabWebsites.WebCrawler.WebCrawlerFacade import WebCrawlerFacade
from src.main.DomainLayer.LabWebsites.Website.WebsiteFacade import WebsiteFacade
from src.main.DomainLayer.LabWebsites.Notifications.NotificationsFacade import NotificationsFacade
from src.main.DomainLayer.LabWebsites.User.AllWebsitesUserFacade import AllWebsitesUserFacade
from src.main.Util.ExceptionsEnum import ExceptionsEnum


class LabSystemController:
    _singleton_instance = None

    def __init__(self):
        self.webCrawlerFacade = WebCrawlerFacade()
        self.websiteFacade = WebsiteFacade()
        self.notificationsFacade = NotificationsFacade()
        self.allWebsitesUserFacade = AllWebsitesUserFacade()

    @staticmethod
    def get_instance():
        if LabSystemController._singleton_instance is None:
            LabSystemController._singleton_instance = LabSystemController()
        return LabSystemController._singleton_instance

    def enter_lab_website(self, domain):
        """
        Enter a specific lab website
        This function returns a unique userId for the user
        """
        self.allWebsitesUserFacade.error_if_domain_not_exist(domain)
        return self.allWebsitesUserFacade.add_user_to_website(domain)

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator):
        """
        Create a new lab website with the given domain, lab members, lab managers, and site creator.
        Each lab member, lab manager, and site creator now includes a degree field.
        """
        self.websiteFacade.create_new_website(domain)
        self.allWebsitesUserFacade.add_new_webstie_userFacade(domain)
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)

        # Add lab members
        for lab_member_email, lab_member_details in lab_members.items():
            full_name = lab_member_details["full_name"]
            degree = lab_member_details["degree"]
            userFacade.register_new_LabMember(lab_member_email, full_name, degree) #FOR DATA WE NEED: either return the member to save it here with domain or pass the domain to function

        # Add lab managers
        for lab_manager_email, lab_manager_details in lab_managers.items():
            full_name = lab_manager_details["full_name"]
            degree = lab_manager_details["degree"]
            userFacade.create_new_site_manager(lab_manager_email, full_name, degree) #SAME AS ABOVE

        # Set site creator
        site_creator_email = site_creator.get("email")
        site_creator_full_name = site_creator.get("full_name")
        site_creator_degree = site_creator.get("degree")
        userFacade.set_site_creator(site_creator_email, site_creator_full_name, site_creator_degree) #SAME AS ABOVE

    def login(self, domain, userId, email):
        """
        Login user into a specific website by email (should be via google in the future)
        If the given email is not associated with a member, an email is sent to all managers in order to approve\reject
        the registration request
        """
        self.allWebsitesUserFacade.error_if_domain_not_exist(domain)
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        member = userFacade.get_member_by_email(email)
        if member is None:
            alumni = userFacade.get_alumni_by_email(email)
            if alumni is None:
                # check if registration request already sent to managers:
                userFacade.error_if_email_is_in_requests_and_wait_approval(email)
                # error if registration request already sent to managers and rejected:
                userFacade.error_if_email_is_in_requests_and_rejected(email)
                # send registration request to all LabManagers:
                self.send_registration_notification_to_all_LabManagers(domain, email) #notification here
                # keep the email in the requests list, so next time the user will login, a registration request wont be sent again:
                userFacade.add_email_to_requests(email)
                raise Exception(ExceptionsEnum.USER_NOT_REGISTERED.value)
            else:
                userFacade.login(userId, email)
        else:
            userFacade.login(userId, email)

    def send_registration_notification_to_all_LabManagers(self, domain, requestedEmail):
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        managers = userFacade.getManagers()
        siteCreator = userFacade.getSiteCreator()
        recipients = {**managers, **siteCreator}
        print("recipients: ", recipients)
        for managerEmail in recipients:
            self.notificationsFacade.send_registration_request_notification(requestedEmail, managerEmail, domain)

    def logout(self, domain, userId):
        """
        Logout user from a specific website
        """
        self.allWebsitesUserFacade.logout(domain, userId)

    def approve_registration_request(self, domain, manager_userId, requested_full_name, requested_degree, notification_id):
        """
        Approve registration request of a specific email, by a lab manager
        """
        requested_email = self.mark_as_read(manager_userId, domain, notification_id)
        self.allWebsitesUserFacade.approve_registration_request(domain, manager_userId, requested_email,
                                                                requested_full_name, requested_degree)

    def reject_registration_request(self, domain, manager_userId, notification_id):
        """
        Reject registration request of a specific email, by a lab manager
        """
        requested_email = self.mark_as_read(manager_userId, domain, notification_id)
        self.allWebsitesUserFacade.reject_registration_request(domain, manager_userId, requested_email)

    def create_new_site_manager_from_labWebsite(self, nominator_manager_userId, domain, nominated_manager_email):
        """
        Define and add new manager to a specific website, directly from the lab website.
        The given nominated_manager_email must be associated with a Lab Member of the given website.
        This operation can be done only by lab manager
        """
        self.allWebsitesUserFacade.create_new_site_manager_from_labWebsite(nominator_manager_userId,
                                                                           nominated_manager_email, domain)

    def register_new_LabMember_from_labWebsite(self, manager_userId, email_to_register, lab_member_fullName,
                                               lab_member_degree, domain):

        """
        Define a new lab member in a specific website, directly from the lab website.
        The given email_to_register must not be associated with a member(manager/lab member/creator..) of the given website.
        This operation can be done only by lab manager
        """
        self.allWebsitesUserFacade.register_new_LabMember_from_labWebsite(manager_userId, email_to_register,
                                                                          lab_member_fullName, lab_member_degree,
                                                                          domain)

    def create_new_site_manager_from_generator(self, domain, nominated_manager_email):
        """
        Define and add new manager to a specific website, from generator site.
        The given nominated_manager_email must be associated with a Lab Member of the given website.
        """
        self.allWebsitesUserFacade.create_new_site_manager_from_generator(nominated_manager_email, domain)

    def register_new_LabMember_from_generator(self, email_to_register, lab_member_fullName, lab_member_degree, domain):
        """
        Define a new lab member in a specific website, from generator site.
        The given email_to_register must not be associated with a member(manager/lab member/creator..) of the given website.
        """
        self.allWebsitesUserFacade.register_new_LabMember_from_generator(email_to_register, lab_member_fullName,
                                                                         lab_member_degree, domain)

    def crawl_for_publications(self):
        """
        Fetches publications for the given authors and year from all WebCrawlers for all websites, and send
        notifications to authors for initial approve/disapprove.
        """
        # get list of all websites
        websites = self.websiteFacade.get_all_websites()

        # for each website, send to the webCrawler facade the members and current year to fetch publications
        for website in websites:
            members_names = self.allWebsitesUserFacade.get_active_members_names(website.get_domain())
            websitePublications = self.webCrawlerFacade.fetch_publications(members_names, datetime.now().year)

            # check for each publication that is not already in website members publications
            for publication in websitePublications:
                if not website.check_publication_exist(publication):
                    authorsEmails = []
                    for author in publication.authors:
                        authorsEmails.append(self.allWebsitesUserFacade.getMemberEmailByName(author, website.domain))
                    website.create_publication(publication, authorsEmails)

                    # send notifications to the website authors about the new publications, for initial approve
                    for authorEmail in authorsEmails:
                        self.notificationsFacade.send_publication_notification(publication, authorEmail,
                                                                               website.get_domain())

    def initial_approve_publication_by_author(self, userId, domain, notification_id):
        """
        Approve a publication by its author in the initial review stage.
        If the publication has not yet been final approved by a lab manager,
        the system sends a notification to lab managers requesting final approval.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_by_userId(userId)
        publication_id = self.mark_as_read(userId, domain, notification_id)
        self.websiteFacade.error_if_member_is_not_publication_author(domain, publication_id, email)
        if not self.websiteFacade.check_if_publication_approved(domain, publication_id):
            managers_emails = list(userFacade.getManagers().keys())
            # check if useId is manager. if he is not, do the following rows
            if not userFacade.verify_if_member_is_manager(email):
                self.websiteFacade.initial_approve_publication(domain, publication_id)
                for manager_email in managers_emails:
                    publicationDTO = self.websiteFacade.get_publication_by_paper_id(domain, publication_id)
                    self.notificationsFacade.send_publication_notification_for_final_approval(publicationDTO,
                                                                                              manager_email, domain)
            else:
                self.final_approve_publication_by_manager(userId, domain, publication_id)
        else:
            raise Exception(ExceptionsEnum.PUBLICATION_ALREADY_APPROVED.value)

    def final_approve_publication_by_manager(self, userId, domain, notification_id):
        """
        Approve a publication by a lab manager in the final review stage.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        userFacade.error_if_user_is_not_manager(userId)
        publication_id = self.mark_as_read(userId, domain, notification_id)
        self.websiteFacade.final_approve_publication(domain, publication_id)

    def reject_publication(self, userId, domain, notification_id):
        """
        Reject a publication by a lab manager in the final review stage.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        publication_id = self.mark_as_read(userId, domain, notification_id)
        self.websiteFacade.reject_publication(domain, publication_id)

    def add_publication_manually(self, user_id, domain, publication_link, git_link, video_link, presentation_link):
        """A Lab Member updates the website with new research publications"""
        self.allWebsitesUserFacade.error_if_domain_not_exist(domain)
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(user_id)
        userFacade.error_if_user_not_logged_in(user_id)
        userFacade.error_if_user_is_not_labMember_manager_creator(user_id)

        # Get publication details
        publication_details = self.webCrawlerFacade.get_details_by_link(publication_link)

        # Replace author names with emails
        if 'authors' in publication_details:
            authors_emails = [
                userFacade.getMemberEmailByName(author) for author in publication_details['authors']
            ]

        # Create the new publication
        publication_id = self.websiteFacade.create_new_publication(
            domain, publication_link, publication_details, git_link, video_link, presentation_link, authors_emails
        )

        email = userFacade.get_email_by_userId(user_id)
        if not userFacade.verify_if_member_is_manager(email):
            managers_emails = list(userFacade.getManagers().keys())
            for manager_email in managers_emails:
                publicationDTO = self.websiteFacade.get_publication_by_paper_id(domain, publication_id)
                self.notificationsFacade.send_publication_notification_for_final_approval(publicationDTO, manager_email,
                                                                                          domain)
        else:
            self.websiteFacade.final_approve_publication(domain, publication_id)

    def get_all_approved_publication(self, domain):
        """
        return all approved publications of a specific website
        (in order to display them on the publication component of the website)
        """
        return self.websiteFacade.get_all_approved_publication(domain)

    def get_all_approved_publications_of_member(self, domain, user_id):
        """
        return all approved publications of a specific member of the lab website
        (in order to display them on his personal profile on the website)
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(user_id)
        userFacade.error_if_user_not_logged_in(user_id)
        email = userFacade.get_email_by_userId(user_id)
        return self.websiteFacade.get_all_approved_publications_of_member(domain, email)

    def define_member_as_alumni_from_generator(self, member_email, domain):
        """
        define member (lab manager or lab member) as alumni
        Only managers can perform this operation.
        Site creator cant be defined as alumni.
        """
        return self.allWebsitesUserFacade.define_member_as_alumni_from_generator(member_email, domain)

    def define_member_as_alumni(self, manager_userId, member_email, domain):
        """
        define member (lab manager or lab member) as alumni
        Only managers can perform this operation.
        Site creator cant be defined as alumni.
        """
        # TODO: Change it so site creator can be defined as alumni if he is replaced by another site creator
        return self.allWebsitesUserFacade.define_member_as_alumni(manager_userId, member_email, domain)

    def remove_manager_permission(self, manager_userId, manager_toRemove_email, domain):
        """A Lab Manager(manager_userId) removes the administrative permissions of another Lab Manager,
        reverting their role to a Lab Member.
        The permissions of the lab creator cannot be removed, it must always remain a Lab Manager"""
        return self.allWebsitesUserFacade.remove_manager_permission(manager_userId, manager_toRemove_email, domain)

    def remove_manager_permission_from_generator(self, manager_toRemove_email, domain):
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.remove_manager_permissions(manager_toRemove_email)

    def remove_alumni_from_generator(self, alumni_email, domain):
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.remove_alumni(alumni_email)

    def get_all_alumnis(self, domain):
        return self.allWebsitesUserFacade.get_all_alumnis(domain)

    def get_all_lab_members(self, domain):
        return self.allWebsitesUserFacade.get_all_lab_members(domain)

    def get_all_lab_managers(self, domain):
        """notice! this function returns all managers including site creator!"""
        return self.allWebsitesUserFacade.get_all_lab_managers(domain)

    def set_secondEmail_by_member(self, userid, secondEmail, domain):
        self.allWebsitesUserFacade.set_secondEmail_by_member(userid, secondEmail, domain)

    def set_linkedin_link_by_member(self, userid, linkedin_link, domain):
        self.allWebsitesUserFacade.set_linkedin_link_by_member(userid, linkedin_link, domain)

    def set_media_by_member(self, userid, media, domain):
        self.allWebsitesUserFacade.set_media_by_member(userid, media, domain)

    def set_fullName_by_member(self, userid, fullName, domain):
        self.allWebsitesUserFacade.set_fullName_by_member(userid, fullName, domain)

    def set_degree_by_member(self, userid, degree, domain):
        self.allWebsitesUserFacade.set_degree_by_member(userid, degree, domain)

    def set_bio_by_member(self, userid, bio, domain):
        self.allWebsitesUserFacade.set_bio_by_member(userid, bio, domain)



    def get_preview_url(self, original_url):
        # Handle YouTube links
        youtube_match = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w\-]+)", original_url)
        if youtube_match:
            video_id = youtube_match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"

        # Handle Google Drive links
        drive_match = re.search(r"drive\.google\.com/file/d/([\w-]+)", original_url)
        if drive_match:
            file_id = drive_match.group(1)
            return f"https://drive.google.com/file/d/{file_id}/preview"

        return original_url  # If the URL is neither YouTube nor Google Drive
    
    def set_publication_video_link(self, userId, domain, publication_id, video_link):
        """
        Set video link for a publication.
        - Authors can add video links, but it must be approved by a lab manager (the notification feature - in the future).
        - Lab managers can add video links directly without approval.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_by_userId(userId)
        if userFacade.verify_if_member_is_manager(email):
            self.websiteFacade.set_publication_video_link(domain, publication_id, self.get_preview_url(video_link))
        else:
            self.websiteFacade.error_if_member_is_not_publication_author(domain, publication_id, email)
            self.websiteFacade.set_publication_video_link(domain, publication_id, self.get_preview_url(video_link))

    def set_publication_git_link_by_author(self, userId, domain, publication_id, git_link):
        """
        Set git link for a publication.
        - Authors can add git links, but it must be approved by a lab manager (the notification feature - in the future).
        - Lab managers can add git links directly without approval.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_by_userId(userId)
        if userFacade.verify_if_member_is_manager(email):
            self.websiteFacade.set_publication_git_link(domain, publication_id, git_link)
        else:
            self.websiteFacade.error_if_member_is_not_publication_author(domain, publication_id, email)
            self.websiteFacade.set_publication_git_link(domain, publication_id, git_link)

    def set_publication_presentation_link_by_author(self, userId, domain, publication_id, presentation_link):
        """
        Set presentation link for a publication .
        - Authors can add presentation links, but it must be approved by a lab manager (the notification feature - in the future).
        - Lab managers can add presentation links directly without approval.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_by_userId(userId)
        if userFacade.verify_if_member_is_manager(email):
            self.websiteFacade.set_publication_presentation_link(domain, publication_id, presentation_link)
        else:
            self.websiteFacade.error_if_member_is_not_publication_author(domain, publication_id, email)
            self.websiteFacade.set_publication_presentation_link(domain, publication_id, presentation_link)
            # TODO: in the future, send notification to lab manager for approve

    def get_all_members_names(self, domain):
        '''
        returns all lab members + managers + site creator + alumnis names
        '''
        return self.allWebsitesUserFacade.get_all_members_names(domain)

    def get_pending_registration_emails(self, userid, domain):
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userid)
        userFacade.error_if_user_not_logged_in(userid)
        return self.allWebsitesUserFacade.get_pending_registration_emails(domain)

    def set_site_about_us_from_generator(self, domain, about_us):
        """
        Set the about us section of the website.
        """
        self.websiteFacade.set_site_about_us(domain, about_us)

    def set_site_about_us_from_labWebsite(self, userId, domain, about_us):
        """
        Set the about us section of the website.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        userFacade.error_if_user_is_not_manager_or_site_creator(userId)
        self.websiteFacade.set_site_about_us(domain, about_us)

    def set_site_contact_info_from_generator(self, domain, contact_info_dto):
        """
        Set the contact us section of the website.
        """
        self.websiteFacade.set_site_contact_info(domain, contact_info_dto)

    def set_site_contact_info_from_labWebsite(self, userId, domain, contact_info_dto):
        """
        Set the contact us section of the website.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        userFacade.error_if_user_is_not_manager_or_site_creator(userId)
        self.websiteFacade.set_site_contact_info(domain, contact_info_dto)

    def get_about_us(self, domain):
        """
        Get the about us section of the website.
        """
        return self.websiteFacade.get_about_us(domain)

    def get_all_lab_members_details(self, domain):
        """
        Get all lab members details.
        """
        return self.allWebsitesUserFacade.get_all_lab_members_details(domain)

    def get_all_lab_managers_details(self, domain):
        """
        Get all lab managers details.
        """
        return self.allWebsitesUserFacade.get_all_lab_managers_details(domain)

    def get_all_alumnis_details(self, domain):
        """
        Get all alumnis details.
        """
        return self.allWebsitesUserFacade.get_all_alumnis_details(domain)

    def get_user_details(self, userId, domain):
        """
        Get user details.
        """
        return self.allWebsitesUserFacade.get_user_details(userId, domain)

    def get_contact_us(self, domain):
        return self.websiteFacade.get_contact_us(domain)

    def site_creator_resignation_from_lab_website(self, user_id, domain, nominate_email, new_role):
        """
        Site creator resignation from lab website.
        """
        self.allWebsitesUserFacade.site_creator_resignation_from_lab_website(user_id, domain, nominate_email, new_role)

    def site_creator_resignation_from_generator(self, domain, nominate_email, new_role):
        """
        Site creator resignation from generator.
        """
        self.allWebsitesUserFacade.site_creator_resignation_from_generator(domain, nominate_email, new_role)

    def get_all_member_notifications(self, userId, domain):
        """
        Get all notifications of a specific user.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_by_userId(userId)
        return self.notificationsFacade.get_notifications_for_user(domain, email)

    def mark_as_read(self, userId, domain, notification_id):
        """
        Mark notification as read, and return the email\ publication id of the notification.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_notExist(userId)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_by_userId(userId)
        return self.notificationsFacade.mark_notification_as_read(domain, email, notification_id)

    def connect_user_socket(self, email, domain, sid):
        """
        Connect a user socket to the system.
        """
        self.notificationsFacade.connect_user_socket(email, domain, sid)

    def disconnect_user_socket(self, sid):
        """
        Disconnect a user socket from the system.
        """
        self.notificationsFacade.disconnect_user_socket(sid)
