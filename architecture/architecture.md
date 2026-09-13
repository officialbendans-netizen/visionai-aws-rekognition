# VisionAI — Architecture Details

## Overview
VisionAI is a fully serverless AI image recognition application.
Zero servers to manage. Scales automatically. Costs nothing when idle.

## Flow
1. User opens web app hosted on S3
2. User drags or selects an image
3. Browser compresses image automatically (max 800x800, 70% quality)
4. Frontend sends compressed image to API Gateway as base64
5. API Gateway triggers Lambda function
6. Lambda decodes image and sends to Amazon Rekognition
7. Rekognition detects labels, objects, scenes and faces
8. Results saved to DynamoDB with Decimal types
9. Lambda returns labels and confidence scores to frontend
10. Frontend displays results with animated confidence bars

## Services

### Amazon S3 — Two Buckets
- image-recognition-uploads-benjamin — stores processed images (private)
- image-recognition-frontend-benjamin — hosts the web app (public)

### AWS Lambda
- Runtime: Python 3.12
- Timeout: 60 seconds
- Handles both S3 triggers and API Gateway requests
- Uses Decimal types for DynamoDB compatibility

### Amazon Rekognition
- detect_labels — finds objects and scenes (max 15, min 70% confidence)
- detect_faces — counts faces in the image

### Amazon DynamoDB
- Table: image-recognition-results
- Partition key: imageId
- Capacity: On-demand
- Stores labels as Decimal types

### Amazon API Gateway
- REST API with Lambda proxy integration
- CORS enabled
- Stage: prod

## Key Lessons Learned
- DynamoDB does not accept float — use Decimal types
- API Gateway has 10MB payload limit — compress images first
- Lambda proxy integration required for CORS headers to pass through
- Always redeploy API Gateway after CORS changes
