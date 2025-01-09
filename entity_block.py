import tkinter as tk
from tkinter import ttk



def create_enum_block(parent_frame, enum_name, enum_block):
    """Create a block for defining an enum."""
    frame = ttk.LabelFrame(parent_frame, text=f"", relief="solid", padding=5)
    frame.pack(fill="x", padx=5, pady=5)

    enum_frame = ttk.Frame(frame)
    enum_frame.pack(fill="x", padx=5, pady=5)

    # Top row: Enum name and buttons
    top_row_frame = ttk.Frame(enum_frame)
    top_row_frame.pack(side="top", fill="x", pady=5)

    ttk.Label(top_row_frame, text=f"Enum: {enum_name}").pack(side="left", padx=5)

    # Buttons for removing the enum block and adding fields
    remove_btn = ttk.Button(top_row_frame, text="Remove Enum", command=lambda: remove_enum(frame, enum_block))
    remove_btn.pack(side="right", padx=5)

    add_field_btn = ttk.Button(top_row_frame, text="Add Enum Field", command=lambda: add_enum_field(enum_frame, enum_block))
    add_field_btn.pack(side="right", padx=5)

    # Enum fields container
    fields_frame = ttk.Frame(enum_frame)
    fields_frame.pack(side="top", fill="x", pady=5)

    # Store fields frame reference in the enum block for adding fields dynamically
    enum_block["fields_frame"] = fields_frame
    enum_block["fields"] = []  # To store individual enum field blocks

    # Store reference for the parent frame
    enum_block["frame"] = frame


def add_enum_field(fields_frame, enum_block):
    """Add a new field to the enum block."""
    field_frame = ttk.Frame(fields_frame)
    field_frame.pack(fill="x", padx=5, pady=2)

    # Enum field name
    ttk.Label(field_frame, text="Field Value:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    field_name_entry = ttk.Entry(field_frame, width=22)
    field_name_entry.grid(row=0, column=1, padx=5, pady=5)
    field_name_entry.insert(0, "FIELD_NAME")

    # Remove field button
    remove_field_btn = ttk.Button(
        field_frame,
        text="Remove Field",
        command=lambda: remove_enum_field(field_frame, enum_block, field_entry)
    )
    remove_field_btn.grid(row=0, column=2, padx=5, pady=5)

    # Add field entry to enum block
    field_entry = {"name": field_name_entry}
    enum_block["fields"].append(field_entry)


def remove_enum(enum_frame, enum_block):
    """Remove the entire enum block."""
    enum_frame.destroy()
    enum_block.clear()


def remove_enum_field(field_frame, enum_block, field_entry):
    """Remove a single field from the enum block."""
    field_frame.destroy()
    enum_block["fields"].remove(field_entry)



def create_entity_block(parent_frame, entity_name, entity_block,enum_names):
    """Create an entity block frame with a label frame for visual effect."""
    frame = ttk.LabelFrame(parent_frame, relief="solid", padding=5)
    frame.pack(fill="x", padx=5, pady=5)
    
    entity_frame = ttk.Frame(frame, width=400)  # Set a fixed width for the entity block
    entity_frame.pack(side="top", fill="x", pady=5)

    # Row 1: Entity name and buttons
    row_frame = ttk.Frame(entity_frame)
    row_frame.pack(side="top", fill="x", pady=5)

    ttk.Label(row_frame, text=f"Entity: {entity_name}").pack(side="left", padx=5)

  
   

    # Buttons: Remove Entity and Add Attribute
    remove_btn = ttk.Button(row_frame, text="Remove Entity", command=lambda: remove_entity(frame, entity_block, id_row_frame))
    remove_btn.pack(side="right", padx=5)

    add_attr_btn = ttk.Button(row_frame, text="Add Attribute", command=lambda: add_attribute_block(entity_frame, entity_block,enum_names))
    add_attr_btn.pack(side="right", padx=5)

    # Row 2: ID Type Label, Combobox and ID Name Textfield
    id_row_frame = ttk.Frame(entity_frame)
    id_row_frame.pack(side="top", fill="x", pady=5)

    # ID Name Label and Textfield
    ttk.Label(id_row_frame, text="ID Name:").pack(side="left", padx=10, pady=5)
    id_name_entry = ttk.Entry(id_row_frame, width=15)
    id_name_entry.pack(side="left", padx=10, pady=5)
    id_name_entry.insert(0, f"id{entity_name}")  # Set a default value for ID name
    type_id_var = tk.StringVar()

    # ID Type Label and Combobox
    ttk.Label(id_row_frame, text="ID Type:").pack(side="left", padx=10, pady=5)
    id_type_combobox = ttk.Combobox(id_row_frame, textvariable=type_id_var, values=["IDENTITY", "AUTO", "SEQUENCE", "UUID"], width=10)
    id_type_combobox.pack(side="left", padx=5, pady=5)
    id_type_combobox.set("IDENTITY")  # Default to IDENTITY

    # Store the ID type selection and ID name entry in the entity block
    entity_block["id_type_combobox"] = type_id_var
    entity_block["id_name_entry"] = id_name_entry

    # Row 3: Attribute Frame (if any)
    attribute_frame = ttk.Frame(entity_frame)
    attribute_frame.pack(side="top", fill="x", pady=5)

    # Store the reference for later use
    entity_block["frame"] = entity_frame

    # Finally, pack the main entity frame
    entity_frame.pack(side="top", fill="x", pady=10)

def add_attribute_block(entity_frame, entity_block,enum_names):
    """Add attribute block to an entity."""
    attr_frame = ttk.Frame(entity_frame)
    attr_frame.pack(fill="x", padx=5, pady=2)

    # Name field
    name_entry = ttk.Entry(attr_frame, width=14)
    name_entry.grid(row=0, column=0, padx=5)
    name_entry.insert(0, "name")

    # Type dropdown
    type_var = tk.StringVar()
   
    type_dropdown = ttk.Combobox(attr_frame, textvariable=type_var, values=["String", "int", "Date", "boolean", "List", "Long"] + enum_names, width=10)
    
    type_dropdown.grid(row=0, column=1, padx=5)
    type_dropdown.set("String")

    

    # Add Attribute button
    add_attr_btn = ttk.Button(attr_frame, text="Remove Attribute", command=lambda: remove_attribute(attr_frame, entity_block, attribute))
    add_attr_btn.grid(row=0, column=3, padx=5)

    

    # Attribute object
    attribute = {"name": name_entry, "type": type_var}
    print(type(attribute))
    entity_block["attributes"].append(attribute)

def remove_entity(entity_frame, entity_block,id_row_frame):
    """Remove entity block."""
    entity_frame.destroy()
    id_row_frame.destroy()
    entity_block["attributes"].clear()
    entity_block["id_name_entry"].clear()
    entity_block["id_type_combobox"].clear()

def remove_attribute(attr_frame, entity_block, attribute):
    """Remove attribute block."""
    attr_frame.destroy()
    entity_block["attributes"].remove(attribute)

