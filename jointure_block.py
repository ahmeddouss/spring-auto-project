import tkinter as tk
from tkinter import ttk



def add_join_block(self , join_frame, join_blocks, entities):
    """Add a new row of comboboxes for a new join."""
    # Track row for new fields
    row_counter = len(join_blocks)
    cardinalities = ["*", "1"]  # Example cardinalities
    directions = ["->", "<->","<-"]  # Example directions

    # Create comboboxes for entity 1
    combobox_entity1 = ttk.Combobox(join_frame, values=self.join_value, width=7)
    combobox_entity1.set("Entity 1")
    combobox_entity1.grid(row=row_counter, column=0, padx=5, pady=5)

    # Create comboboxes for cardinality 1
    combobox_cardinality1 = ttk.Combobox(join_frame, values=cardinalities, width=3)
    combobox_cardinality1.set("*")
    combobox_cardinality1.grid(row=row_counter, column=1, padx=5, pady=5)

    # Create comboboxes for direction
    combobox_direction = ttk.Combobox(join_frame, values=directions, width=13)
    combobox_direction.set("->")
    combobox_direction.grid(row=row_counter, column=2, padx=5, pady=5)

    # Create comboboxes for cardinality 2
    combobox_cardinality2 = ttk.Combobox(join_frame, values=cardinalities, width=3)
    combobox_cardinality2.set("*")
    combobox_cardinality2.grid(row=row_counter, column=3, padx=5, pady=5)

    # Create comboboxes for entity 2
    combobox_entity2 = ttk.Combobox(join_frame, values=entities, width=7)
    combobox_entity2.set("Entity 2")
    combobox_entity2.grid(row=row_counter, column=4, padx=5, pady=5)

    # Add the created fields to the join blocks
    join_block = {
        "entity1": combobox_entity1,
        "cardinality1": combobox_cardinality1,
        "direction": combobox_direction,
        "cardinality2": combobox_cardinality2,
        "entity2": combobox_entity2
    }
    join_blocks.append(join_block)