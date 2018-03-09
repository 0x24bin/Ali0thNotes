import gzip

TEMP_PATH = r"C:/Users/muhe/Desktop/"

def untar(fname, dirs):
    f = gzip.open(fname, 'r')
    print(f.filename)
    file_content = f.read()
    print(file_content)
    f.close()


if __name__ == "__main__":
    untar(TEMP_PATH + "pt.rules.tar.gz", TEMP_PATH)