from google import genai
from google.genai import types
from PIL import Image as PILImage
from io import BytesIO
import base64
import os
from dotenv import load_dotenv
from IPython.display import Image, display
import datetime

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("No Gemini API key found. Please set the GEMINI_API_KEY environment variable.")

client = genai.Client(api_key=GEMINI_API_KEY)

def construct_image_prompt(survey_name, medical_specialty, tone, image_style="professional", include_text=True):
    """
    Constructs a detailed prompt for generating HCP survey campaign images
    
    Args:
        survey_name: Name of the survey
        medical_specialty: Target medical specialty (e.g., "cardiology", "oncology", "primary care")
        tone: Overall tone ("professional", "modern", "approachable", "clinical")
        image_style: Visual style ("professional", "infographic", "medical_illustration", "clean_modern")
        include_text: Whether to include text overlay on the image
    """
    
    # Base professional requirements
    base_prompt = f"""
Create a high-quality, professional medical survey campaign image for healthcare professionals.

CAMPAIGN DETAILS:
- Survey Focus: {survey_name}
- Target Specialty: {medical_specialty}
- Visual Tone: {tone}
- Style: {image_style}

VISUAL REQUIREMENTS:
- Dimensions: 16:9 landscape format, suitable for email headers and web banners
- Resolution: High-resolution, crisp and clear
- Color scheme: Professional medical colors (blues, teals, whites, subtle accent colors)
- Professional aesthetic suitable for medical professionals
- Clean, uncluttered design with plenty of white space
"""

    # Specialty-specific visual elements
    specialty_elements = {
        "cardiology": "subtle heart imagery, ECG patterns, stethoscope elements, cardiovascular icons",
        "oncology": "cellular imagery, research lab elements, microscope motifs, hope and healing themes",
        "primary_care": "diverse patient care imagery, family medicine elements, community health themes",
        "neurology": "brain imagery, neural networks, neurological examination tools",
        "pediatrics": "child-friendly colors, pediatric care elements, family-centered themes",
        "psychiatry": "mental health awareness imagery, brain and mind connection themes",
        "emergency_medicine": "urgent care elements, emergency room themes, critical care imagery",
        "surgery": "surgical precision imagery, OR themes, medical precision elements",
        "radiology": "imaging equipment, scan imagery, diagnostic themes",
        "pharmacy": "pharmaceutical elements, medication management themes",
        "general": "universal medical symbols, healthcare collaboration imagery, medical professionalism"
    }
    
    specialty_visual = specialty_elements.get(medical_specialty.lower(), specialty_elements["general"])
    base_prompt += f"\n- Specialty Elements: Incorporate {specialty_visual}"

    # Style-specific instructions
    style_instructions = {
        "professional": """
PROFESSIONAL STYLE:
- Clean, corporate medical aesthetic
- Subtle gradients and professional typography
- Medical professionals in business attire
- Hospital or clinic environment backgrounds
- Sophisticated color palette with medical blues and whites
- Icons and symbols should be minimal and elegant
""",
        "infographic": """
INFOGRAPHIC STYLE:
- Data visualization elements (charts, graphs, statistics)
- Clear information hierarchy
- Iconography representing survey benefits
- Step-by-step visual flow
- Bold, readable typography
- Engaging data presentation elements
""",
        "medical_illustration": """
MEDICAL ILLUSTRATION STYLE:
- Detailed medical diagrams and anatomical elements
- Scientific accuracy in medical representations
- Educational poster aesthetic
- Medical textbook illustration quality
- Precise, technical visual elements
- Professional medical publication style
""",
        "clean_modern": """
CLEAN MODERN STYLE:
- Minimalist design with lots of white space
- Modern typography and clean lines
- Subtle shadows and depth
- Contemporary medical technology elements
- Fresh, approachable color palette
- Modern healthcare facility aesthetics
"""
    }
    
    base_prompt += style_instructions.get(image_style.lower(), style_instructions["professional"])

    # Text overlay specifications
    if include_text:
        base_prompt += f"""

TEXT OVERLAY REQUIREMENTS:
- Main headline: "{survey_name}" (prominent, readable typography)
- Subtitle: "Healthcare Professional Survey" or "Medical Research Study"
- Call-to-action element: "Share Your Expertise" or "Join the Research"
- Text should be easily readable against the background
- Use professional, medical-appropriate fonts
- Ensure text contrast meets accessibility standards
"""
    else:
        base_prompt += "\n- Create image without text overlay (background/template only)"

    # Final composition guidelines
    base_prompt += """

COMPOSITION GUIDELINES:
- Center-weighted composition with clear focal point
- Balance between imagery and negative space
- Professional lighting and color temperature
- Avoid overly complex or busy designs
- Ensure scalability from large banners to small email thumbnails
- Create a sense of trust, expertise, and medical authority
- Make it appealing to busy healthcare professionals
- Include subtle elements that suggest collaboration and knowledge sharing

TECHNICAL SPECIFICATIONS:
- High contrast for readability
- Professional color grading
- Sharp, crisp details
- Suitable for both digital and print applications
- Optimized for professional medical communications

Create this medical survey campaign image now with careful attention to professional medical aesthetics and clear visual communication.
"""
    
    return base_prompt.strip()

def generate_survey_image(survey_name, medical_specialty="general", tone="professional", 
                         image_style="professional", include_text=True, save_filename=None):
    prompt = construct_image_prompt(survey_name, medical_specialty, tone, image_style, include_text)
    
    print(f"Generating image for: {survey_name}")
    print(f"Specialty: {medical_specialty} | Style: {image_style} | Tone: {tone}")
    print("-" * 60)
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print("AI Description:", part.text)
                print("-" * 60)
            elif part.inline_data is not None:
                # Create PIL image
                pil_image = PILImage.open(BytesIO(part.inline_data.data))
                
                # Save with custom filename if provided
                if save_filename:
                    filename = save_filename
                else:
                    # Generate filename based on survey details
                    safe_name = "".join(c for c in survey_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"survey_image_{safe_name.replace(' ', '_')}_{timestamp}.png"
                
                pil_image.save(filename)
                print(f"Image saved as: {filename}")
                
                # Display the image
                display(Image(data=part.inline_data.data))
                
                return pil_image, filename
                
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None, None
# Example 1: Cardiology Survey - Professional Style
print("GENERATING CARDIOLOGY SURVEY IMAGE")
print("=" * 60)
generate_survey_image(
        survey_name="Advanced Heart Failure Management Survey 2025",
        medical_specialty="cardiology",
        tone="professional",
        image_style="professional",
        include_text=True
)

# Function to generate image template without text (for reusability)
def generate_image_template(medical_specialty, style="professional"):
    """Generate a reusable template without survey-specific text"""
    return generate_survey_image(
        survey_name="Medical Research Template",
        medical_specialty=medical_specialty,
        tone="professional",
        image_style=style,
        include_text=False,
        save_filename=f"template_{medical_specialty}_{style}.png"
    )



