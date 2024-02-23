import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import os
import cairosvg

# Ensure the directory for the resized images exists
os.makedirs('resized_images', exist_ok=True)

def download_and_resize_image(url, output_path, symbol):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors

        if url.endswith('.svg'):
            # Convert SVG to PNG in memory
            png_data = cairosvg.svg2png(bytestring=response.content)
            img = Image.open(BytesIO(png_data))
        else:
            # Open the image directly from bytes for non-SVG formats
            img = Image.open(BytesIO(response.content))

        # Resize and save the image
        img = img.resize((120, 120), Image.Resampling.LANCZOS)
        img.save(output_path, 'PNG')
    except UnidentifiedImageError:
        print(f"Could not process image: {url}. The format might not be supported.")
    except Exception as e:
        print(f"Error with {symbol} at {url}: {e}")

def main():
    json_url = 'https://storage.googleapis.com/mrgn-public/mrgn-token-metadata-cache.json'

    response = requests.get(json_url)
    tokens = response.json()

    for token in tokens:
        symbol = token.get('symbol')
        logo_uri = token.get('logoURI')
        if logo_uri and symbol:
            output_path = os.path.join('resized_images', f"{symbol}.png")
            download_and_resize_image(logo_uri, output_path, symbol)
            print(f"Processed {symbol}.png")

if __name__ == "__main__":
    main()
