#!/bin/bash

echo "🤗 Setting up Hugging Face Space for Skin Disease Detection"
echo "========================================================"

# Step 1: Clone the Hugging Face Space
echo "📂 Step 1: Cloning Hugging Face Space..."
cd /home/ramji/desktop/sha
git clone https://huggingface.co/spaces/Ramji2311/Skin-diseases
cd Skin-diseases

# Step 2: Copy necessary files
echo "📋 Step 2: Copying application files..."

# Copy FastAPI app
cp ../backend/fastapi_app.py ./app.py

# Copy requirements
cp ../backend/requirements-hf.txt ./requirements.txt

# Copy Dockerfile
cp ../backend/Dockerfile-hf ./Dockerfile

# Copy environment example
cp ../backend/.env.example ./

echo "📄 Step 3: Creating additional configuration files..."

# Create README for the space
cat > README.md << 'EOF'
---
title: Skin Disease Detection
emoji: 🏥
colorFrom: blue
colorTo: red
sdk: docker
pinned: false
license: mit
---

# Skin Disease Detection AI

An AI-powered skin disease classification system using deep learning. Upload an image of a skin condition to get:

- **Disease Classification**: Identifies from 23 different skin conditions
- **Confidence Score**: Shows prediction accuracy
- **Treatment Recommendations**: Provides initial guidance
- **Telegram Integration**: Share reports directly

## Features

- 🧠 **Deep Learning Model**: TensorFlow-based CNN for accurate classification
- 📱 **Easy Upload**: Simple image upload interface  
- 🔬 **23 Disease Types**: Covers major skin conditions
- 💬 **Telegram Bot**: Share results instantly
- ⚡ **Fast Processing**: Quick analysis and results

## Supported Conditions

- Acne and Rosacea
- Skin Cancer (Melanoma, Basal Cell Carcinoma)
- Eczema and Dermatitis
- Fungal Infections
- Bacterial Infections
- And 18 more conditions...

## Usage

1. Upload a clear image of the skin condition
2. Wait for AI analysis (few seconds)
3. Review the prediction and recommendations
4. Optionally share via Telegram

## API Endpoints

- `GET /` - Health check
- `POST /predict` - Upload image for prediction
- `POST /share-telegram` - Share results via Telegram
- `GET /diseases` - List supported diseases

## Disclaimer

⚠️ **This is an AI tool for educational purposes only. Always consult qualified healthcare professionals for proper medical diagnosis and treatment.**

## Technology Stack

- **Backend**: FastAPI
- **ML Framework**: TensorFlow/Keras
- **Deployment**: Hugging Face Spaces (Docker)
- **Image Processing**: Pillow, NumPy
EOF

# Create .gitignore for the space
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.h5
*.hdf5
.env
.DS_Store
.vscode/
*.log
EOF

echo "✅ Step 4: Files ready for Hugging Face Space!"
echo ""
echo "📋 Files created:"
echo "  ✓ app.py (FastAPI application)"
echo "  ✓ requirements.txt (Python dependencies)"  
echo "  ✓ Dockerfile (Container configuration)"
echo "  ✓ README.md (Space documentation)"
echo "  ✓ .gitignore (Git ignore rules)"
echo ""
echo "🚀 Next steps:"
echo "  1. Set up environment variables in HF Space settings:"
echo "     - TELEGRAM_BOT_TOKEN=8327110814:AAEUYJqkifkImQSHnhKPv1cTB7Zh1O5Xshk"
echo "     - TELEGRAM_CHAT_ID=6791150444"
echo ""  
echo "  2. Commit and push to deploy:"
echo "     git add ."
echo "     git commit -m 'Deploy skin disease detection API'"
echo "     git push"
echo ""
echo "  3. Your space will be live at:"
echo "     https://huggingface.co/spaces/Ramji2311/Skin-diseases"
echo ""
echo "🎉 Setup complete! Ready to deploy to Hugging Face Spaces!"
EOF