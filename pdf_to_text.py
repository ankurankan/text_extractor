""" Extracts text from docx and pdf and writes to out.txt"""

import sys

def pdf_extract_text(path):
    import subprocess

    def extract_text(path):
        p = subprocess.Popen(['python','../pdfminer/tools/pdf2txt.py', path], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        while (True):
            retcode = p.poll()
            line = p.stdout.readline()
            yield line
            if (retcode is not None):
                break
    with open('out.txt', 'w') as out:
        for line in extract_text(path):
            out.write(line)

def docx_extract_text(path):
    import zipfile, re

    docx = zipfile.ZipFile(path)
    content = docx.read('word/document.xml')
    cleaned = re.sub('<(.|\n)*?>','',content)

    with open('out.txt', 'w') as out:
        out.write(cleaned)

def extract(path):
    file_type = path.split('.')[-1]
    if file_type == 'docx':
        docx_extract_text(path)
    elif file_type == 'pdf':
        pdf_extract_text(path)
    else:
        print("Unknown file type %s") %(file_type)
	sys.exit()

def usage():
    print 'Usage: ' + sys.argv[0] + 'path to docx or pdf file'
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()

    path = sys.argv[1]
    extract(path)
