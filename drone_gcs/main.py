import tkinter as tk
from tkinter.ttk import *
from tkinter import*
import cv2
from PIL import Image, ImageTk
from PIL import *
from video_utility import GetVideo, VideoData
import keyboard
import numpy as np
import io
import datetime
import os
from tkinter import messagebox

#download ghostscript
# ghostscript_path = r'C:\Program Files (x86)\gs\gs10.02.1\bin'
# os.environ['PATH'] += os.pathsep + ghostscript_path
class InputVideo:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Viewer")
        self.root.resizable(False, False)
        self.root.iconbitmap("images\logodrone.ico")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - 490) // 2
        y_position = (screen_height - 540) // 2
        self.root.geometry(f"490x540+{x_position}+{y_position}")

        self.root.resizable(False, False)

        self.cam_labels = ["Camera 1", "Camera 2", "Camera 3", "Camera 4", "Camera 5"]
        self.entry_variables = [StringVar() for _ in range(5)]

        self.additional_labels = ["Input 1", "Input 2", "Input 3", "Input 4", "Input 5"]
        self.additional_entry_variables = [StringVar() for _ in range(5)]


        self.title_box()

    def title_box(self):
        label_judul_frame = Label(self.root, text="Ground Control System\nConfiguration", font=("Consolas", 12))
        label_judul_frame.pack(pady=5)

        for i, cam_label in enumerate(self.cam_labels):
            gap = 20  

            camera_label = Label(self.root, text=f"{cam_label} =", font=("consolas", 12))
            camera_label.place(x=10, y=60 + (60 + gap) * i)

            entry_camera = Entry(self.root, textvariable=self.entry_variables[i], width=40, font=("consolas", 11))
            entry_camera.place(x=140, y=65 + (60 + gap) * i)

            label_label = Label(self.root, text=f"Label {i + 1} =", font=("consolas", 12))
            label_label.place(x=10, y=90 + (60 + gap) * i)

            entry_label = Entry(self.root, textvariable=self.additional_entry_variables[i], width=40, font=("consolas", 11))
            entry_label.place(x=140, y=95 + (60 + gap) * i)
        

        submit_button = Button(self.root, text="Execute", command=self.show_main_frame,
                               font=("consolas",11),width=12, height=1, bg="yellow" )
        submit_button.place(x=360, y=470)

    def show_main_frame(self):
        try:

            if any(entry.get() == "" for entry in self.entry_variables + self.additional_entry_variables):
                messagebox.showwarning("Warning", "Please fill in all the entry boxes.")
                return  
            
            cam_values = [int(entry.get()) for entry in self.entry_variables]
            label = self.additional_values = [entry.get() for entry in self.additional_entry_variables]

            self.root.destroy()  # Close the InputVideo window
            main_frame = MainFrame(cam_values,label)
            main_frame.run()
        except ValueError:
            # Handle the case where non-integer values are entered
            print("Error", "Please enter valid integer values for cameras.")


