# CollegeEvents — College Event Management System

CollegeEvents is a Django-based web application designed to help college students discover and register for events organized by college clubs.

The system provides a centralized platform where students can explore upcoming events, filter events by category, view event details, register for events, and manage their registrations. It also provides club-level functionality for managing events and monitoring registrations.

## Problem Statement

College events are often announced through different platforms and communication channels, making it difficult for students to discover events and keep track of registrations.

There can also be problems with multiple events being scheduled at the same venue and time.

CollegeEvents aims to provide a single platform for:

* Discovering college events
* Managing club events
* Registering for events
* Organizing events by category
* Preventing venue scheduling conflicts
* Managing student and club information

## Features

### Student Features

* User registration and login
* Browse upcoming college events
* Filter events by category
* View detailed event information
* Register for events
* View registered events through the student dashboard
* View registration details
* Search for students using unique student information
* Responsive interface for desktop, tablet, and mobile devices

### Club Features

* Club dashboard for authorized club members
* Create events
* Edit events
* Delete events
* Manage club event information
* View event registrations
* Club membership management
* Core-member and president-based access control

### Event Management

Each event can contain information such as:

* Event name
* Description
* Category
* Organizing club
* Date
* Start time
* End time
* Venue
* Registration fee
* Event image
* Registration information

The system also checks for venue scheduling conflicts when events are created.

### User Interface

* Bootstrap-based responsive design
* Light and dark themes
* Persistent theme selection using browser local storage
* Animated background elements
* Responsive event cards
* Responsive dashboards
* Event and club images
* Mobile-friendly navigation

## Technologies Used

### Backend

* Python
* Django
* SQLite

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

### Development Tools

* Visual Studio Code
* Git
* GitHub

## Project Structure


CollegeEvents/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── events/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   └── base.html
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md


## Installation and Setup

### 1. Clone the repository


git clone https://github.com/YOUR_USERNAME/college-events-management-system.git


Move into the project directory:


cd college-events-management-system


### 2. Create a virtual environment

Windows:
python -m venv .venv


Activate it:
.venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Apply migrations
python manage.py migrate

### 5. Create a superuser
python manage.py createsuperuser


Follow the instructions in the terminal to create the administrator account.

### 6. Start the development server
python manage.py runserver

Open the application in your browser at:
http://127.0.0.1:8000/


## Database

The project currently uses SQLite for development.

The database file is intentionally excluded from the Git repository through `.gitignore`.

After cloning the project, run:

python manage.py migrate

to create the required database structure.

## Access Control

CollegeEvents provides different functionality based on the user's role.

### Students

Students can:

* Browse events
* View event details
* Register for events
* View their registrations

### Club Members

Authorized club members can access club-specific functionality such as:

* Creating events
* Editing events
* Deleting events
* Viewing event registrations

The system distinguishes between regular members and core club members/presidents for access control.

## Event Scheduling

One of the important features of the system is venue conflict prevention.

When creating an event, the system checks whether another event is already scheduled at the same venue during an overlapping time period.

This helps prevent situations where multiple college events are assigned to the same venue at the same time.

## Screenshots

Screenshots of the application can be added here to demonstrate the main interfaces.

### Home Page

*Add screenshot here*

### Events Page

*Add screenshot here*

### Event Details

*Add screenshot here*

### Student Dashboard

*Add screenshot here*

### Club Dashboard

*Add screenshot here*

### Dark Theme

*Add screenshot here*

## Future Improvements

Possible future improvements include:

* Email notifications for event registrations
* Event reminders
* Advanced event search
* Calendar integration
* QR-based event check-in
* Event attendance tracking
* Improved club administration
* Deployment to a cloud platform
* REST API integration
* Analytics dashboard for event participation
* AI-powered event recommendations

## Learning Outcomes

This project provided practical experience with:

* Django project and application structure
* Model design and database relationships
* Django ORM
* Authentication and authorization
* Forms and validation
* CRUD operations
* Template inheritance
* URL routing
* Static and media file handling
* Bootstrap-based responsive design
* JavaScript-based theme persistence
* Git and GitHub workflow
* Implementing business logic such as venue conflict detection

## Project Status

**Status: Completed — Development Version**

The core functionality of the CollegeEvents platform has been implemented and tested locally.

The project is currently intended as a development/portfolio project and has not yet been deployed to a production server.

## Author

**Swati Gangannavar**

Computer Science and Engineering Student

---

If you find this project useful or have suggestions for improvement, feel free to explore the repository and contribute ideas.
