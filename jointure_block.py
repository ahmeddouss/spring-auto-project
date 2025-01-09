import tkinter as tk
from tkinter import ttk





def add_join_block(self, join_frame, join_blocks, entities):
    """Add a new row of comboboxes and a Menubutton for a new join."""
    # Track row for new fields
    row_counter = len(join_blocks)
    cardinalities = ["*", "1"]  # Example cardinalities
    directions = ["->", "<->", "<-"]  # Example directions
    actions = ["desaffect", "affect","add-affect"]

    # Create comboboxes for entity 1
    combobox_entity1 = ttk.Combobox(join_frame, values=entities, width=7)
    combobox_entity1.set("Entity 1")
    combobox_entity1.grid(row=row_counter, column=0, padx=5, pady=5)

    # Create comboboxes for cardinality 1
    combobox_cardinality1 = ttk.Combobox(join_frame, values=cardinalities, width=2)
    combobox_cardinality1.set("*")
    combobox_cardinality1.grid(row=row_counter, column=1, padx=2, pady=2)

    combobox_direction = ttk.Combobox(join_frame, values=directions, width=3)
    combobox_direction.set("->")
    combobox_direction.grid(row=row_counter, column=2, padx=3, pady=3)

    

    # Create comboboxes for cardinality 2
    combobox_cardinality2 = ttk.Combobox(join_frame, values=cardinalities, width=2)
    combobox_cardinality2.set("*")
    combobox_cardinality2.grid(row=row_counter, column=3, padx=5, pady=5)

    # Create comboboxes for entity 2
    combobox_entity2 = ttk.Combobox(join_frame, values=entities, width=7)
    combobox_entity2.set("Entity 2")
    combobox_entity2.grid(row=row_counter, column=4, padx=5, pady=5)

    # Create multi-select for direction
    multi_select = MultiSelectCombobox(join_frame, actions)
    multi_select.grid(row=row_counter, column=5, padx=(0,5), pady=5)

    # Add the created fields to the join blocks
    join_block = {
        "entity1": combobox_entity1,
        "cardinality1": combobox_cardinality1,
        "direction": combobox_direction,
        "cardinality2": combobox_cardinality2,
        "entity2": combobox_entity2,
        "actions": multi_select.get_selected_values
          # Get selected actions here
    }
    join_blocks.append(join_block)


class MultiSelectCombobox(ttk.Frame):
    def __init__(self, parent, values, **kwargs):
        super().__init__(parent, **kwargs)
        self.values = values
        self.selected_values = values.copy()  # Initialize with all values selected

        # Button to toggle dropdown
        self.dropdown_button = ttk.Button(
            self, text="Affect ▼", width=7, command=self.toggle_dropdown
        )
        self.dropdown_button.grid(row=0, column=0, padx=5, pady=5)

        # Dropdown frame for checkboxes
        self.dropdown_frame = tk.Frame(self, relief=tk.SOLID, bd=1)
        self.checkboxes = []

        for value in self.values:
            var = tk.BooleanVar(value=True)  # Set initial state to True
            chk = ttk.Checkbutton(self.dropdown_frame, text=value, variable=var, command=self.update_selected)
            chk.pack(anchor='w', padx=5, pady=2)
            self.checkboxes.append((value, var))

        self.dropdown_frame.grid_remove()

    def toggle_dropdown(self):
        if self.dropdown_frame.winfo_ismapped():
            self.dropdown_frame.grid_remove()
        else:
            self.dropdown_frame.grid(row=1, column=0, sticky='ew')

    def update_selected(self):
        self.selected_values = [value for value, var in self.checkboxes if var.get()]

    def get_selected_values(self):
        return self.selected_values