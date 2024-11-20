# Todo Assistant

A modern, feature-rich task management web application built with Flask and Google OAuth authentication. Organize your tasks efficiently with groups, due dates, and real-time updates.

## Features

- **Google Authentication**
  - Secure login with Google account
  - User-specific todo lists
  - Protected routes and data privacy

- **Task Management**
  - Create, complete, and delete tasks
  - Set due dates and end times
  - Track task completion status
  - Organize tasks in groups and subgroups

- **Group Organization**
  - Create hierarchical task groups
  - Nested subgroups for better organization
  - Easy navigation through group structure
  - Group-specific task views

- **User Interface**
  - Clean, modern design
  - Responsive layout
  - Intuitive navigation
  - Real-time updates

## Tech Stack

- **Backend**
  - Python Flask
  - SQLAlchemy with SQLite
  - Flask-Login for session management
  - Google OAuth 2.0 for authentication

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Google Identity Services

- **Database**
  - SQLite (development)
  - SQLAlchemy ORM

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Haywardchan/Todo_Assistant.git
   cd Todo_Assistant
   ```

2. **Set Up Python Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   - Copy `.env.example` to `.env`
   - Set up Google OAuth 2.0 credentials:
     1. Go to [Google Cloud Console](https://console.cloud.google.com)
     2. Create a new project or select existing one
     3. Enable Google Identity Services API
     4. Create OAuth 2.0 credentials
     5. Add authorized origins:
        - http://localhost:5000
        - http://127.0.0.1:5000
     6. Add authorized redirect URIs:
        - http://localhost:5000/callback
        - http://127.0.0.1:5000/callback
     7. Copy the client ID to your `.env` file

4. **Initialize Database**
   ```bash
   python init_db.py
   ```

5. **Run Migrations**
   ```bash
   python migrate_db.py
   ```

6. **Start the Application**
   ```bash
   python app.py
   ```

7. **Access the Application**
   - Open your browser and navigate to `http://localhost:5000`
   - Sign in with your Google account
   - Start managing your tasks!

## Usage Guide

1. **Authentication**
   - Click "Login" or "Sign Up" to authenticate with Google
   - Your tasks and groups are private to your account

2. **Managing Tasks**
   - Create new tasks with the input form at the top
   - Set due dates and end times for tasks
   - Mark tasks as complete by clicking the checkbox
   - Delete tasks using the delete button

3. **Group Organization**
   - Create groups from the sidebar
   - Add subgroups to existing groups
   - Click on a group to view its tasks
   - Delete groups and their tasks as needed

4. **Task Filtering**
   - View all tasks or group-specific tasks
   - Tasks are automatically organized by groups
   - Navigate through group hierarchy in the sidebar

## Development

- **Database Migrations**
  ```bash
  python migrate_db.py
  ```

- **Reset Database**
  ```bash
  python reset_db.py
  ```

## Security

- Environment variables for sensitive data
- Google OAuth for secure authentication
- User-specific data isolation
- Protected routes and API endpoints

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Identity Services for authentication
- Flask community for the excellent web framework
- SQLAlchemy team for the powerful ORM
