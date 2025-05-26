# break down a text into 'chapters'
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

start_string = '*** START OF THE PROJECT GUTENBERG EBOOK'
end_string = '*** END OF THE PROJECT GUTENBERG EBOOK'

def extract_chapters_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        text = soup.get_text()
        chapters.append(text)
    return chapters


# process from a straight text block
def extract_chapters_from_text(text_path,start_text,end_text):
    chunk_size = 4096
    file_content = ''
    # read the file in
    with open(text_path,'r') as file:
        adding = False
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            if start_text in chunk:
                # have the start --> start adding
                adding = True
            if end_text in chunk:
                adding = False
                break #finished
            if adding:
                file_content += chunk
    # now we have a huge text chunk
    # need to break down by chapters
            
        


if __name__ == '__main__':
    epub_filepath = '../../data/moby-dick.epub'  # test epub
    extracted_chapters = extract_chapters_from_epub(epub_filepath)

    for i, chapter in enumerate(extracted_chapters):
        print(f"Chapter {len(chapter)} chars : {len(chapter) / 4} tokens")
        # print(f"Chapter {i+1}:\n{chapter}\n{'-'*50}\n")
