from tkinter import *
from tkinter import messagebox

class InputVideo:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Viewer")
        self.root.resizable(False, False)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - 480) // 2
        y_position = (screen_height - 340) // 2
        self.root.geometry(f"480x340+{x_position}+{y_position}")

        self.root.resizable(False, False)

        self.cam_labels = ["Camera 1", "Camera 2", "Camera 3", "Camera 4", "Camera 5"]
        self.entry_variables = [StringVar() for _ in range(5)]

        self.title_box()

    def title_box(self):
        label_judul_frame = Label(self.root, text="Ground Control System\nConfiguration", font=("Consolas", 12))
        label_judul_frame.pack(pady=5)

        for i, cam_label in enumerate(self.cam_labels):
            label = Label(self.root, text=cam_label, font=("consolas", 12))
            label.place(x=10, y=60 + 30 * i)

            entry = Entry(self.root, textvariable=self.entry_variables[i], width=40, font=("consolas", 11))
            entry.place(x=90, y=65 + 30 * i)

        submit_button = Button(self.root, text="Submit", command=self.show_main_frame)
        submit_button.place(x=200, y=220)

    def show_main_frame(self):
        try:
            cam_values = [int(entry.get()) for entry in self.entry_variables]
            self.root.destroy()  # Close the InputVideo window
            main_frame = MainFrame(cam_values)
            main_frame.run()
        except ValueError:
            # Handle the case where non-integer values are entered
            messagebox.showerror("Error", "Please enter valid integer values for cameras.")

class MainFrame:
    def __init__(self, input_video_data):
        self.cam1, self.cam2, self.cam3, self.cam4, self.cam5 = input_video_data

    def show_values(self):
        print(f"Camera 1: {self.cam1} (type: {type(self.cam1)})")
        print(f"Camera 2: {self.cam2} (type: {type(self.cam2)})")
        print(f"Camera 3: {self.cam3} (type: {type(self.cam3)})")
        print(f"Camera 4: {self.cam4} (type: {type(self.cam4)})")
        print(f"Camera 5: {self.cam5} (type: {type(self.cam5)})")

    def run(self):
        root = Tk()
        root.title("Main Frame")
        root.geometry("300x200")

        label = Label(root, text="Main Frame", font=("Consolas", 12))
        label.pack(pady=10)

        self.show_values()

        root.mainloop()

def run_input_video():
    root = Tk()
    input_video = InputVideo(root)
    root.mainloop()

if __name__ == "__main__":
    run_input_video()
