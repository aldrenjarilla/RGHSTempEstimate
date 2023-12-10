import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Button

def hue_to_rgb(hue):
    hsv_color = np.array([[[hue, 1, 1]]], dtype=np.float32)
    rgb_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2RGB)
    return rgb_color[0, 0]

def normalize_rgb(rgb):
    return rgb / 255.0

def estimate_temperature(image_path):
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue_channel = hsv_image[:, :, 0]
    non_black_hues = hue_channel[hue_channel > 10]
    histogram, bin_edges = np.histogram(non_black_hues, bins=180, range=[0, 180])
    colors = [normalize_rgb(hue_to_rgb(hue)) for hue in bin_edges[0:-1]]
    plt.bar(bin_edges[0:-1], histogram, color=colors, width=1)
    plt.title('Color Spectrum Histogram')
    plt.xlabel('Color (Visible Spectrum)')
    plt.ylabel('Frequency')


    def hue_to_temperature(hue):
        return hue * 5  

    temperatures = [hue_to_temperature(hue) for hue in bin_edges[0:-1]]
    plt.twinx().plot(bin_edges[0:-1], temperatures, color='r', label='Temperature (K)')

    plt.show()

def open_file_dialog():
    root = Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename(title="Select an Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if file_path:
        estimate_temperature(file_path)

if __name__ == "__main__":
    root = Tk()
    root.title("Flame Temperature Estimation")

    file_picker_button = Button(root, text="Open Image File", command=open_file_dialog)
    file_picker_button.pack(pady=20)

    root.mainloop()
