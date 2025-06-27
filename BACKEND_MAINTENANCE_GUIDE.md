# Lab Website Generator Backend - Maintenance Guide

## General Information

The backend of the Lab Website Generator is a **Python Flask project** that serves as the core API server for the entire system. The architecture follows a **domain-driven design pattern** with clear separation of concerns.

### Architecture Overview

The backend architecture flow operates as follows:

1. **Flask Application (`app.py`)** - Main entry point that defines all API endpoints
2. **Service Layer** - Business logic is handled by service classes:
   - `GeneratorSystemService` - Manages website generation and customization
   - `LabSystemService` - Handles lab website operations and user management
3. **Controller Layer** - Domain controllers that implement core business rules
4. **Data Layer** - Handles data persistence and file storage

### Project Structure
```
src/main/DomainLayer/
├── app.py                          # Main Flask application with all API endpoints
├── GeneratorSystemService.py       # Website generation service
├── LabWebsites/
│   ├── LabSystemService.py        # Lab website management service
│   └── LabSystem/
│       └── LabSystemController.py  # Lab domain controller
├── LabGenerator/
│   └── GeneratorSystemService.py   # Generator domain service
└── socketio_instance.py           # Socket.IO configuration
```

### Key Technologies
- **Flask** - Web framework
- **Flask-RESTful** - RESTful API development
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-SocketIO** - Real-time WebSocket communication
- **Google OAuth2** - Authentication
- **Base64** - Image encoding/decoding
- **Pandas** - CSV file processing

## API System

### API Structure

All API endpoints are defined in `app.py` using Flask-RESTful `Resource` classes. Each endpoint follows this pattern:

```python
class EndpointName(Resource):
    def post(self):  # or get(), put(), delete()
        parser = reqparse.RequestParser()
        parser.add_argument('parameter_name', type=str, required=True, help="Description")
        args = parser.parse_args()
        
        try:
            # Business logic here
            response = service.method(args['parameter_name'])
            if response.is_success():
                return jsonify({"message": response.get_message(), "response": "true"})
            return jsonify({"message": response.get_message(), "response": "false"})
        except Exception as e:
            return jsonify({"error": str(e), "response": "false"})
```

### Service Integration

The API layer delegates business logic to appropriate services:

- **Generator System Operations** → `generator_system` instance
- **Lab Website Operations** → `lab_system_service` instance

### Response Format

All API endpoints return standardized JSON responses:

```json
{
  "response": "true|false",
  "message": "Success/error message",
  "data": "Optional data payload",
  "error": "Error details if response is false"
}
```

## How to Add New API Calls

### Step 1: Define the Resource Class

Create a new class in `app.py`:

```python
class YourNewEndpoint(Resource):
    def post(self):  # Choose appropriate HTTP method
        parser = reqparse.RequestParser()
        
        # Define required parameters
        parser.add_argument('user_id', type=str, required=True, help="User ID is required")
        parser.add_argument('domain', type=str, required=True, help="Domain is required")
        parser.add_argument('your_param', type=str, required=False, help="Optional parameter")
        
        args = parser.parse_args()
        
        try:
            # Call appropriate service method
            response = lab_system_service.your_new_method(
                args['user_id'], 
                args['domain'], 
                args['your_param']
            )
            
            if response.is_success():
                return jsonify({
                    "message": response.get_message(), 
                    "response": "true",
                    "data": response.get_data()  # Optional
                })
            return jsonify({
                "message": response.get_message(), 
                "response": "false"
            })
            
        except Exception as e:
            return jsonify({"error": str(e), "response": "false"})
```

### Step 2: Register the Endpoint

Add your endpoint to the API registration section at the bottom of `app.py`:

```python
api.add_resource(YourNewEndpoint, '/api/yourNewEndpoint')
```

### Step 3: Implement Service Method

Add the corresponding method to the appropriate service class:

