import requests

# Replace with your actual values
access_token = 'EAAWTIoxiHiYBO5f6uhxwcopyQqQC3YYaPAUanuVuJ3y4ZC7hReKSvZAanJEwZAobP528mGbklD4E1EGiomLzHvtldBYlEDIeHl8kFp0xJSSIXZB1lDjoBUGFD9F99jEvZCgebZClTxJj5YxCybeupV4bH6yQ6bVFaIXbg7FX9C2pEQhTxzHgK4Uy98qMtPHGEaUsJFBiM5AbdIm2f0TFojIHZCCGIgZD'
instagram_user_id = '66697169718'
video_file_path = 'videoplayback.mp4'  
# 1. Initiate Video Upload
url = f'https://graph.facebook.com/{instagram_user_id}/media'
data = {
    'media_type': 'REELS',
    'video_url': None,  # Or upload the video file directly if not using a URL
}
files = {
    'source': open(video_file_path, 'rb')
}
headers = {
    'Authorization': f'Bearer {access_token}'
}
response = requests.get(url, data=data, files = files ,headers=headers)

if response.status_code == 200:
    upload_session_id = response.json()['id']

    # 2. Publish the Reel (After video upload is complete, if applicable)
    publish_url = f'https://graph.facebook.com/{instagram_user_id}/media_publish'
    publish_data = {
        'creation_id': upload_session_id
    }
    publish_response = requests.post(publish_url, data=publish_data, headers=headers)

    if publish_response.status_code == 200:
        media_id = publish_response.json()['id']
        print(f'Reel published successfully with media ID: {media_id}')
    else:
        print(f'Error publishing Reel: {publish_response.json()}')
else:
    print(f'Error initiating upload: {response.json()}')
