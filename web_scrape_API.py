import requests
from bs4 import BeautifulSoup
import json
import validators
import os

JSON_FILE_PATH = 'visualization_data.json'  # Path to the JSON file

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        scraped_data = {
            'website': url,
            'data': {}
        }
        
        # Extracting the title
        title_element = soup.find('title')
        if title_element:
            scraped_data['data']['title'] = title_element.get_text()

        # Extracting the author
        author_element = soup.find('meta', attrs={'name': 'author'})
        if author_element:
            scraped_data['data']['author'] = author_element.get_text()

        # Extracting the publish date
        publish_date_element = soup.find('meta', attrs={'name': 'publish-date'})
        if publish_date_element:
            scraped_data['data']['publish_date'] = publish_date_element.get_text()

        # Extracting the topic
        topic_element = soup.find('meta', attrs={'name': 'topic'})
        if topic_element:
            scraped_data['data']['topic'] = topic_element.get_text()
        
        # Extracting the excerpt
        excerpt_element = soup.find('meta', attrs={'name': 'excerpt'})
        if excerpt_element:
            scraped_data['data']['excerpt'] = excerpt_element.get_text()
        
        # Extracting the text
        text_element = soup.find('meta', attrs={'name': 'text'})
        if text_element:
            scraped_data['data']['text'] = text_element.get_text()
        
        # Extracting the media type and url
        media_element = soup.find('meta', attrs={'name': 'media'})
        if media_element:
            media_string = media_element.get_text()
            if '|' in media_string:
                media_parts = media_string.split('|')
                scraped_data['data']['media_type'] = media_parts[0].strip()
                scraped_data['data']['media_url'] = media_parts[1].strip()
            else:
                scraped_data['data']['media_type'] = None
                scraped_data['data']['media_url'] = None
        
        # Extracting the source
        source_element = soup.find('meta', attrs={'name': 'source'})
        if source_element:
            scraped_data['data']['source'] = source_element.get_text()
        
        # Extracting all paragraphs
        paragraphs = soup.find_all('p')
        if paragraphs:
            scraped_data['data']['paragraphs'] = [p.get_text() for p in paragraphs]
            
        transformed_data = transform_data(scraped_data['data'])
        scraped_data['data'] = transformed_data
        
        return scraped_data
        
    except requests.exceptions.RequestException as e:
        error_message = f"Request Error: {str(e)}"
        return {'error_type': 'Request Error', 'error': error_message}

    except Exception as e:
        error_message = f"Scraping Error: {str(e)}"
        return {'error_type': 'Scraping Error', 'error': error_message}

def transform_data(data):
    # Perform data transformations, formatting, or additional processing here
    transformed_data = data  # Placeholder for now
    return transformed_data

def update_json_file(url):
    scraped_data = scrape_website(url)
    
    if 'error' in scraped_data:
        # Handle error case
        return jsonify({'error': scraped_data['error']})
    
    # Prepare the data for visualization by selecting relevant fields
    visualization_data = {
        'website': scraped_data['website'],
        'data': scraped_data['data']
        # Add any additional fields needed for visualization
    }
    
    if os.path.exists(JSON_FILE_PATH):
        # Load existing data from the JSON file
        with open(JSON_FILE_PATH, 'r') as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Append the new visualization data to the existing data
    existing_data.append(visualization_data)

    # Write the updated data to the JSON file
    with open(JSON_FILE_PATH, 'w') as json_file:
        json.dump(existing_data, json_file)
    
    return {'message': 'JSON file updated successfully'}

# Flask is used to create a basic API endpoint
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def api_scrape():
    url = request.args.get('url')
    
    if not validators.url(url):
        return jsonify({'error_type': 'Invalid URL', 'error': 'Please provide a valid URL'})
    
    scraped_data = scrape_website(url)
    return jsonify(scraped_data)

@app.route('/generate_json', methods=['POST'])
def generate_json():
    url = request.json.get('url')

    # Validate the URL
    if not validators.url(url):
        return jsonify({'error': 'Invalid URL'})

    try:
        result = update_json_file(url)
        return jsonify(result)
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to retrieve scraped data from the web scraping API'})
    except json.JSONDecodeError as e:
        return jsonify({'error': 'Failed to decode JSON file'})
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)})

if __name__ == '__main__':
    app.run()
