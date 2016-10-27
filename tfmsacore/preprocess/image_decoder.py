import tarfile


class ImageDecoder:
    def __init__(self):
        print("!!")

    def decode_tar_file(self, path, file):
        file_path = "{0}/{1}".format(path, file)
        extract_path = "{0}/{1}".format(path, "extrat")
        tar = tarfile.open(file_path)
        tar.extractall(extract_path)


