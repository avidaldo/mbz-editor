import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from pathlib import Path
import mbz_utils


class MBZEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("MBZ Editor")
        self.root.geometry("600x400")
        self.root.minsize(600, 400)
        
        # Set up the main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # App title
        title_label = ttk.Label(main_frame, text="Moodle Backup File (MBZ) Editor", font=("Helvetica", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_decompress_tab()
        self.create_compress_tab()
        self.create_analyze_tab()
        
        # Status section
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, font=("Helvetica", 10))
        status_label.pack(side=tk.LEFT, pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
        self.progress.pack(side=tk.RIGHT, pady=5)

    def create_decompress_tab(self):
        """Create the decompress tab"""
        decompress_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(decompress_tab, text="Decompress")
        
        # Decompress section
        instructions = ttk.Label(decompress_tab, 
                               text="Select an MBZ file to decompress. The contents will be extracted to a folder.")
        instructions.pack(fill=tk.X, pady=(0, 10))
        
        # File selection
        file_frame = ttk.Frame(decompress_tab)
        file_frame.pack(fill=tk.X, pady=5)
        
        file_label = ttk.Label(file_frame, text="MBZ File:")
        file_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.mbz_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.mbz_file_var, width=40)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_mbz_file)
        browse_btn.pack(side=tk.LEFT)
        
        # Output directory selection
        dir_frame = ttk.Frame(decompress_tab)
        dir_frame.pack(fill=tk.X, pady=5)
        
        dir_label = ttk.Label(dir_frame, text="Output Dir:")
        dir_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.output_dir_var = tk.StringVar()
        dir_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var, width=40)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_dir_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_output_dir)
        browse_dir_btn.pack(side=tk.LEFT)
        
        # Option section
        option_frame = ttk.Frame(decompress_tab)
        option_frame.pack(fill=tk.X, pady=5)
        
        self.open_after_var = tk.BooleanVar(value=True)
        open_after_check = ttk.Checkbutton(option_frame, text="Open folder after extraction", 
                                         variable=self.open_after_var)
        open_after_check.pack(side=tk.LEFT)
        
        # Decompress button
        decompress_btn = ttk.Button(decompress_tab, text="Decompress MBZ File", command=self.decompress_mbz)
        decompress_btn.pack(pady=10)
        
        # Results frame
        result_frame = ttk.LabelFrame(decompress_tab, text="Results", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.decompress_result = scrolledtext.ScrolledText(result_frame, height=5, wrap=tk.WORD)
        self.decompress_result.pack(fill=tk.BOTH, expand=True)

    def create_compress_tab(self):
        """Create the compress tab"""
        compress_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(compress_tab, text="Compress")
        
        # Compress section
        instructions = ttk.Label(compress_tab, 
                               text="Select a folder to compress into an MBZ file for Moodle import.")
        instructions.pack(fill=tk.X, pady=(0, 10))
        
        # Folder selection
        folder_frame = ttk.Frame(compress_tab)
        folder_frame.pack(fill=tk.X, pady=5)
        
        folder_label = ttk.Label(folder_frame, text="Source Folder:")
        folder_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.source_dir_var = tk.StringVar()
        folder_entry = ttk.Entry(folder_frame, textvariable=self.source_dir_var, width=40)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_folder_btn = ttk.Button(folder_frame, text="Browse", command=self.browse_source_dir)
        browse_folder_btn.pack(side=tk.LEFT)
        
        # Output file selection
        out_file_frame = ttk.Frame(compress_tab)
        out_file_frame.pack(fill=tk.X, pady=5)
        
        out_file_label = ttk.Label(out_file_frame, text="Output MBZ:")
        out_file_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.output_file_var = tk.StringVar()
        out_file_entry = ttk.Entry(out_file_frame, textvariable=self.output_file_var, width=40)
        out_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_out_file_btn = ttk.Button(out_file_frame, text="Browse", command=self.browse_output_file)
        browse_out_file_btn.pack(side=tk.LEFT)
        
        # Compress button
        compress_btn = ttk.Button(compress_tab, text="Compress to MBZ File", command=self.compress_to_mbz)
        compress_btn.pack(pady=10)
        
        # Compression warning
        warning_label = ttk.Label(compress_tab, 
                               text="Important: Make sure the folder structure is exactly as extracted,\nwithout extra or missing files to ensure Moodle import works.",
                               foreground="red")
        warning_label.pack(pady=5)
        
        # Results frame
        result_frame = ttk.LabelFrame(compress_tab, text="Results", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.compress_result = scrolledtext.ScrolledText(result_frame, height=5, wrap=tk.WORD)
        self.compress_result.pack(fill=tk.BOTH, expand=True)

    def create_analyze_tab(self):
        """Create the analyze tab"""
        analyze_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(analyze_tab, text="Analyze")
        
        # Analyze section
        instructions = ttk.Label(analyze_tab, 
                               text="Analyze an MBZ file to view its structure and contents.")
        instructions.pack(fill=tk.X, pady=(0, 10))
        
        # File selection
        file_frame = ttk.Frame(analyze_tab)
        file_frame.pack(fill=tk.X, pady=5)
        
        file_label = ttk.Label(file_frame, text="MBZ File:")
        file_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.analyze_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.analyze_file_var, width=40)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(file_frame, text="Browse", 
                               command=lambda: self.browse_file(self.analyze_file_var))
        browse_btn.pack(side=tk.LEFT)
        
        # Analyze button
        analyze_btn = ttk.Button(analyze_tab, text="Analyze MBZ File", command=self.analyze_mbz)
        analyze_btn.pack(pady=10)
        
        # Results frame
        result_frame = ttk.LabelFrame(analyze_tab, text="Analysis Results", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.analyze_result = scrolledtext.ScrolledText(result_frame, height=10, wrap=tk.WORD)
        self.analyze_result.pack(fill=tk.BOTH, expand=True)

    def browse_mbz_file(self):
        """Browse for an MBZ file"""
        file_path = filedialog.askopenfilename(
            title="Select MBZ File",
            filetypes=[("MBZ files", "*.mbz"), ("All files", "*.*")]
        )
        if file_path:
            self.mbz_file_var.set(file_path)

    def browse_output_dir(self):
        """Browse for output directory"""
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir_var.set(dir_path)

    def browse_source_dir(self):
        """Browse for source directory"""
        dir_path = filedialog.askdirectory(title="Select Folder to Compress")
        if dir_path:
            self.source_dir_var.set(dir_path)
            
            # Auto-suggest output MBZ filename based on folder name
            folder_name = os.path.basename(dir_path)
            suggested_output = os.path.join(os.path.dirname(dir_path), f"{folder_name}.mbz")
            self.output_file_var.set(suggested_output)

    def browse_output_file(self):
        """Browse for output MBZ file"""
        file_path = filedialog.asksaveasfilename(
            title="Save MBZ File",
            defaultextension=".mbz",
            filetypes=[("MBZ files", "*.mbz"), ("All files", "*.*")]
        )
        if file_path:
            self.output_file_var.set(file_path)

    def browse_file(self, string_var):
        """Generic file browser that sets the value to the provided StringVar"""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("MBZ files", "*.mbz"), ("All files", "*.*")]
        )
        if file_path:
            string_var.set(file_path)
            
    def decompress_mbz(self):
        """Decompress an MBZ file to a folder"""
        mbz_file = self.mbz_file_var.get()
        output_dir = self.output_dir_var.get()
        open_after = self.open_after_var.get()
        
        if not mbz_file:
            messagebox.showerror("Error", "Please select an MBZ file")
            return
            
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return
        
        self.status_var.set("Decompressing...")
        self.progress.start()
        self.root.update()
        
        try:
            result = mbz_utils.extract_mbz(mbz_file, output_dir, open_after)
            
            if result.startswith("Error:"):
                self.status_var.set("Error occurred")
                self.decompress_result.delete(1.0, tk.END)
                self.decompress_result.insert(tk.END, result)
            else:
                self.status_var.set(f"Successfully decompressed to {result}")
                self.decompress_result.delete(1.0, tk.END)
                self.decompress_result.insert(tk.END, f"MBZ file successfully decompressed to:\n{result}\n\n")
                
                # List XML files
                xml_files = mbz_utils.list_xml_files(result)
                if xml_files:
                    self.decompress_result.insert(tk.END, f"Found {len(xml_files)} XML files:\n")
                    for xml_file in xml_files[:10]:  # Show only first 10
                        rel_path = os.path.relpath(xml_file, result)
                        self.decompress_result.insert(tk.END, f"- {rel_path}\n")
                    
                    if len(xml_files) > 10:
                        self.decompress_result.insert(tk.END, f"... and {len(xml_files) - 10} more XML files")
                
        except Exception as e:
            self.status_var.set("Error occurred")
            self.decompress_result.delete(1.0, tk.END)
            self.decompress_result.insert(tk.END, f"Error: {str(e)}")
        
        finally:
            self.progress.stop()

    def compress_to_mbz(self):
        """Compress a folder to an MBZ file"""
        source_dir = self.source_dir_var.get()
        output_file = self.output_file_var.get()
        
        if not source_dir:
            messagebox.showerror("Error", "Please select a source folder")
            return
            
        if not output_file:
            messagebox.showerror("Error", "Please select an output MBZ file")
            return
        
        # Confirm operation
        if not messagebox.askyesno("Confirm", 
                              "Make sure the folder structure is exactly as extracted, without modifications to the structure.\n\nContinue with compression?"):
            return
        
        self.status_var.set("Compressing...")
        self.progress.start()
        self.root.update()
        
        try:
            success, message = mbz_utils.create_mbz(source_dir, output_file)
            
            self.compress_result.delete(1.0, tk.END)
            
            if success:
                self.status_var.set(f"Successfully compressed to {output_file}")
                self.compress_result.insert(tk.END, f"Folder successfully compressed to:\n{output_file}\n\n")
                
                # Show file size
                file_size = os.path.getsize(output_file)
                size_kb = file_size / 1024
                size_mb = size_kb / 1024
                
                if size_mb >= 1:
                    self.compress_result.insert(tk.END, f"File size: {size_mb:.2f} MB")
                else:
                    self.compress_result.insert(tk.END, f"File size: {size_kb:.2f} KB")
            else:
                self.status_var.set("Error occurred")
                self.compress_result.insert(tk.END, message)
                
        except Exception as e:
            self.status_var.set("Error occurred")
            self.compress_result.delete(1.0, tk.END)
            self.compress_result.insert(tk.END, f"Error: {str(e)}")
        
        finally:
            self.progress.stop()

    def analyze_mbz(self):
        """Analyze an MBZ file"""
        mbz_file = self.analyze_file_var.get()
        
        if not mbz_file:
            messagebox.showerror("Error", "Please select an MBZ file")
            return
        
        self.status_var.set("Analyzing...")
        self.progress.start()
        self.root.update()
        
        try:
            info = mbz_utils.analyze_mbz(mbz_file)
            
            self.analyze_result.delete(1.0, tk.END)
            
            if "error" in info:
                self.status_var.set("Error occurred")
                self.analyze_result.insert(tk.END, f"Error: {info['error']}")
            else:
                self.status_var.set("Analysis complete")
                
                # Format file size
                size_bytes = info["file_size"]
                size_kb = size_bytes / 1024
                size_mb = size_kb / 1024
                
                if size_mb >= 1:
                    size_str = f"{size_mb:.2f} MB"
                else:
                    size_str = f"{size_kb:.2f} KB"
                
                # Display analysis results
                self.analyze_result.insert(tk.END, f"File: {info['file_name']}\n")
                self.analyze_result.insert(tk.END, f"Size: {size_str}\n")
                self.analyze_result.insert(tk.END, f"Valid MBZ: {'Yes' if info['is_valid'] else 'No'}\n")
                self.analyze_result.insert(tk.END, f"Total files: {info.get('total_files', 'Unknown')}\n")
                self.analyze_result.insert(tk.END, f"XML files: {info['xml_files']}\n")
                self.analyze_result.insert(tk.END, f"Top-level items: {info['top_level_items']}\n\n")
                
                # Show some of the contents
                if info['contents']:
                    self.analyze_result.insert(tk.END, "Sample contents:\n")
                    for item in info['contents'][:10]:  # Show first 10 items
                        self.analyze_result.insert(tk.END, f"- {item}\n")
                    
                    if len(info['contents']) > 10:
                        self.analyze_result.insert(tk.END, f"... and more items")
                
        except Exception as e:
            self.status_var.set("Error occurred")
            self.analyze_result.delete(1.0, tk.END)
            self.analyze_result.insert(tk.END, f"Error: {str(e)}")
        
        finally:
            self.progress.stop()


if __name__ == "__main__":
    root = tk.Tk()
    app = MBZEditor(root)
    root.mainloop() 