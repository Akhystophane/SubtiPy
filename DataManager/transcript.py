def extract_text_from_srt(srt_file_path, output_txt_path):
    """
    Extracts the text from an SRT file and writes it to a text file in a single paragraph.

    :param srt_file_path: Path to the SRT file
    :param output_txt_path: Path to the output text file
    """
    try:
        # Reading the SRT file
        with open(srt_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Extracting the text from each subtitle
        subtitles_text = []
        for line in lines:
            # Skipping lines with timestamps or empty lines
            if '-->' in line or line.strip().isdigit() or line.strip() == '':
                continue
            subtitles_text.append(line.strip())

        # Writing the extracted text to the output TXT file as a single paragraph
        with open(output_txt_path, 'w', encoding='utf-8') as file:
            file.write(' '.join(subtitles_text))

        return f"Subtitles text has been successfully extracted to {output_txt_path}"
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
srt_file_path = '/Users/emmanuellandau/Documents/EditLab/TODO/entretiens/audio.srt'  # Replace with the path to your SRT file
output_txt_path = '/Users/emmanuellandau/Documents/EditLab/TODO/entretiens/trasncript.txt'  # Replace with your desired output path

# Note: This is an example. The paths need to be replaced with actual file paths.
extract_text_from_srt(srt_file_path, output_txt_path)
