# Project Structure Documentation

## Overview

This document outlines the complete structure of the AI Virtual Try-On Application, organized for production deployment and easy maintenance.

## 📁 Directory Structure

```
ai-virtual-tryon/
├── 📄 main.py                    # FastAPI application entry point
├── 📄 kling_ai_client.py         # AI processing client
├── 📄 run.py                     # Simple application launcher
├── 📄 requirements.txt           # Python dependencies
├── 📄 .env.example              # Environment variables template
├── 📄 .gitignore                # Git ignore rules
├── 📄 LICENSE                   # MIT license
├── 📄 README.md                 # Main documentation
├── 📄 Dockerfile                # Container configuration
├── 📄 docker-compose.yml        # Multi-container setup
│
├── 📂 templates/                # HTML templates
│   └── 📄 index.html           # Main application interface
│
├── 📂 static/                   # Static web assets
│   ├── 📂 css/                 # Stylesheets
│   │   ├── 📄 liquid-glass.css # Main UI styles
│   │   └── 📄 enhancements.css # Additional styles
│   └── 📂 js/                  # JavaScript files
│       └── 📄 app.js          # Frontend logic
│
├── 📂 scripts/                 # Utility scripts
│   └── 📄 run_app.py          # Advanced launcher with checks
│
├── 📂 tests/                   # Test suites
│   ├── 📄 test_integration.py  # Full system tests
│   └── 📄 test_auth.py        # Authentication tests
│
├── 📂 sample_images/           # Example images
│   ├── 📄 man-with-arms-crossed.jpg
│   └── 📄 10334540.jpg
│
└── 📂 docs/                    # Documentation
    ├── 📄 PROJECT_STRUCTURE.md # This file
    ├── 📄 RUNNING.md           # User guide
    ├── 📄 CHANGES.md           # Version history
    └── 📄 SETUP_GUIDE.md       # Advanced setup
```

## 📄 Core Files

### Application Core

- **`main.py`** - FastAPI application with routing, authentication, and API endpoints
- **`kling_ai_client.py`** - AI service integration, image processing, and task management
- **`run.py`** - Simple launcher script for quick startup

### Configuration

- **`requirements.txt`** - Python package dependencies
- **`.env.example`** - Template for environment variables
- **`.gitignore`** - Git ignore rules for secure development

### Deployment

- **`Dockerfile`** - Container configuration for Docker deployment
- **`docker-compose.yml`** - Multi-container orchestration setup
- **`LICENSE`** - MIT license for open-source compliance

## 📂 Directory Purposes

### `/templates/`
Contains Jinja2 HTML templates for the web interface:
- **`index.html`** - Main application page with upload forms and results display

### `/static/`
Static web assets served by FastAPI:
- **`/css/`** - Stylesheets for professional UI design
- **`/js/`** - Client-side JavaScript for interactivity

### `/scripts/`
Utility scripts for development and deployment:
- **`run_app.py`** - Advanced launcher with system checks and diagnostics

### `/tests/`
Comprehensive test suite:
- **`test_integration.py`** - End-to-end system testing
- **`test_auth.py`** - Authentication and security testing

### `/sample_images/`
Example images for testing and demonstration:
- High-quality sample person and garment images
- Used by test suites for automated testing

### `/docs/`
Complete documentation suite:
- Technical documentation and user guides
- Setup instructions and troubleshooting

## 🔧 File Responsibilities

### Core Application (`main.py`)
```python
# Primary responsibilities:
- FastAPI application setup and configuration
- HTTP Basic Authentication implementation
- Route definitions and request handling
- Image upload processing and validation
- AI service integration and fallback logic
- API endpoint definitions
- Error handling and response formatting
```

### AI Client (`kling_ai_client.py`)
```python
# Primary responsibilities:
- KlingAI API integration and authentication
- JWT token generation and management
- Image preprocessing and optimization
- Task submission and status polling
- Result downloading and conversion
- Error handling and retry logic
- Async processing management
```

### Frontend (`templates/index.html`)
```html
<!-- Primary responsibilities: -->
- User interface layout and styling
- Image upload forms and preview
- Processing status display
- Results presentation
- Professional design elements
- Responsive layout
- Accessibility features
```

### Styling (`static/css/`)
```css
/* Primary responsibilities: */
- Professional liquid glass UI design
- Provider status indicators
- Responsive layout rules
- Animation and transition effects
- Color scheme and typography
- Interactive element styling
```

### Client Logic (`static/js/app.js`)
```javascript
// Primary responsibilities:
- File upload handling
- Form validation
- Progress indication
- API communication
- UI state management
- Error display
- Interactive animations
```

## 🚀 Deployment Structure

### Development Setup
```bash
# Minimal setup for development
python run.py --dev
```

### Production Deployment
```bash
# Docker containerized deployment
docker-compose up --profile production
```

### Testing Structure
```bash
# Run all tests
python tests/test_integration.py
python tests/test_auth.py
```

## 📊 Data Flow

### Request Processing Flow
```
1. User uploads images via web interface
2. FastAPI receives and validates uploads
3. Images converted to base64 format
4. KlingAI client processes virtual try-on
5. Results downloaded and converted
6. Response sent back to user interface
7. Results displayed with download option
```

### File Organization Principles
- **Separation of Concerns** - Each directory has a specific purpose
- **Production Ready** - Clean structure suitable for deployment
- **Developer Friendly** - Easy to navigate and understand
- **Scalable** - Can accommodate future features and expansion
- **Secure** - Sensitive files properly excluded from version control

## 🔒 Security Considerations

### Protected Files
- `.env` - Contains sensitive credentials (gitignored)
- `logs/` - Application logs (gitignored)
- `uploads/` - User uploaded files (gitignored)

### Public Files
- All files in `static/` - Served publicly by web server
- `sample_images/` - Demonstration images only
- Documentation in `docs/` - Safe for public access

## 🛠️ Maintenance

### Regular Updates
- **Dependencies** - Update `requirements.txt` as needed
- **Documentation** - Keep `docs/` current with changes
- **Tests** - Maintain test coverage in `tests/`

### Version Control
- **Git Workflow** - Main branch for production-ready code
- **Branching** - Feature branches for development
- **Releases** - Tagged releases for deployment

## 📝 Notes

- All paths are relative to project root
- Configuration through environment variables
- Docker support for containerized deployment
- Comprehensive test coverage
- Production-ready security measures
- Professional documentation standards

This structure ensures maintainable, scalable, and secure deployment while remaining developer-friendly for ongoing development and enhancement.