import os
import feedparser as feedparser
import requests

# Define the URL of your favourite podcast's RSS feed
podcast_feed_url = 'https://www.marketplace.org/feed/podcast/marketplace/'

# Define where you want to save your podcast mp3 files
save_location = '/Users/mtodd/Desktop'

def check_mounted(drive_paths):
    for drive_path in drive_paths:
        if os.path.ismount(drive_path):
            print(f'Drive {drive_path} is mounted.')
        else:
            print(f'Drive {drive_path} is not mounted.')

def download_file(url):
    
    # Check if the save location is mounted
    if not os.path.ismount(save_location):
        print(f'Drive {save_location} is not mounted. Aborting.')
        return
    
    local_filename = url.split('/')[-1]
    local_filename = os.path.join(save_location, local_filename)
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

# Use feedparser to parse the RSS feed
feed = feedparser.parse(podcast_feed_url)

# Get the first (latest) podcast entry
if len(feed.entries) > 0:
    first_entry = feed.entries[0]
    print(f'Downloading podcast {first_entry.title}...')
    if 'enclosures' in first_entry:
        for enclosure in first_entry.enclosures:
            if 'audio/mpeg' in enclosure.type:
                mp3_url = enclosure.href
                download_file(mp3_url)
    print('Download complete!')
else:
    print('No entries found in podcast RSS feed!')
