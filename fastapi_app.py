from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Skin Disease Detection API",
    description="AI-powered skin disease classification using deep learning",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hugging Face Spaces needs this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model configuration
MODEL_PATH = 'skin_disease_model.h5'
MODEL_URL = 'https://drive.google.com/uc?export=download&id=1k1wJY7mfBloaDEmqwD9Xpgs2f7z_Oeub'

# Download model if not exists
if not os.path.exists(MODEL_PATH):
    print(f"Model not found. Downloading from Google Drive...")
    try:
        r = requests.get(MODEL_URL, allow_redirects=True, timeout=300)
        with open(MODEL_PATH, 'wb') as f:
            f.write(r.content)
        print("Model downloaded successfully.")
    except Exception as e:
        print(f"Error downloading model: {e}")

# Load model
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

CLASS_NAMES = [
    'Acne and Rosacea Photos', 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions', 
    'Atopic Dermatitis Photos', 'Bullous Disease Photos', 'Cellulitis Impetigo and other Bacterial Infections', 
    'Eczema Photos', 'Exanthems and Drug Eruptions', 'Hair Loss Photos Alopecia and other Hair Diseases', 
    'Herpes HPV and other STDs Photos', 'Light Diseases and Disorders of Pigmentation', 
    'Lupus and other Connective Tissue diseases', 'Melanoma Skin Cancer Nevi and Moles', 
    'Nail Fungus and other Nail Disease', 'Poison Ivy Photos and other Contact Dermatitis', 
    'Psoriasis pictures Lichen Planus and related diseases', 'Scabies Lyme Disease and other Infestations and Bites', 
    'Seborrheic Keratoses and other Benign Tumors', 'Systemic Disease', 
    'Tinea Ringworm Candidiasis and other Fungal Infections', 'Urticaria Hives', 
    'Vascular Tumors', 'Vasculitis Photos', 'Warts Molluscum and other Viral Infections'
]

TREATMENT_DATABASE = {
    'Acne and Rosacea Photos': {
        'treatment': 'Common inflammatory skin conditions that can be managed with proper skincare, topical treatments, and sometimes oral medications.',
        'recommendations': ['🧴 Use gentle, non-comedogenic skincare products', '☀️ Apply sunscreen daily', '👨‍⚕️ Consult a dermatologist for persistent cases'],
        'critical': False
    },
    'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions': {
        'treatment': 'This category includes pre-cancerous and cancerous lesions that require immediate medical attention for diagnosis and treatment, which may include removal.',
        'recommendations': ['‼️ URGENT: Seek immediate consultation with a dermatologist.', '🔬 A biopsy is necessary for a definitive diagnosis.', '☀️ Practice rigorous sun protection.'],
        'critical': True
    },
    'Default': {
        'treatment': 'Could not determine the specific condition with high confidence. It is essential to consult a healthcare professional for an accurate diagnosis.',
        'recommendations': ['❓ Low confidence prediction.', '👨‍⚕️ Please see a qualified dermatologist.', '🔬 Further tests may be required.'],
        'critical': True
    }
    # Add other conditions as needed...
}

# Pydantic models for request/response
class TelegramShareRequest(BaseModel):
    disease: str
    confidence: float
    treatment: str

class HealthResponse(BaseModel):
    status: str
    message: str
    model_loaded: bool

class PredictionResponse(BaseModel):
    disease: str
    confidence: float
    treatment: str
    recommendations: list
    critical: bool

@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Skin Disease Detection API is running on Hugging Face Spaces!",
        model_loaded=model is not None
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_disease(image: UploadFile = File(...)):
    """Predict skin disease from uploaded image"""
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process image
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Resize and normalize
        img = pil_image.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        
        # Make prediction
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        
        predicted_disease = CLASS_NAMES[predicted_class_index]
        
        # Get treatment info
        if confidence < 0.50:
            disease_info = TREATMENT_DATABASE['Default']
            predicted_disease = "Uncertain"
        else:
            disease_info = TREATMENT_DATABASE.get(predicted_disease, TREATMENT_DATABASE['Default'])
        
        return PredictionResponse(
            disease=predicted_disease,
            confidence=confidence,
            treatment=disease_info['treatment'],
            recommendations=disease_info['recommendations'],
            critical=disease_info['critical']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/share-telegram")
async def share_telegram(request: TelegramShareRequest):
    """Send diagnosis report to Telegram"""
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        raise HTTPException(status_code=500, detail="Telegram configuration missing")
    
    message_text = f"""
<b>🔬 AI Diagnosis Report</b>

<b>Disease Detected:</b> {request.disease}
<b>Confidence:</b> {request.confidence:.2%}

<b>Treatment Information:</b>
{request.treatment}

<i>⚠️ This is an AI prediction. Please consult a healthcare professional for proper diagnosis.</i>
"""
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    try:
        response = requests.post(url, json={
            'chat_id': chat_id,
            'text': message_text,
            'parse_mode': 'HTML'
        })
        response.raise_for_status()
        return {"message": "Message sent successfully"}
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@app.get("/diseases")
async def get_diseases():
    """Get list of supported diseases"""
    return {"diseases": CLASS_NAMES}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)