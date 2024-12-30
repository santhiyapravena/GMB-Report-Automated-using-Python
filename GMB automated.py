from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, lightblue, lightgreen, lightgrey, black, white, red, yellow, blue, green
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
import matplotlib.pyplot as plt
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.shapes import Circle
from datetime import datetime
import json
from math import cos, sin ,radians
import os
from io import BytesIO

# Input and output paths
json_file = r"C:/Users/SANTHIYA/Downloads/Coimbatore2.json"
pdf_output = r"C:/Users/SANTHIYA/Downloads/enhanced_report_with_features.pdf"

def generate_stars(rating):
    """Generate a list of stars with their colors based on the rating value."""
    full_stars = int(rating)
    half_star = 1 if rating % 1 >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = []
    stars.extend([('★', HexColor("#FFD700"))] * full_stars)  # Gold for full stars
    if half_star:
        stars.append(('★', HexColor("#FFD700")))  # Gold for half star
    stars.extend([('★', HexColor("#A9A9A9"))] * empty_stars)  # Grey for empty stars
    
    return stars

def draw_shadowed_box(c, x, y, width, height, color):
    """Draw a box with a shadow effect."""
    # Draw shadow
    c.setFillColor(HexColor("#d3d3d3"))  # Light grey for shadow
    c.roundRect(x + 2, y - 2, width, height, 5, fill=1, stroke=0)  # Shadow offset
    # Draw main box
    c.setFillColor(color)
    c.roundRect(x, y, width, height, 5, fill=1, stroke=0)  # Rounded corners

