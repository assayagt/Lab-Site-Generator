import threading
import time
from datetime import datetime, timedelta
import re
from src.main.DomainLayer.LabWebsites.WebCrawler.WebCrawlerFacade import WebCrawlerFacade
from src.main.DomainLayer.LabWebsites.Website.WebsiteFacade import WebsiteFacade
from src.main.DomainLayer.LabWebsites.Notifications.NotificationsFacade import NotificationsFacade
from src.main.DomainLayer.LabWebsites.User.AllWebsitesUserFacade import AllWebsitesUserFacade
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class LabSystemController:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(LabSystemController, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.webCrawlerFacade = WebCrawlerFacade()
        self.websiteFacade = WebsiteFacade()
        self.notificationsFacade = NotificationsFacade()
        self.allWebsitesUserFacade = AllWebsitesUserFacade()
        self._initialized = True


    @classmethod
    def get_instance(cls):
        return cls()

    # @classmethod
    # def reset_instance(cls):
    #     """Reset the singleton instance. Useful for unit tests."""
    #     with cls._instance_lock:
    #         if cls._instance:
    #             cls._instance._stop_eviction.set()
    #         cls._instance = None

    def enter_lab_website(self, domain):
        """
        Enter a specific lab website
        This function returns a unique userId for the user
        """
        self.allWebsitesUserFacade.error_if_domain_not_exist(domain)
        return self.allWebsitesUserFacade.add_user_to_website(domain)

    def create_new_lab_website(self, domain, lab_members, lab_managers, site_creator, creator_scholar_link):
        """
        Create a new lab website with the given domain, lab members, lab managers, and site creator.
        Each lab member, lab manager, and site creator now includes a degree field.
        """
        self.websiteFacade.create_new_website(domain)
        # self.allWebsitesUserFacade.add_new_webstie_userFacade(domain)
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)

        # Add lab members
        for lab_member_email, lab_member_details in lab_members.items():
            full_name = lab_member_details["full_name"]
            degree = lab_member_details["degree"]
            userFacade.register_new_LabMember(lab_member_email, full_name, degree) 

        # Add lab managers
        for lab_manager_email, lab_manager_details in lab_managers.items():
            full_name = lab_manager_details["full_name"]
            degree = lab_manager_details["degree"]
            userFacade.create_new_site_manager(lab_manager_email, full_name, degree) 

        # Set site creator
        site_creator_email = site_creator.get("email")
        site_creator_full_name = site_creator.get("full_name")
        site_creator_degree = site_creator.get("degree")
        userFacade.set_site_creator(site_creator_email, site_creator_full_name, site_creator_degree, creator_scholar_link) 

        #fetch publications initially
        self.crawl_publications_for_website(website_domain=domain, with_notifications=False)
        time.sleep(10)


    def login(self, domain, google_token):
        """
        Login user into a specific website by google_token.
        If the given email is not associated with a member, an email is sent to all managers in order to approve or reject
        the registration request
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        email = userFacade.get_email_from_token(google_token)
        # userFacade.error_if_user_notExist(userId)
        member = userFacade.get_member_by_email(email)
        if member is None:
            # check if registration request already sent to managers:
            userFacade.error_if_email_is_in_requests_and_wait_approval(email)
            # error if registration request already sent to managers and rejected:
            userFacade.error_if_email_is_in_requests_and_rejected(email)
            # send registration request to all LabManagers:
            self.send_registration_notification_to_all_LabManagers(domain, email) #notification here
            # keep the email in the requests list, so next time the user will login, a registration request wont be sent again:
            userFacade.add_email_to_requests(email)
            raise Exception(ExceptionsEnum.USER_NOT_REGISTERED.value)
        return email

    def send_registration_notification_to_all_LabManagers(self, domain, requestedEmail):
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        managers = userFacade.get_managers_emails()
        siteCreator = userFacade.get_site_creator_emails()
        recipients = managers + siteCreator
        print("recipients: ", recipients)
        for managerEmail in recipients:
            send_email_notification = self.get_if_email_notifications_enabled(managerEmail,
                                                                              domain)
            self.notificationsFacade.send_registration_request_notification(requestedEmail, managerEmail, domain, send_email_notification)

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
        """
        self.allWebsitesUserFacade.create_new_site_manager_from_labWebsite(
            nominator_manager_userId,
            nominated_manager_email,
            domain
        )
        #NOTE: not adding new user to the website so no crawling needed
        # #name = self.allWebsitesUserFacade.get_fullName_by_email(nominated_manager_email, domain)
        # threading.Thread(
        #     target=self.webCrawlerFacade.fetch_publications_new_member,
        #     args=([name], domain),
        #     daemon=True
        # ).start()

    def register_new_LabMember_from_labWebsite(self, manager_userId, email_to_register, lab_member_fullName,
                                               lab_member_degree, domain):
        """
        Define a new lab member in a specific website, directly from the lab website.
        """
        self.allWebsitesUserFacade.register_new_LabMember_from_labWebsite(
            manager_userId,
            email_to_register,
            lab_member_fullName,
            lab_member_degree,
            domain
        )
        #NOTE: new users will need to crawl publications with button when adding scholar link================================================================================
        # threading.Thread(
        #     target=self.webCrawlerFacade.fetch_publications_new_member,
        #     args=([lab_member_fullName], domain),
        #     daemon=True
        # ).start()

    def create_new_site_manager_from_generator(self, domain, nominated_manager_email):
        """
        Define and add new manager to a specific website, from generator site.
        """
        self.allWebsitesUserFacade.create_new_site_manager_from_generator(
            nominated_manager_email, domain
        )
        name = self.allWebsitesUserFacade.get_fullName_by_email(nominated_manager_email, domain)
        #NOTE: not adding new user to the website so no crawling needed
        # threading.Thread(
        #     target=self.webCrawlerFacade.fetch_publications_new_member,
        #     args=([name], domain),
        #     daemon=True
        # ).start()

    def register_new_LabMember_from_generator(self, email_to_register, lab_member_fullName, lab_member_degree, domain):
        """
        Define a new lab member in a specific website, from generator site.
        """
        self.allWebsitesUserFacade.register_new_LabMember_from_generator(
            email_to_register, lab_member_fullName, lab_member_degree, domain
        )
        #NOTE: new users will need to crawl publications with button when adding scholar link================================================================================
        # threading.Thread(
        #     target=self.webCrawlerFacade.fetch_publications_new_member,
        #     args=([lab_member_fullName], domain),
        #     daemon=True
        # ).start()

    def crawl_for_publications(self):
        """
        Fetches publications for the given authors and year from all WebCrawlers for all websites, and send
        notifications to authors for initial approve/disapprove.
        """
        # get list of all websites
        website_domains = self.websiteFacade.get_all_website_domains()

        # for each website, send to the webCrawler facade the members and current year to fetch publications
        for domain in website_domains:
            self.crawl_publications_for_website(website_domain=domain, with_notifications=True)

    def initial_approve_multiple_publications_by_author(self, userId, domain, publication_ids: list[str]):
        """
        Approve a list of publications fetched with the web crawler.
        The system send a notification to lab managers for review
        """
        print(publication_ids)
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_from_token(userId)
        is_manager = userFacade.verify_if_member_is_manager(email=email)
        if is_manager:
            self.final_approve_multiple_publications_by_manager(userId, domain, publication_ids)
            return
        for publication_id in publication_ids:
            self.websiteFacade.error_if_member_is_not_publication_author(domain, publication_id, email)
            if not self.websiteFacade.check_if_publication_approved(domain, publication_id):      
                # check if userId is manager. if he is not, do the following rows
                if not is_manager:
                    self.websiteFacade.initial_approve_publication(domain, publication_id)
            else:
                raise Exception(ExceptionsEnum.PUBLICATION_ALREADY_APPROVED.value)
        if not is_manager:
            managers_emails = userFacade.get_managers_emails()
            for mail in managers_emails:
                self.notificationsFacade.send_multiple_pubs_notification_for_final_approval(mail, domain)
                        
    def initial_approve_publication_by_author(self, userId, domain, notification_id):
        """
        Approve a publication by its author in the initial review stage.
        If the publication has not yet been final approved by a lab manager,
        the system sends a notification to lab managers requesting final approval.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_from_token(userId)
        publication_id = self.mark_as_read(userId, domain, notification_id)
        self.websiteFacade.error_if_member_is_not_publication_author(domain, publication_id, email)
        if not self.websiteFacade.check_if_publication_approved(domain, publication_id):
            managers_emails = userFacade.get_managers_emails()
            # check if userId is manager. if he is not, do the following rows
            if not userFacade.verify_if_member_is_manager(email):
                self.websiteFacade.initial_approve_publication(domain, publication_id)
                for manager_email in managers_emails:
                    publicationDTO = self.websiteFacade.get_publication_by_paper_id(domain, publication_id)
                    send_email_notification = self.get_if_email_notifications_enabled(manager_email,
                                                                                      domain)
                    self.notificationsFacade.send_publication_notification_for_final_approval(publicationDTO,
                                                                                              manager_email, domain, send_email_notification)
            else:
                self.final_approve_publication_by_manager(userId, domain, publication_id)
        else:
            raise Exception(ExceptionsEnum.PUBLICATION_ALREADY_APPROVED.value)

    def final_approve_publication_by_manager(self, userId, domain, notification_id): #TODO place fill publication details here!
        """
        Approve a publication by a lab manager in the final review stage.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(userId)
        userFacade.error_if_user_is_not_manager_or_site_creator(userId)
        publication_id = self.mark_as_read(userId, domain, notification_id)
        pub_dto = self.websiteFacade.get_publication_by_paper_id(domain, publication_id)
        future = self.webCrawlerFacade.fill_async([pub_dto])
        def _on_done(fut):
            try:
                filled_pubs = fut.result()
                filled_pub = filled_pubs[0]
                self.websiteFacade.update_publication(domain, pub_dto)
                self.websiteFacade.final_approve_publication(domain, publication_id)
            except Exception as e:
                print(f"[ERROR] final approve callback failed: {e}")
        future.add_done_callback(_on_done)
        return future
        
        
        
    def final_approve_multiple_publications_by_manager(self, userId, domain, publicationIds:list[str]):
        """
        Approve multiple publicatios at once by a lab manager in the final review stage.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(userId)
        userFacade.error_if_user_is_not_manager_or_site_creator(userId)

        pub_dtos = [self.websiteFacade.get_publication_by_paper_id(domain, pubId)
                     for pubId in publicationIds]
        future = self.webCrawlerFacade.fill_async(pubs=pub_dtos)
        def _on_done(fut):
            try:
                filled_pubs = fut.result()
                for pub in filled_pubs:
                    self.websiteFacade.update_publication(domain, pub)
                    self.websiteFacade.final_approve_publication(domain, pub.get_paper_id())
            except Exception as e:
                print(f"[ERROR] final-approve-multiple callback failed: {e}")
        future.add_done_callback(_on_done)
        return future
        # for pubId in publicationIds:
        #     pub_dto = self.websiteFacade.get_publication_by_paper_id(domain,pubId)
        #     self.webCrawlerFacade.fill_pub_details([pub_dto])
        #     self.websiteFacade.update_publication(domain, pub_dto)
        #     self.websiteFacade.final_approve_publication(domain, pubId)

    def reject_publication(self, userId, domain, notification_id):
        """
        Reject a publication by a lab manager in the final review stage.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_from_token(userId)
        userFacade.error_if_user_is_not_labMember_manager_creator(email)
        publication_id = self.mark_as_read(userId, domain, notification_id)
        self.websiteFacade.reject_publication(domain, publication_id)

    def reject_multiple_publications(self, userId, domain, publicationIds:list[str]):
        """
        Reject multiple publications by a lab manager in the final review stage.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(userId=userId)
        email = userFacade.get_email_from_token(userId)
        userFacade.error_if_user_is_not_labMember_manager_creator(email)
        for pubId in publicationIds:
            self.websiteFacade.reject_publication(domain, pubId)

    def remove_publication_by_manager(self, userId, domain, publicationId):
        """
        Delete publication by lab manager
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(userId=userId)
        email = userFacade.get_email_from_token(userId)
        userFacade.error_if_user_is_not_labMember_manager_creator(email)
        self.websiteFacade.error_if_publication_is_rejected(domain=domain, publication_id=publicationId)
        
        email = userFacade.get_email_from_token(userId)
        rejecting_name = userFacade.get_fullName_by_email(email)
        pub = self.websiteFacade.get_publication_by_paper_id(domain=domain, paper_id=publicationId)
        authors = pub.author_emails
        self.websiteFacade.reject_publication(domain, publication_id=publicationId)
        for author in authors:
            self.notificationsFacade.send_email_notification_removing_pub(recipientEmail=author, publicationDTO=pub, deleting_manager_name=rejecting_name, domain=domain)

    def add_publication_manually(self, user_id, domain, publication_link, git_link, video_link, presentation_link):
        """A Lab Member updates the website with new research publications"""
        self.allWebsitesUserFacade.error_if_domain_not_exist(domain)
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(user_id)
        userFacade.error_if_user_is_not_labMember_manager_creator(user_id)

        # Get publication details
        publication_details = self.webCrawlerFacade.get_details_by_link(publication_link)

        # Replace author names with emails
        if 'authors' in publication_details:
            authors_emails = [
            email for email in (
                userFacade.getMemberEmailByName(author) for author in publication_details['authors']
            ) if email is not None
        ]
        if len(authors_emails)==0:
            raise Exception(ExceptionsEnum.AUTHOR_NOT_A_USER.value)
        # Create the new publication
        publication_id = self.websiteFacade.create_new_publication(
            domain, publication_link, publication_details, git_link, video_link, presentation_link, authors_emails
        )

        email = userFacade.get_email_from_token(user_id)
        if not userFacade.verify_if_member_is_manager(email):
            managers_emails = userFacade.get_managers_emails()
            for manager_email in managers_emails:
                publicationDTO = self.websiteFacade.get_publication_by_paper_id(domain, publication_id)
                #TODO: Add email notification
                send_email_notification = self.get_if_email_notifications_enabled(manager_email,
                                                                                  domain)
                self.notificationsFacade.send_publication_notification_for_final_approval(publicationDTO, manager_email,
                                                                                          domain, send_email_notification)
        else:
            self.websiteFacade.final_approve_publication(domain, publication_id)
        return publication_id

    def get_all_approved_publication(self, domain):
        """
        return all approved publications of a specific website
        (in order to display them on the publication component of the website)
        """
        return self.websiteFacade.get_all_approved_publication(domain)
    
    def get_all_not_approved_publications(self, domain):
        """
        return all non aprovved publications for some website
        """
        return self.websiteFacade.get_all_not_approved_publications(domain)

    def get_all_approved_publications_of_member(self, domain, user_id):
        """
        return all approved publications of a specific member of the lab website
        (in order to display them on his personal profile on the website)
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(user_id)
        email = userFacade.get_email_from_token(user_id)
        return self.websiteFacade.get_all_approved_publications_of_member(domain, email)
    
    def get_all_not_approved_publications_of_member(self, domain, user_id):
        """
        return all not approved publications of a specific member of the lab website
        (in order to display them on his personal profile on the website)
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(user_id)
        email = userFacade.get_email_from_token(user_id)
        return self.websiteFacade.get_all_not_approved_publications_of_member(domain, email)

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

    def set_secondEmail_by_member(self, userid, secondEmail, domain):
        self.allWebsitesUserFacade.set_secondEmail_by_member(userid, secondEmail, domain)

    def set_linkedin_link_by_member(self, userid, linkedin_link, domain):
        self.allWebsitesUserFacade.set_linkedin_link_by_member(userid, linkedin_link, domain)

    def set_scholar_link_by_member(self, userid, schoalr_link, domain):
        self.allWebsitesUserFacade.set_scholar_link_by_member(userid, schoalr_link, domain)

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
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_from_token(userId)
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
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_from_token(userId)
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
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_from_token(userId)
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
        # checko that phone number is valid
        if not re.match(r"^\+?[0-9\s\-()]+$", contact_info_dto.lab_phone_num):
            raise Exception(ExceptionsEnum.INVALID_PHONE_NUMBER.value)
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
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
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_from_token(userId)
        return self.notificationsFacade.get_notifications_for_user(domain, email)

    def mark_as_read(self, userId, domain, notification_id):
        """
        Mark notification as read, and return the email/ publication id of the notification.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_from_token(userId)
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

    def reset_system(self):
        """
        Reset the system.
        """
        self.allWebsitesUserFacade.reset_system()
        self.websiteFacade.reset_system()
        self.notificationsFacade.reset_system()

    def remove_alumni_from_labWebsite(self, manager_user_id, alumni_email, domain):
        """
        Remove an alumni and revert them to a lab member (from the lab website, by a manager).
        Only managers can perform this operation.
        Site creator cannot be removed as alumni.
        """
        return self.allWebsitesUserFacade.remove_alumni_from_labWebsite(manager_user_id, alumni_email, domain)

    def crawl_publications_for_website(self, website_domain, with_notifications=True):
        """
            this function crawls publications for some website with the option to get notifications for every new publication found
        """
        website = self.websiteFacade.get_website(website_domain)
        member_scholar_links = self.allWebsitesUserFacade.get_active_members_scholarLinks(website_domain)
        print(member_scholar_links)
        future = self.webCrawlerFacade.fetch_async(member_scholar_links)
        def _on_done(fut):
            try:
                publist = fut.result()
                for pub in publist:
                    if not website.check_publication_exist(pub):
                        print(pub.authors)
                        authorEmails = []
                        for author in pub.authors:
                            email = self.allWebsitesUserFacade.getMemberEmailByName(author=author, domain=website_domain)
                            if email:
                                print(f"found: {email}")
                                authorEmails.append(email)
                        if not authorEmails:
                            continue
                        pub.set_author_emails(authorEmails)
                        pub.set_domain(website_domain)
                        self.websiteFacade.create_new_publication_fromDTO(domain=website_domain, pubDTO=pub, author_emails=authorEmails)
                        print("added pub successfully")
                        if with_notifications:
                            # send notifications to the website authors about the new publications, for initial approval.
                            for authorEmail in authorEmails:
                                send_email_notification = self.get_if_email_notifications_enabled(authorEmail,
                                                                                                  website_domain)
                                self.notificationsFacade.send_publication_notification(pub, authorEmail,
                                                                                    website_domain, send_email_notification)
            except Exception as e:
                print(f"[ERROR] post-crawl processing failed: {e}")
        future.add_done_callback(_on_done)
        return future
                        

    def crawl_publications_for_labMember(self, website_domain, userId, with_notifications=True):
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(website_domain)
        userFacade.error_if_user_not_logged_in(userId)
        email = userFacade.get_email_from_token(userId)
        website = self.websiteFacade.get_website(website_domain)
        scholar_link = self.allWebsitesUserFacade.get_scholar_link_by_email(domain=website_domain, email=email)
        if not scholar_link:
            return
        fetch_fut = self.webCrawlerFacade.fetch_async([scholar_link])
        def _on_done(fut):
            try:
                member_pubs = fut.result()
                for pub in member_pubs:
                    if not website.check_publication_exist(pub):
                        authorEmails = []
                        for author in pub.authors:
                            email = self.allWebsitesUserFacade.getMemberEmailByName(author=author, domain=website_domain)
                            if email:
                                authorEmails.append(email)
                        pub.set_author_emails(author_emails=authorEmails)
                        website.create_publication(publicationDTO=pub, authors_emails=authorEmails)
                        if with_notifications:
                            # send notifications to the website authors about the new publications, for initial approve
                            for authorEmail in authorEmails:
                                send_email_notification = self.get_if_email_notifications_enabled(authorEmail, website_domain)
                                self.notificationsFacade.send_publication_notification(pub, authorEmail,
                                                                                    website_domain, send_email_notification)
            except Exception as e:
                print(f"[ERROR] crawl failed for {scholar_link}: {e}")
                return
        fetch_fut.add_done_callback(_on_done)
        return fetch_fut

    def add_news_record(self, user_id, domain, text, link, date):
        """
        Add a news record to the website.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(user_id)
        self.websiteFacade.add_news_record(domain, text, link, date)

    def get_news(self, domain):
        """
        Get all news records of the website.
        """
        return self.websiteFacade.get_news(domain)

    def add_profile_picture(self, user_id, domain, file_path):
        """
        Add a profile picture for a user.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(user_id)
        userFacade.add_profile_picture(user_id, file_path)

    def set_member_email_notifications(self, user_id, domain, email_notifications):
        """
        Set email notifications preference for a user.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        userFacade.error_if_user_not_logged_in(user_id)
        userFacade.set_email_notifications(user_id, email_notifications)

    def get_if_email_notifications_enabled(self, email, domain):
        """
        Get email notifications preference for a user.
        """
        userFacade = self.allWebsitesUserFacade.getUserFacadeByDomain(domain)
        return userFacade.get_email_notifications(email)

