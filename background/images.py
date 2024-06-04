import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse



load_dotenv()
c = 0
def getImages(query, start_index=1, num_images=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": os.getenv('CUSTOM_SEARCH_API'),
        "cx": os.getenv('SEARCH_ENGINE_ID'),
        "searchType": "image",
        "num": num_images,
        "start": start_index,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    results = response.json()
    image_urls = [item["link"] for item in results["items"]]
    total_results = int(results["searchInformation"]["totalResults"])

    print(f'Found {total_results} images for the query "{query}".')
    print(f'Fetching images from index {start_index} to {start_index + num_images - 1}...')

    downloadImages(image_urls, num_images)

    while start_index + num_images < total_results:
        user_input = input("Do you want to fetch the next page of results? (yes/no): ")
        if user_input.lower() == "yes":
            start_index += num_images
            return getImages(query, start_index, num_images)
        else:
            break


def downloadImages(image_urls, num_images, folder_name="images"):
    global c
    os.makedirs(folder_name, exist_ok=True)
    count = 0
    for i, url in enumerate(image_urls):
        if count == num_images:
            break
        try:
            response = requests.get(url)
            response.raise_for_status()


            parsed_url = urlparse(url)
            file_extension = os.path.splitext(parsed_url.path)[1][1:]
            if not file_extension:
                file_extension = "jpg" 

            file_name = f"image{c + 1}.{file_extension}"
            file_path = os.path.join(folder_name, file_name)
            print('File Path :',file_path)
            with open(file_path, "wb") as file:
                file.write(response.content)

            print(f"Downloaded: {file_name}")
            count += 1
            c += 1
        except Exception as e:  # Catches any type of exception

            print(e)
    print('All Images downloaded ...')



query = 'Are deepfakes the frightening future of election campaigns? India is already there.'
num_images_per_page = 10

getImages(query, 1, num_images_per_page) 
