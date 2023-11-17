
from tkinter import *

def create_input_video_window():
    root = Tk()
    root.title("Video Viewer")
    root.resizable(False, False)
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - 480) // 2
    y_position = (screen_height - 340) // 2
    root.geometry(f"480x340+{x_position}+{y_position}")
    root.resizable(False, False)
    
    return root

def title_box(root, main_frame_callback):
    label_judul_frame = Label(root, text="Ground Control System\nConfiguration", font=("Consolas", 12))
    label_judul_frame.pack(pady=5)

    cam_labels = ["Camera 1", "Camera 2", "Camera 3", "Camera 4", "Camera 5"]
    entry_variables = [StringVar() for _ in range(5)]

    for i, cam_label in enumerate(cam_labels):
        label = Label(root, text=cam_label, font=("consolas", 12))
        label.place(x=10, y=60 + 30 * i)

        entry = Entry(root, textvariable=entry_variables[i], width=40, font=("consolas", 11))
        entry.place(x=90, y=65 + 30 * i)

    submit_button = Button(root, text="Submit", command=lambda: trigger_main_frame(main_frame_callback, entry_variables, root))
    submit_button.place(x=200, y=220)

def trigger_main_frame(main_frame_callback, entry_variables, root):
    try:
        cam_values = [int(entry.get()) for entry in entry_variables]
        main_frame_callback(*cam_values)
        root.destroy()
    except ValueError:
        # Handle the case where non-integer values are entered
        messagebox.showerror("Error", "Please enter valid integer values for cameras.")

def run_input_video():
    root = create_input_video_window()
    title_box(root, main_frame_callback)

    root.mainloop()

def main_frame_callback(cam1, cam2, cam3, cam4, cam5):
    print(f"Camera 1: {cam1} (type: {type(cam1)})")
    print(f"Camera 2: {cam2} (type: {type(cam2)})")
    print(f"Camera 3: {cam3} (type: {type(cam3)})")
    print(f"Camera 4: {cam4} (type: {type(cam4)})")
    print(f"Camera 5: {cam5} (type: {type(cam5)})")

if __name__ == "__main__":
    run_input_video()