def generate_enhanced_pdf(json_data, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4
    margin = 35  # Margin for alignment

    # Title Section with Full Background
    c.setFillColor(HexColor("#D6EAF8"))  # Attractive blue
    c.rect(0, height - 90, width, 90, fill=1, stroke=0)

    # Add Left Logo
    left_logo_path = "C:/Users/SANTHIYA/Downloads/eywalogo.png"  # Update with your logo path
    c.drawImage(left_logo_path, margin-15, height - 60, width=100, height=38, mask="auto")  # Adjust size as needed

    # Add Right Logo
    right_logo_path = "C:/Users/SANTHIYA/Downloads/bealogo.webp"  # Update with your logo path
    c.drawImage(right_logo_path, width - margin - 50, height - 70, width=60, height=45, mask="auto")  # Adjust size as needed

    # Title Text
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(HexColor("#154360"))
    c.drawCentredString(width / 2, height - 40, json_data.get('title', 'Enhanced PDF Report'))
    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 70, "Branch Performance Overview")
    
    # Branch and Month Section
    # Set font and color for the branch text
    c.setFont("Helvetica-Bold", 14)  # Increased font size for the branch
    c.setFillColor(HexColor("#33529c"))

    # Create a centered layout for Branch
    branch_text = f"Branch: {json_data.get('branch', 'N/A')}"
    branch_width = c.stringWidth(branch_text, "Helvetica-Bold", 16)

    # Center the branch text
    c.drawString((width - branch_width) / 2, height - 110, branch_text)

    # Set font and color for the month text
    c.setFont("Helvetica-Bold", 12)  # Smaller font size for the month
    month_text = f"Month: {json_data.get('month', 'N/A')}"
    month_width = c.stringWidth(month_text, "Helvetica-Bold", 14)

    # Center the month text below the branch text
    c.drawString((width - month_width) / 2, height - 130, month_text)

    # Ratings Displayed in Four Boxes
    total_reviews = json_data['total_reviews']
    box_width = 130 
    box_height = 60
    box_y = height - 200
    
    # Box 1: Total Ratings
    draw_shadowed_box(c, (width - (box_width * 4 + 60)) / 2, box_y, box_width, box_height, HexColor("#FDFEFE"))
    c.setFillColor(HexColor("#1F618D"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString((width - (box_width * 4 + 60)) / 2 + box_width / 2, box_y + 40, "Total Ratings")  # Label
    c.setFont("Helvetica-Bold", 20)  # Set font for the value
    c.drawCentredString((width - (box_width * 4 + 60)) / 2 + box_width / 2, box_y + 20, str(total_reviews['total_rating']))  # Value below the label

    # Determine the arrow direction based on the rating value
    rating_value = total_reviews['total_rating']
    arrow = "↑" if rating_value > 50 else "↓"  # Example threshold: 3
    arrow_color = HexColor("#165f07") if rating_value > 50 else HexColor("#dc3545")  # Green for up, red for down

    # Create a small box for the arrow and percentage
    small_box_width = 40  # Width to accommodate both arrow and percentage
    small_box_height = 15
    small_box_x = (width - (box_width * 4 + 60)) / 2 + box_width / 2 - 20  # Center the small box
    small_box_y = box_y + 2  # Position the small box below the value

    # Draw the small box
    c.setFillColor(HexColor("#D6EAF8"))  # Background color for the small box
    c.rect(small_box_x, small_box_y, small_box_width, small_box_height, fill=1, stroke=0)  # Draw the small box with a border

    # Draw the arrow
    c.setFont("Helvetica", 10)  # Set a larger font size for the arrow
    c.setFillColor(arrow_color)  # Set color for the arrow
    c.drawString(small_box_x + 3, small_box_y + 4, arrow)  # Position the arrow in the small box

    # Draw the percentage
    percentage = f"{(rating_value / 100) * 100:.1f}%"  # Calculate percentage based on a scale of 5
    c.setFillColor(HexColor("#154360"))  # Set text color to black
    c.setFont("Helvetica", 8)  # Set font for the percentage
    c.drawString(small_box_x + 17, small_box_y + 5, percentage)  # Position the percentage to the right of the arrow

    # Box 2: Average Ratings
    draw_shadowed_box(c, (width - (box_width * 4 + 60)) / 2 + box_width + 20, box_y, box_width, box_height, HexColor("#FDFEFE"))
    c.setFillColor(HexColor("#1F618D"))
    c.setFont("Helvetica-Bold", 10)
    average_rating = total_reviews['average_rating']
    stars = generate_stars(average_rating)

    # Draw the average rating label
    c.drawCentredString((width - (box_width * 4 + 60)) / 2 + box_width + 20 + box_width / 2, box_y + 40, "Average Rating")

    # Draw the average rating value
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString((width - (box_width * 4 + 60)) / 2 + box_width + 20 + box_width / 2, box_y + 20, f"{average_rating:.1f}")

    # Draw the stars below the average rating value
    star_x = (width - (box_width * 4 + 60)) / 2 + box_width + 20 + box_width / 2
    star_y = box_y + 6  # Position the stars below the average rating value
    c.setFont("Helvetica", 16)
    for i, (star, color) in enumerate(stars):
        c.setFillColor(color)  # Set the color for each star
        c.drawString(star_x + (i * 13) - (len(stars) * 6), star_y, star)  # Adjust position for each star

    # Box 3: Unanswered Reviews
    draw_shadowed_box(c, (width - (box_width * 4 + 60)) / 2 + (box_width * 2) + 40, box_y, box_width, box_height, HexColor("#FDFEFE"))
    c.setFillColor(HexColor("#1F618D"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString((width - (box_width * 4 + 60)) / 2 + (box_width * 2) + 40 + box_width / 2, box_y + 40, "Unanswered Reviews")  # Label
    unanswered_reviews = total_reviews.get('unanswered_reviews', 0)  # Default to 0 if not found
    c.setFont("Helvetica-Bold", 20)  # Set font for the value
    c.drawCentredString((width - (box_width * 4 + 60)) / 2 + (box_width * 2) + 40 + box_width / 2, box_y + 20, str(unanswered_reviews))  # Value below the label

    # Box 4: Unverified Listings
    draw_shadowed_box(c, (width - (box_width * 4 + 60)) / 2 + (box_width * 3) + 60, box_y, box_width, box_height, HexColor("#FDFEFE"))
    c.setFillColor(HexColor("#1F618D"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString((width - (box_width * 4 + 60)) / 2 + (box_width * 3) + 60 + box_width / 2, box_y + 40, "Unverified Listings")  # Label
    c.setFont("Helvetica-Bold", 20)  # Set font for the value
    c.drawCentredString((width - (box_width * 4 + 60)) / 2 + (box_width * 3) + 60 + box_width / 2, box_y + 20, str(total_reviews['unverified_listings']))  # Value below the label

   # Section Title: Ratings Breakdown
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(HexColor("#2E4053"))
    c.drawString(margin, box_y - 40, "Ratings Breakdown")

    # Ratings Breakdown: Stars
    ratings = total_reviews['ratings_breakdown']
    ratings_data = [ratings["5-star"], ratings["4-star"], ratings["3-star"], ratings["2-star"], ratings["1-star"]]
    ratings_labels = ["5-star", "4-star", "3-star", "2-star", "1-star"]

    plt.bar(ratings_labels, ratings_data)
    plt.xlabel('Ratings', fontsize=12)
    

    # Define colors for each rating
    label_colors = [
        HexColor("#2E4053"),  
        HexColor("#2E4053"),  
        HexColor("#2E4053"),  
        HexColor("#2E4053"), 
        HexColor("#2E4053")   
        ]

    # Positioning for stars
    star_x_start = margin  # Starting x position for stars
    star_y_start = box_y - 75  # Starting y position for stars
    star_spacing = 25  # Space between each rating section

    # Draw stars for each rating
    for i, (label, count) in enumerate(zip(ratings_labels, ratings_data)):
        c.setFillColor(label_colors[i])  # Set color based on the index
        c.setFont("Helvetica-Bold", 15)
        c.drawString(star_x_start, star_y_start - (i * star_spacing), label)

        # Draw the stars
        stars = generate_stars(5 - i)  # Generate stars for the current rating (5 to 1)
        star_x = star_x_start + 60  # Starting x position for stars
        star_y = star_y_start - (i * star_spacing)  # Y position for stars

        # Draw the stars
        for j, (star, color) in enumerate(stars):
            c.setFillColor(color)  # Set the color for each star
            c.drawString(star_x + (j * 15), star_y, star)  # Adjust position for each star

        # Draw the count next to the stars
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)  # Set color for the count text
        c.drawString(star_x + (len(stars) * 10) + 30, star_y, str(count))  # Position the count next to the stars

    # Ratings Breakdown Table
    ratings_table_data = [
        ["Rating", "Count"],
        ["5-star", ratings["5-star"]],
        ["4-star", ratings["4-star"]],
        ["3-star", ratings["3-star"]],
        ["2-star", ratings["2-star"]],
        ["1-star", ratings["1-star"]],
        ]

    # Ratings Breakdown Table
    ratings_table = Table(ratings_table_data, colWidths=[150, 100])
    ratings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#494253")),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),  # Header text color
        ('TEXTCOLOR', (0, 1), (0, 1), HexColor("#00004d")), 
        ('TEXTCOLOR', (1, 1), (1, 1), HexColor("#00004d")),
        ('TEXTCOLOR', (0, 2), (0, 2), HexColor("#00004d")), 
        ('TEXTCOLOR', (1, 2), (1, 2), HexColor("#00004d")),
        ('TEXTCOLOR', (0, 3), (0, 3), HexColor("#00004d")), 
        ('TEXTCOLOR', (1, 3), (1, 3), HexColor("#00004d")),
        ('TEXTCOLOR', (0, 4), (0, 4), HexColor("#00004d")), 
        ('TEXTCOLOR', (1, 4), (1, 4), HexColor("#00004d")),
        ('TEXTCOLOR', (0, 5), (0, 5), HexColor("#00004d")), 
        ('TEXTCOLOR', (1, 5), (1, 5), HexColor("#00004d")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header
        ('BACKGROUND', (0, 1), (-1, -1), HexColor("#F5F5F5")),  # Default row background
        ('BACKGROUND', (0, 1), (-1, -1), HexColor("#FFFFFF")),  # Default row background
        ('BACKGROUND', (0, 2), (-1, 2), HexColor("#F5F5F5")),  # Alternate row background
        ('BACKGROUND', (0, 4), (-1, 4), HexColor("#F5F5F5")),  # Alternate row background
        ('GRID', (0, 0), (-1, -1), 1, HexColor("#3b3c36")),  # Grid lines
        ('LEFTPADDING', (0, 0), (-1, -1), 10),  # Left padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Right padding
        ]))
    ratings_table.wrapOn(c, width, height)
    ratings_table.drawOn(c, margin + 270, box_y - 170)

    # Section Title: Sentiment Analysis
    c.setFillColor(HexColor("#2E4053"))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, box_y - 225, "Sentiment Analysis")

# Sentiment Data
    sentiment = json_data['sentiment_analysis']
    sentiment_data = [sentiment['Positive'], sentiment['Neutral'], sentiment['Negative']]
    sentiment_labels = ['Positive', 'Neutral', 'Negative']

    # Create the pie chart
    pie_chart = Drawing(250, 150)
    pie = Pie()
    pie.x = 30
    pie.y = 20
    pie.width = 115
    pie.height = 115
    pie.data = sentiment_data
    pie.labels = sentiment_labels
  
# Define colors for the slices
    pie.slices[0].fillColor = HexColor("#00a550")  # Green for positive
    pie.slices[1].fillColor = HexColor("#f0e130")  # Yellow for neutral
    pie.slices[2].fillColor = HexColor("#dc143c")  # Soft red for negative

# Adjust pie chart appearance
    pie.startAngle = 80  # Start at the top
    pie.slices.strokeWidth = 0

    

# Add custom labels inside the pie slices with percentages
    total = sum(sentiment_data)
    label_offset = 20
    pie.labels = [f"{label} ({data})" for label, data in zip(sentiment_labels, sentiment_data)]
    for i, count in enumerate(sentiment_data):
        percentage = (count / total) * 100
        angle = pie.startAngle + sum(pie.data[:i]) / total * 360 + (pie.data[i] / total * 180)
    
    # Calculate the position for the label inside the slice
        angle_rad = radians(angle)  # Convert angle to radians
        
        label_x = pie.x + pie.width / 2 + (pie.width / 1.4) * cos(angle_rad) + label_offset * cos(angle_rad)
        label_y = pie.y + pie.height / 2 + (pie.height / 1.4) * sin(angle_rad) + label_offset * sin(angle_rad)

        # Adjust the label position (you can offset the label if needed)
        label_x +=5  # Shift the label right by 5 units (modify this value to adjust)
        label_y -=5  # Shift the label up by 3 units (modify this value to adjust)
    
        label = Label()
        
        label.text = f"{sentiment_labels[i]} ({count})"
        label.fontName = 'Helvetica-Bold'
        label.fontSize = 12
        label.fillColor = HexColor("#FFFFFF")  # White text for visibility
        pie_chart.add(label)
# Add the pie chart to the drawing
    pie_chart.add(pie)


    # Draw the hole (center circle) for the doughnut effect
    hole_radius = 30 # Radius of the hole
    hole_x = pie.x + pie.width / 2
    hole_y = pie.y + pie.height / 2
    hole = Circle(hole_x, hole_y, hole_radius)
    hole.fillColor = HexColor("#FFFFFF")  # White color for the hole (to make it appear empty)

# Add the hole to the drawing (on top of the pie chart)
    pie_chart.add(hole)

# Draw the pie chart on the canvas
    pie_chart.drawOn(c, margin, box_y - 400)
# Create a legend for the pie chart
    legend_x = margin + 170  # Position the legend to the right of the pie chart
    legend_y = box_y - 300
    legend_height = 20  # Height for each legend item

# Define colors and labels for the legend
    legend_items = [
        ("C:/Users/SANTHIYA/Pictures/Screenshots/Screenshot 2024-12-26 171720.png", "Positive"),
        ("C:/Users/SANTHIYA/Pictures/Screenshots/Screenshot 2024-12-26 171744.png", "Neutral"),
        ("C:/Users/SANTHIYA/Pictures/Screenshots/Screenshot 2024-12-26 171805.png", "Negative"),
        ]

    c.setFont("Helvetica", 8)

    # Draw the legend
    for i, (emoji_path, label) in enumerate(legend_items):
        emoji_x = legend_x  # X position for the emoji
        emoji_y = legend_y - i * legend_height  # Y position for the emoji (adjusted for vertical alignment)
        c.drawImage(emoji_path, emoji_x, emoji_y, width=15, height=15, mask="auto")

    # Draw the label text
        text_x = legend_x + 20  # X position for the text (adjusted to be next to the emoji)
        text_y = emoji_y + 5  # Y position for the text (adjusted for vertical alignment)
        c.drawString(text_x, text_y, label)


    # Sentiment Analysis Table
    sentiment_table_data = [
        ["Sentiment", "Count"],
        ["Positive", sentiment['Positive']],
        ["Neutral", sentiment['Neutral']],
        ["Negative", sentiment['Negative']],
    ]

    # Sentiment Analysis Table
    sentiment_table = Table(sentiment_table_data, colWidths=[150, 100])
    sentiment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#494253")),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),  # Header text color
        ('TEXTCOLOR', (0, 1), (0, 1), HexColor("#00004d")), 
        ('TEXTCOLOR', (1, 1), (1, 1), HexColor("#00004d")),
        ('TEXTCOLOR', (0, 2), (0, 2), HexColor("#00004d")),
        ('TEXTCOLOR', (1, 2), (1, 2), HexColor("#00004d")), 
        ('TEXTCOLOR', (0, 3), (0, 3), HexColor("#00004d")), 
        ('TEXTCOLOR', (1, 3), (1, 3), HexColor("#00004d")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header
        ('BACKGROUND', (0, 2), (-1, -1), HexColor("#F5F5F5")),  # Default row background
        ('BACKGROUND', (0, 3), (-1, 3), HexColor("#FFFFFF")),  # Default row background
        ('BACKGROUND', (0, 4), (-1, 4), HexColor("#F5F5F5")),  # Alternate row background
        ('GRID', (0, 0), (-1, -1), 1, HexColor("#3b3c36")),  # Grid lines
        ('LEFTPADDING', (0, 0), (-1, -1), 10),  # Left padding    
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Right padding
        ]))
    sentiment_table.wrapOn(c, width, height)
    sentiment_table.drawOn(c, margin + 270, box_y - 330)


    # Performance Metrices view 
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(HexColor("#2E4053"))
    c.drawString(margin, box_y - 425, "Performance Metrics")

    # Performance Metrics: Horizontal Bar Chart
    performance = json_data['performance']
    performance_data = [
        performance['website_clicks'],
        performance['business_impressions']['desktop_search'],
        performance['business_impressions']['mobile_search'],
        performance['business_directions'],
        performance['call_clicks'],
        ]
    performance_labels = ["Website Clicks", "Desktop Search", "Mobile Search", "Directions", "     Call Clicks"]

    # Create a Drawing for the horizontal bar chart
    horizontal_bar_chart = Drawing(300, 150)
    x_start = 45
    y_start = 30
    bar_height = 15  # Reduced bar height for compact visualization
    bar_gap = 10

    # Assign distinct colors
    bar_colors = [
        HexColor("#FFDAB9"), 
        HexColor("#E6E6FA"),  
        HexColor("#32CD32"),  
        HexColor("#FF7F50"), 
        HexColor("#ADD8E6"),  
        ]
    label_x_position = 10

    # Draw bars manually
    for i, value in enumerate(performance_data):
        bar_width = value / 7  # Adjust scaling factor to reduce bar width
        bar_x = x_start
        bar_y = y_start + i * (bar_height + bar_gap)
        horizontal_bar_chart.add(Rect(bar_x, bar_y, bar_width, bar_height, fillColor=bar_colors[i]))
    # Add labels to the left of each bar
        label_x = bar_x - 10
        label_x_position = 10
        horizontal_bar_chart.add(String(label_x, bar_y + bar_height / 2, performance_labels[i], textAnchor="end"))
    # Add values at the end of each bar
        value_x = bar_x + bar_width + 10  
        horizontal_bar_chart.add(String(value_x, bar_y + bar_height / 2, str(value), textAnchor="start"))


