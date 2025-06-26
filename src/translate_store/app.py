import boto3
import json
import os
import csv
from io import StringIO
import urllib.parse
from datetime import datetime

# Initialize AWS clients
s3_client = boto3.client('s3')
translate_client = boto3.client('translate')

def lambda_handler(event, context):
    """
    This function processes a multi-language transcription, uses Amazon Translate's
    auto-detection to translate, and appends it to a master CSV file.
    """
    # 1. Get bucket and key from the S3 event
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    final_bucket = os.environ['FINAL_DATA_BUCKET']
    final_csv_key = 'political_speeches_data.csv'

    try:
        # 2. Get the transcription job output JSON from S3
        transcription_response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
        transcription_content = json.loads(transcription_response['Body'].read().decode('utf-8'))

        # 3. Extract the full transcribed text
        transcribed_text = transcription_content['results']['transcripts'][0]['transcript']
        
        # 4. Translate the text, letting Amazon Translate auto-detect the source language
        translation_response = translate_client.translate_text(
            Text=transcribed_text,
            SourceLanguageCode='auto',
            TargetLanguageCode='en'
        )
        english_translation = translation_response['TranslatedText']
        detected_source_language = translation_response['SourceLanguageCode']

        # 5. Prepare the new data record for the CSV
        speech_record = {
            'Speech_ID': transcription_content['jobName'],
            'Processing_Timestamp': datetime.utcnow().isoformat(),
            'Detected_Source_Language': detected_source_language,
            'Transcription': transcribed_text,
            'Translation_English': english_translation,
            'Transcription_Job_Name': s3_key
        }

        # 6. Read existing CSV from S3, append the new record, and write it back.
        # This "read-append-write" pattern is necessary as S3 objects are immutable.
        try:
            existing_csv_obj = s3_client.get_object(Bucket=final_bucket, Key=final_csv_key)
            existing_csv_content = existing_csv_obj['Body'].read().decode('utf-8')
        except s3_client.exceptions.NoSuchKey:
            # If the file doesn't exist, create an empty string to start with
            existing_csv_content = ''

        output_buffer = StringIO()
        
        # Define fieldnames to ensure consistent CSV column order
        fieldnames = [
            'Speech_ID', 'Processing_Timestamp', 'Detected_Source_Language', 
            'Transcription', 'Translation_English', 'Transcription_Job_Name'
        ]
        
        writer = csv.DictWriter(output_buffer, fieldnames=fieldnames)

        if not existing_csv_content:
            writer.writeheader()
            writer.writerow(speech_record)
        else:
            # To append, we write the existing content first, then the new row without the header
            output_buffer.write(existing_csv_content)
            # Ensure there's a newline before appending the new data
            if not existing_csv_content.endswith('\n'):
                 output_buffer.write('\n')
            
            # Use a temporary buffer to write just the new row as a string
            temp_buffer = StringIO()
            temp_writer = csv.DictWriter(temp_buffer, fieldnames=fieldnames)
            temp_writer.writerow(speech_record)
            output_buffer.write(temp_buffer.getvalue().splitlines()[1] + '\n') # Write only the data row
        
        # Upload the updated CSV content back to S3
        s3_client.put_object(
            Bucket=final_bucket,
            Key=final_csv_key,
            Body=output_buffer.getvalue(),
            ContentType='text/csv'
        )
        
        print(f"Successfully processed and stored multi-language data for {s3_key}")
        return {'status': 'SUCCESS'}

    except Exception as e:
        print(f"Error processing transcription for {s3_key}: {e}")
        raise e