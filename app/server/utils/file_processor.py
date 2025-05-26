import mimetypes
import os
import filetype

def detect_mime_type(file_path):
    if not os.path.exists(file_path):
        return None
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type == None:
        kind = filetype.guess(file_path)
        mime_type = kind.mime
    return mime_type


if __name__ == '__main__':
    f_type = detect_mime_type('../../../data/dellnlp-wp.pdf')
    print(f_type)
    f_type = detect_mime_type('../../../data/dellnlp.nothing')
    print(f_type)    
    f_type = detect_mime_type('../../../data/moby-dick.epub')
    print(f_type)        
    f_type = detect_mime_type('../../../data/moby-dick.txt')
    print(f_type)            