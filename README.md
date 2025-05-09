# Helsinki City Tour Challenge

A Streamlit-based interactive city tour application that turns exploring Helsinki into an engaging team-based challenge. Teams compete to complete various tasks at iconic Helsinki locations while documenting their experiences through photos, videos, and answers.

## Features

- **Team-Based Competition**: Support for multiple teams with individual progress tracking
- **Interactive Challenges**: 7 unique locations with custom tasks and requirements
- **Rich Media Support**: Upload photos and videos to document your journey
- **Real-time Progress Tracking**: Monitor your team's progress and compare with others
- **Admin Dashboard**: Comprehensive overview of all teams' progress and submissions
- **Secure Authentication**: Password-protected team access and admin controls

## Technical Requirements

- Python 3.x
- Streamlit
- PIL (Python Imaging Library)
- Required Python packages:
  ```
  streamlit
  pillow
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd helsinki-tour
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

### For Teams
1. Access the application through your web browser
2. Enter your team password to begin
3. Follow the challenges in sequence
4. Upload required media and complete tasks
5. Track your progress against other teams

### For Administrators
1. Log in with the admin password
2. Monitor all teams' progress
3. View submitted answers and media
4. Manage team data and reset progress if needed

## Data Storage

- Team progress is stored in `data/team_progress.json`
- Uploaded media is stored in the `uploads` directory
- All data is automatically saved and persisted between sessions

## Security

- Team access is password-protected
- Admin access requires special credentials
- File uploads are restricted to specific formats
- Session state management ensures data integrity

## Contributing

Feel free to submit issues and enhancement requests!


## Acknowledgments

- Helsinki City for the inspiration
- Streamlit for the amazing framework
- All the teams participating in the challenge
