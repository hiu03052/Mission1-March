from flask import Flask, request, render_template
from flask_cors import CORS 
import requests

app = Flask(__name__)
CORS(app)

AZURE_KEY = "iVz9t5fbqkPuHcwzJdaw5f6RsjLRTRE6VZnHfJnq1PMHiYaO326jJQQJ99BCACL93NaXJ3w3AAAJACOGdj31"
PROJECT_ID = "09689286-91b1-44f8-ae68-f66c04751175" 
ITERATION_NAME = "Iteration 1"  # blank
AZURE_URL = f"https://mission1ck.cognitiveservices.azure.com/customvision/v3.0/Prediction/{PROJECT_ID}/classify/iterations/{ITERATION_NAME}/url"

print(AZURE_URL) # for test.....

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        image_url = request.form["image_url"]  
        if not image_url:  
            result = {'error': 'Image URL is required!'}
        else:
            headers = {
                'Prediction-Key': AZURE_KEY,  
                'Content-Type': 'application/json'
            }
            data = {'Url': image_url}  

            try:
                response = requests.post(AZURE_URL, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()

            except requests.exceptions.RequestException as e:
                result = {'error': f"Error occurred: {str(e)}"}

        return render_template("index.html", image_url=image_url, result=result)

    return render_template("index.html", result=result)  

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
