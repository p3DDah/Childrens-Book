import re
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extract_chapter_text(response, check):
    patterns = [
        r'Chapter\s+[\w\s]+:\s*([^\n]+)',  # Standard format: "Chapter X: Title"
        r'CHAPTER\s*([^\n]+)',  # All caps: "CHAPTER Title"
        r'Chap\.\s*(\d+)\s*-\s*([^\n]+)',  # Abbreviated with number: "Chap. X - Title"
        r'Titel:\s*([^\n]+)'  # Matches "Titel: Title"
        r'\b(\d+)\.\s*([^\n]+)',  # Simple numeric: "X. Title"
        r'(\w+)\s+Chapter\s*-\s*([^\n]+)',  # Word before chapter: "Word Chapter - Title"
        r'(\d+)\s*:\s*([^\n]+)',  # Numeric colon: "X: Title"
        r'\*\*\s*Chapter\s+(\d+)\s*\*\*\s*([^\n]+)',  # Bold markdown: "** Chapter X ** Title"
        r'\[\s*Chapter\s+(\d+)\s*\]\s*([^\n]+)',  # Square brackets: "[ Chapter X ] Title"
        r'--\s*Chapter\s+(\d+)\s*--\s*([^\n]+)',  # Dashes: "-- Chapter X -- Title"
        r'(\w+)\s+Chapter\s*(\d+)\s*:\s*([^\n]+)',  # Word, chapter, number: "Word Chapter X: Title"
    ]

    # Searching for the pattern in the text
    match = re.search(patterns[check], response, re.IGNORECASE)

    if match:
        # Extracting the title
        chapter_title = match.group(1).strip()

        # Splitting the text at the chapter heading
        parts = re.split(patterns[check], response, maxsplit=1, flags=re.IGNORECASE)

        if len(parts) > 1:
            # The rest of the text will be the second part after splitting
            chapter_text = parts[2].lstrip()
        else:
            chapter_text = response

        return chapter_title, chapter_text

    return "No chapter title found", response

# Function to validate the extracted options
def is_valid_option(option):
        return bool(option['Title'].strip()) and bool(option['Text'].strip())    
    
def extract_decisions(response, check):
    # Define a list of regular expression patterns to try
    patterns = [
        r'\d+\)\s+(.*?):\s+(.*?)(?=\n\d+\)|\Z)',  # Numbered Options with Colon Separator
        r'Option\s+\d+\s+\((.*?)\):\s+(.*?)(?=\nOption|\Z)',  # Labeled Options with Brackets
        r'-\s+(.*?):\s+(.*?)(?=\n-|\Z)',  # Sequential Bullets with Dash Separator
        r'[A-Z]\)\s+(.*?):\s+(.*?)(?=\n[A-Z]\)|\Z)',  # Alphabetic Labels with Period Separator
        r'Decision\s+\d+:\s+(.*?)(?=\nDecision\s+\d+|\Z)',  # Numbered with 'Decision' Prefix
        r'\d+\.\s+(.*?)(?=\n\d+\.|\Z)',  # Simple Numbered List
        r'Q:\s*(.*?)\s*A:\s*(.*?)(?=\nQ:|\Z)',  # Question-Answer Format
        r'\*\s+(.*?)\s+-\s+(.*?)(?=\n\*|\Z)',  # Bullet Points with Emphasis on Title
        r'\*\*(.*?)\*\*\s+(.*?)(?=\n\*\*|\Z)'  # Title in Bold Followed by Text
        r'Choice\s+\d+:\s+(.*?)(?=\nChoice\s+\d+|\Z)'  # Numbered with 'Choice' Keyword
    ]

    matches = re.findall(patterns[check], response, re.DOTALL)
    options = {f'Option {i}': {'Title': title.strip(), 'Text': text.strip()} 
                for i, (title, text) in enumerate(matches, 1)}

    # Check if all options are valid
    if all(is_valid_option(option) for option in options.values()):
        return options

    return {}  # Return an empty dictionary if no patterns match or if validation fails


