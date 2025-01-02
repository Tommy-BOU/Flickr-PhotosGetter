import os
import requests
from flickrapi import FlickrAPI
from tqdm import tqdm

# Flickr API credentials
API_KEY = 'API_KEY'
API_SECRET = 'API_SECRET'

# Flickr username (replace with the account's username)
USERNAME = 'USERNAME'

# Directory to save the downloaded photos
DOWNLOAD_DIR = 'flickr_photos'

# Initialize Flickr API
flickr = FlickrAPI(API_KEY, API_SECRET, format='parsed-json')

def get_user_id(username):
    """Fetches the user ID based on the username."""
    response = flickr.people.findByUsername(username=username)
    return response['user']['id']

def get_photos(user_id):
    """Fetches all photo URLs from the user's photostream."""
    photos = []
    page = 1
    while True:
        response = flickr.people.getPhotos(user_id=user_id, per_page=500, page=page)
        photos.extend(response['photos']['photo'])
        if page >= response['photos']['pages']:
            break
        page += 1
    return photos

def download_photo(photo, download_dir):
    """Downloads a single photo."""
    filename = os.path.join(download_dir, f"{photo['id']}.jpg")
    if os.path.exists(filename):
        return

    url = f"https://farm{photo['farm']}.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}.jpg"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    else:
        raise RuntimeError(f"Failed to download photo: {url} - Status code: {response.status_code} - Content: {response.content}")

def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    print(f"Fetching user ID for username: {USERNAME}")
    user_id = get_user_id(USERNAME)
    print(f"User ID found: {user_id}")
    photos = get_photos(user_id)
    print(f"Found {len(photos)} photos to download.")

    for photo in tqdm(photos, desc="Downloading photos"):
        download_photo(photo, DOWNLOAD_DIR)

if __name__ == '__main__':
    main()


