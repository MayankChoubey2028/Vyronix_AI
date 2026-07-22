import easyocr


class OCRReader:

    def __init__(self):

        self.reader = easyocr.Reader(['en'])


    def extract_text(self, frame):

        results = self.reader.readtext(frame)

        text = []

        for item in results:

            text.append(item[1])

        return " ".join(text)