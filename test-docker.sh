#!/bin/bash

echo "🚀 Testing Skin Disease API in Docker"
echo "=================================="

# Wait for container to start
echo "⏳ Waiting for API to start..."
sleep 15

# Test health check
echo "🏥 Testing health check endpoint..."
curl -s http://localhost:5000/ | python3 -m json.tool || echo "❌ Health check failed"

echo ""
echo "📊 Testing prediction endpoint..."
echo "Note: This will fail without an actual image file, but should show endpoint is accessible"

# Test prediction endpoint (will fail without image but shows it's reachable)
curl -s -X POST http://localhost:5000/predict -F "test=dummy" || echo "❌ Expected failure - no image provided"

echo ""
echo "📱 Testing Telegram endpoint..."
curl -s -X POST http://localhost:5000/share-telegram \
  -H "Content-Type: application/json" \
  -d '{"disease": "Test", "confidence": 0.95, "treatment": "Test treatment"}' | python3 -m json.tool || echo "❌ Telegram test failed"

echo ""
echo "✅ Docker testing complete!"
echo "If you see JSON responses above, your API is working! 🎉"