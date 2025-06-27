# Lab Website Generator API - Maintenance Manual

## General Information

This API is the backend access interface for the Lab Website Generator system. The frontend uses this API to communicate with the backend Flask server. The backend is accessed via HTTP GET and POST requests to server endpoints.

**Base URL:** `http://127.0.0.1:5000/api/`

## Data Objects Used

### Response Object
All API endpoints return a standardized response structure:
```json
{
  // "true" if succeeded, "false" if failed
  "response": string,
  // holds the success message if response is "true"
  "message": string,
  // holds the error message if response is "false"
  "error": string,
  // contains the requested data (varies by endpoint)
  "data": object
}
```

### User Object
```json
{
  "user_id": string,
  "email": string,
  "fullName": string,
  "bio": string,
  "degree": string,
  "secondEmail": string,
  "linkedin_link": string,
  "scholar_link": string,
  "emailNotifications": boolean
}
```

### Publication Object
```json
{
  "paper_id": string,
  "title": string,
  "publication_year": string,
  "publication_link": string,
  "git_link": string,
  "video_link": string,
  "presentation_link": string,
  "status": string // "Approved", "pending", "rejected", etc.
}
```

### Website Object
```json
{
  "domain": string,
  "name": string,
  "template": string,
  "components": string[],
  "logo": string, // base64 encoded image
  "home_picture": string, // base64 encoded image
  "about_us": string,
  "contact_us": object,
  "gallery_images": string[]
}
```

### Notification Object
```json
{
  "id": string,
  "subject": string,
  "body": string,
  "timestamp": string
}
```

### ContactInfo Object
```json
{
  "lab_address": string,
  "lab_mail": string,
  "lab_phone_num": string
}
```

## API Endpoints

### Generator System Endpoints

#### Enter Generator System
- **URL:** `/api/enterGeneratorSystem`
- **Method:** GET
- **Description:** Generates a new guest ID for entering the system
- **Response:**
```json
{
  "user_id": string,
  "message": string
}
```

#### Login
- **URL:** `/api/Login`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "google_token": string
}
```
- **Response:**
```json
{
  "message": string,
  "response": string,
  "email": string
}
```

#### Logout
- **URL:** `/api/Logout`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string
}
```

#### Generate Website
- **URL:** `/api/generateWebsite`
- **Method:** POST
- **Parameters:**
```json
{
  "domain": string,
  "about_us": string,
  "lab_address": string,
  "lab_mail": string,
  "lab_phone_num": string,
  "participants": [
    {
      "email": string,
      "fullName": string,
      "degree": string,
      "isLabManager": boolean
    }
  ],
  "creator_scholar_link": string
}
```

#### Choose Domain
- **URL:** `/api/chooseDomain`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "old_domain": string,
  "domain": string
}
```

#### Choose Components
- **URL:** `/api/chooseComponents`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "components": string, // comma-separated list
  "domain": string
}
```

#### Choose Template
- **URL:** `/api/chooseTemplate`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "template": string,
  "domain": string
}
```

#### Choose Name
- **URL:** `/api/chooseName`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "website_name": string,
  "domain": string
}
```

#### Get Custom Websites
- **URL:** `/api/getCustomWebsites`
- **Method:** GET
- **Parameters:** `user_id` (query parameter)
- **Response:**
```json
{
  "websites": object, // map of domain to site details
  "response": string
}
```

#### Get Custom Site
- **URL:** `/api/getCustomSite`
- **Method:** GET
- **Parameters:** `user_id`, `domain` (query parameters)
- **Response:**
```json
{
  "data": {
    "domain": string,
    "name": string,
    "components": string[],
    "template": string,
    "logo": string,
    "home_picture": string,
    "about_us": string,
    "contact_us": object
  },
  "response": string
}
```

#### Delete Website
- **URL:** `/api/deleteWebsite`
- **Method:** DELETE
- **Parameters:** `user_id`, `domain` (query parameters)

### Lab Website Endpoints

#### Enter Lab Website
- **URL:** `/api/enterLabWebsite`
- **Method:** GET
- **Parameters:** `domain` (query parameter)
- **Response:**
```json
{
  "message": string,
  "user_id": string,
  "response": string
}
```

#### Login Website
- **URL:** `/api/loginWebsite`
- **Method:** POST
- **Parameters:**
```json
{
  "domain": string,
  "user_id": string,
  "google_token": string
}
```

#### Logout Website
- **URL:** `/api/logoutWebsite`
- **Method:** POST
- **Parameters:**
```json
{
  "domain": string,
  "user_id": string
}
```

