# Medical Survey Campaign Generator

A Flask web application that generates professional email campaigns and images for healthcare professional (HCP) surveys.

## Features

✅ **Email Generation**: AI-powered professional survey invitation emails using Google Gemini API  
✅ **Image Generation**: Professional medical-themed campaign images with Gemini API + fallback  
✅ **Medical Specialties**: Supports cardiology, oncology, neurology, primary care, and more  
✅ **Multiple Tones**: Professional, casual, educational, and compelling email tones  
✅ **Web Interface**: Clean, responsive Flask web application  
✅ **Download Support**: Generated images can be downloaded directly  

## Project Structure

```
project_campaign/
├── app.py                 # Main Flask application
├── image_generator.py     # Image generation with Gemini API + fallback
├── text_generation.py    # Email generation using Gemini API
├── local_fallback.py     # Professional fallback image generator
├── img_maker.py          # Standalone image generator (reference)
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Web interface
└── static/
    └── images/           # Generated images
```

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup**:
   Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Run Application**:
   ```bash
   python app.py
   ```

4. **Access Interface**:
   Open `http://localhost:5000` in your browser

## API Integration

### Gemini API
- **Text Generation**: Uses `gemini-1.5-flash` for email content
- **Image Generation**: Uses `gemini-2.0-flash-preview-image-generation` 
- **Fallback**: Professional PIL-based image generation when API unavailable

### Medical Specialties Supported
- Cardiology - Heart disease and cardiovascular research
- Oncology - Cancer treatment and research  
- Neurology - Brain and nervous system conditions
- Primary Care - General family medicine
- Pediatrics - Children's healthcare
- Surgery - Surgical procedures and techniques
- Emergency Medicine - Critical care and emergency treatment
- And more...

## Usage

1. Fill out the survey form with:
   - Survey name and details
   - Target medical specialty
   - Compensation amount
   - Interview length
   - Desired tone (professional, casual, educational, compelling)

2. Click "Generate Campaign" to create:
   - Professional email invitation
   - Medical-themed campaign image
   - Downloadable image file

## Technical Details

- **Framework**: Flask (Python web framework)
- **AI Integration**: Google Gemini API for text and image generation
- **Image Processing**: PIL/Pillow for image manipulation
- **Styling**: Professional medical color schemes and typography
- **Error Handling**: Graceful fallback when APIs are unavailable

## Generated Content

### Email Templates
- Professional medical language
- Clear value propositions
- Appropriate compensation mentions
- Medical specialty targeting
- Call-to-action optimization

### Campaign Images
- 16:9 professional format
- Medical specialty-specific themes
- High-resolution output (1280x720)
- Professional color schemes
- Clean, modern medical aesthetics

---

**Note**: This application requires a valid Google Gemini API key for full functionality. Fallback image generation works without API access.
