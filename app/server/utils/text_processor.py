# break down a text into 'chapters'
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader, PdfWriter
import os
import fitz  # PyMuPDF

from server.service.llm_text_processor import send_prompt

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

def get_first_chunk(text_path,token_size):
    chunk_size = token_size * 4
    file_content = ''
    with open(text_path,'r') as file:
        while True:
            chunk = file.read(chunk_size)
            file_content += chunk
            break
    return file_content

def get_page(text_path,token_size,page=0):
    chunk_size = token_size * 4
    file_content = ''
    counter = 0
    with open(text_path,'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if counter == page:
                file_content += chunk
                break
            else:
                counter += 1
    return file_content, page

# prompt_chapter = 'You are an expert librarian. Read the following text, identify the first sentence of the first chapter, and return only it.  If the text does not contain the first sentence, answer with only "First Sentence Not Found" Text = TEXT'
prompt_chapter = 'You are an expert librarian. Read the following text and identify the chapter starter marker based on the first sentence after it.  If the chapter starter marker is found, return only the chapter starter marker.  If the text does not contain the chapter start marker, answer with only "Chapter Start Not Found" Text = TEXT'

def get_chapters(text_path,token_size):
    # build a set of chapters from a plain text file
    # loop and extract starter of a chapter and then
    # break down further
    have_starting_chapter = False
    starter = None
    while have_starting_chapter == False:
        page = 0
        print(f"getting page no. {page}")
        chunk, page = get_page(text_path,token_size,page)    
        # invoke and validate
        prompt = prompt_chapter.replace('TEXT',chunk)
        response = send_prompt(prompt)
        # get the text
        result = response.text
        if 'Chapter Start Not Found' not in result:
            # got the first break for the chapter
            starter = result
            have_starting_chapter = True
        # now move on
    # now we have the starter, we need to find it in the corpus of the whole text
    print(f"chapter starter is: {starter}")


def gutenberg_cleaner(text_path):
    start_string = "*** START OF THE PROJECT GUTENBERG EBOOK "
    end_string = "*** END OF THE PROJECT GUTENBERG EBOOK "
    line_end = "***"
    chunk_size = 4096 # it's in the beginning of the book
    is_gutenberg = False
    # read an input file and create a new copy IF it has a gutenberg starter
    with open(text_path,'r') as file:
        chunk = file.read(chunk_size)
        if start_string in chunk:
            is_gutenberg = True
    if is_gutenberg:
        # read it into RAM
        with open(text_path,'r') as file:
            corpus = file.read()
            # trim the first and last
            start_start_index = corpus.find(start_string)
            start_end_index = corpus.find(line_end,start_start_index+1)
            start_end_index += len(line_end)
            # use the start_end_index to 'start' the trim
            corpus = corpus[start_end_index:]
            # now get the end
            end_start_index = corpus.find(end_string)
            corpus = corpus[:end_start_index]
        # write the corpus out
        output_path = text_path + ".trim"
        with open(output_path,'w+') as file:
            file.write(corpus)
        return output_path
    else:
        return text_path



def split_pdf(pdf_path, output_dir=None):
    """Splits a PDF file into individual pages.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_dir (str, optional): Path to the directory where the output files will be saved. 
                                    If None, the output files will be saved in the same directory as the input file.
    """
    if output_dir is None:
       output_dir = os.path.dirname(pdf_path)
    
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])

            output_filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{page_num + 1}.pdf"
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)        



def extract_text_images(pdf_path, output_folder="output"):
    pdf_document = fitz.open(pdf_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]

        # Extract text
        text = page.get_text()
        with open(f"page_{page_num + 1}.txt", "w", encoding="utf-8") as text_file:
            text_file.write(text)

        # Extract images
        image_list = page.get_images(full=True)
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            with open(f"page_{page_num + 1}_img_{img_index}.{image_ext}", "wb") as image_file:
                image_file.write(image_bytes)


# if __name__ == '__main__':
    # filepath = '../../data/anne-of-green-gables.txt'
    # filepath = '../../data/moby-dick.txt'
    # chunk, page = get_page(filepath,1000)
    # page += 1
    # chunk,page = get_page(filepath,1000,page)
    # get_chapters(filepath,1000)

    # epub_filepath = '../../data/moby-dick.epub'  # test epub
    # extracted_chapters = extract_chapters_from_epub(epub_filepath)

    # for i, chapter in enumerate(extracted_chapters):
    #     print(f"Chapter {len(chapter)} chars : {len(chapter) / 4} tokens")
    #     # print(f"Chapter {i+1}:\n{chapter}\n{'-'*50}\n")
    # filepath = '../../data/dellnlp-wp.pdf'
    # split_pdf(filepath,'../../data/')
    # extract_text_images(filepath,'../../data/')
