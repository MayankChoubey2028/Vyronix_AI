class SceneMemory:

    def __init__(self):

        self.objects = set()

        self.last_text = ""


    def update_objects(self, detected_objects):

        self.objects.update(detected_objects)


    def update_text(self, text):

        self.last_text = text


    def get_scene(self):

        return {
            "objects": list(self.objects),
            "text": self.last_text
        }


    def clear(self):

        self.objects.clear()
        self.last_text = ""