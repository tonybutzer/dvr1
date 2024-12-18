# wget http://dopey:32400/playlists/7111/items
import xml.etree.ElementTree as ET

def parse_plex_playlist(xml_file):
    """Parses a Plex playlist XML file and returns a list of media items.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        list: A list of dictionaries, each representing a media item with keys:
            - title: Title of the media item
            - key: Plex key of the media item (for further API interactions)
            # Add more keys as needed, e.g., duration, summary, etc.
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()

    media_items = []
    for item in root.findall('Video') + root.findall('Track'):
        media_item = {
            'title': item.find('title').text,
            'key': item.find('key').text
        }
        # Add more fields as needed
        media_items.append(media_item)

    return media_items

# Example usage:
xml_file_path = './playlist_sample.xml'
playlist_items = parse_plex_playlist(xml_file_path)

for item in playlist_items:
    print(f"Title: {item['title']}")
    print(f"Plex Key: {item['key']}")
