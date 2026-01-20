# download_images.py
import requests
import os
from PIL import Image  # For resizing if needed

# Create assets directory if it doesn't exist
os.makedirs('assets', exist_ok=True)

# CORRECTED NASA Earth image URL
earth_url = "https://eoimages.gsfc.nasa.gov/images/imagerecords/57000/57730/land_shallow_topo_2048.jpg"

try:
    print("🌍 Downloading Earth image from NASA...")
    earth_response = requests.get(earth_url, timeout=10)
    earth_response.raise_for_status()  # Check for HTTP errors
    
    with open('assets/earth.jpg', 'wb') as f:
        f.write(earth_response.content)
    print("✅ Earth image downloaded successfully!")
    
except requests.exceptions.RequestException as e:
    print(f"❌ Error downloading Earth image: {e}")
    print("⚠️ Using fallback image or skipping Earth image...")

# NASA Moon image
moon_url = "https://moon.nasa.gov/system/resources/gltf_webp/444/444_Moon_New_4K.jpg"

try:
    print("🌙 Downloading Moon image from NASA...")
    moon_response = requests.get(moon_url, timeout=10)
    moon_response.raise_for_status()
    
    with open('assets/moon.jpg', 'wb') as f:
        f.write(moon_response.content)
    print("✅ Moon image downloaded successfully!")
    
except requests.exceptions.RequestException as e:
    print(f"❌ Error downloading Moon image: {e}")
    print("⚠️ Using fallback image or skipping Moon image...")

# Optional: Resize images if they're too large
print("\n🔄 Optimizing images for the project...")
try:
    # Resize Earth image (optional)
    earth_img = Image.open('assets/earth.jpg')
    if earth_img.size[0] > 800:  # If width > 800px
        earth_img = earth_img.resize((800, 400))
        earth_img.save('assets/earth.jpg')
        print("✅ Earth image resized to 800x400")
    
    # Resize Moon image (optional)
    moon_img = Image.open('assets/moon.jpg')
    if moon_img.size[0] > 800:
        moon_img = moon_img.resize((800, 400))
        moon_img.save('assets/moon.jpg')
        print("✅ Moon image resized to 800x400")
        
except Exception as e:
    print(f"⚠️ Could not resize images: {e}")

print("\n🎉 Image setup complete!")
print("Assets created in: ./assets/")
print("\nFiles:")
for file in os.listdir('assets'):
    print(f"  - {file}")