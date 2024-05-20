from tkinter import *
import subprocess
from tkinter import filedialog
import ttkbootstrap as tb

root = tb.Window(themename='darkly')

root.title('Santivirus')
# Set window size to full screen
root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))

file_path = ''
upload_type = 'file'  # Default upload type is file


def file_dialog():
    """Open a file dialog to choose a file or directory.
     Display the chosen path in the file_label widget.
    """
    global file_path
    if upload_type == 'file':
        file_path = filedialog.askopenfilename()
        print(file_path)
    else:
        file_path = filedialog.askdirectory()
        print(file_path)
    if file_path:
        file_label.config(text='Chosen path: ' + file_path)
    else:
        file_label.config(text='No path selected')


def scanner():
    """Execute scanning.py and capture the output.
    Display the output in the output_text widget.
    """
    if file_path:
        # Execute scanning.py and capture output
        file_label.config(text=file_path)
        if choice.get() == 'Just scan':
            result = subprocess.run(['python', '.\\scanning.py', file_path, 'scan'], stdout=subprocess.PIPE)
        elif choice.get() == 'Scan and delete':
            result = subprocess.run(['python', '.\\scanning.py', file_path, 'delete'], stdout=subprocess.PIPE)

        output_text['state'] = 'normal'
        output_text.delete(1.0, 'end')  # Clear previous output
        output_text.insert('end', result.stdout.decode())  # Insert captured output
        output_text.see('end')
        output_text['state'] = 'disabled'

        print(result)
    else:
        file_label.config(text='No path selected')


def toggle_upload_type():
    """Toggle between file and directory upload.
    Change the text of the toggle_button accordingly."""
    global upload_type
    if upload_type == 'file':
        upload_type = 'directory'
        toggle_button.config(text='Switch to File Upload')
    else:
        upload_type = 'file'
        toggle_button.config(text='Switch to Directory Upload')


my_label = tb.Label(text='Santivirus', font=('Helvetica', 30))
my_label.pack(pady=10)

my_text = tb.Label(text='Wanna see some virus? Check your computer now!', font=('Helvetica', 20))
my_text.pack(pady=10)

# Add a toggle button to switch between file and directory upload
toggle_button = tb.Button(text='Switch to Directory Upload', command=toggle_upload_type)
toggle_button.config(padding='40 15')
toggle_button.pack(pady=10)

file_label = tb.Label(text="", font=("Helvetica", 12))
file_label.pack(pady=10)

# Load 'upload' icon
image = PhotoImage(file='images/upload_image.png')

# Create a label with the image
image_button = tb.Label(image=image)
image_button.pack(pady=10)

# Bind the click event of the image to the file_dialog function
image_button.bind('<Button-1>', lambda event: file_dialog())

# Create a dropdown menu
CHOICES = ['Just scan', 'Scan and delete']
# make a combobox with the given choices and read only
choice = tb.Combobox(root, values=CHOICES, state='readonly')

choice.pack(pady=10)
choice.current(0)  # Set the default option to 'Just scan'

# Use lambda function to run scanner when scan_button is clicked
scan_button = tb.Button(text='Scan', command=scanner)
scan_button.config(padding='40 15')
scan_button.pack(padx=10, pady=10)

my_label = tb.Label(text='Scan results', font=('Helvetica', 30))
my_label.pack(pady=20)

# Create a text widget to display the output
output_text = Text(root, width=200, height=12, wrap='word', font=('Helvetica', 14), state='disabled')
output_text.pack()

root.mainloop()
