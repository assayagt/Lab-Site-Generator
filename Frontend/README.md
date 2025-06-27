# Lab-Site-Generator Frontend Documentation

## Overview
The frontend of Lab-Site-Generator is divided into two separate React applications, each serving a distinct purpose in the lab website generation ecosystem:

1. **Lab Website Generator Frontend** (`lab-gen/`): A comprehensive management interface that enables users to create, configure, and manage lab websites. This is the control center where administrators can set up new lab websites, manage existing ones, and handle all administrative tasks.

2. **Lab Website Templates** (`template1/` and `template2/`): The actual lab website templates that are generated and served to end users. These templates are customizable React applications that serve as the foundation for individual lab websites. Each template can be customized with different components, styles, and content.

## Lab Website Generator Frontend (lab-gen)

### General Information
The lab website generator frontend is a sophisticated React application that serves as the central hub for lab website management. It provides a comprehensive set of features:

- **Website Creation**: A step-by-step wizard for creating new lab websites, including:
  - Domain selection and configuration
  - Template selection
  - Component customization
  - Initial content setup

- **Website Management**: Tools for managing existing lab websites:
  - Member management (adding, removing, updating roles)
  - Publication management
  - Content updates
  - Settings configuration

- **Administrative Features**:
  - User authentication and authorization
  - Role-based access control
  - Activity logging
  - System monitoring

### Components
The generator frontend is built with a modular component architecture, located in `lab-gen/src/components/`:

#### Form Components
- `WebsiteCreationForm`: Multi-step form for creating new websites
- `MemberManagementForm`: Interface for managing lab members
- `PublicationForm`: Form for adding and editing publications
- `SettingsForm`: Website configuration interface

#### Management Interfaces
- `Dashboard`: Overview of all managed websites
- `MemberList`: List and management of lab members
- `PublicationList`: List and management of publications
- `TemplateSelector`: Interface for choosing website templates

### Services
The generator frontend uses a service-oriented architecture for handling business logic and API calls:

#### Generator Service
- Handles website creation and management
- Manages website configurations
- Handles template customization
- Processes website generation requests

#### Authentication Service
- Manages user authentication
- Handles JWT tokens
- Provides role-based access control
- Manages user sessions

#### API Service
- Centralizes all API calls
- Handles request/response interceptors
- Manages error handling
- Provides consistent API interface

### Models
The generator frontend uses TypeScript interfaces to define data structures:

#### Website Model
Defines the structure of a lab website, including:
- Domain and basic information
- Template selection
- Component configuration
- Member and publication data
- Website settings

#### Lab Member Model
Defines the structure of lab member data, including:
- Personal information
- Role and permissions
- Associated publications
- Profile information

### Dependencies
The generator frontend relies on several key packages:

- **Core Dependencies**:
  - React and React DOM for the UI framework
  - React Router for navigation
  - Material-UI for component library

- **Form Handling**:
  - Formik for form management
  - Yup for form validation

- **API and State Management**:
  - Axios for API calls
  - React Query for data fetching
  - Socket.IO for real-time updates

### Page Hierarchy
The generator frontend follows a hierarchical structure:

```
App
├── Authentication
│   ├── Login
│   └── Register
├── Dashboard
│   ├── WebsiteList
│   └── QuickActions
├── WebsiteCreation
│   ├── TemplateSelection
│   ├── ComponentSelection
│   ├── MemberManagement
│   └── FinalReview
├── WebsiteManagement
│   ├── Overview
│   ├── MemberList
│   ├── PublicationList
│   ├── Settings
│   └── Analytics
└── System
    ├── UserManagement
    └── SystemSettings
```

### Routing
The routing system is implemented using React Router v6, providing:
- Nested routes for complex navigation
- Route parameters for dynamic content
- Protected routes for authentication
- Lazy loading for performance

### Expanding the API
To add new features to the generator frontend:

1. **Define the Endpoint**:
   - Add the endpoint to the API service
   - Implement proper error handling
   - Add request/response types

2. **Create a Service Function**:
   - Implement business logic
   - Handle data transformation
   - Manage error states

3. **Implement in Component**:
   - Create UI components
   - Handle user interactions
   - Manage component state

## Lab Website Templates (template1)

### General Information
The lab website templates are sophisticated React applications designed to serve as the foundation for individual lab websites. They are highly customizable and include:

- **Responsive Design**: Adapts to all screen sizes
- **Dynamic Content**: Updates in real-time
- **Interactive Features**: Maps, publication lists, member profiles
- **SEO Optimization**: Built-in meta tags and sitemap generation

### Components
The template includes a comprehensive set of components:

