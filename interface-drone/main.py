import tkinter as tk
from tkinter import Canvas, filedialog
from PIL import Image, ImageTk
import cv2
import time

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')
        self.root.title("GCS Drone")

        self.video_source = tk.StringVar()
        self.dest_folder = tk.StringVar()
        self.label_var = tk.StringVar()

        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        self.view_page = ViewPage(self)
        self.setup_page = SetupPage(self, self.view_page)
        self.about_page = AboutPage(self)

        self.current_page = None

        pages = {"Setup": self.setup_page, "View": self.view_page, "About": self.about_page}
        for page_name, page_instance in pages.items():
            menu_bar.add_command(label=page_name, command=lambda page=page_instance: self.show_page(page))

        #default initial page --> setup
        self.show_page(self.setup_page)
        self.view_page.hide()
        self.about_page.hide()

    def show_page(self, page):
        if self.current_page:
            self.current_page.hide()
        self.current_page = page
        self.current_page.show()

class SetupPage:
    def __init__(self, app, view_page):
        self.app = app
        self.view_page = view_page
        self.frame = tk.Frame(app.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        video_source_frame = tk.Frame(self.frame, padx=20, pady=10)
        video_source_frame.grid(row=0, column=0, sticky='w', columnspan=3)

        tk.Label(video_source_frame, text="Video Source:").grid(row=0, column=0)
        tk.Entry(video_source_frame, textvariable=app.video_source, width=50).grid(row=0, column=1, padx=38)

        dest_folder_frame = tk.Frame(self.frame, padx=20, pady=10)
        dest_folder_frame.grid(row=1, column=0, sticky='w', columnspan=3)

        tk.Label(dest_folder_frame, text="Destination Folder:").grid(row=1, column=0)
        tk.Entry(dest_folder_frame, textvariable=app.dest_folder, width=50).grid(row=1, column=1, padx=10)
        tk.Button(dest_folder_frame, text="Browse", command=self.browse_destination_folder).grid(row=1, column=2)

        tk.Button(self.frame, text="Start Stream", command=self.start_stream).grid(row=2, column=0, sticky='news', padx=20, pady=20, columnspan=3)

    def browse_destination_folder(self):
        folder_path = filedialog.askdirectory()
        self.app.dest_folder.set(folder_path)
        self.view_page.save_path = folder_path

    def start_stream(self):
        #release previous vid capture
        if hasattr(self.app, 'cap'):
            self.app.cap.release()

        #set new vid source
        source = self.app.video_source.get()
        
        if 'rtsp://' not in source:
            source = int(self.app.video_source.get())

        self.app.cap = cv2.VideoCapture(source)
        
        if isinstance(source, int):
            self.app.video_width = int(self.app.cap.get(cv2.CAP_PROP_FRAME_WIDTH)+490)
        else: 
            self.app.video_width = int(self.app.cap.get(cv2.CAP_PROP_FRAME_WIDTH)-144)
            
        self.app.video_height = int(self.app.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.app.target_height = int((9 / 16) * self.app.video_width)

        #self.view_page.update_video()

        timestamp = time.strftime("%Y%m%d%H%M%S")
        filename = f"labels_{timestamp}"
        self.view_page.label_file = filename

    def hide(self):
        self.frame.pack_forget()

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

class ViewPage:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame)
        self.label.grid(row=0, column=0, pady=10, sticky="news")

        self.save_button = tk.Button(self.frame, text="Save Frame", font=('arial 12'), height=2, command=self.save_frame)
        self.save_button.grid(row=2, column=1, pady=10, padx=10)

        self.label_var = tk.StringVar(self.frame)
        self.label_var.set("Normal")
        self.label_dropdown = tk.OptionMenu(self.frame, self.label_var, "Normal", "Damaged")
        self.label_dropdown.config(font=('arial 12'))
        self.label_dropdown.grid(row=2, column=0, pady=10, padx=10, sticky="news")

        self.save_path_var = tk.StringVar(self.frame)
        self.label_file = tk.StringVar()

        # Streaming status
        self.streaming_label = tk.Label(self.frame, text="Streaming Status: Stopped", fg="red", font=('arial 10'))
        self.streaming_label.grid(row=1, column=0, pady=10, padx=10, sticky="news")

        self.stream_button = tk.Button(self.frame, text="Start Stream", font=('arial 12'), height=2, command=self.toggle_stream)
        self.stream_button.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="news")

        self.is_streaming = False  # Flag track streaming status
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

    def toggle_stream(self):
        if self.is_streaming:
            self.stop_stream()
        else:
            self.start_stream()

    def start_stream(self):
        self.is_streaming = True
        self.stream_button.config(text="Stop Stream")
        self.streaming_label.config(text="Streaming Status: Started", fg="green", font=('arial 10'))

        self.update_video()

    def stop_stream(self):
        self.is_streaming = False
        self.stream_button.config(text="Start Stream")
        self.streaming_label.config(text="Streaming Status: Stopped", fg="red", font=('arial 10'))

    def update_video(self):
        if self.is_streaming:
            ret, frame = self.app.cap.read()
            if ret:
                frame = cv2.resize(frame, (self.app.video_width, self.app.target_height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(img)
                self.label.img = img
                self.label.config(image=img)
                self.label.after(10, self.update_video)

    def save_frame(self):
        if self.is_streaming:
            frame = self.app.cap.read()[1]
            label = self.label_var.get()
            save_path = self.save_path
            label_file = self.label_file

            timestamp = time.strftime("%Y%m%d%H%M%S")
            filename = f"{label}_{timestamp}_frame.jpg"

            cv2.imwrite(f"{save_path}/{filename}", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            with open(f"{save_path}/{label_file}.txt", "a") as label_file:
                label_file.write(f"{filename} {label}\n")

    def hide(self):
        self.frame.pack_forget()

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

class AboutPage:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(self.app.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # about text + logo
        tk.Label(self.frame, text="Ground Control Station - Drone", font=('Arial 16 bold')).grid(row=0, column=0, sticky="news", columnspan=3, pady=10)
        tk.Label(self.frame, text="in collaboration with", font=('arial 12')).grid(row=1, column=0, columnspan=3)

        # about: image 
        image_paths = ["about/BINUS.png", "about/ITB.png", "about/TerraDrone.png"]
        self.tk_images = []

        for i, image in enumerate(image_paths):
            original_image = Image.open(image)
            resized_image = original_image.resize((200, 200), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(resized_image)
            self.tk_images.append(tk_image)
            tk.Label(self.frame, image=tk_image).grid(row=2, column=i, pady=100)

        # Mengatur kolom dengan properti weight untuk memusatkan frame di tengah jendela
        self.frame.grid_columnconfigure(0, weight=1)
        for i in range(len(image_paths)):
            self.frame.grid_columnconfigure(i, weight=1)

    def hide(self):
        self.frame.pack_forget()

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    
    height = 500
    width = 800
    x = (root.winfo_screenwidth()//2) - (width//2)
    y = (root.winfo_screenheight()//2) - (height//2)
    
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.mainloop()
