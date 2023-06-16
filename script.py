from bs4 import BeautifulSoup  # For parsing the XML (SVG is XML-based)
import re  # Regular expressions for finding numbers in strings
import sys  # To access command-line arguments


# Function to get rid of zero after the decimal point
def convert_non_decimal_floats_to_integer(number):
    if number.is_integer():
        return int(number)
    else:
        return number


# Function to scale the values in SVG tag attributes
def scale_attributes(soup, attributes, scale_factor):
    # Regex pattern to match a number (integer or decimal)
    number_pattern = re.compile(r"-?\d+\.?\d*")

    # For each attribute that we may need to scale
    for attribute in attributes:
        # Find all SVG tags that have that attribute and a number as its value
        for tag in soup.find_all(attrs={attribute: number_pattern}):
            # Get the original value of the attribute and convert it to float
            original_value = float(tag[attribute])
            # Multiply it by the scale factor and update the attribute in the SVG
            new_value = original_value * scale_factor
            # Convert the value to a string and update the attribute
            tag[attribute] = convert_non_decimal_floats_to_integer(new_value)


# Function to scale the coordinates in a path data string
def scale_path_data(path_data, scale_factor):
    # Regex pattern to match numbers in the path data string
    number_pattern = re.compile(r"-?\d+\.?\d*")

    # Find all numbers in the path data
    numbers = re.findall(number_pattern, path_data)

    for i in range(len(numbers)):
        # Scale each number by multiplying it with the scale factor
        scaled_number = float(numbers[i]) * scale_factor
        # Update the path data string
        numbers[i] = convert_non_decimal_floats_to_integer(scaled_number)

    # Replace the original numbers with the scaled numbers in the path data
    scaled_path_data = number_pattern.sub(lambda m: str(numbers.pop(0)), path_data)

    return scaled_path_data


# Function to scale the paths in the SVG file
def scale_paths(soup, scale_factor):
    # Find all path tags in the SVG
    for path_tag in soup.find_all("path"):
        # Get the original path data and scale it
        original_path_data = path_tag.get("d")
        scaled_path_data = scale_path_data(original_path_data, scale_factor)
        # Update the path data attribute with the scaled data
        path_tag["d"] = scaled_path_data


# Function to scale the font size of the text elements
def scale_text_font_size(soup, scale_factor):
    # Find all text tags in the SVG
    for text_tag in soup.find_all("text"):
        # Get the original font size and convert it to float
        original_font_size = float(text_tag.get("font-size"))
        # Multiply it by the scale factor and update the font-size attribute
        new_font_size = original_font_size * scale_factor
        # Convert the font size to a string and update the attribute
        text_tag["font-size"] = convert_non_decimal_floats_to_integer(new_font_size)


def scale_viewbox(soup, scale_factor):
    # Find the SVG root tag
    svg_tag = soup.find("svg")

    # Check if viewBox attribute exists
    if 'viewBox' in svg_tag.attrs:
        # Get the original viewBox values
        original_viewbox = svg_tag.get('viewBox')

        # Split into individual values and convert to float
        values = list(map(float, original_viewbox.split()))

        # Scale the width and height
        values[2] = round(values[2] * scale_factor, 2)  # width
        values[3] = round(values[3] * scale_factor, 2)  # height

        # Convert the values back to string and join
        new_viewbox = ' '.join(map(str, values))

        # Update the viewBox attribute with the new values
        svg_tag['viewBox'] = new_viewbox


# Function to scale an SVG file
def scale_svg(input_file, output_file, scale_factor):
    # Open the input SVG file and read its contents
    with open(input_file, 'r') as file:
        data = file.read()

    # Parse the SVG XML
    soup = BeautifulSoup(data, 'xml')

    # List of SVG tag attributes that may need to be scaled
    attributes_to_scale = ["cx", "cy", "width", "height", "x", "y", "r"]

    # Scale the values in attributes
    scale_attributes(soup, attributes_to_scale, scale_factor)

    # Scale the paths in the SVG file
    scale_paths(soup, scale_factor)

    # Scale the font size of the text elements
    scale_text_font_size(soup, scale_factor)

    # Scale the viewBox of the SVG
    scale_viewbox(soup, scale_factor)

    # Write the modified SVG XML to the output file
    with open(output_file, 'w') as file:
        file.write(str(soup.prettify()))


# Main code execution starts here
if __name__ == '__main__':
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        # If not, print the usage message and exit with an error status
        print("Usage: python3 script.py <input_file> <output_file> <scale_factor>")
        sys.exit(1)

    # Parse the command-line arguments
    arg_input_file = sys.argv[1]
    arg_output_file = sys.argv[2]
    arg_scale_factor = float(sys.argv[3])

    # Call the function to scale the SVG
    scale_svg(arg_input_file, arg_output_file, arg_scale_factor)
