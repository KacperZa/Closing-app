import customtkinter
from tkinter import messagebox
import subprocess
import sys
import os


# function for svg icon
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# function for shutting down
def shutdown_command(minutes, hours):
    global shutdown_active
    minutes = int(minutes) if minutes.strip() else 0
    hours = int(hours) if hours.strip() else 0
    time = minutes * 60 + hours * 3600
    result = subprocess.run(
        f"shutdown /s /t {time}",
        capture_output=True,
        text=True,
        encoding="cp850",
    )
    shutdown_active = True
    button_cancel.configure(state="normal", fg_color="#D44644")
    button_cancel.update_idletasks()
    return print(result.stdout)


# function for showing info about shutting down
def show_info(minutes, hours):
    messagebox.showinfo(
        "Info", f"Computer will shut down in {hours} hours and {minutes} minutes."
    ) if hours.strip() else messagebox.showinfo(
        "Info", f"Computer will shut down in {minutes} minutes."
    )


# combining these two above functions
def shutdown(minutes, hours):
    shutdown_command(minutes, hours)
    show_info(minutes, hours)


# cancelling shutdown
def cancel_shutdown_command():
    result = subprocess.run(
        "shutdown /a",
        capture_output=True,
        text=True,
        encoding="cp850",
    )
    print(result.stdout)
    button_cancel.configure(state="disabled", fg_color="gray")


# showing info about cancelled shutdwon
def show_info_cancelled():
    messagebox.showinfo("Info", "Shutdown cancelled.")


# combining these two above functions
def cancel_shutdown():
    cancel_shutdown_command()
    show_info_cancelled()


icon_path = resource_path("icon.svg")


# gui
app = customtkinter.CTk()
app.title("Close app")
app.geometry("300x150")
app.resizable(height=False, width=False)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

label1 = customtkinter.CTkLabel(app, text="When should the computer shut down?")
label1.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0))
hours = customtkinter.CTkEntry(app, width=50, placeholder_text="Hours")
hours.grid(row=1, column=0, padx=20, pady=10, sticky="we")
minutes = customtkinter.CTkEntry(app, width=50, placeholder_text="Minutes")
minutes.grid(row=1, column=1, padx=20, pady=0, sticky="we")

button = customtkinter.CTkButton(
    app,
    text="SET",
    command=lambda: shutdown(minutes.get(), hours.get()),
    fg_color="#5CE65C",
    hover_color="#4BB64B",
    text_color="black",
)
button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")


button_cancel = customtkinter.CTkButton(
    app,
    text="CANCEL",
    command=lambda: cancel_shutdown(),
    fg_color="gray",
    hover_color="#963232",
    text_color="black",
    state="disabled",
    text_color_disabled="white",
)
button_cancel.grid(row=2, column=1, padx=20, pady=10, sticky="we")


app.mainloop()
