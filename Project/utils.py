import re

def extract_chapter_text(response):
    chapter_pattern = r'Chapter\s+[\w\s]+:\s*([^\n]+)'

    # Searching for the pattern in the text
    match = re.search(chapter_pattern, response, re.IGNORECASE)
    
    # Extracting the title
    if match:
        # The title is captured in the first group of the pattern
        chapter_title = match.group(1)
    else:
        chapter_title = "No chapter title found"

    # Splitting the text at the chapter heading
    parts = re.split(chapter_pattern, response, maxsplit=1)

    # The rest of the text will be the second part after splitting, if the pattern is found
    if len(parts) > 1:
        # Strip leading and trailing whitespaces and newlines
        return chapter_title, parts[2].lstrip()
    else:
        return chapter_title, response
    
    
def extract_decisions(response):
    # Regular expression pattern to match the option format
    option_pattern = r'Option\s+\d+\s+\((.*?)\):\s+(.*?)(?=\nOption|\Z)'
    
    # Find all matches in the text
    matches = re.findall(option_pattern, response, re.DOTALL)
    
    # Creating a dictionary to hold the extracted options
    options = {}
    for i, match in enumerate(matches, 1):
        title, option_text = match
        options[f'Option {i}'] = {'Title': title, 'Text': option_text.strip()}

    return options


def ordinal(number):
    """Convert an integer into its ordinal representation."""
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
    return str(number) + suffix