# Virtual Try-On Application - Running Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Application
```bash
python3 run_app.py
```

### 3. Access the Application
- Open your browser and go to: `http://127.0.0.1:8000`
- Login with credentials: `admin` / `tryon2024`

## Usage Instructions

### Step 1: Upload Images
1. **Person Image**: Upload a clear photo of yourself (preferably full body or upper body)
2. **Garment Image**: Upload an image of the clothing item you want to try on

### Step 2: Generate Try-On
1. Click the "Generate Try-On" button
2. Wait for processing (typically 1-3 minutes)
3. View your AI-generated virtual try-on result

### Step 3: Save Results
- Click "Download Result" to save the image
- Use "Share Result" to copy the link

## Advanced Options

### Custom Port/Host
```bash
python3 run_app.py --port 3000 --host 0.0.0.0
```

### Development Mode
```bash
python3 run_app.py --dev
```

### Direct FastAPI Start
```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

## System Requirements

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- Maximum file size: 10MB

### Recommended Image Guidelines
- **Person Image**: Clear, well-lit photo showing the person clearly
- **Garment Image**: Clean product image with good contrast
- **Resolution**: At least 512x512 pixels for best results

## AI Processing

The application uses advanced AI processing with automatic fallback:

1. **Primary Service**: High-quality AI processing for best results
2. **Fallback Service**: Alternative processing if primary is unavailable

## Troubleshooting

### Common Issues

**"Processing failed" Error**
- Check image formats (JPEG/PNG only)
- Ensure images are under 10MB
- Verify internet connection

**"Authentication failed" Error**
- Use correct login: `admin` / `tryon2024`
- Clear browser cache if needed

**Slow Processing**
- Processing typically takes 1-3 minutes
- Avoid closing the browser during processing
- Check network connectivity

### Technical Support

**Check System Status**
```bash
python3 test_integration.py
```

**View Logs**
- Run with `--dev` flag for detailed logs
- Check browser console for frontend issues

## Features

✅ **AI-Powered Virtual Try-On**: Advanced machine learning algorithms  
✅ **Professional UI**: Modern liquid glass interface design  
✅ **Multi-Provider Support**: Automatic fallback for reliability  
✅ **Secure Authentication**: Protected access to the application  
✅ **Real-Time Status**: Live processing updates and progress tracking  
✅ **Image Optimization**: Automatic image processing and optimization  
✅ **Cross-Platform**: Works on all modern browsers and devices  

## API Information

### Status Endpoint
```
GET /api/status
```
Returns current system status and provider information.

### Processing Endpoint
```
POST /process
```
Handles virtual try-on image processing (requires authentication).

## Security Notes

- The application uses HTTP Basic Authentication
- Default credentials are for demo purposes only
- Change credentials in production environments
- All uploaded images are processed temporarily and not stored permanently

## Performance Tips

1. **Optimal Image Sizes**: 1024x1024 pixels or smaller
2. **Clear Images**: Well-lit, high-contrast photos work best
3. **Stable Connection**: Ensure reliable internet during processing
4. **Browser**: Use modern browsers (Chrome, Firefox, Safari, Edge)

## Environment Variables

The application supports the following optional environment variables:

```bash
# Custom AI service credentials (optional)
export KLING_ACCESS_KEY="your_access_key"
export KLING_SECRET_KEY="your_secret_key"
```

If not provided, the application uses built-in defaults.

---

**Need Help?** Run `python3 run_app.py --help` for additional options.