class MainFrame:
    def __init__(self,input_video_data, input_label):
        self.root = tk.Tk()
        self.root.iconbitmap("images\logodrone.ico")
        self.root.state('zoomed')
        self.root.title("Main video")
        self.root.resizable(False,False)
        
        
        self.cam1, self.cam2, self.cam3, self.cam4, self.cam5 = input_video_data
        self.label1, self.label2, self.label3, self.label4, self.label5 = input_label

        self.__data1 = VideoData()
        self.__data2 = VideoData()
        self.__data3 = VideoData()
        self.__data4 = VideoData()
        self.__data5 = VideoData()

        self.__fetcher1 = GetVideo(self.__data1, self.cam1)
        self.__fetcher2 = GetVideo(self.__data2, self.cam2)
        self.__fetcher3 = GetVideo(self.__data3, self.cam3)
        self.__fetcher4 = GetVideo(self.__data4, self.cam4)
        self.__fetcher5 = GetVideo(self.__data5, self.cam5)

        self.__fetcher1.start_fetch()
        self.__fetcher2.start_fetch()
        self.__fetcher3.start_fetch()
        self.__fetcher4.start_fetch()
        self.__fetcher5.start_fetch()

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.frame_atas = tk.Frame(self.root, width=self.screen_width // 1.3, height=self.screen_height // 1.57, bg="white",
                                   highlightbackground="black", highlightthickness=3)
        self.frame_atas.pack_propagate(False)
        self.frame_atas.pack(pady=10, padx=10, anchor=tk.NW)

        background_color = self.frame_atas.cget("bg")
        label_di_frame = tk.Label(self.frame_atas, text="Main Camera Video", font=("Consolas", 18), bg=background_color)
        label_di_frame.pack(pady=10)

        self.frame_bawah = tk.Frame(self.root, width=self.screen_width // 1.015, height=self.screen_height // 3.4, bg="white",
                                    highlightbackground="black", highlightthickness=3)
        self.frame_bawah.pack_propagate(False)
        self.frame_bawah.pack(pady=2)
        background_color = self.frame_bawah.cget("bg")
        label_di_frame = tk.Label(self.frame_bawah, text="Feed Camera", font=("Consolas", 18), bg=background_color)
        label_di_frame.pack(pady=5)

        self.frame_kotak = tk.Frame(self.root, width=self.screen_width // 4.8, height=self.screen_height // 1.57, bg="white",
                                    highlightbackground="black", highlightthickness=3)
        self.frame_kotak.pack_propagate(False)
        self.frame_kotak.place(x=1125, y=10)

        self.canvas1 = tk.Canvas(self.frame_atas, width=1050, height=480)
        self.canvas1.place(x=25, y=60)
        self.canvas1.pack_propagate(False)

        self.canvas2 = tk.Canvas(self.frame_bawah, width=340, height=190)
        self.canvas2.place(x=25, y=50)
        self.canvas2.pack_propagate(False)

        self.canvas3 = tk.Canvas(self.frame_bawah, width=340, height=190)
        self.canvas3.place(x=367, y=50)
        self.canvas3.pack_propagate(False)

        self.canvas4 = tk.Canvas(self.frame_bawah, width=340, height=190)
        self.canvas4.place(x=708, y=50)
        self.canvas4.pack_propagate(False)

        self.canvas5 = tk.Canvas(self.frame_bawah, width=340, height=190)
        self.canvas5.place(x=1050, y=50)
        self.canvas5.pack_propagate(False)

        self.switch_button = tk.Button(self.frame_kotak, text="Switch Videos",
                                       width=38,height=2,
                                       font=("consolas bold",10),
                                       command=self.switch_videos)
        self.switch_button.place(x=10,y=370)

        self.root.bind('<space>', self.switch_videos)

        self.current_canvas = 1

        self.battery_level = 100
        self.drone_speed = 20

        self.x = 10.13
        self.y = 23.435
        self.z = 43.535

        self.dummy_time = datetime.datetime.now()
        self.flight_time = self.dummy_time.strftime("%H:%M:%S")
        self.altitude = 3.17
        self.voltage = 12.59
        self.flight_mode = "Stabilize"
        
        self.drone_status()
        self.update()

    

    def switch_videos(self, event=None):
        if self.current_canvas == 1:
            self.current_canvas = 2
        elif self.current_canvas == 2:
            self.current_canvas = 3
        elif self.current_canvas == 3:
            self.current_canvas = 4
        elif self.current_canvas == 4:
            self.current_canvas = 5
        elif self.current_canvas == 5:
            self.current_canvas = 1

        self.canvas1.delete("all")
        self.canvas2.delete("all")
        self.canvas3.delete("all")
        self.canvas4.delete("all")
        self.canvas5.delete("all")

    # def save_canvas_image(self, event=None):
    #     # if self.current_canvas == 1:
    #     x = datetime.datetime.now()
    #     canvas_image = self.canvas1.postscript(colormode='color')
    #     image = Image.open(io.BytesIO(canvas_image.encode('utf-8')))
    #     image = np.array(image)

    #     image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

    #     directory = r'C:\Users\XPS15\PycharmProjects\drone_gcs\images' #change to new directory
    #     if not os.path.exists(directory):
    #         os.makedirs(directory)

    #     filename = os.path.join(directory, f"Capture_at_{x.hour}_{x.minute}_{x.second}.png")
    #     cv2.imwrite(filename, image)
    #     print(f"Frame from canvas1 saved in {filename}")

    def resize_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1054, 484))
        return frame

    def minimize_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (340, 190))
        return frame

    def update(self):

        ret1, frame1 = self.__data1.getImage()
        ret2, frame2 = self.__data2.getImage()
        ret3, frame3 = self.__data3.getImage()
        ret4, frame4 = self.__data4.getImage()
        ret5, frame5 = self.__data5.getImage()

        frame1_resized = None
        frame2_resized = None
        frame3_resized = None
        frame4_resized = None
        frame5_resized = None

        if ret1 and ret2 and ret3 and ret4 and ret5:

            if self.current_canvas == 1:
                frame1_resized = self.resize_frame(frame1)
                frame2_resized = self.minimize_frame(frame2)
                frame3_resized = self.minimize_frame(frame3)
                frame4_resized = self.minimize_frame(frame4)
                frame5_resized = self.minimize_frame(frame5)

            elif self.current_canvas == 2:
                frame1_resized = self.minimize_frame(frame1)
                frame2_resized = self.resize_frame(frame2)
                frame3_resized = self.minimize_frame(frame3)
                frame4_resized = self.minimize_frame(frame4)
                frame5_resized = self.minimize_frame(frame5)
            elif self.current_canvas == 3:
                frame1_resized = self.minimize_frame(frame1)
                frame2_resized = self.minimize_frame(frame2)
                frame3_resized = self.resize_frame(frame3)
                frame4_resized = self.minimize_frame(frame4)
                frame5_resized = self.minimize_frame(frame5)

            elif self.current_canvas == 4:
                frame1_resized = self.minimize_frame(frame1)
                frame2_resized = self.minimize_frame(frame2)
                frame3_resized = self.minimize_frame(frame3)
                frame4_resized = self.resize_frame(frame4)
                frame5_resized = self.minimize_frame(frame5)

            elif self.current_canvas == 5:
                frame1_resized = self.minimize_frame(frame1)
                frame2_resized = self.minimize_frame(frame2)
                frame3_resized = self.minimize_frame(frame3)
                frame4_resized = self.minimize_frame(frame4)
                frame5_resized = self.resize_frame(frame5)

        if frame1_resized is not None and frame2_resized is not None and frame3_resized is not None and frame4_resized is not None and frame5_resized is not None:

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8
            font_color = (255, 255, 255)
            font_thickness = 2

            # =================================== Video Label ================================================== #
            text1 = f"{self.label1}"
            text2 = f"{self.label2}"
            text3 = f"{self.label3}"
            text4 = f"{self.label4}"
            text5 = f"{self.label5}"
            # =================================== Video Label ================================================== #

            cv2.putText(frame1_resized, text1, (10, 30), font, font_scale, font_color, font_thickness)
            cv2.putText(frame2_resized, text2, (10, 30), font, font_scale, font_color, font_thickness)
            cv2.putText(frame3_resized, text3, (10, 30), font, font_scale, font_color, font_thickness)
            cv2.putText(frame4_resized, text4, (10, 30), font, font_scale, font_color, font_thickness)
            cv2.putText(frame5_resized, text5, (10, 30), font, font_scale, font_color, font_thickness)

            self.photo1 = ImageTk.PhotoImage(image=Image.fromarray(frame1_resized))
            self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(frame2_resized))
            self.photo3 = ImageTk.PhotoImage(image=Image.fromarray(frame3_resized))
            self.photo4 = ImageTk.PhotoImage(image=Image.fromarray(frame4_resized))
            self.photo5 = ImageTk.PhotoImage(image=Image.fromarray(frame5_resized))

            if self.current_canvas == 1:
                images = [self.photo1, self.photo2, self.photo3, self.photo4, self.photo5]
            elif self.current_canvas == 2:
                images = [self.photo2, self.photo3, self.photo4, self.photo5, self.photo1]
            elif self.current_canvas == 3:
                images = [self.photo3, self.photo4, self.photo5, self.photo1, self.photo2]
            elif self.current_canvas == 4:
                images = [self.photo4, self.photo5, self.photo1, self.photo2, self.photo3]
            else:
                images = [self.photo5, self.photo1, self.photo2, self.photo3, self.photo4]

            self.canvas1.create_image(0, 0, image=images[0], anchor='nw')
            self.canvas2.create_image(0, 0, image=images[1], anchor='nw')
            self.canvas3.create_image(0, 0, image=images[2], anchor='nw')
            self.canvas4.create_image(0, 0, image=images[3], anchor='nw')
            self.canvas5.create_image(0, 0, image=images[4], anchor='nw')

        self.root.after(10, self.update)

    def decrease_battery(self):
        if self.battery_level > 0:
            self.battery_level -= 1
            self.battery_progress["value"] = self.battery_level
            self.battery_label.config(text=f"{self.battery_level}%")
            self.root.after(10000, self.decrease_battery)

    
    def drone_status(self):

        background_color = self.frame_kotak.cget("bg")
        label_judul_frame = tk.Label(self.frame_kotak, text="Drone Status", font=("Consolas", 18), bg=background_color)
        label_judul_frame.pack(pady=10)

        label_batere_frame = tk.Label(self.frame_kotak, text='Battery', font=("Consolas", 12), bg=background_color)
        label_batere_frame.place(x=5, y=60)
        label_batere_frame.pack_propagate(False)

        self.battery_label = tk.Label(self.frame_kotak, text=f"{self.battery_level}%", font=("Consolas", 12),
                                      bg=background_color)
        self.battery_label.place(x=180, y=60)
        label_batere_frame.pack_propagate(False)

        self.battery_progress = Progressbar(self.frame_kotak, length=100, maximum=100, value=self.battery_level)
        self.battery_progress.place(x=75, y=61)
        label_batere_frame.pack_propagate(False)

        #======================== Speed Label ====================================================== #

        speed_label = tk.Label(self.frame_kotak, text=f"Speed = {self.drone_speed} m/s ", font=("Consolas", 11),
                               bg="green", fg="white")
        speed_label.place(x=5, y=95)
        label_batere_frame.pack_propagate(False)

        # flight_info = tk.Label(self.frame_kotak,
        #                        text=f"Altitude = {self.altitude} m\nFlight Mode = {self.flight_mode}\nFlight Time = {self.flight_time}",
        #                        font=("Consolas", 11), bg=background_color, justify='left', anchor='w')
        # flight_info.place(x=5, y=130)
        

        # ============================= Flight data =========================================== #

        flight_data = tk.Frame(self.frame_kotak, width=285, height=120, bg="white", highlightbackground="black",
                               highlightthickness=2)
        flight_data.place(x=5, y=130)
        flight_data.pack_propagate(False)

        flight_data_label = tk.Label(flight_data, text="Flight Data", font=("Consolas", 11), fg="black", bg= background_color)
        flight_data_label.pack(pady=1)

        voltage = tk.Label(flight_data, text=f"Voltage\t\t= {self.voltage}", font=("Consolas", 10), fg="black", bg= background_color)
        voltage.place(x=5, y= 25)

        altitude = tk.Label(flight_data, text=f"Altitude\t= {self.altitude}", font=("Consolas", 10), fg="black", bg= background_color)
        altitude.place(x=5, y= 45)

        fligt_mode = tk.Label(flight_data, text=f"Flight Mode\t= {self.flight_mode}", font=("Consolas", 10), fg="black", bg= background_color)
        fligt_mode.place(x=5, y= 65)

        voltage = tk.Label(flight_data, text=f"Flight Time\t= {self.flight_time}", font=("Consolas", 10), fg="black", bg= background_color)
        voltage.place(x=5, y= 85)
    
        # ============================ Campuss Logo ============================================ #

        campus = tk.Label(self.frame_kotak, text=f"In Partnership With", font=("Consolas", 11), fg="black", bg= background_color)
        campus.place(x=72, y= 460)

        self.image = PhotoImage(file="images/trias3.png")
        self.photo = Label(self.frame_kotak,image=self.image )
        self.photo["bd"] = 0
        self.photo.place(x=11,y=495)
        
        # ============================ frame Coordinates ======================================= #

        coordinates = tk.Frame(self.frame_kotak, width=285, height=100, bg="white", highlightbackground="black",
                               highlightthickness=2)
        coordinates.place(x=5, y=260)
        coordinates.pack_propagate(False)


        coordinate_label = tk.Label(coordinates, text="Coordinates", font=("Consolas", 10), bg="green", fg="white")
        coordinate_label.pack(pady=1)

        coordinates_label = tk.Label(coordinates, text=f"X = {self.x}\tY = {self.y}\n\nZ = {self.z}",
                                     font=("Consolas", 11), bg=background_color)
        coordinates_label.pack(pady=1)


        self.decrease_battery()



    def on_closing(self):
        self.__fetcher1.stop_fetch()
        self.__fetcher2.stop_fetch()
        self.__fetcher3.stop_fetch()
        self.__fetcher4.stop_fetch()
        self.__fetcher5.stop_fetch()

        self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()




if __name__ == '__main__':
    root = Tk()
    input_video = InputVideo(root)
    root.mainloop()
    

    # app = MainFrame(root)

   

    #