# Add the horizontal bar chart to the canvas
    horizontal_bar_chart.drawOn(c, margin + 23, box_y - 600)
    # Performance Metrics Table
    performance_table_data = [
        ["Metric", "Value"],
        ["Call Clicks", performance['call_clicks']],
        ["Directions", performance['business_directions']],
        ["Mobile Search", performance['business_impressions']['mobile_search']],
        ["Desktop Search", performance['business_impressions']['desktop_search']],
        ["Website Clicks", performance['website_clicks']],
        
       
        
       
    ]

    # Performance Metrics Table
    performance_table = Table(performance_table_data, colWidths=[150, 100])
    performance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#494253")),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),  # Header text color
        ('TEXTCOLOR', (0, 1), (0, 1), HexColor("#00004d")), 
        ('TEXTCOLOR', (1, 1), (1, 1), HexColor("#00004d")),
        ('TEXTCOLOR', (0, 2), (0, 2), HexColor("#00004d")), 
        ('TEXTCOLOR', (1, 2), (1, 2), HexColor("#00004d")),
        ('TEXTCOLOR', (0, 3), (0, 3), HexColor("#00004d")), 
        ('TEXTCOLOR', (1, 3), (1, 3), HexColor("#00004d")),
        ('TEXTCOLOR', (0, 4), (0, 4), HexColor("#00004d")), 
        ('TEXTCOLOR', (1, 4), (1, 4), HexColor("#00004d")),
        ('TEXTCOLOR', (0, 5), (0, 5), HexColor("#00004d")), 
        ('TEXTCOLOR', (1, 5), (1, 5), HexColor("#00004d")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header
        ('BACKGROUND', (0, 1), (-1, 1), HexColor("#FFFFFF")),  # Default row background
        ('BACKGROUND', (0, 2), (-1, 2), HexColor("#F5F5F5")),  # Default row background
        ('BACKGROUND', (0, 3), (-1, 3), HexColor("#FFFFFF")),  # Default row background
        ('BACKGROUND', (0, 4), (-1, 4), HexColor("#F5F5F5")),  # Alternate row background
        ('BACKGROUND', (0, 5), (-1, 5), HexColor("#FFFFFF")),  # Default row background
        ('GRID', (0, 0), (-1, -1), 1, HexColor("#3b3c36")),  # Grid lines
        ('LEFTPADDING', (0, 0), (-1, -1), 10),  # Left padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Right padding
        ('TOPPADDING', (0, 0), (-1, -1), 5),  # Top padding for all cells
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),  # Bottom padding for all cells
        ]))
    performance_table.wrapOn(c, width, height)
    performance_table.drawOn(c, margin + 270, box_y - 570)

    # Footer with Page Number and Date
    c.setFont("Helvetica", 10)
    c.drawString(margin, 30, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawRightString(width - margin, 30, "Page 1")

    # Save PDF
    c.save()
    print(f"PDF report saved to: {output_pdf}")

# Load JSON and Generate Report
if os.path.exists(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    generate_enhanced_pdf(data, pdf_output)
else:
    print(f"Error: JSON file '{json_file}' not found.")