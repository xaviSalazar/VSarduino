from tkinter import *

root = Tk()
root.title('ACE - EV !')
#root.iconbitmap('circle.ico')
root.geometry("1920x1920")

# Keep track of the button state on/off
global is_on
is_on = False

# Create Label
my_label = Label(root, 
text="The Switch is Off!", 
fg="grey",
font = ("Helvetica", 32))

my_label.pack(pady=20)

# Define our switch function
def switch():
    global is_on
    # Determine is on or off
    if is_on:
        on_button.config(image=off)
        my_label.config(text="The switch is off", fg = "grey")
        is_on = False
        print("false")
    else:
        on_button.config(image=on)
        my_label.config(text="The switch is on", fg = "green")
        is_on = True
        print("true")


# Define Our Images
on = PhotoImage(file = "onButton.png")
off = PhotoImage(file = "offButton.png")

# Create A Button
on_button = Button(root, image = off, bd=0, command=switch)
on_button.pack(pady=50)

root.mainloop()