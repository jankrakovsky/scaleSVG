# Import required libraries
from bs4 import BeautifulSoup  # For parsing the XML (SVG is XML-based)
import re  # Regular expressions for finding numbers in strings
import sys  # To access command-line arguments

# Function to scale an SVG file
def scale_svg(input_file, output_file, scale_factor):
    # Open the input SVG file and read its contents
    with open(input_file, 'r') as file:
        data = file.read()

    # Parse the SVG XML
    soup = BeautifulSoup(data, 'xml')

    # List of SVG tag attributes that may need to be scaled
    attributes_to_scale = ["cx", "cy", "width", "height", "x", "y", "r"]
    
    # Regex pattern to match a number (integer or decimal)
    number_regex = re.compile(r"-?\d+\.?\d*")

    # For each attribute that we may need to scale
    for attribute in attributes_to_scale:
        # Find all SVG tags that have that attribute and a number as its value
        for tag in soup.find_all(attrs={attribute: number_regex}):
            # Get the original value of the attribute and convert it to float
            original_value = float(tag[attribute])
            # Multiply it by the scale factor and update the attribute in the SVG
            tag[attribute] = str(original_value * scale_factor)

    # The viewBox attribute needs special handling as it's a space-separated list of numbers
    svg_tag = soup.svg
    if 'viewBox' in svg_tag.attrs:
        # Convert the viewBox attribute value to a list of floats
        values = list(map(float, svg_tag['viewBox'].split()))
        # Scale the width and height values
        values[2] *= scale_factor  # Scaling width
        values[3] *= scale_factor  # Scaling height
        # Convert the values back to a string and update the viewBox attribute
        svg_tag['viewBox'] = ' '.join(map(str, values))

    # Write the modified SVG XML to the output file
    with open(output_file, 'w') as file:
        file.write(str(soup.prettify()))

# If this script is run from the command line
if __name__ == "__main__":
    # Check that we have exactly three command-line arguments
    if len(sys.argv) != 4:
        # If not, print the usage message and exit with an error status
        print("Usage: python3 script.py <input_file> <output_file> <scale_factor>")
        sys.exit(1)

    # Parse the command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    scale_factor = float(sys.argv[3])

    # Call the function to scale the SVG
    scale_svg(input_file, output_file, scale_factor)
