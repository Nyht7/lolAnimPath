import os
import re
import sys
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Modify the animation file with the new folder path
def convert_path(folder_path):
    # Normalize path separators
    folder_path = folder_path.replace("\\", "/")
    
    # Ensure the path contains "ASSETS" or "DATA"
    match = re.search(r".*?(ASSETS|DATA)(/.*)", folder_path, re.IGNORECASE)
    if match:
        new_path = match.group(1).upper() + match.group(2)
    else:
        return "Error: Selected path must contain 'ASSETS' or 'DATA'."
    
    return new_path

def modify_animation_file(file_path, folder_path):
    new_path = convert_path(folder_path)
    if "Error" in new_path:
        return new_path
    
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    content = re.sub(r'(mAnimationFilePath: string = ")([^"]+/)([^/]+\.anm")', rf'\1{new_path}/\3', content)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return "Repath has been successfully updated."

def modify_skin_file(file_path, new_name):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    content = re.sub(r'("DATA/Characters/.*/Animations/)(.*?)(\.bin")', rf'\1{new_name}\3', content)
    content = re.sub(r'(animationGraphData: link = "Characters/.*/Animations/)(.*?)"', rf'\1{new_name}"', content)
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return "Skin.py (Skins Folder) has been successfully modified."

def modify_py_file(file_path, new_name):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    content = re.sub(r'("Characters/[^/]+/Animations/)[^/]+(" = animationGraphData {)', rf'\1{new_name}\2', content)
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    new_file_path = os.path.join(os.path.dirname(file_path), f"{new_name}.py")
    os.rename(file_path, new_file_path)

    return "Skin.py (Animations Folder) has been successfully modified."

# File selection dialogs
def select_skin_file(new_name, feedback_label):
    if not new_name:
        messagebox.showerror("Error", "Custom name is required before proceeding!")
        return
    
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    if file_path:
        result = modify_skin_file(file_path, new_name)
        feedback_label.configure(text=result)

def select_animation_file(new_name, feedback_label):
    if not new_name:
        messagebox.showerror("Error", "Custom name is required before proceeding!")
        return
    
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    if file_path:
        result = modify_py_file(file_path, new_name)
        feedback_label.configure(text=result)

def select_folder_and_modify_animation_file(feedback_label):
    folder_path = filedialog.askdirectory(title="Select Folder Path")
    if folder_path:
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            result = modify_animation_file(file_path, folder_path)
            feedback_label.configure(text=result)

# Main GUI
def main():
    root = ctk.CTk()
    root.title("lolAnimPath")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root.geometry("700x600")
    root.resizable(False, False)

    title = ctk.CTkLabel(root, text="League of Legends Animation Path Editor", font=("Helvetica", 18, "bold"))
    title.pack(pady=20)

    frame = ctk.CTkFrame(root)
    frame.pack(padx=20, pady=10, fill="x")

    name_label = ctk.CTkLabel(frame, text="Enter Custom Name:")
    name_label.pack(side="left", padx=10)

    name_entry = ctk.CTkEntry(frame, placeholder_text="Enter name here")
    name_entry.pack(side="right", fill="x", expand=True, padx=10)

    def get_name():
        return name_entry.get().strip()

    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=20)

    feedback_label = ctk.CTkLabel(root, text="", font=("Helvetica", 12))
    feedback_label.pack(pady=10)

    ctk.CTkButton(button_frame, text="Select Skin.py (Skins)", width=200,
                  command=lambda: select_skin_file(get_name(), feedback_label)).pack(side="left", padx=10)

    ctk.CTkButton(button_frame, text="Select Skin.py (Animations)", width=200,
                  command=lambda: select_animation_file(get_name(), feedback_label)).pack(side="left", padx=10)

    ctk.CTkButton(button_frame, text="Repath Animations", width=200,
                  command=lambda: select_folder_and_modify_animation_file(feedback_label)).pack(side="left", padx=10)

    instructions_text = (
        "Instructions:\n\n"  # Adding extra newlines here
        "1. (REQUIRED) Enter the desired custom name for your skin and animation.\n\n"  # Extra newline between each step
        "2. Use 'Select Skin.py (Skins)' to modify the skin.py file.\n\n"
        "3. Use 'Select Skin.py (Animations)' to modify the animations file.\n\n"
        "4. Use 'Repath Animations' to update the path inside skin.py (Animations Folder).\n\n"
        "5. First, select the folder where you want to repath your animations.\n\n"
        "6. Then, select the skin.py (Animations Folder) to apply the new path.\n\n"
        "7. Feedback will appear below when the task is completed."
    )

    instructions_label = ctk.CTkLabel(root, 
                                      text=instructions_text, 
                                      font=("Helvetica", 16),  # Increased font size
                                      justify="left", 
                                      wraplength=650,  # Prevent text from stretching too wide
                                      padx=20,  # Add more horizontal padding
                                      pady=10)  # Add some internal padding for spacing

    # Adding external padding to ensure more spacing at the top and bottom of the instructions
    instructions_label.pack(pady=(30, 20), padx=20)  # Top padding of 30px, bottom padding of 20px


    root.mainloop()

if __name__ == "__main__":
    main()
