import math
from datetime import datetime


def generate_clock_svg(dt: datetime) -> str:
    """Generate an analog clock SVG showing the current time."""
    hour = dt.hour % 12
    minute = dt.minute
    second = dt.second
    
    # Calculate angles (0 degrees = 12 o'clock, clockwise)
    second_angle = (second / 60) * 360
    minute_angle = (minute / 60) * 360 + (second / 60) * 6
    hour_angle = (hour / 12) * 360 + (minute / 60) * 30
    
    # Clock dimensions
    size = 200
    center = size / 2
    
    # Hand lengths
    hour_length = 50
    minute_length = 70
    second_length = 80
    
    # Calculate hand positions
    def angle_to_coords(angle, length):
        # Convert to radians and adjust for 12 o'clock being 0 degrees
        rad = math.radians(angle - 90)
        x = center + length * math.cos(rad)
        y = center + length * math.sin(rad)
        return x, y
    
    hour_x, hour_y = angle_to_coords(hour_angle, hour_length)
    minute_x, minute_y = angle_to_coords(minute_angle, minute_length)
    second_x, second_y = angle_to_coords(second_angle, second_length)
    
    # Generate SVG
    svg = f'''<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
  <!-- Clock face -->
  <circle cx="{center}" cy="{center}" r="95" fill="white" stroke="#333" stroke-width="3"/>
  
  <!-- Hour markers -->'''
    
    for i in range(12):
        angle = i * 30
        start_x, start_y = angle_to_coords(angle, 85)
        end_x, end_y = angle_to_coords(angle, 95)
        svg += f'\n  <line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" stroke="#333" stroke-width="3"/>'
    
    svg += f'''
  
  <!-- Hour hand -->
  <line x1="{center}" y1="{center}" x2="{hour_x}" y2="{hour_y}" stroke="#333" stroke-width="6" stroke-linecap="round"/>
  
  <!-- Minute hand -->
  <line x1="{center}" y1="{center}" x2="{minute_x}" y2="{minute_y}" stroke="#666" stroke-width="4" stroke-linecap="round"/>
  
  <!-- Second hand -->
  <line x1="{center}" y1="{center}" x2="{second_x}" y2="{second_y}" stroke="#e74c3c" stroke-width="2" stroke-linecap="round"/>
  
  <!-- Center dot -->
  <circle cx="{center}" cy="{center}" r="6" fill="#333"/>
  
  <!-- Time text -->
  <text x="{center}" y="{center + 130}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#666">
    {dt.strftime("%Y/%m/%d %H:%M:%S")}
  </text>
</svg>'''
    
    return svg
