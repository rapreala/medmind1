#!/bin/bash

# Wake Up API Script
# Use this before demos or video recording to ensure API is ready

echo "=========================================="
echo "Waking Up MedMind Adherence Prediction API"
echo "=========================================="
echo ""

API_URL="https://medmind-adherence-api.onrender.com"

echo "Checking API health..."
echo "This may take 30-60 seconds if API is sleeping..."
echo ""

START_TIME=$(date +%s)

# Make health check request
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$API_URL/health" --max-time 90)

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Extract HTTP status
HTTP_STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | grep -v "HTTP_STATUS")

echo "Response time: ${DURATION} seconds"
echo "HTTP Status: $HTTP_STATUS"
echo "Response: $BODY"
echo ""

if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ API is AWAKE and READY!"
    echo ""
    echo "You can now:"
    echo "  - Use the Flutter app for predictions"
    echo "  - Record your video demonstration"
    echo "  - Test the Swagger UI"
    echo ""
    echo "API will stay awake for ~15 minutes of inactivity."
else
    echo "❌ API health check failed"
    echo "Please check:"
    echo "  - Internet connection"
    echo "  - API URL: $API_URL"
    echo "  - Render service status"
fi

echo "=========================================="
