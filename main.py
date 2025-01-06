import tkinter as tk
from tkinter import ttk, messagebox
from entity_block import create_entity_block,create_enum_block
from entity_logic import generate_entities
from jointure_block import add_join_block
import os



class SpringEntityGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Spring Boot Entity Generator")
        
        self.root.geometry("555x400")

        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(fill="x", padx=10, pady=10)
        self.cardinalities = ["*", "1"]
        self.directions = ["<-","->", "<->"]
        # Entity Data
        self.entities = []
        self.join_blocks = []
        self.join_value = []
        self.enums_names = []

        self.enums = []

        # Base Path for the project
        self.base_path = tk.StringVar()

        # Project Path Label and Entry
        ttk.Label(self.top_frame, text="Project Path:").pack(side="left", padx=(20, 5), pady=15)
        self.path_entry = ttk.Entry(self.top_frame, textvariable=self.base_path, width=30)
        self.path_entry.pack(side="left", padx=(0, 10), pady=15)

        # Generate Button
        self.generate_button = ttk.Button(self.top_frame, text="Generate", command=self._call_generate_entities)
        self.generate_button.pack(side="left", pady=15)

        # Tab control
        self.tab_control = ttk.Notebook(root)

        self.entity_tab = ttk.Frame(self.tab_control)
        self.join_tab = ttk.Frame(self.tab_control)
        self.schedule_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.entity_tab, text="Entity")
        self.tab_control.add(self.join_tab, text="Join")
        self.tab_control.add(self.schedule_tab, text="Scheduler")

        self.tab_control.pack(expand=1, fill="both")

        

        # Entity tab setup
        self.setup_entity_tab()

        # Join tab setup (can be used in the future)
        self.setup_join_tab()

        # Schedule tab setup (can be used in the future)
        self.setup_schedule_tab()

    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling for the canvas."""
        if event.delta:  # Windows and macOS
            if event.delta > 0:  # Scroll up
                self.canvas.yview_scroll(-1, "units")
            elif event.delta < 0:  # Scroll down
                self.canvas.yview_scroll(1, "units")
        elif event.num in (4, 5):  # Linux (using buttons)
            if event.num == 4:  # Scroll up
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:  # Scroll down
                self.canvas.yview_scroll(1, "units")

    def setup_entity_tab(self):
        """Set up the entity tab components with smooth scrolling and no white border."""
        outer_frame = ttk.Frame(self.entity_tab)
        outer_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(outer_frame, highlightthickness=0)  # Remove white border
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Bind mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows and macOS
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)    # Linux scroll up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)    # Linux scroll down

        # Configure grid layout
        self.scrollable_frame.columnconfigure(1, weight=1)  # Allow column 1 (entry fields) to expand
        self.scrollable_frame.columnconfigure(3, weight=0)  # Prevent button columns from expanding

       

        # Name Label and Entry
        ttk.Label(self.scrollable_frame, text="Name:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entity_name_entry = ttk.Entry(self.scrollable_frame, width=17)  # Adjusted width
        self.entity_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Buttons
        self.add_entity_button = ttk.Button(self.scrollable_frame, text="Add Entity", width=7, command=self.add_entity)
        self.add_entity_button.grid(row=1, column=2, padx=5, pady=5)

        self.add_enum_button = ttk.Button(self.scrollable_frame, text="Add Enum", width=7, command=self.add_enum)
        self.add_enum_button.grid(row=1, column=3, padx=(5,20), pady=5)

        # Entities Frame
        self.entities_frame = ttk.Frame(self.scrollable_frame)
        self.entities_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        

    def _call_generate_entities(self):
        """Call the generate_entities function with necessary arguments."""
        project_path = self.base_path.get()
        print(f"Project Path: {project_path}")  # Check what path is being entered
        if not os.path.exists(project_path):
            messagebox.showerror("Error", "Invalid project path!")
            return
        generate_entities(self, project_path)

    def setup_join_tab(self):
        outer_frame = ttk.Frame(self.join_tab)
        outer_frame.pack(fill="both", expand=True)

        self.canvas_joinb = tk.Canvas(outer_frame, highlightthickness=0)  # Remove white border
        self.canvas_joinb.pack(side="left", fill="both", expand=True)

        self.scrollbar_join = ttk.Scrollbar(outer_frame, orient="vertical", command=self.canvas_joinb.yview)
        self.scrollbar_join.pack(side="right", fill="y")

        self.canvas_joinb.configure(yscrollcommand=self.scrollbar_join.set)
        self.scrollable_frame_join = ttk.Frame(self.canvas_joinb)
        self.canvas_window_join = self.canvas_joinb.create_window((0, 0), window=self.scrollable_frame_join, anchor="nw")

        # Ensure the layout manager handles all widgets well
        self.scrollable_frame_join.columnconfigure(0, weight=1)  # Configure column 0 for expansion
        self.scrollable_frame_join.columnconfigure(1, weight=1)  # For any other dynamic elements

        self.scrollable_frame_join.grid_rowconfigure(0, weight=0)  # Don't let row 0 (the "Add Join" button) expand unnecessarily

        # Button to add a new join row
        self.add_join_button = ttk.Button(self.scrollable_frame_join, text="Add Join", command=self.add_join)
        self.add_join_button.pack(side="top", pady=10, anchor="w")  # Use pack instead of grid
           
        self.join_frame = ttk.Frame(self.scrollable_frame_join)
        self.join_frame.pack(side="top", fill="x", pady=5)

             
        
    

    def setup_schedule_tab(self):
        """Set up the Scheduler tab with cron expression generator."""
        outer_frame = ttk.Frame(self.schedule_tab)
        outer_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer_frame, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Scheduler Inputs
        ttk.Label(scrollable_frame, text="Spring Scheduler Annotation Generator", font=("Arial", 14, "bold")).pack(pady=10)

        def create_dropdown(label, var, values):
            ttk.Label(scrollable_frame, text=label).pack()
            combo = ttk.Combobox(scrollable_frame, textvariable=var, values=values)
            combo.pack()

        second_var = tk.StringVar(value="*")
        minute_var = tk.StringVar(value="*")
        hour_var = tk.StringVar(value="*")
        day_var = tk.StringVar(value="*")
        month_var = tk.StringVar(value="*")
        day_of_week_var = tk.StringVar(value="*")

        create_dropdown("Second (0-59, * for every second):", second_var, [str(i) for i in range(60)] + ["*"])
        create_dropdown("Minute (0-59, * for every minute):", minute_var, [str(i) for i in range(60)] + ["*"])
        create_dropdown("Hour (0-23, * for every hour):", hour_var, [str(i) for i in range(24)] + ["*"])
        create_dropdown("Day of Month (1-31, * for any day):", day_var, [str(i) for i in range(1, 32)] + ["*"])
        create_dropdown("Month (1-12, JAN-DEC, * for any month):", month_var, [str(i) for i in range(1, 13)] + ["*"])
        create_dropdown("Day of the Week (0-7, MON-SUN, * for any day):", day_of_week_var, [str(i) for i in range(8)] + ["*"])

        # Generate Annotation
        result_label = ttk.Label(scrollable_frame, text="", font=("Arial", 10), wraplength=400)
        result_label.pack(pady=10)

        def generate_cron():
            cron_expression = f"@Scheduled(cron = \"{second_var.get()} {minute_var.get()} {hour_var.get()} {day_var.get()} {month_var.get()} {day_of_week_var.get()}\")"
            result_label.config(text=cron_expression)
            root.clipboard_clear()
            root.clipboard_append(cron_expression)
            root.update()
            messagebox.showinfo("Copied to Clipboard", "The annotation has been copied to the clipboard!")

        generate_button = ttk.Button(scrollable_frame, text="Generate Annotation", command=generate_cron)
        generate_button.pack(pady=10)

    


    def add_join(self):
        """Add an entity block dynamically."""
        # Create a new join block and add it to the list
        add_join_block(self , self.join_frame, self.join_blocks, self.join_value)



    def add_entity(self):
        """Add an entity block dynamically."""
        entity_name = self.entity_name_entry.get()
        if not entity_name:
            messagebox.showerror("Error", "Entity name cannot be empty!")
            return
        
        # Create the entity block and add it to the list
        entity_block = {"id_name_entry": "", "id_type_combobox": "", "name": entity_name, "attributes": []}
        self.entities.append(entity_block)  # Add the entity name to the list of entities

        # Create dynamic block for entity
        create_entity_block(self.entities_frame, entity_name, entity_block, self.enums_names)

        # Update all join comboboxes with the latest entities
        self.join_value.append(self.entity_name_entry.get())


    

    def add_enum(self):
        """Add an entity block dynamically."""
        enum_name = self.entity_name_entry.get()
        if not enum_name:
            messagebox.showerror("Error", "Enum name cannot be empty!")
            return

        # Create the entity block and add it to the list
        enum_block = {"name": enum_name, "fields": []}
        self.enums.append(enum_block)
        self.join_value.append(self.entity_name_entry.get())
        self.enums_names.append(self.entity_name_entry.get())



        # Create dynamic block for entity
        create_enum_block(self.entities_frame, enum_name, enum_block)
    
    

    








if __name__ == "__main__":
    root = tk.Tk()
    app = SpringEntityGenerator(root)
    root.mainloop()