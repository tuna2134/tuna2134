import math
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


def generate_clock_image(dt: datetime, output_path: str = "clock.png") -> str:
    """Generate an analog clock image using Pillow showing the current time.
    
    Args:
        dt: The datetime to display
        output_path: Path where the clock image will be saved
        
    Returns:
        The output path where the image was saved
    """
    hour = dt.hour % 12
    minute = dt.minute
    second = dt.second
    
    # Calculate angles (0 degrees = 12 o'clock, clockwise)
    second_angle = (second / 60) * 360
    minute_angle = (minute / 60) * 360 + (second / 60) * 6
    hour_angle = (hour / 12) * 360 + (minute / 60) * 30
    
    # Clock dimensions
    size = 400
    center = size / 2
    
    # Create image with white background
    img = Image.new('RGB', (size, size + 60), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw clock face circle
    padding = 10
    draw.ellipse([padding, padding, size - padding, size - padding], 
                 outline='#333333', width=6, fill='white')
    
    # Hand lengths
    hour_length = 100
    minute_length = 140
    second_length = 160
    
    # Calculate hand positions
    def angle_to_coords(angle, length):
        # Convert to radians and adjust for 12 o'clock being 0 degrees
        rad = math.radians(angle - 90)
        x = center + length * math.cos(rad)
        y = center + length * math.sin(rad)
        return x, y
    
    # Draw hour markers
    for i in range(12):
        angle = i * 30
        start_x, start_y = angle_to_coords(angle, 170)
        end_x, end_y = angle_to_coords(angle, 190)
        draw.line([(start_x, start_y), (end_x, end_y)], fill='#333333', width=6)
    
    # Draw hour hand
    hour_x, hour_y = angle_to_coords(hour_angle, hour_length)
    draw.line([(center, center), (hour_x, hour_y)], fill='#333333', width=12)
    
    # Draw minute hand
    minute_x, minute_y = angle_to_coords(minute_angle, minute_length)
    draw.line([(center, center), (minute_x, minute_y)], fill='#666666', width=8)
    
    # Draw second hand
    second_x, second_y = angle_to_coords(second_angle, second_length)
    draw.line([(center, center), (second_x, second_y)], fill='#e74c3c', width=4)
    
    # Draw center dot
    dot_radius = 12
    draw.ellipse([center - dot_radius, center - dot_radius, 
                  center + dot_radius, center + dot_radius], 
                 fill='#333333')
    
    # Draw timestamp text
    timestamp_text = dt.strftime("%Y/%m/%d %H:%M:%S")
    
    # Try to use a nicer font, fall back to default if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except (IOError, OSError):
        font = ImageFont.load_default()
    
    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), timestamp_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (size - text_width) / 2
    text_y = size + 20
    
    draw.text((text_x, text_y), timestamp_text, fill='#666666', font=font)
    
    # Save the image
    img.save(output_path)
    return output_path
