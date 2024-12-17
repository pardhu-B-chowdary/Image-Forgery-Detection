from tkinter import *
from tkinter import filedialog, ttk, messagebox
from PIL import ImageTk, Image
from single_image_test import main as img_test
import cv2
import numpy as np

# Global variables
IMG_WIDTH = 400
IMG_HEIGHT = 400


def getImage(path, width, height):
    """
    Function to return an image as a PhotoImage object
    :param path: A string representing the path of the image file
    :param width: The width of the image to resize to
    :param height: The height of the image to resize to
    :return: The image represented as a PhotoImage object
    """
    img = Image.open(path)
    img = img.resize((width, height), Image.Resampling.LANCZOS)

    return ImageTk.PhotoImage(img)


def overlay_images(background_path):
    foreground_path = "../data/icons/no.png"
    output_path = "../data/icons/results.png"
    # print((f"foreground image:{foreground_path} \n background image:{background_path}"))
    # Load the images
    background_img = cv2.imread(background_path)
    foreground_img = cv2.imread(foreground_path, cv2.IMREAD_UNCHANGED)

    # Resize the foreground image to match the background image size
    foreground_img = cv2.resize(foreground_img, (background_img.shape[1], background_img.shape[0]))

    # Extract the alpha channel and use it as a mask
    alpha_mask = foreground_img[:, :, 3] / 255.0
    alpha_mask = cv2.merge([alpha_mask, alpha_mask, alpha_mask])

    # Convert the background image to float32 for compatibility
    background_img_float = background_img.astype(np.float32)

    # Blend the foreground and background images with explicit output type
    result_float = cv2.multiply(alpha_mask, foreground_img[:, :, :3], dtype=cv2.CV_32F) + cv2.multiply(1 - alpha_mask,
                                                                                                       background_img_float,
                                                                                                       dtype=cv2.CV_32F)
    # Convert the result back to uint8 format
    result = result_float.astype('uint8')
    # Save the overlaid image
    cv2.imwrite(output_path, result)
    return output_path


# A class representing the GUI of the detection software
class GUI(Frame):
    def __init__(self, parent=None):
        """
        Initialize the GUI object. Populate the GUI
        :param parent: The parent of the Frame
        :return: None
        """
        self.uploaded_image = None

        # Initialize the frame
        Frame.__init__(self, parent)
        self.pack()

        # Label for the results of scan
        self.Title = Label(self, text="Digital Image Forgery Detection", font=("Courier", 50))
        self.Title.grid(row=0, column=0, columnspan=2)
        Grid.rowconfigure(self, 0, weight=1)
        # Label for the results of scan
        self.resultLabel = Label(self, text=" ", font=("Courier", 50))
        self.resultLabel.grid(row=1, column=0, columnspan=2)
        Grid.rowconfigure(self, 0, weight=1)

        # Get the blank image
        blank_img = getImage("../data/icons/blank.png", IMG_WIDTH, IMG_HEIGHT)

        # Displays the input image
        self.imagePanel = Label(self, image=blank_img)
        self.imagePanel.image = blank_img
        self.imagePanel.grid(row=2, column=0, padx=5)

        # Label to display the output image
        self.resultPanel = Label(self, image=blank_img)
        self.resultPanel.image = blank_img
        self.resultPanel.grid(row=2, column=1, padx=5)

        # Label to display the path of the input image
        self.fileLabel = Label(self, text="No file selected", fg="grey", font=("Times", 15))
        self.fileLabel.grid(row=3, column=0, columnspan=2)

        # Progress bar
        self.progressBar = ttk.Progressbar(self, length=500)
        self.progressBar.grid(row=4, column=0, columnspan=2)

        # Configure the style of the buttons
        s = ttk.Style()
        s.configure('my.TButton', font=('Times', 15))

        # Button to upload images
        self.uploadButton = ttk.Button(self, text="Upload Image", style="my.TButton", command=self.browseFile)
        self.uploadButton.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=5)

        # Button to run the detection algorithm
        self.startButton = ttk.Button(self, text="Start", style="my.TButton", command=self.runProg)
        self.startButton.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=5)

    def browseFile(self):
        """
        Function to open a browser for users to select an image
        :return: None
        """
        # Only accept jpg and png files
        filename = filedialog.askopenfilename(title="Select an image", filetype=[("Image file", "*.jpg *.png")])

        # No file selected (User closes the browsing window)
        if filename == "":
            return

        self.uploaded_image = filename
        self.progressBar['value'] = 0  # Reset the progress bar
        self.fileLabel.configure(text=filename)  # Set the path name in the fileLabel
        # Display the input image in imagePanel
        img = getImage(filename, IMG_WIDTH, IMG_HEIGHT)
        self.imagePanel.configure(image=img)
        self.imagePanel.image = img
        # Display blank image in resultPanel
        blank_img = getImage("../data/icons/blank.png", IMG_WIDTH, IMG_HEIGHT)
        self.resultPanel.configure(image=blank_img)
        self.resultPanel.image = blank_img
        # Reset the resultLabel
        self.resultLabel.configure(text="READY TO SCAN", foreground="black")

    # Function to run the program the copy-move detection algorithm
    def runProg(self):
        """
        Function to run the copy-move detection algorithm on an uploaded image
        :return: None
        """
        # Retrieve the path of the image file
        path = self.uploaded_image

        # User has not selected an input image
        if path is None:
            messagebox.showerror('Error', "Please select image")  # Show error message
            return

        result: int = img_test(img=path)[0]
        # Set the progress bar to 100%
        self.progressBar['value'] = 100

        # If copy-move is detected
        if result:
            r_path = overlay_images(path)
            # Retrieve the output image and display in resultPanel
            img = getImage(r_path, IMG_WIDTH, IMG_HEIGHT)
            self.resultPanel.configure(image=img)
            self.resultPanel.image = img
            # Display results in resultLabel
            self.resultLabel.configure(text="FORGED IMAGE", foreground="red")

        else:
            # Retrieve the thumbs up image and display in resultPanel
            img = getImage("../data/icons/thumbs_up.png", IMG_WIDTH, IMG_HEIGHT)
            self.resultPanel.configure(image=img)
            self.resultPanel.image = img
            # Display results in resultLabel
            self.resultLabel.configure(text="ORIGINAL IMAGE", foreground="green")


# Main Function
def main():
    """
    Main function which runs the Copy-Move detection application
    """
    # Initialize the app window
    root = Tk()
    root.title("Copy-Move Detector")
    # root.iconbitmap('images/icon.ico')
    # Ensure the program closes when window is closed
    # root.protocol("WM_DELETE_WINDOW", root.quit)
    # Maximize the size of the window
    root.state("zoomed")
    # Add the GUI into the Tkinter window
    GUI(parent=root)
    # Open the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
input()
