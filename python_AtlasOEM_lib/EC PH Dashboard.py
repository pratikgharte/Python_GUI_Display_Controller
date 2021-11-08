from AtlasOEM_PH import AtlasOEM_PH
from AtlasOEM_EC import AtlasOEM_EC
import OEM_PH_EC_DO_example
import OEM_PH_example
import time
import tkinter as tk
import tkinter.font as tkFont
###############################################################################
# Parameters and global variables
PH = AtlasOEM_PH()
# Declare global variables
root = None
dfont = None
frame = None
EC_val = None
OEM_reading_closure  = None

# Global variable to remember if we are fullscreen or windowed
fullscreen = False

###############################################################################
# Functions

# Toggle fullscreen
def toggle_fullscreen(event=None):

    global root
    global fullscreen

    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize()

# Return to windowed mode
def end_fullscreen(event=None):

    global root
    global fullscreen

    # Turn off fullscreen mode
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize()

# Automatically resize font size based on window size
def resize(event=None):

    global dfont
    global frame

    # Resize font based on frame height (minimum size of 12)
    # Use negative number for "pixels" instead of "points"
    new_size = -max(12, int((frame.winfo_height() / 10)))
    dfont.configure(size=new_size)

# Read values from the sensors at regular intervals
def poll():

    global root
    global ec_val     
    global ph_val 

    try:
            val1 = round(OEM_PH_example.pH_reading, 2)
            pH_reading.set(val1)
            val2 = round(get_all_EC_values(), 1)
            EC_val.set(val2)
    except:
            pass

    # Schedule the poll() function for another 500 ms from now
    root.after(1, poll)

###############################################################################
# Main script

# Create the main window
root = tk.Tk()
root.title("The Big Screen")

# Create the main container
frame = tk.Frame(root)

# Lay out the main container (expand to fit window)
frame.pack(fill=tk.BOTH, expand=1)

# Variables for holding temperature and light data
PH = tk.DoubleVar()
EC = tk.DoubleVar()

# Create dynamic font for text
dfont = tkFont.Font(size=-24)

# Create widgets
label_temp = tk.Label(frame, text="PH", font=dfont)
label_celsius = tk.Label(frame, textvariable=PH, font=dfont)
#label_unitc = tk.Label(frame, text="°C", font=dfont)
label_light = tk.Label(frame, text="EC", font=dfont)
label_lux = tk.Label(frame, textvariable=EC, font=dfont)
label_unitlux = tk.Label(frame, text="uS", font=dfont)
button_quit = tk.Button(frame, text="Quit", font=dfont, command=root.destroy)

# Lay out widgets in a grid in the frame
label_temp.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
label_celsius.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
#label_unitc.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
label_light.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
label_lux.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
label_unitlux.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
button_quit.grid(row=2, column=2, padx=5, pady=5)

# Make it so that the grid cells expand out to fill window
for i in range(0, 3):
    frame.rowconfigure(i, weight=1)
for i in range(0, 3):
    frame.columnconfigure(i, weight=1)

# Bind F11 to toggle fullscreen and ESC to end fullscreen
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

# Have the resize() function be called every time the window is resized
root.bind('<Configure>', resize)

# Initialize our sensors





# Schedule the poll() function to be called periodically
root.after(1, poll)

# Start in fullscreen mode and run
toggle_fullscreen()
root.mainloop()