#### Get Homepage Details
- **URL:** `/api/getHomepageDetails`
- **Method:** GET
- **Parameters:** `domain` (query parameter)
- **Response:**
```json
{
  "data": {
    "domain": string,
    "name": string,
    "components": string[],
    "template": string,
    "logo": string,
    "home_picture": string,
    "about_us": string,
    "news": object[]
  },
  "response": string
}
```

### User Management Endpoints

#### Get User Details
- **URL:** `/api/getUserDetails`
- **Method:** GET
- **Parameters:** `domain`, `user_id` (query parameters)
- **Response:**
```json
{
  "user": {
    "bio": string,
    "email": string,
    "secondEmail": string,
    "degree": string,
    "linkedin_link": string,
    "fullName": string,
    "scholar_link": string,
    "emailNotifications": boolean
  },
  "response": string
}
```

#### Set Bio
- **URL:** `/api/setBio`
- **Method:** POST
- **Parameters:**
```json
{
  "userid": string,
  "bio": string,
  "domain": string
}
```

#### Set Degree
- **URL:** `/api/setDegree`
- **Method:** POST
- **Parameters:**
```json
{
  "userid": string,
  "degree": string,
  "domain": string
}
```

#### Set Second Email
- **URL:** `/api/setSecondEmail`
- **Method:** POST
- **Parameters:**
```json
{
  "userid": string,
  "secondEmail": string,
  "domain": string
}
```

#### Set LinkedIn Link
- **URL:** `/api/setLinkedInLink`
- **Method:** POST
- **Parameters:**
```json
{
  "userid": string,
  "linkedin_link": string,
  "domain": string
}
```

#### Set Scholar Link
- **URL:** `/api/setScholarLink`
- **Method:** POST
- **Parameters:**
```json
{
  "userid": string,
  "scholar_link": string,
  "domain": string
}
```

### Publication Management Endpoints

#### Get Approved Publications
- **URL:** `/api/getApprovedPublications`
- **Method:** GET
- **Parameters:** `domain` (query parameter)
- **Response:**
```json
{
  "publications": Publication[],
  "response": string
}
```

#### Add Publication
- **URL:** `/api/addPublication`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "publication_link": string,
  "domain": string,
  "git_link": string,
  "video_link": string,
  "presentation_link": string
}
```

#### Get Member Publications
- **URL:** `/api/getMemberPublications`
- **Method:** GET
- **Parameters:** `domain`, `user_id` (query parameters)

#### Get Not Approved Member Publications
- **URL:** `/api/getNotApprovedMemberPublications`
- **Method:** GET
- **Parameters:** `domain`, `user_id` (query parameters)

#### Set Publication Video Link
- **URL:** `/api/setPublicationVideoLink`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "domain": string,
  "publication_id": string,
  "video_link": string
}
```

#### Set Publication Git Link
- **URL:** `/api/setPublicationGitLink`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "domain": string,
  "publication_id": string,
  "git_link": string
}
```

#### Set Publication Presentation Link
- **URL:** `/api/setPublicationPttxLink`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "domain": string,
  "publication_id": string,
  "presentation_link": string
}
```

#### Initial Approve Publication By Author
- **URL:** `/api/initialApprovePublicationByAuthor`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "domain": string,
  "notification_id": string
}
```

#### Final Approve Publication By Manager
- **URL:** `/api/finalApprovePublicationByManager`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "domain": string,
  "notification_id": string
}
```

#### Reject Publication
- **URL:** `/api/RejectPublication`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "domain": string,
  "notification_id": string
}
```

#### Initial Approve Multiple Publications By Author
- **URL:** `/api/initialApproveMultiplePublicationsByAuthor`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "domain": string,
  "publication_IDs": string // comma-separated list
}
```

#### Reject Multiple Publications
- **URL:** `/api/rejectMultiplePublications`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "domain": string,
  "publication_IDs": string[]
}
```

### Lab Management Endpoints

#### Get All Lab Managers
- **URL:** `/api/getAllLabManagers`
- **Method:** GET
- **Parameters:** `domain` (query parameter)
- **Response:**
```json
{
  "managers": object[],
  "response": string
}
```

#### Get All Lab Members
- **URL:** `/api/getAllLabMembers`
- **Method:** GET
- **Parameters:** `domain` (query parameter)
- **Response:**
```json
{
  "members": object[],
  "response": string
}
```

#### Get All Alumni
- **URL:** `/api/getAllAlumni`
- **Method:** GET
- **Parameters:** `domain` (query parameter)
- **Response:**
```json
{
  "alumni": object[],
  "response": string
}
```

#### Add Lab Member From Website
- **URL:** `/api/addLabMemberFromWebsite`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "email": string,
  "full_name": string,
  "degree": string,
  "domain": string
}
```

