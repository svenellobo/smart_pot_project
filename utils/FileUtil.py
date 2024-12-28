from PIL import Image, ImageTk

class FileUtil:

    @staticmethod
    def convertToBinaryData(filename):
        with open(filename, 'rb') as file:
            picture = file.read()
        return picture


    @staticmethod
    def write_file(data, filename):
        with open(filename, 'wb') as file:
            file.write(data)

    @staticmethod
    def resize_picture(pic, width, height):
        resized = pic.resize((width, height))
        return resized

    @staticmethod
    def work_on_img(pic, width, height):
        try:
            img = Image.open(pic)
            resized = img.resize((width, height))
            finished_img = ImageTk.PhotoImage(resized)
            return finished_img
        except:
            pass
