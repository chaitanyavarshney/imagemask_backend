# **Image-Mask**

**Image-Mask** is a FastAPI-based service that allows users to upload an image and its corresponding mask, store them in AWS S3, and save metadata in MongoDB. The service provides an easy-to-use API for handling image and mask uploads, with integration for tracking and storing relevant metadata.

---

## **Features**

- **Image and Mask Upload**: Upload an image and its corresponding mask.
- **AWS S3 Integration**: Store images and masks in an S3 bucket.
- **MongoDB Storage**: Save metadata for each image and mask in MongoDB.
- **CORS Support**: The API supports cross-origin requests from a configured frontend.

---

## **Tech Stack**

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python Web Framework)
- **File Storage**: [AWS S3](https://aws.amazon.com/s3/)
- **Database**: [MongoDB](https://www.mongodb.com/)
- **Caching/Queue**: Redis (if needed for additional features)
- **Containerization**: Docker
- **Authentication**: (Future work, if needed)

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone git@github.com:your-username/image-mask.git
cd image-mask
```
### **2. Clone the Repository**
Make sure you have Python and pip installed. Then run:
```bash
pip install -r requirements.txt
```
### **3. Configure Environment Variables**
Create a .env file in the root directory and add the following variables:
```bash
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your_s3_bucket_name
MONGO_URI=mongodb://localhost:27017
```

### **4.  Run the Application**
•	Development Mode (Without Docker):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

•	Production Mode (With Docker):
```bash
docker-compose up --build
```

### **5.  Access the Application**
Visit the application at: http://localhost:8000.

###  **API Endpoints**
###  **1. Upload Image and Mask**

POST /upload/
Request Body:
```bash
{
  "image": "<image_file>",
  "mask": "<mask_file>"
}
```

Response:
```bash
{
  "message": "Upload successful",
  "image_data": {
    "filename": "image.jpg",
    "is_mask": false,
    "s3_url": "https://your-bucket-name.s3.amazonaws.com/unique_image_key",
    "uploaded_at": "2024-12-21T00:00:00.000Z"
  },
  "mask_data": {
    "filename": "mask.jpg",
    "is_mask": true,
    "s3_url": "https://your-bucket-name.s3.amazonaws.com/unique_mask_key",
    "uploaded_at": "2024-12-21T00:00:00.000Z",
    "image_id": "image_id_from_mongo"
  }
}
```
### **2.  Error Handlingn**
If there’s an error in uploading, you will receive a 500 error with the message:
```bash
{
  "detail": "Error message here"
}
```
### ** Deployment**
To deploy the application, ensure that the environment variables are correctly configured and use Docker for easy deployment.
```bash
{
  docker-compose -f docker-compose.prod.yml up --build
}
```
Docker Compose Configuration:
```bash
{
  version: '3'
services:
  fastapi:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
}
```

---
**Additional Notes**

- The AWS S3 service is used to store images and masks. Ensure your AWS credentials have the necessary permissions to access S3.
- MongoDB is used to store metadata for the uploaded images and masks.
-The application uses CORS middleware to allow requests from your frontend, specified in the configuration.
---
**Contributing**
Feel free to fork this repository and submit pull requests. Make sure to follow the coding standards and write tests for new features.