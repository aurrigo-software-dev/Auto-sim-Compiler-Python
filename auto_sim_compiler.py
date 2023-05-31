import tkinter.filedialog
import subprocess
import os
import shutil
import customtkinter as ctk
from tkinter.font import Font
import sys
from tkinter import filedialog

class AutoSimCompiler(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.deactivate_automatic_dpi_awareness()
        self.title("AUTO-SIM Installation Compiler")
        self.geometry(f"{1000}x{500}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.minsize(1000,500)
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)

        self.launcher_path = ""
        self.visualiser_path = ""
        self.simulator_path = ""
        self.build_folder_path = ""

        #We need multiple things in here:
        #We need to get the path to the Launcher
        #Label: Auto-Sim Launcher (Godot)
        self.auto_sim_launcher_label = ctk.CTkLabel(self, text='Auto Sim Launcher')
        self.auto_sim_launcher_label.grid(row=0, column=0)
        self.auto_sim_launcher_button = ctk.CTkButton(self, text='...', command=lambda: self.GetFilePath('launcher'), width=200)
        self.auto_sim_launcher_button.grid(row=1, column=0)

        self.auto_sim_vis_label = ctk.CTkLabel(self, text='Auto Sim Visualiser')
        self.auto_sim_vis_label.grid(row=2, column=0)
        self.auto_sim_vis_button = ctk.CTkButton(self, text='...', command=lambda: self.GetFilePath('visualiser'), width=200)
        self.auto_sim_vis_button.grid(row=3, column=0)

        self.auto_sim_sim_label = ctk.CTkLabel(self, text='Auto Sim Simulator')
        self.auto_sim_sim_label.grid(row=4, column=0)
        self.auto_sim_sim_button = ctk.CTkButton(self, text='...', command=lambda: self.GetFilePath('simulator'), width=200)
        self.auto_sim_sim_button.grid(row=5, column=0)

        self.auto_sim_get_build_folder_label = ctk.CTkLabel(self, text='Get Build Folder')
        self.auto_sim_get_build_folder_label.grid(row=6, column=0)
        self.auto_sim_get_build_folder_button = ctk.CTkButton(self, text='...', command=lambda: self.GetFilePath('build'), width=200)
        self.auto_sim_get_build_folder_button.grid(row=7, column=0)

        self.auto_sim_version_label = ctk.CTkLabel(self, text='Version No')
        self.auto_sim_version_label.grid(row=8, column=0)

        self.auto_sim_version_entry = ctk.CTkFrame(self, height=30, fg_color='transparent')
        self.auto_sim_version_entry.grid(row=9, column=0)

        self.auto_sim_version_entry.columnconfigure((0,1,2), weight=1)


        self.auto_sim_version_major = tkinter.Spinbox(self.auto_sim_version_entry, width=10)
        self.auto_sim_version_major.grid(row=0, column=0, sticky='nw')

        self.auto_sim_version_major_dot = ctk.CTkLabel(self.auto_sim_version_entry, text=' . ')
        self.auto_sim_version_major_dot.grid(row=0, column=1, sticky='nw')


        self.auto_sim_version_minor = tkinter.Spinbox(self.auto_sim_version_entry, width=10)
        self.auto_sim_version_minor.grid(row=0, column=2, sticky='nw')

        self.auto_sim_version_minor_dot = ctk.CTkLabel(self.auto_sim_version_entry, text=' . ')
        self.auto_sim_version_minor_dot.grid(row=0, column=3, sticky='nw')

        self.auto_sim_version_patch = tkinter.Spinbox(self.auto_sim_version_entry, width=10)
        self.auto_sim_version_patch.grid(row=0, column=4, sticky='nw')


        self.export_button = ctk.CTkButton(self, text='Compile Installer', command=self.ExportSim, width=200)
        self.export_button.grid(row=10, column=0)

        self.console = tkinter.Text(self)
        self.console.grid(row=0, rowspan=11, column=1, sticky='nsew')

        scrollbar = tkinter.Scrollbar(self)

        scrollbar.grid(row=0, column=2, rowspan=11, sticky='nse')

        self.console.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.console.yview)

        self.custom_font = Font(family="Consolas", size=8, weight="normal")
        self.console.configure(font=self.custom_font, bg='black', fg='white')


    def GetFilePath(self, component):
        path = tkinter.filedialog.askdirectory()
        match component:
            case 'launcher':
                self.launcher_path = path
                self.auto_sim_launcher_button.configure(text='Launcher OK', width=200)
            case 'visualiser':
                self.visualiser_path = path
                self.auto_sim_vis_button.configure(text='Visualiser OK', width=200)
            case 'simulator':
                self.simulator_path = path
                self.auto_sim_sim_button.configure(text='Simulator OK', width=200)
            case 'build':
                self.build_folder_path = path
                self.auto_sim_get_build_folder_button.configure(text='Installer OK', width=200)


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
        self.console.insert(tkinter.END, "################# Launcher ###################")
        godot_loc =  os.path.dirname(os.path.abspath(__file__)) + "\\compilers\\godot3.5\\godot"

        result = subprocess.Popen(godot_loc + " --path " + self.launcher_path + " --export Windows " + path + "\\AUTO-SIM.exe --no-window",
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
        with result.stdout:
            for line in iter(result.stdout.readline, ''):
                self.console.insert(tkinter.END, line)
                self.console.see(tkinter.END)
                self.console.update()
        result.wait()


    def compile_visualier(self, path):
        self.console.insert(tkinter.END, "################# Visualiser ###################")
        output_path = path + "\\Files\\AUTO-SIM-Visualiser"
        godot_loc = os.path.dirname(os.path.abspath(__file__)) + "\\compilers\\godot4\\godot"
        os.makedirs(output_path, exist_ok=True)
        result = subprocess.Popen(godot_loc + " --path " + self.visualiser_path + " --export-debug python_export " + output_path + "\\AUTO-SIM-Visualiser.dll --no-window",
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
        with result.stdout:
            for line in iter(result.stdout.readline, ''):
                self.console.insert(tkinter.END, line)
                self.console.see(tkinter.END)
                self.console.update()
        result.wait()

    def compile_simulator(self, path):
        self.console.insert(tkinter.END, "################# Simulator ###################")
        output_path = path + "\\Files"
        os.makedirs(output_path, exist_ok=True)
        result = subprocess.Popen("pyinstaller --noconfirm --onedir --console " + \
        "--add-data C:/Users/njones/Documents/GitHub/Aurrigo_FMS_Simulator/Assets;Assets/ " + \
        "--add-data C:/Users/njones/Documents/GitHub/Aurrigo_FMS_Simulator/customtkinter;customtkinter " + \
        "--hidden-import babel.numbers " + \
        self.simulator_path + "\\AUTO_SIMULATOR.py " +\
        "--distpath " + output_path,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
        with result.stdout:
            for line in iter(result.stdout.readline, ''):
                self.console.insert(tkinter.END, line)
                self.console.see(tkinter.END)
                self.console.update()
        result.wait()

    def create_installer(self, path):
        self.console.insert(tkinter.END, "################# Create Installer ###################")
        inno_loc = os.path.dirname(os.path.abspath(__file__)) + "\\compilers\\inno\\ISCC.exe"
        version = str(self.auto_sim_version_major.get()) + '.' + \
                  str(self.auto_sim_version_minor.get()) + '.' + \
                  str(self.auto_sim_version_patch.get())
        path = path + '\\AutoSimInstallerScript.iss'
        args = "/DMyAppVersion=" + version
        command = "ISCC.exe", path, args
        print(command)
        result = subprocess.Popen(command,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
        with result.stdout:
            for line in iter(result.stdout.readline, ''):
                self.console.insert(tkinter.END, line)
                self.console.see(tkinter.END)
                self.console.update()
        result.wait()

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = AutoSimCompiler()
    app.mainloop()