**For Lab Website operations** - Add to `LabSystemService.py`:
```python
def your_new_method(self, user_id, domain, your_param):
    """
    Description of what this method does.
    """
    try:
        # Delegate to controller
        result = self.lab_system_controller.your_controller_method(user_id, domain, your_param)
        return Response(result, "Operation completed successfully")
    except Exception as e:
        return Response(None, str(e))
```

**For Generator operations** - Add to `GeneratorSystemService.py`:
```python
def your_new_method(self, user_id, domain, your_param):
    """
    Description of what this method does.
    """
    try:
        result = self.generator_system_controller.your_controller_method(user_id, domain, your_param)
        return Response(result, "Operation completed successfully")
    except Exception as e:
        return Response(None, str(e))
```

### Step 4: Implement Controller Logic

Add the business logic to the appropriate controller class.

### Step 5: Update Frontend Service

Add the corresponding function to the frontend `websiteService.js`:

```javascript
export const yourNewEndpoint = async (userId, domain, yourParam) => {
  try {
    const response = await axios.post(`${baseApiUrl}yourNewEndpoint`, {
      user_id: userId,
      domain: domain,
      your_param: yourParam,
    });
    return response.data;
  } catch (error) {
    console.error("Error calling your new endpoint:", error);
    return null;
  }
};
```

## Adding New Web Crawlers

The system currently supports publication crawling functionality. Here's how to extend or modify the web crawling capabilities:

### Current Crawling System

The publication crawling is handled through the `CrawlPublicationsForMember` endpoint which calls:
```python
lab_system_service.crawl_publications_for_labMember(user_id, domain)
```

### Adding New Crawlers

#### Step 1: Create Crawler Class

Create a new crawler class in the appropriate domain layer:

```python
class YourNewCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def crawl_publications(self, scholar_profile_url):
        """
        Crawl publications from a specific source.
        
        Returns:
            List of publication dictionaries with standardized format
        """
        try:
            response = self.session.get(scholar_profile_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            publications = []
            
            # Extract publication data
            for pub_element in soup.find_all('div', class_='publication-item'):
                publication = {
                    'title': self._extract_title(pub_element),
                    'authors': self._extract_authors(pub_element),
                    'year': self._extract_year(pub_element),
                    'venue': self._extract_venue(pub_element),
                    'url': self._extract_url(pub_element)
                }
                publications.append(publication)
            
            return publications
            
        except Exception as e:
            raise Exception(f"Crawling failed: {str(e)}")
    
    def _extract_title(self, element):
        """Extract publication title from HTML element"""
        title_elem = element.find('h3', class_='title')
        return title_elem.text.strip() if title_elem else ""
    
    def _extract_authors(self, element):
        """Extract authors from HTML element"""
        authors_elem = element.find('div', class_='authors')
        return authors_elem.text.strip() if authors_elem else ""
    
    def _extract_year(self, element):
        """Extract publication year from HTML element"""
        year_elem = element.find('span', class_='year')
        return year_elem.text.strip() if year_elem else ""
    
    def _extract_venue(self, element):
        """Extract publication venue from HTML element"""
        venue_elem = element.find('span', class_='venue')
        return venue_elem.text.strip() if venue_elem else ""
    
    def _extract_url(self, element):
        """Extract publication URL from HTML element"""
        url_elem = element.find('a', class_='publication-link')
        return url_elem.get('href') if url_elem else ""
```

#### Step 2: Integrate Crawler

Modify the crawling service method to use your new crawler:

```python
def crawl_publications_for_labMember(self, user_id, domain):
    try:
        # Get user's scholar profile
        user_details = self.get_user_details(user_id, domain)
        scholar_url = user_details.get_data().get('scholar_link')
        
        if not scholar_url:
            return Response(None, "No Google Scholar profile found")
        
        # Choose appropriate crawler based on URL
        if 'scholar.google.com' in scholar_url:
            crawler = GoogleScholarCrawler()
        elif 'your-new-site.com' in scholar_url:
            crawler = YourNewCrawler()
        else:
            return Response(None, "Unsupported publication source")
        
        # Crawl publications
        publications = crawler.crawl_publications(scholar_url)
        
        # Process and store publications
        for pub in publications:
            self.lab_system_controller.add_crawled_publication(
                user_id, domain, pub
            )
        
        return Response(True, f"Successfully crawled {len(publications)} publications")
        
    except Exception as e:
        return Response(None, str(e))
```

