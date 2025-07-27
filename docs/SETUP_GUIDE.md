# 🚀 Quick Setup Guide - Virtual Try-On with Kling AI

This guide will get you up and running with the Virtual Try-On application in just a few minutes!

## 📋 Prerequisites

- Python 3.8 or higher
- Internet connection
- Kling AI API key (optional but recommended)

## ⚡ Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure API (Optional but Recommended)
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Kling AI API key
# Get your API key from: https://app.klingai.com/global/dev/document-api
```

Edit the `.env` file:
```
KLING_AI_API_KEY=your_actual_api_key_here
```

### Step 3: Test Your Setup
```bash
python test_kling_integration.py
```

### Step 4: Start the Application
```bash
# Easy way (with automatic checks)
python start_with_checks.py

# OR manual way
python main.py
```

### Step 5: Access the Application
1. Open your browser
2. Go to: `http://localhost:8000`
3. Login with:
   - **Username**: `admin`
   - **Password**: `tryon2024`

## 🎯 That's It!

You're now ready to:
1. Upload a person image
2. Upload a garment image  
3. Click "Generate Try-On"
4. Wait for AI magic ✨

---

## 🔧 Detailed Setup (If You Need Help)

### Option A: Get Kling AI API Key (Recommended)

1. Go to [Kling AI Developer Portal](https://app.klingai.com/global/dev/document-api)
2. Sign up / Login
3. Create a new API key
4. Copy the key to your `.env` file

**Benefits:**
- ✅ Higher quality results
- ✅ Faster processing (30-120 seconds)
- ✅ Better clothing fit
- ✅ Enhanced details

### Option B: Use Without API Key (Free)

If you don't have a Kling AI API key, the app will automatically use Hugging Face as fallback:
- ✅ Free to use
- ✅ No registration required
- ⏱️ Slower processing (1-3 minutes)
- 📊 Good quality results

## 🛠️ Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "KLING_AI_API_KEY not found" warning
- This is OK! The app will use Hugging Face instead
- To use Kling AI, add your API key to `.env` file

### Server won't start
```bash
# Check if port 8000 is busy
python main.py --port 8001

# OR kill any process using port 8000
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -ti:8000 | xargs kill
```

### Images not processing
1. Check image formats (JPEG, PNG, JPG only)
2. Check file size (max 10MB)
3. Ensure stable internet connection
4. Check console logs for errors

## 📊 Provider Status

The application shows which AI provider is active:

- 🔴 **Kling AI**: High-quality, fast processing
- 🟡 **Hugging Face**: Reliable fallback, free
- 🔄 **Auto-Switch**: Automatically switches on failure

## 🎨 Usage Tips

### For Best Results:
- **Person Images**: Clear, full-body or upper-body shots
- **Garment Images**: Clean background, well-lit product photos
- **File Size**: Under 5MB for faster processing
- **Resolution**: 512x512 to 1024x1024 works best

### What Works Well:
- ✅ T-shirts, shirts, dresses
- ✅ Jackets, hoodies, sweaters  
- ✅ Clear lighting conditions
- ✅ Front-facing person photos

### What's Challenging:
- ⚠️ Very complex patterns
- ⚠️ Transparent/sheer materials
- ⚠️ Multiple layered clothing
- ⚠️ Poor lighting/blurry images

## 🔐 Security & Privacy

- **Local Processing**: All images processed through secure APIs
- **No Storage**: Images are not permanently stored
- **Authentication**: Basic auth protects the interface
- **API Keys**: Stored securely in environment variables

## 📱 Access from Other Devices

To access from other devices on your network:

1. Find your IP address:
   ```bash
   # Windows
   ipconfig
   
   # Mac/Linux  
   ifconfig
   ```

2. Start server with your IP:
   ```bash
   python main.py --host 0.0.0.0
   ```

3. Access from other devices:
   ```
   http://YOUR_IP_ADDRESS:8000
   ```

## 🆘 Getting Help

### Check Status
```bash
# Test your setup
python test_kling_integration.py

# Check API status
curl http://localhost:8000/api/status
```

### View Logs
- Server logs appear in your terminal
- Look for `🚀 Using Kling AI...` or `📞 Calling Hugging Face...`
- Error messages will show specific issues

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Slow processing | Normal for AI models, wait 1-3 minutes |
| "Provider failed" | App will auto-switch to backup provider |
| Login not working | Use `admin` / `tryon2024` |
| Port already in use | Use `--port 8001` or kill other process |
| API key invalid | Check key format in `.env` file |

## 🚀 Advanced Configuration

### Custom Settings
Edit `main.py` to customize:
```python
VALID_USERNAME = "your_username"
VALID_PASSWORD = "your_password"
```

### Environment Variables
Add to `.env` file:
```bash
# Server settings
HOST=0.0.0.0
PORT=8080

# API settings
KLING_API_TIMEOUT=300
DEBUG_MODE=true

# Authentication
VALID_USERNAME=admin
VALID_PASSWORD=tryon2024
```

## 🎉 You're All Set!

The Virtual Try-On application is now ready to use. Upload your images and experience AI-powered virtual clothing try-on!

**Need more help?** Check the main `README.md` for detailed documentation.

---

*Happy try-on experiences! 👕✨*