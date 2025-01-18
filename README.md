# Django Task Manager

A full-featured task management application built with Django. This project was created as part of the [Dev.to Django Challenge](https://dev.to/).

## Features

- ✅ User authentication and authorization
- 📋 CRUD operations for tasks
- 🔄 Real-time task status updates
- 🏷️ Task prioritization
- 📅 Due date management
- 🔍 Search and filter capabilities
- 📱 Responsive design

## Tech Stack

- Django 4.x
- Python 3.x
- Bootstrap 5
- JavaScript (ES6+)
- Sqlite3
## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/freshstart-taskmanager.git
cd freshstart-taskmanager
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
todoproject/
├── tasks/                  # Main app directory
│   ├── models.py          # Task model definitions
│   ├── views.py           # View logic
│   ├── forms.py           # Form definitions
│   └── templates/         # HTML templates
├── static/                # Static files (JS, CSS)
└── templates/             # Base templates
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License


NONE
