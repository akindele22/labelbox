import cloudinary
import cloudinary.uploader
import cloudinary.api
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# MongoDB Connection
client = MongoClient("mongodb+srv://Bash-Anno1:1234567890@cluster-1.zcyy0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-1")
db = client["annotation_db"]
tasks_collection = db["img_annotations"]

# Upload Image to Cloudinary and Save URL in MongoDB
def upload_image_and_store_in_db(image_path, project_name):
    try:
        upload_result = cloudinary.uploader.upload(image_path)
        image_url = upload_result.get("secure_url")
        
        if image_url:
            tasks_collection.insert_one({
                "project_name": project_name,
                "image_url": image_url,
                "status": "pending"
            })
            print(f"Image uploaded and URL saved to MongoDB: {image_url}")
    except Exception as e:
        print(f"Error: {e}")


# Example Usage
upload_image_and_store_in_db("dog.jpg", "Annotation Task 9")