#### Step 3: Update Website Detection

Add logic to detect which crawler to use based on the profile URL:

```python
def get_appropriate_crawler(self, profile_url):
    """
    Returns the appropriate crawler based on the profile URL
    """
    if 'scholar.google.com' in profile_url:
        return GoogleScholarCrawler()
    elif 'researchgate.net' in profile_url:
        return ResearchGateCrawler()
    elif 'orcid.org' in profile_url:
        return OrcidCrawler()
    elif 'your-new-site.com' in profile_url:
        return YourNewCrawler()
    else:
        raise Exception("Unsupported publication source")
```

### Crawler Best Practices

1. **Rate Limiting**: Add delays between requests to avoid being blocked
2. **Error Handling**: Implement robust error handling for network issues
3. **Data Validation**: Validate extracted data before storing
4. **Caching**: Implement caching to avoid redundant requests
5. **User Agents**: Use appropriate user agents to avoid detection

## Database Management

### Data Persistence

The system uses file-based storage and in-memory data structures. Key data is stored in:

- **Website Configurations**: Stored in JSON files in `./LabWebsitesUploads/{domain}/`
- **User Sessions**: Managed in-memory by service classes
- **File Storage**: Images and documents in domain-specific folders

### Data Models

The system works with several key data objects:

#### User Data
```python
{
    'user_id': str,
    'email': str,
    'fullName': str,
    'bio': str,
    'degree': str,
    'linkedin_link': str,
    'scholar_link': str
}
```

#### Publication Data
```python
{
    'paper_id': str,
    'title': str,
    'publication_year': str,
    'publication_link': str,
    'git_link': str,
    'video_link': str,
    'presentation_link': str,
    'status': str  # "Approved", "pending", "rejected"
}
```

### Adding New Data Fields

To add new data fields:

1. **Update Data Models** in the appropriate service classes
2. **Modify API Endpoints** to accept new parameters
3. **Update Storage Logic** in controller classes
4. **Update Frontend** to send new data

## File Management

### File Storage Structure

Files are organized by domain:
```
./LabWebsitesUploads/
├── {domain}/
│   ├── logo.{ext}                 # Website logo
│   ├── homepagephoto.{ext}        # Homepage image
│   ├── gallery/                   # Gallery images
│   │   └── gallery_{timestamp}.{ext}
│   └── profile_pictures/          # User profile pictures
│       └── profile_{timestamp}.{ext}
```

### Adding New File Types

To support new file types:

#### Step 1: Create Upload Endpoint

```python
class UploadNewFileType(Resource):
    def post(self):
        try:
            domain = request.form['domain']
            user_id = request.form['user_id']
            
            # Create directory structure
            website_folder = os.path.join(GENERATED_WEBSITES_FOLDER, domain)
            new_file_folder = os.path.join(website_folder, 'new_file_type')
            os.makedirs(new_file_folder, exist_ok=True)
            
            file = request.files['new_file']
            if not file:
                return {"error": "No file provided"}, 400
            
            # Validate file type
            extension = os.path.splitext(file.filename)[1].lower()
            if extension not in ['.pdf', '.doc', '.docx']:  # Allowed extensions
                return {"error": "Invalid file type"}, 400
            
            # Generate unique filename
            timestamp = int(time.time() * 1000)
            file_path = os.path.join(new_file_folder, f"document_{timestamp}{extension}")
            
            # Save file
            file.save(file_path)
            
            # Update database/storage
            response = lab_system_service.add_new_file_type(user_id, domain, file_path)
            
            return {"message": "File uploaded successfully", "filename": os.path.basename(file_path)}, 200
            
        except Exception as e:
            return {"error": str(e)}, 500
```

