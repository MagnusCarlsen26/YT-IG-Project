import boto3
from dotenv import load_dotenv,dotenv_values
import os
load_dotenv()

def aws_polly(text,output_file='audio.mp3', voice_id='Joanna'):
    aws_regions = [
        "us-east-2",      # US East (Ohio)
        "us-east-1",      # US East (N. Virginia)
        "us-west-1",      # US West (N. California)
        "us-west-2",      # US West (Oregon)
        "af-south-1",     # Africa (Cape Town)
        "ap-east-1",      # Asia Pacific (Hong Kong)
        "ap-south-1",     # Asia Pacific (Mumbai) 
        "ap-northeast-1",  # Asia Pacific (Tokyo)
        "ap-northeast-2",  # Asia Pacific (Seoul)
        "ap-northeast-3",  # Asia Pacific (Osaka)
        "ap-southeast-1",  # Asia Pacific (Singapore)
        "ap-southeast-2",  # Asia Pacific (Sydney)
        "ap-southeast-3",  # Asia Pacific (Jakarta)
        "ca-central-1",    # Canada (Central)
        "eu-central-1",    # Europe (Frankfurt)
        "eu-west-1",      # Europe (Ireland)
        "eu-west-2",      # Europe (London)
        "eu-west-3",      # Europe (Paris)
        "eu-north-1",     # Europe (Stockholm)
        "eu-south-1",     # Europe (Milan)
        "eu-south-2",     # Europe (Spain)
        "me-south-1",     # Middle East (Bahrain)
        "sa-east-1",      # South America (São Paulo)
        # ... (and any newer regions added by AWS)
    ]

    for aws_region in aws_regions :
        try :
            print(f"Trying {aws_region}")
            polly_client = boto3.client('polly', region_name=aws_region,
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
            break
        except Exception as e:
            print(f"Failed {e}")
    

