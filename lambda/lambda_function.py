import boto3
import json
import uuid
import base64
from urllib.parse import unquote_plus
from datetime import datetime
from decimal import Decimal

rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('image-recognition-results')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    if event.get('httpMethod'):
        return handle_api_request(event)
    return handle_s3_trigger(event)

def handle_s3_trigger(event):
    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = unquote_plus(event['Records'][0]['s3']['object']['key'])
        print(f'Analyzing image from S3: {object_key}')
        response = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': object_key}},
            MaxLabels=15, MinConfidence=70
        )
        labels = []
        for label in response['Labels']:
            labels.append({
                'name': label['Name'],
                'confidence': Decimal(str(round(label['Confidence'], 2)))
            })
        face_response = rekognition.detect_faces(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': object_key}},
            Attributes=['ALL']
        )
        face_count = len(face_response['FaceDetails'])
        image_id = str(uuid.uuid4())
        table.put_item(Item={
            'imageId': image_id, 'fileName': object_key,
            'bucketName': bucket_name, 'labels': labels,
            'faceCount': face_count, 'analyzedAt': datetime.now().isoformat(),
            'status': 'analyzed'
        })
        return {
            'statusCode': 200,
            'body': json.dumps({
                'imageId': image_id,
                'labels': [{'name': l['name'], 'confidence': float(l['confidence'])} for l in labels],
                'faceCount': face_count
            })
        }
    except Exception as e:
        print(f'Error: {str(e)}')
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def handle_api_request(event):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    try:
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        image_data = body.get('image', '')
        file_name = body.get('fileName', 'upload.jpg')
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        rek_response = rekognition.detect_labels(
            Image={'Bytes': image_bytes}, MaxLabels=15, MinConfidence=70
        )
        labels = []
        for label in rek_response['Labels']:
            labels.append({
                'name': label['Name'],
                'confidence': Decimal(str(round(label['Confidence'], 2)))
            })
        face_response = rekognition.detect_faces(
            Image={'Bytes': image_bytes}, Attributes=['ALL']
        )
        face_count = len(face_response['FaceDetails'])
        unique_name = str(uuid.uuid4()) + '_' + file_name
        s3.put_object(
            Bucket='image-recognition-uploads-benjamin',
            Key=unique_name, Body=image_bytes, ContentType='image/jpeg'
        )
        image_id = str(uuid.uuid4())
        table.put_item(Item={
            'imageId': image_id, 'fileName': unique_name,
            'bucketName': 'image-recognition-uploads-benjamin',
            'labels': labels, 'faceCount': face_count,
            'analyzedAt': datetime.now().isoformat(), 'status': 'analyzed'
        })
        labels_json = [{'name': l['name'], 'confidence': float(l['confidence'])} for l in labels]
        return {
            'statusCode': 200, 'headers': headers,
            'body': json.dumps({
                'message': 'Success', 'imageId': image_id,
                'labels': labels_json, 'faceCount': face_count, 'fileName': unique_name
            })
        }
    except Exception as e:
        print(f'Error: {str(e)}')
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e)})}
