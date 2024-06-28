from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Load the image
image = Image.open('__assets__/provinces.bmp')
image_np = np.array(image)

# Function to zoom into the image
def zoom_image(image, zoom_factor, center=None):
    width, height = image.size
    if center is None:
        center = (width // 2, height // 2)

    x, y = center
    new_width = int(width / zoom_factor)
    new_height = int(height / zoom_factor)
    
    left = max(0, x - new_width // 2)
    upper = max(0, y - new_height // 2)
    right = min(width, x + new_width // 2)
    lower = min(height, y + new_height // 2)
    
    image_cropped = image.crop((left, upper, right, lower))
    return image_cropped.resize((width, height), Image.Resampling.NEAREST)

# Function to edit a pixel
def edit_pixel(image_np, x, y, color):
    image_np[y, x] = color

# Zoom into the image
zoomed_image = zoom_image(image, zoom_factor=2)
zoomed_image_np = np.array(zoomed_image)

# Edit a pixel
edit_pixel(zoomed_image_np, 50, 50, [255, 0, 0])

# Display the edited image
plt.imshow(zoomed_image_np)
plt.axis('off')
plt.show()
