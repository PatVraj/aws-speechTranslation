import boto3
import os
import uuid
import urllib.parse

# Initialize the Transcribe client
transcribe_client = boto3.client('transcribe')

def lambda_handler(event, context):
    """
    This function is triggered by an S3 event and starts an Amazon Transcribe job
    with automatic multi-language identification enabled.
    """
    # 1. Get bucket and key from the S3 event
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    # Use urllib.parse.unquote_plus for object keys with spaces or special characters
    s3_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    # Generate a unique job name to avoid collisions
    job_name = f"transcription-job-{uuid.uuid4()}"
    media_uri = f"s3://{s3_bucket}/{s3_key}"

    # 2. Get environment variables
    output_bucket = os.environ['TRANSCRIBED_BUCKET_NAME']
    
    print(f"Starting multi-language transcription job {job_name} for {media_uri}")

    try:
        # 3. Define the languages to identify.
        # Add all potential languages spoken in your media files.
        # e.g., Hindi, Indian English, Tamil, Telugu, Kannada, Bengali
        language_options = ['hi-IN', 'en-IN', 'ta-IN', 'te-IN', 'kn-IN', 'bn-IN']

        # 4. Start the transcription job with language identification
        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            IdentifyMultipleLanguages=True,
            LanguageOptions=language_options,
            Media={'MediaFileUri': media_uri},
            MediaFormat=s3_key.split('.')[-1],
            OutputBucketName=output_bucket,
            OutputKey=f"{job_name}.json" # Store output with a predictable name
        )
        
        print(f"Successfully started transcription job: {response['TranscriptionJob']['TranscriptionJobName']}")
        return {'status': 'SUCCESS', 'jobName': job_name}

    except Exception as e:
        print(f"Error starting transcription job: {e}")
        raise e