#### Create New Site Manager From Lab Website
- **URL:** `/api/createNewSiteManagerFromLabWebsite`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "email": string,
  "domain": string
}
```

#### Remove Manager Permission
- **URL:** `/api/removeManagerPermission`
- **Method:** POST
- **Parameters:**
```json
{
  "manager_userId": string,
  "manager_toRemove_email": string,
  "domain": string
}
```

### Registration Management Endpoints

#### Approve Registration
- **URL:** `/api/approveRegistration`
- **Method:** POST
- **Parameters:**
```json
{
  "domain": string,
  "manager_userId": string,
  "requested_full_name": string,
  "requested_degree": string,
  "notification_id": string
}
```

#### Reject Registration
- **URL:** `/api/rejectRegistration`
- **Method:** POST
- **Parameters:**
```json
{
  "domain": string,
  "manager_userId": string,
  "notification_id": string
}
```

### File Upload Endpoints

#### Upload Files and Data
- **URL:** `/api/uploadFile`
- **Method:** POST
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `domain`: string
  - `website_name`: string
  - `logo`: file (SVG, PNG, JPG, JPEG)
  - `homepagephoto`: file (JPG, JPEG, PNG)

#### Upload Gallery Images
- **URL:** `/api/uploadGalleryImages`
- **Method:** POST
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `domain`: string
  - `gallery`: file[] (JPG, JPEG, PNG, GIF)

#### Upload Profile Picture
- **URL:** `/api/uploadProfilePicture`
- **Method:** POST
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `user_id`: string
  - `domain`: string
  - `profile_picture`: file (JPG, JPEG, PNG, GIF)

### Gallery Management Endpoints

#### Get Gallery Images
- **URL:** `/api/getGallery`
- **Method:** GET
- **Parameters:** `domain` (query parameter)
- **Response:**
```json
{
  "images": string[],
  "response": string
}
```

#### Delete Gallery Image
- **URL:** `/api/deleteGalleryImage`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "image_name": string,
  "domain": string
}
```

### News Management Endpoints

#### Add News Record
- **URL:** `/api/addNewsRecord`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "domain": string,
  "text": string,
  "link": string,
  "date": string
}
```

### Contact Information Endpoints

#### Get Contact Us
- **URL:** `/api/getContactUs`
- **Method:** GET
- **Parameters:** `domain` (query parameter)
- **Response:**
```json
{
  "data": {
    "lab_address": string,
    "lab_mail": string,
    "lab_phone_num": string
  },
  "response": string
}
```

#### Set Site About Us By Manager From Lab Website
- **URL:** `/api/setSiteAboutUsByManagerFromLabWebsite`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "domain": string,
  "about_us": string
}
```

#### Set Site Contact Info By Manager From Lab Website
- **URL:** `/api/setSiteContactInfoByManagerFromLabWebsite`
- **Method:** POST
- **Parameters:**
```json
{
  "user_id": string,
  "domain": string,
  "lab_address": string,
  "lab_mail": string,
  "lab_phone_num": string
}
```

### Notification Endpoints

#### Get All Members Notifications
- **URL:** `/api/getAllMembersNotifications`
- **Method:** GET
- **Parameters:** `user_id`, `domain` (query parameters)
- **Response:**
```json
{
  "notifications": Notification[],
  "response": string
}
```

## Error Handling

All endpoints return standardized error responses:
```json
{
  "error": string,
  "response": "false"
}
```

Common error scenarios:
- Invalid parameters
- User not authenticated
- User not authorized
- Domain not found
- File upload errors
- Database errors

## Authentication

The API uses Google OAuth2 tokens for authentication. The `google_token` parameter should contain a valid Google ID token that gets verified server-side.

Session management is handled through:
- `user_id`: Generated session identifier
- `domain`: Website domain for context
- Server-side session storage

## File Storage

Files are stored in the following structure:
```
./LabWebsitesUploads/
├── {domain}/
│   ├── logo.{ext}
│   ├── homepagephoto.{ext}
│   ├── gallery/
│   │   └── gallery_{timestamp}.{ext}
│   └── profile_pictures/
│       └── profile_{timestamp}.{ext}
```

## WebSocket Support

The API includes Socket.IO support for real-time notifications:
- Connection events: `connect`, `disconnect`
- Registration events: `register_manager`
- Notification broadcasts for registration requests

## Dependencies

- Flask
- Flask-RESTful
- Flask-CORS
- Flask-SocketIO
- Google Auth libraries
- Pandas (for CSV processing)
- Base64 encoding for image handling 