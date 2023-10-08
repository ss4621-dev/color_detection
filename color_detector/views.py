import cv2
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from .models import ColorDetection  # Import the ColorDetection model

# Function to calculate mean color of contours


def calculate_mean_color(contours, image):
    colors = []
    for contour in contours:
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

        # Calculate the mean color of the region
        mean_color = cv2.mean(image, mask=mask)[:3]
        colors.append([int(value) for value in mean_color])  # Convert to list

    return colors


def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']

        # Read the uploaded image
        image = cv2.imdecode(np.fromstring(
            uploaded_image.read(), np.uint8), cv2.IMREAD_COLOR)

        # Define color ranges for detection (e.g., red, green, blue)
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])

        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])

        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([140, 255, 255])

        # Create binary masks for each color
        mask_red = cv2.inRange(image, lower_red, upper_red)
        mask_green = cv2.inRange(image, lower_green, upper_green)
        mask_blue = cv2.inRange(image, lower_blue, upper_blue)

        # Find contours in the binary masks
        contours_red, _ = cv2.findContours(
            mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(
            mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(
            mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate the mean color of each detected region
        red_colors = calculate_mean_color(contours_red, image)
        green_colors = calculate_mean_color(contours_green, image)
        blue_colors = calculate_mean_color(contours_blue, image)

        # Combine the detected colors
        all_colors = red_colors + green_colors + blue_colors

        # Ensure we have exactly 10 colors
        while len(all_colors) < 10:
            all_colors.append([0, 0, 0])  # Add placeholder black color
        if len(all_colors) > 10:
            all_colors = all_colors[:10]  # Truncate to the top 10 colors

        # Save colors to the database (if needed)
        color_detection = ColorDetection(colors=all_colors)
        color_detection.save()

        # Return results as JSON
        return JsonResponse({"colors": all_colors})

    return render(request, 'color_detector/upload_image.html')