def ordinal(number):
    """Convert an integer into its ordinal representation."""
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
    return str(number) + suffix

def check_GPU():
    print(torch.cuda.is_available())
    print(torch.cuda.device_count())
    print(torch.cuda.current_device())
    print(torch.cuda.device(0))
    print(torch.cuda.get_device_name(0))
    print(torch.version.cuda)

    # Check if CUDA is available
    if torch.cuda.is_available():
        # Get the number of GPUs available
        num_gpus = torch.cuda.device_count()

        for i in range(num_gpus):
            print(f"GPU {i}:")
            gpu_properties = torch.cuda.get_device_properties(i)

            # Total memory
            total_memory = gpu_properties.total_memory / 1024**2  # Convert to MB
            print(f"  Total Memory: {total_memory:.2f} MB")

            # Current memory usage
            allocated_memory = torch.cuda.memory_allocated(i) / 1024**2  # Convert to MB
            print(f"  Allocated Memory: {allocated_memory:.2f} MB")

            # Cached memory
            cached_memory = torch.cuda.memory_reserved(i) / 1024**2  # Convert to MB
            print(f"  Cached Memory: {cached_memory:.2f} MB")

            print("--------------------------------------------------")
    else:
        print("CUDA is not available. No GPU detected.")

    print(torch.tensor([1.0, 2.0], device='cuda'))
    
def translate_decisions(decisions, TL, to_code):
    """
    Translates the titles and texts of each decision in the decisions dictionary.

    :param decisions: Dictionary of decisions to translate.
    :param translate_function: Function to use for translation.
    :param to_code: Target language code for translation.
    :return: Translated decisions dictionary.
    """
    translated_decisions = {}
    for key, value in decisions.items():
        translated_title = TL(value['Title'], to_code=to_code)
        translated_text = TL(value['Text'], to_code=to_code)
        translated_decisions[key] = {'Title': translated_title, 'Text': translated_text}

    return translated_decisions

def find_best_matching_mood(llm_response, predefined_moods):
    # Combine the response with the list of moods
    documents = [llm_response] + list(predefined_moods)

    # Create the TF-IDF model
    tfidf = TfidfVectorizer().fit_transform(documents)

    # Calculate cosine similarity between the response and each mood
    cosine_similarities = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten() # type: ignore

    # Find the index of the highest scoring mood
    best_mood_idx = np.argmax(cosine_similarities)

    return list(predefined_moods)[best_mood_idx]

def get_mood_from_path(song_path, predefined_songs):
    for mood, path in predefined_songs.items():
        if path in song_path:
            return mood
    return None

# Function to generate a prompt for evaluating chapter title extraction
def generate_story_prompt(original_text, chapter_title, text):
    return (
        "Evaluate the following text for chapter title extraction. "
        "The exact title should be present, separated from the main text and any prefix like 'Chapter 1:'. "
        "The extracted text should only consists of the original text, if theres more or less text (except the title suffix in the same line) then answer False"
        "Respond with True if the title extraction meets these criteria, otherwise False.\n\n"
        f"Original Text: {original_text}\n\n"
        f"Extracted Chapter Title: {chapter_title}\nExtracted Text: {text}"
    )

# Function to generate a prompt for evaluating decision title extraction
def generate_decision_prompt(original_text, decisions):
    formatted_decisions = '\n'.join(
        f"Option {i}: Title - '{decision['Title']}', Text - '{decision['Text']}'" 
        for i, decision in decisions.items()
    )
    return (
        "Evaluate the following text for decision title extraction. "
        "Each decision's title should be exactly to its text, and well-separated from any prefixes. "
        "The extracted text should only consists of the original text, if theres more or less text (except the title suffix in the same line) then answer False"
        "Respond with True if all decision title extractions meet these criteria, otherwise False.\n\n"
        f"Original Text: {original_text}\n\n"
        f"Extracted Decisions:\n{formatted_decisions}"
    )