#### Step 2: Register Endpoint

```python
api.add_resource(UploadNewFileType, '/api/uploadNewFileType')
```

#### Step 3: Update Service Layer

Add file handling logic to the appropriate service class.

## Authentication System

### Google OAuth Integration

The system uses Google OAuth2 for authentication:

```python
# In Login endpoint
try:
    idinfo = id_token.verify_oauth2_token(google_token, requests.Request(), GOOGLE_CLIENT_ID)
    email = idinfo['email']
except ValueError as e:
    return jsonify({"error": "Invalid Google token", "response": "false"})
```

### Session Management

Sessions are managed through:
- **User ID**: Generated session identifier
- **Domain Context**: Website domain for operations
- **In-Memory Storage**: Session data stored in service classes

### Adding New Authentication Methods

To add new authentication providers:

1. **Install Required Libraries** (e.g., for Facebook, Microsoft)
2. **Add Token Verification Logic**
3. **Update Login Endpoints**
4. **Modify Frontend Integration**

## Socket.IO Integration

### Real-Time Features

The system supports real-time notifications through Socket.IO:

```python
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('register_manager')
def handle_register_user(data):
    email = data.get("email")
    domain = data.get("domain")
    if email:
        sid = request.sid
        response = lab_system_service.connect_user_socket(email, domain, sid)
```

### Adding New Socket Events

To add new real-time features:

#### Step 1: Define Socket Event Handler

```python
@socketio.on('your_new_event')
def handle_your_event(data):
    try:
        # Process the event data
        result = process_event_data(data)
        
        # Emit response to specific room/user
        socketio.emit('your_response_event', result, room=data.get('room_id'))
        
    except Exception as e:
        socketio.emit('error', {'message': str(e)}, room=request.sid)
```

#### Step 2: Emit Events from API Endpoints

```python
# In your API endpoint
def some_api_method(self):
    # ... API logic ...
    
    # Emit real-time notification
    socketio.emit('notification_update', {
        'message': 'New notification',
        'data': notification_data
    }, room=domain)
```

## Deployment and Configuration

### Environment Configuration

Create configuration management:

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or './uploads'
    DEBUG = os.environ.get('FLASK_DEBUG') or False

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
```

### Running the Server

Development:
```bash
python app.py
```

Production (with Gunicorn):
```bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

### Dependencies Management

Key dependencies in `requirements.txt`:
```
Flask==2.3.3
Flask-RESTful==0.3.10
Flask-CORS==4.0.0
Flask-SocketIO==5.3.6
google-auth==2.23.3
pandas==2.1.1
python-socketio==5.9.0
eventlet==0.33.3
```

## Error Handling and Logging

### Standardized Error Responses

All endpoints should return consistent error formats:

```python
try:
    # API logic here
    pass
except AuthenticationError as e:
    return jsonify({"error": "Authentication failed", "response": "false"}), 401
except AuthorizationError as e:
    return jsonify({"error": "Access denied", "response": "false"}), 403
except ValidationError as e:
    return jsonify({"error": f"Validation error: {str(e)}", "response": "false"}), 400
except Exception as e:
    return jsonify({"error": f"Internal server error: {str(e)}", "response": "false"}), 500
```

### Adding Logging

Implement comprehensive logging:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# In your endpoints
logger.info(f"User {user_id} accessed endpoint /api/yourEndpoint")
logger.error(f"Error in endpoint: {str(e)}")
```

## Testing

### Unit Testing Structure

Create test files for each major component:

```python
import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestYourEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_your_endpoint_success(self):
        response = self.app.post('/api/yourEndpoint', json={
            'user_id': 'test_user',
            'domain': 'test_domain'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['response'], 'true')
    
    def test_your_endpoint_missing_params(self):
        response = self.app.post('/api/yourEndpoint', json={})
        
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
```

This comprehensive guide should help you maintain and extend the Lab Website Generator backend effectively. The modular architecture makes it easy to add new features while maintaining code quality and consistency. 