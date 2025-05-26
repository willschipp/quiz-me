##
# Orchestrates immediate next steps when a file is uploaded
# - processes mimetype
# - extracts text
# - asks LLM about the text
# - creates question bank and chapter context
##

from server.utils.file_processor import detect_mime_type
from server.utils.text_processor import extract_text_images, extract_chapters_from_epub, get_chapters

token_size = 1000 # 4,000 tokens per 'chunk'

#function to determine mimetype
def flow(file_location,target_location='../../../data/'):
    # determine the mimetype
    mimetype = detect_mime_type(file_location)
    # holders
    chapters = []
    # switch based on mimetype to break down the file
    if 'pdf' in mimetype:
        # process as a pdf
        extract_text_images(file_location,target_location)
        # now need to process which parts are actually chapters
    elif 'epub' in mimetype:
        # get the chapters from the epub
        chapters = extract_chapters_from_epub(file_location)
    elif 'text/plain' in mimetype:
        # ordinary text --> chunk and check
        chapters = get_chapters(file_location,token_size)