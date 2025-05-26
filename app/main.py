from server.utils.text_processor import get_chapters, gutenberg_cleaner


if __name__ == '__main__':
    filepath = '../data/moby-dick.txt'
    output = gutenberg_cleaner(filepath)
    print(output)            
