import pymongo, os, base64
from io import BytesIO
from PIL import Image

from flask import Flask, request, jsonify
from flask_cors import CORS

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB
user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
db_name = os.getenv("MONGO_DB_NAME")
db_collection = os.getenv("MONGO_DB_COLLECTION")

client = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@{host}/{db_name}?retryWrites=true&w=majority")

@app.route("/")
def index():
    return "API is running"

@app.route("/processImage", methods=["POST"])
def processImage():
    if request.method == "POST":
        # Get image data from request
        if 'image' in request.files:
            image = request.files['image']
            image_data = image.read()
            
            # Get parameters from request
            format_img = request.args.get('format')

            # Convert binary image data to Base64
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            
            # Save image in MongoDB
            db = client[db_name]
            collection = db[db_collection]
            collection.insert_one({
                "image": encoded_image,
                "format": format_img
            })
            
            # Return response
            return jsonify({
                "message": "L'image a été reçue avec succès",
                "message_test": "TEST",
                "upload_image": "data:image/{};base64,{}".format(format_img, encoded_image),
            })
        else:
            return jsonify({"message": "Aucune image trouvée"})
    else:
        return jsonify({"message": "Method not allowed"})

if __name__ == "__main__":
    app.run(debug=True)