from bs4 import BeautifulSoup  # BeautifulSoup is used to parse and manipulate XML data
import re  # re (regular expressions) is used to match and find numerical values
import sys  # sys is used to handle command-line arguments


def scale_svg(input_file, output_file, scale_factor):
    """
    The function takes an input SVG file, scales it by the provided scale_factor,
    and writes the output to the output_file.
    """
    # Open the input SVG file and read its contents
    with open(input_file, 'r') as file:
        data = file.read()

    # Create a BeautifulSoup object and parse the data as XML
    soup = BeautifulSoup(data, 'xml')

    # List of attributes that need to be scaled
    attributes_to_scale = ["cx", "cy", "width", "height", "x", "y", "r"]

    # Compile a regular expression to find any kind of number
    number_regex = re.compile(r"-?\d+\.?\d*")

    # For each attribute, find all SVG elements with that attribute
    for attribute in attributes_to_scale:
        for tag in soup.find_all(attrs={attribute: number_regex}):
            # Scale the attribute value and update it
            original_value = float(tag[attribute])
            tag[attribute] = str(original_value * scale_factor)

    # Write the modified SVG data to the output file
    with open(output_file, 'w') as file:
        file.write(str(soup.prettify()))  # The prettify() method formats the data with indentation


# If the script is run directly (not imported as a module), the following code is executed
if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python3 script.py <input_file> <output_file> <scale_factor>")
        sys.exit(1)

    # Get the command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    scale_factor = float(sys.argv[3])  # Convert the scale factor from string to float

    # Call the scale_svg function with the command-line arguments
    scale_svg(input_file, output_file, scale_factor)
