import tkinter as tk
from tkinter import PhotoImage

# swap images between main and sub images
def swap_images(selected_image):
    # current main view
    current_main_image = main_image_label.cget("image")

    # set clicked sub-image as the new main view
    main_image_label.config(image=selected_image.cget("image"))

    # set the previous main view as a sub-image
    selected_image.config(image=current_main_image)

root = tk.Tk()
root.title("Image Swapper")

image_frame = tk.Frame(root)
image_frame.pack()

# main image
main_image_file = "image1.png"
main_image = PhotoImage(file=main_image_file)


# label to display the main image
main_image_label = tk.Label(image_frame, image=main_image)
main_image_label.pack()

sub_images_frame = tk.Frame(root)
sub_images_frame.pack()

# list to store the PhotoImage objects for sub-images
sub_images = []

sub_image_files = ["image2.png", "image3.png", "image4.png"]

for sub_image_file in sub_image_files:
    sub_image = PhotoImage(file=sub_image_file)
    sub_images.append(sub_image)

    # labels for sub-images
    sub_image_label = tk.Label(sub_images_frame, image=sub_image)
    sub_image_label.pack(side=tk.LEFT)

    # bind the click event to swap the images
    sub_image_label.bind("<Button-1>", lambda event, label=sub_image_label: swap_images(label))

root.mainloop()
