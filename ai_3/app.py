from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Groq client
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Base fashion context prompt
FASHION_CONTEXT = """
You are VogueRadar™, an AI fashion trend analyzer. Consider:
- Latest Fashion Week shows (New York, Paris, Milan, London)
- Current celebrity street styles and red carpet appearances
- Social media fashion trends
- Regional fashion preferences and cultural contexts
- Seasonal appropriateness
- Individual's physical characteristics
"""

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "Welcome to VogueRadar™ API",
        "description": "TrendForecasterAI- Personalized fashion trend analysis and prediction API",
        "version": "1.0.0",
        "endpoints": {
            "/": "This documentation",
            "/analyze": "POST - Analyze fashion content with personal preferences"
        }
    })

@app.route('/analyze', methods=['POST'])
def analyze_fashion():
    try:
        data = request.json
        
        # Extract user inputs
        gender = data.get('gender')
        season = data.get('season')
        celebrity = data.get('celebrity')
        country = data.get('country')
        face_type = data.get('faceType')
        face_color = data.get('faceColor')
        style_preference = data.get('stylePreference', 'casual')  # Optional additional parameter
        
        # Construct the prompt
        prompt = f"""{FASHION_CONTEXT}

Please provide personalized fashion recommendations for:
- Gender: {gender}
- Current Season: {season}
- Style Inspiration: {celebrity}
- Location: {country}
- Face Type: {face_type}
- Skin Tone: {face_color}
- Style Preference: {style_preference}

Provide detailed recommendations including:
1. Top/Upper body wear suggestions
2. Bottom wear recommendations
3. Footwear options
4. Accessory suggestions
5. Color palette recommendations
6. Specific designer pieces or affordable alternatives
7. Current Fashion Week references

Format the response in a structured way, citing specific Fashion Week collections 
and celebrity style references. Include both high-end and accessible options."""

        # Call Groq API
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",  # or your preferred Groq model
            messages=[
                {"role": "system", "content": FASHION_CONTEXT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Process and structure the response
        fashion_advice = response.choices[0].message.content

        return jsonify({
            "status": "success",
            "data": {
                "recommendations": fashion_advice,
                "metadata": {
                    "analyzed_for": {
                        "gender": gender,
                        "season": season,
                        "location": country,
                        "inspiration": celebrity
                    }
                }
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    

if __name__ == '__main__':
    app.run(debug=True)