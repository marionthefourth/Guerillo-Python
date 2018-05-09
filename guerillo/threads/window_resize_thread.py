from threading import Thread


class WindowResizeThread(Thread):

    def __init__(self, root, direction, size):
        super().__init__()
        self.root = root
        self.direction = direction
        self.size = size

    def run(self):
        if self.direction.lower() == "expand":
            self.window_width = int(self.root.geometry().split("+")[0].split("x")[0])
            self.window_height = int(self.root.geometry().split("+")[0].split("x")[1])
            while self.window_width < self.size:
                self.root.geometry(str(self.window_width + 3) + "x" + str(self.window_height + 5))
                self.root.update()
                self.window_width = int(self.root.geometry().split("+")[0].split("x")[0])
                self.window_height = int(self.root.geometry().split("+")[0].split("x")[1])
        elif self.direction.lower() == "contract":
            self.window_width = int(self.root.geometry().split("+")[0].split("x")[0])
            self.window_height = int(self.root.geometry().split("+")[0].split("x")[1])
            while self.window_width > self.size:
                self.root.geometry(str(self.window_width - 3) + "x" + str(self.window_height - 5))
                self.root.update()
                self.window_width = int(self.root.geometry().split("+")[0].split("x")[0])
                self.window_height = int(self.root.geometry().split("+")[0].split("x")[1])