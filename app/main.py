# main.py
from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import boto3
from datetime import datetime
from pymongo import MongoClient
from app.config import settings
from bson import ObjectId
from io import BytesIO

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:3000",  # Frontend URL
    # You can add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows the frontend to access the backend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Configure S3
s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION
)

# Configure MongoDB
client = MongoClient(settings.MONGO_URI)
db = client.image_db

BUCKET_NAME = settings.S3_BUCKET_NAME

# Helper function to convert ObjectId to string
def serialize_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

@app.post("/upload/")
async def upload_image_and_mask(image: UploadFile, mask: UploadFile):
    try:
        # Read image file content
        image_content = await image.read()
        mask_content = await mask.read()

        # Generate unique keys for both the image and mask
        image_s3_key = f"{datetime.utcnow().isoformat()}_image_{image.filename}"
        mask_s3_key = f"{datetime.utcnow().isoformat()}_mask_{mask.filename}"

        # Create file-like objects
        image_file_like = BytesIO(image_content)
        mask_file_like = BytesIO(mask_content)

        # Upload image and mask to S3
        s3.upload_fileobj(image_file_like, BUCKET_NAME, image_s3_key)
        s3.upload_fileobj(mask_file_like, BUCKET_NAME, mask_s3_key)

        # Save image metadata in MongoDB
        image_data = {
            "filename": image.filename,
            "is_mask": False,
            "s3_url": f"https://{BUCKET_NAME}.s3.amazonaws.com/{image_s3_key}",
            "uploaded_at": datetime.utcnow(),
        }

        image_result = db.images.insert_one(image_data)
        image_data["_id"] = str(image_result.inserted_id)

        # Now that image_data has _id, you can create the mask_data
        mask_data = {
            "filename": mask.filename,
            "is_mask": True,
            "s3_url": f"https://{BUCKET_NAME}.s3.amazonaws.com/{mask_s3_key}",
            "uploaded_at": datetime.utcnow(),
            "image_id": image_data["_id"],  # Reference the image _id after it has been inserted
        }

        # Insert mask metadata into MongoDB
        mask_result = db.images.insert_one(mask_data)
        mask_data["_id"] = str(mask_result.inserted_id)

        return {"message": "Upload successful", "image_data": image_data, "mask_data": mask_data}

    except (NoCredentialsError, PartialCredentialsError):
        raise HTTPException(status_code=500, detail="Invalid AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    try:
        # Read image file content
        image_content = await image.read()
        mask_content = await mask.read()

        # Generate unique keys for both the image and mask
        image_s3_key = f"{datetime.utcnow().isoformat()}_image_{image.filename}"
        mask_s3_key = f"{datetime.utcnow().isoformat()}_mask_{mask.filename}"

        # Upload image and mask to S3
        s3.upload_fileobj(image.file, BUCKET_NAME, image_s3_key)
        s3.upload_fileobj(mask.file, BUCKET_NAME, mask_s3_key)

        # Save image and mask metadata in MongoDB
        image_data = {
            "filename": image.filename,
            "is_mask": False,
            "s3_url": f"https://{BUCKET_NAME}.s3.amazonaws.com/{image_s3_key}",
            "uploaded_at": datetime.utcnow(),
        }

        mask_data = {
            "filename": mask.filename,
            "is_mask": True,
            "s3_url": f"https://{BUCKET_NAME}.s3.amazonaws.com/{mask_s3_key}",
            "uploaded_at": datetime.utcnow(),
            "image_id": image_data["_id"],  # Link to image by _id
        }

        # Insert image and mask metadata into the database
        image_result = db.images.insert_one(image_data)
        mask_data["_id"] = image_result.inserted_id
        mask_result = db.images.insert_one(mask_data)

        # Convert ObjectId to string for response
        image_data["_id"] = str(image_result.inserted_id)
        mask_data["_id"] = str(mask_result.inserted_id)

        return {"message": "Upload successful", "image_data": image_data, "mask_data": mask_data}
    except (NoCredentialsError, PartialCredentialsError):
        raise HTTPException(status_code=500, detail="Invalid AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    try:
        # Read file content
        file_content = await file.read()
        s3_key = f"{datetime.utcnow().isoformat()}_{file.filename}"

        # Upload to S3
        s3.upload_fileobj(file.file, BUCKET_NAME, s3_key)

        # Save metadata in MongoDB
        image_data = {
            "filename": file.filename,
            "is_mask": is_mask,
            "s3_url": f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}",
            "uploaded_at": datetime.utcnow(),
        }
        result = db.images.insert_one(image_data)

        # Convert ObjectId to string in the result
        image_data["_id"] = str(result.inserted_id)

        return {"message": "Upload successful", "data": image_data}
    except (NoCredentialsError, PartialCredentialsError):
        raise HTTPException(status_code=500, detail="Invalid AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))