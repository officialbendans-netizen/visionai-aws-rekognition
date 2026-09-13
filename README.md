# 👁️ VisionAI — Serverless Image Recognition Engine

A fully serverless AI-powered image recognition web application built entirely on AWS. Upload any image and Amazon Rekognition instantly detects objects, scenes, faces and more — all in your browser with zero servers.

![AWS](https://img.shields.io/badge/AWS-Serverless-orange?style=flat-square&logo=amazon-aws)
![Rekognition](https://img.shields.io/badge/Amazon-Rekognition-blue?style=flat-square)
![Lambda](https://img.shields.io/badge/AWS-Lambda-orange?style=flat-square)
![DynamoDB](https://img.shields.io/badge/Amazon-DynamoDB-blue?style=flat-square)

---

## 🌟 Live Demo

Hosted on Amazon S3 Static Website Hosting.

---

## 🏗️ Architecture

```
Browser (S3 Static Frontend)
        ↓
User uploads image → compressed automatically
        ↓
Amazon API Gateway (REST API)
        ↓
AWS Lambda (Python 3.12)
        ↓
Amazon Rekognition (AI Analysis)
        ↓
Results saved to Amazon DynamoDB
        ↓
Labels + Confidence scores displayed in browser
```

---

## ☁️ AWS Services Used

| Service | Purpose |
|---|---|
| **Amazon S3** | Image uploads + frontend hosting |
| **AWS Lambda** | Serverless backend logic |
| **Amazon API Gateway** | REST API endpoint |
| **Amazon Rekognition** | AI image analysis — objects, scenes, faces |
| **Amazon DynamoDB** | Store all analysis results |
| **AWS IAM** | Secure permissions between services |
| **Amazon CloudWatch** | Logging and monitoring |

---

## ✨ Features

- 🖼️ Drag and drop any image to analyze
- 👁️ AI detects objects, scenes and labels instantly
- 👤 Counts faces detected in the image
- 📊 Confidence percentage bars for each label
- ⚡ Automatic image compression before sending
- 📋 Analysis history of last 5 uploads
- 🆓 Runs on AWS Free Tier
- 🔒 Fully serverless — zero server management

---

## 📁 Project Structure

```
visionai-aws-rekognition/
│
├── frontend/
│   └── index.html              # Complete frontend web app
│
├── lambda/
│   └── lambda_function.py      # AWS Lambda backend
│
├── architecture/
│   └── architecture.md         # Full architecture details
│
└── README.md
```

---

## 🚀 How to Deploy

### Prerequisites
- AWS Account (Free Tier works)
- AWS Console access

### Step 1 — Create S3 Bucket for uploads
```
Bucket name: image-recognition-uploads-{yourname}
Block all public access: ON
Versioning: Enable
Encryption: SSE-S3
```

### Step 2 — Create DynamoDB Table
```
Table name: image-recognition-results
Partition key: imageId (String)
Capacity: On-demand
```

### Step 3 — Create Lambda Function
```
Name: image-recognition-processor
Runtime: Python 3.12
Timeout: 60 seconds
Policies: AmazonRekognitionFullAccess
          AmazonS3FullAccess
          AmazonDynamoDBFullAccess
          CloudWatchLogsFullAccess
```
Paste code from lambda/lambda_function.py

### Step 4 — Add S3 Trigger to Lambda
```
Bucket: image-recognition-uploads-{yourname}
Event: PUT
Suffixes: .jpg, .jpeg, .png
```

### Step 5 — Create API Gateway
```
Type: REST API
Resource: /analyze
Method: POST
Integration: Lambda proxy
CORS: Enabled
Stage: prod
```

### Step 6 — Update Frontend
Open frontend/index.html and replace API_URL with your invoke URL:
```javascript
const API_URL = 'https://YOUR_ID.execute-api.us-east-1.amazonaws.com/prod/analyze';
```

### Step 7 — Host Frontend
```
Create S3 bucket: image-recognition-frontend-{yourname}
Uncheck: Block all public access
Enable: Static website hosting
Index document: index.html
Add public read bucket policy
Upload: index.html
```

---

## 🧠 What I Learned

- Serverless AI architecture design
- Amazon Rekognition integration
- DynamoDB Decimal type handling
- CORS configuration for API Gateway
- Image compression in the browser
- Lambda proxy integration
- Real world debugging with CloudWatch
- End to end serverless application development

---

## 👨‍💻 Author

**Benjamin Asare Danquah**
- AWS Certified Cloud Practitioner
- GitHub: [@officialbendans-netizen](https://github.com/officialbendans-netizen)

---

## 📄 License

MIT License — feel free to use and modify.
