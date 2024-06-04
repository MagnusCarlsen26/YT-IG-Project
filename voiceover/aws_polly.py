import boto3
from dotenv import load_dotenv,dotenv_values
import os
load_dotenv()

def aws_polly(text, output_file='audio.mp3', voice_id='Joanna'):

    polly_client = boto3.client('polly', region_name='ap-south-1',
                            aws_access_key_id=os.getenv('AWS_AK'),
                            aws_secret_access_key=os.getenv('AWS_SK'))

    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id
    )

    with open(output_file, 'wb') as file:
        file.write(response['AudioStream'].read())
    
    print("Speech saved to audio.mp3")


