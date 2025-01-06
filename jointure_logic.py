def generate_jointure(join_blocks):
    # Map cardinalities to JPA annotations
    cardinality_map = {
        ("*", "*"): "@ManyToMany",
        ("1", "*"): "@OneToMany",
        ("*", "1"): "@ManyToOne",
        ("1", "1"): "@OneToOne",
    }

    result = []
    for block in join_blocks:
        entity1 = block["entity1"].get()
        entity2 = block["entity2"].get()
        cardinality1 = block["cardinality1"].get()
        cardinality2 = block["cardinality2"].get()
        direction = block["direction"].get()

        # Determine the appropriate JPA annotation
        cardinality_pair = (cardinality1, cardinality2)
        annotation = cardinality_map.get(cardinality_pair, "Unknown")
        
  

        # Handle bidirectional relationships
        if direction == "<->":
            # Determine owner and mapped side
            

            if cardinality1 == "1" and cardinality2 != "1":
                mapped_entity = entity1.lower()
                mapped_annotation = f'@OneToMany(cascade = CascadeType.ALL, mappedBy="{mapped_entity}")'
                mapped_field_type = f"List<{entity2}>" 
                mapped_field_name = f"{entity2.lower()}s"
                mapped_json_annotations = "@ToString.Exclude\n    @JsonIgnore\n"  
                result.append({
                    "entity name": entity1,
                    "jointure code": f"    {mapped_annotation}\n    {mapped_json_annotations}    private {mapped_field_type} {mapped_field_name};"
                })

                owner_field_type =  entity1
                owner_field_name = entity1.lower()
                owner_annotation = f"@ManyToOne"
                owner_json_annotations =  "" 
                result.append({
                    "entity name": entity2,
                    "jointure code": f"    {owner_annotation}\n    private {owner_field_type} {owner_field_name};"
                })



            elif cardinality1 == "*" and cardinality2 == "*":
                
                mapped_entity = f"{entity2.lower()}s"
                mapped_attributes = ", ".join(filter(None, [f'mappedBy = "{mapped_entity}"']))
                mapped_annotation = f"@ManyToMany({mapped_attributes})" 
                mapped_field_type = f"List<{entity1}>" 
                mapped_field_name = f"{entity1.lower()}s"
                mapped_json_annotations = "@ToString.Exclude\n    @JsonIgnore\n"  
                result.append({
                    "entity name": entity2,
                    "jointure code": f"    {mapped_annotation}\n    {mapped_json_annotations}    private {mapped_field_type} {mapped_field_name};"
                })

                owner_field_type =  f"List<{entity2}>" 
                owner_field_name = f"{entity2.lower()}s"
                owner_annotation = f"@ManyToMany"
                owner_json_annotations =  "@ToString.Exclude\n    @JsonIgnore\n"  
                result.append({
                    "entity name": entity1,
                    "jointure code": f"    {owner_annotation}\n    {owner_json_annotations}    private {owner_field_type} {owner_field_name};"
                })



            else:

                cascade = "cascade = CascadeType.ALL" if flip_annotation(annotation) in ["@OneToOne", "@OneToMany"] else None
                mapped_entity = entity2.lower()
                mapped_annotation = f'{flip_annotation(annotation)}(cascade = CascadeType.ALL, mappedBy="{mapped_entity}")'
                mapped_attributes = ", ".join(filter(None, [f'mappedBy = "{mapped_entity}"', cascade]))
                mapped_field_type = f"List<{entity1}>" if flip_annotation(annotation) in ["@ManyToMany", "@OneToMany"] else entity1
                mapped_field_name = f"{entity1.lower()}s" if flip_annotation(annotation) in ["@ManyToMany", "@OneToMany"] else entity1.lower()
                mapped_json_annotations = "@ToString.Exclude\n    @JsonIgnore\n" if flip_annotation(annotation) in ["@ManyToMany", "@OneToMany"] else "" 
                result.append({
                    "entity name": entity2,
                    "jointure code": f"{mapped_annotation}\n    {mapped_json_annotations}    private {mapped_field_type} {mapped_field_name};"
                })

                cascade = "cascade = CascadeType.ALL" if annotation in ["@OneToOne", "@OneToMany"] else None
                owner_field_type = f"List<{entity2}>" if annotation in ["@ManyToMany", "@OneToMany"] else entity2
                owner_field_name = f"{entity2.lower()}s" if annotation in ["@ManyToMany", "@OneToMany"] else entity2.lower()
                owner_attributes = ", ".join(filter(None, [cascade]))
                owner_annotation = f"{annotation}({owner_attributes})" if owner_attributes else annotation
                owner_json_annotations = "@ToString.Exclude\n    @JsonIgnore\n" if annotation in ["@ManyToMany", "@OneToMany"] else "" 
                result.append({
                    "entity name": entity1,
                    "jointure code": f"    {owner_annotation}\n    {owner_json_annotations}    private {owner_field_type} {owner_field_name};"
                })






        elif direction in ["<-", "->"]:
            cascade = "cascade = CascadeType.ALL" if annotation in ["@OneToOne", "@OneToMany"] else None

            # Handle unidirectional relationships
            if direction == "<-":
                field_type = f"List<{entity1}>" if annotation in ["@ManyToMany", "@OneToMany"] else entity1
                field_name = f"{entity1.lower()}s" if "List" in field_type else entity1.lower()
                owning_entity = entity2
            else:
                field_type = f"List<{entity2}>" if annotation in ["@ManyToMany", "@OneToMany"] else entity2
                field_name = f"{entity2.lower()}s" if "List" in field_type else entity2.lower()
                owning_entity = entity1

            json_annotations = "\n    @ToString.Exclude\n    @JsonIgnore" if annotation in ["@ManyToMany", "@OneToMany"] else ""
            attributes = ", ".join(filter(None, [cascade]))
            join_annotation = f"{annotation}({attributes})" if attributes else annotation
            field_declaration = f"{json_annotations}\n    {join_annotation}\n    private {field_type} {field_name};"

            result.append({
                "entity name": owning_entity,
                "jointure code": field_declaration,
            })

    return result


def flip_annotation(relationship_type: str) -> str:
   
    if relationship_type == "@ManyToOne":
        return "@OneToMany"
    elif relationship_type == "@OneToMany":
        return "@ManyToOne"
    elif relationship_type == "@OneToOne":
        return "@OneToOne"  # OneToOne is its own inverse
    elif relationship_type == "@ManyToMany":
        return "@ManyToMany"  # ManyToMany is its own inverse
    else:
        raise ValueError(f"Unsupported relationship type: {relationship_type}")



def get_jointure(entity_name, jointure_list):
    # Create a dictionary to store jointure codes for each entity name
    jointures = {}

    # Iterate over the jointure list and group jointures by entity name
    for jointure in jointure_list:
        if jointure["entity name"] == entity_name:
            # If the entity name already exists in the dictionary, append the jointure code
            if entity_name in jointures:
                jointures[entity_name] += "\n\n" + jointure["jointure code"]
            else:
                jointures[entity_name] = jointure["jointure code"]

    # Return the jointure code for the given entity name, or an empty string if not found
    return jointures.get(entity_name, "")