#### Layout Components
- `Header`: Navigation and branding
- `Footer`: Contact information and links
- `Sidebar`: Additional navigation
- `Layout`: Main layout wrapper

#### Content Components
- `PublicationList`: Displays lab publications
- `MemberList`: Shows lab members
- `ContactForm`: Contact information form
- `NewsSection`: Latest lab news
- `MapComponent`: Lab location map

### Services
The template includes several services for handling different aspects of the website:

#### Publication Service
- Fetches and manages publications
- Handles publication updates
- Manages publication metadata

#### Member Service
- Handles member information
- Manages member profiles
- Updates member data

#### Contact Service
- Manages contact information
- Handles contact form submissions
- Processes inquiries

### Models
The template uses TypeScript interfaces for type safety:

#### Publication Model
Defines the structure of publication data, including:
- Title and authors
- Abstract and DOI
- Publication year and citations
- Related links and resources

#### Member Model
Defines the structure of member data, including:
- Personal information
- Role and responsibilities
- Associated publications
- Contact information

### Dependencies
The template uses modern React libraries:

- **Core**:
  - React and React DOM
  - React Router for navigation
  - Styled Components for styling

- **UI and Styling**:
  - React Leaflet for maps
  - React Icons for icons
  - Custom styling system

- **Data Management**:
  - Axios for API calls
  - Socket.IO for real-time updates
  - React Query for data fetching

### Page Hierarchy
The template follows a clear page structure:

```
App
├── Home
│   ├── Hero
│   ├── About
│   └── News
├── Publications
│   ├── List
│   └── Detail
├── Members
│   ├── List
│   └── Profile
├── About
│   ├── Lab
│   └── Research
└── Contact
    ├── Form
    └── Map
```

### Routing
The template uses React Router for navigation, providing:
- Clean URL structure
- Nested routes for complex pages
- Dynamic route parameters
- Lazy loading for performance

### Expanding the API
To add new features to the template:

1. **Add API Endpoint**:
   - Define the endpoint in the API service
   - Implement proper error handling
   - Add request/response types

2. **Create Service**:
   - Implement business logic
   - Handle data transformation
   - Manage error states

3. **Implement in Component**:
   - Create UI components
   - Handle user interactions
   - Manage component state

## Development Setup

### Lab Website Generator
```bash
# Clone the repository
git clone [repository-url]

# Navigate to the generator frontend
cd Frontend/lab-gen

# Install dependencies
npm install

# Start development server
npm start
```

### Lab Website Template
```bash
# Navigate to the template directory
cd Frontend/template1

# Install dependencies
npm install

# Start development server
npm start
```

## Environment Configuration

### Lab Website Generator
Create a `.env` file in the `lab-gen` directory:
```
REACT_APP_API_URL=http://localhost:5000
REACT_APP_SOCKET_URL=http://localhost:5000
REACT_APP_AUTH_DOMAIN=your-auth-domain
REACT_APP_AUTH_CLIENT_ID=your-client-id
```

### Lab Website Template
Create a `.env` file in the `template1` directory:
```
PORT=3001
PUBLIC_URL=/labs/domain
REACT_APP_API_URL=http://localhost:5000
REACT_APP_SOCKET_URL=http://localhost:5000
```

## Important Notes

1. **Frontend Separation**:
   - Each frontend has its own package.json and dependencies
   - They are developed and deployed independently
   - They communicate through the backend API

2. **Generator Frontend**:
   - Handles website creation and management
   - Provides administrative interface
   - Manages user permissions and roles

3. **Template Frontend**:
   - Serves as the base for generated websites
   - Highly customizable and modular
   - Optimized for performance and SEO

4. **Development Best Practices**:
   - Use TypeScript for type safety
   - Follow component-based architecture
   - Implement proper error handling
   - Write comprehensive tests
   - Document all new features

5. **API Integration**:
   - All API calls go through service layer
   - Implement proper error handling
   - Use appropriate HTTP methods
   - Handle loading and error states

6. **State Management**:
   - Use Context API for global state
   - Implement proper state updates
   - Handle side effects appropriately
   - Maintain data consistency

7. **Code Organization**:
   - Follow consistent file structure
   - Use meaningful component names
   - Implement proper code splitting
   - Maintain clean code practices

## Templates

The project includes multiple templates, each with its own unique features:

### Template1
- Modern, responsive design
- Publication management
- Member profiles
- Interactive maps
- News section

### Template2
- Alternative layout
- Different styling options
- Custom components
- Unique features

Each template is a separate React application with its own:
- Dependencies
- Configuration
- Styling
- Components
- Features 