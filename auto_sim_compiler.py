import tkinter.filedialog
import subprocess
import os
import shutil
import customtkinter as ctk
from tkinter import filedialog

class AutoSimCompiler(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.deactivate_automatic_dpi_awareness()
        self.title("AUTO-SIM Simulation Manager")
        self.geometry(f"{1000}x{500}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.minsize(1000,500)
        self.resizable(False, False)

        self.launcher_path = ""
        self.visualiser_path = ""
        self.simulator_path = ""
        self.build_folder_path = ""

        #We need multiple things in here:
        #We need to get the path to the Launcher
        #Label: Auto-Sim Launcher (Godot)
        self.auto_sim_launcher_label = ctk.CTkLabel(self, text='Auto Sim Launcher')
        self.auto_sim_launcher_label.grid()
        self.auto_sim_launcher_button = ctk.CTkButton(self, text='...', command=lambda: self.GetFilePath('launcher'))
        self.auto_sim_launcher_button.grid()

        self.auto_sim_vis_label = ctk.CTkLabel(self, text='Auto Sim Visualiser')
        self.auto_sim_vis_label.grid()
        self.auto_sim_vis_button = ctk.CTkButton(self, text='...', command=lambda: self.GetFilePath('visualiser'))
        self.auto_sim_vis_button.grid()

        self.auto_sim_sim_label = ctk.CTkLabel(self, text='Auto Sim Simulator')
        self.auto_sim_sim_label.grid()
        self.auto_sim_sim_button = ctk.CTkButton(self, text='...', command=lambda: self.GetFilePath('simulator'))
        self.auto_sim_sim_button.grid()

        self.auto_sim_get_build_folder_label = ctk.CTkLabel(self, text='Get Build Folder')
        self.auto_sim_get_build_folder_label.grid()
        self.auto_sim_get_build_folder_button = ctk.CTkButton(self, text='...', command=lambda: self.GetFilePath('build'))
        self.auto_sim_get_build_folder_button.grid()

        self.export_label = ctk.CTkLabel(self, text='Compile Installer')
        self.export_label.grid()
        self.export_button = ctk.CTkButton(self, text='...', command=self.ExportSim)
        self.export_button.grid()



    def GetFilePath(self, component):
        path = tkinter.filedialog.askdirectory()
        match component:
            case 'launcher':
                self.launcher_path = path
                self.auto_sim_launcher_button.configure(text=path)
            case 'visualiser':
                self.visualiser_path = path
                self.auto_sim_vis_button.configure(text=path)
            case 'simulator':
                self.simulator_path = path
                self.auto_sim_sim_button.configure(text=path)
            case 'build':
                self.build_folder_path = path
                self.auto_sim_get_build_folder_button.configure(text=path)


        #Button which opens a Filepicker, the button text will become the path to the launcher

        #We need to get the path to the SimManager
        #We need to get the path to the Visualiser
        #We need to get the path to the installer

    def ExportSim(self):
        path = tkinter.filedialog.askdirectory()
        self.copy_directory_contents(self.build_folder_path, path)
        self.compile_launcher(path)
        self.compile_visualier(path)
        self.compile_simulator(path)
        self.create_installer(path)

    def copy_directory_contents(self, src_dir, dst_dir):
        # Create the destination directory if it doesn't exist
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        # Recursively copy the contents of the source directory to the destination directory
        for item in os.listdir(src_dir):
            src_item = os.path.join(src_dir, item)
            dst_item = os.path.join(dst_dir, item)
            if os.path.isdir(src_item):
                self.copy_directory_contents(src_item, dst_item)
            else:
                shutil.copy2(src_item, dst_item)

    def compile_launcher(self, path):
       print("################# Launcher ###################")

       result = subprocess.run("godot3.5 --path " + self.launcher_path + " --export Windows " + path + "\\AUTO-SIM.exe --no-window",
                               shell=True, capture_output=True, text=True)
       print(result.stderr)
    def compile_visualier(self, path):
        print("################# Visualiser ###################")
        output_path = path + "\\Files\\AUTO-SIM-Visualiser"
        os.makedirs(output_path, exist_ok=True)
        result = subprocess.run("godot --path " + self.visualiser_path + "\ --export-debug python_export " + output_path + "\\AUTO-SIM-Visualiser.dll --no-window",
                                shell=True, capture_output=True, text=True)
        print(result.stderr)
    def compile_simulator(self, path):
        print("################# Simulator ###################")
        output_path = path + "\\Files"
        os.makedirs(output_path, exist_ok=True)
        result = subprocess.run("pyinstaller --noconfirm --onedir --console " + \
        "--add-data C:/Users/njones/Documents/GitHub/Aurrigo_FMS_Simulator/Assets;Assets/ " + \
        "--add-data C:/Users/njones/Documents/GitHub/Aurrigo_FMS_Simulator/customtkinter;customtkinter " + \
        "--hidden-import babel.numbers " + \
        self.simulator_path + "\\AUTO_SIMULATOR.py " +\
        "--distpath " + output_path, shell=True, capture_output=True, text=True)

        print(result.stderr)
    def create_installer(self, path):
        print("################# Create Installer ###################")
        command = "iscc.exe " + path + "\\AutoSimInstallerScript.iss"
        result = subprocess.run(command)
        print (result.stdout)
        print(result.stderr)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = AutoSimCompiler()
    app.mainloop()

