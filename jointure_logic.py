def generate_jointure(join_blocks , project_path):
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
        entity1_lower = entity1[0].lower() + entity1[1:]

        entity2 = block["entity2"].get()
        entity2_lower = entity2[0].lower() + entity2[1:]
        cardinality1 = block["cardinality1"].get()
        cardinality2 = block["cardinality2"].get()
        direction = block["direction"].get()
        actions = block["actions"]()

        # Determine the appropriate JPA annotation
        cardinality_pair = (cardinality1, cardinality2)
        annotation = cardinality_map.get(cardinality_pair, "Unknown")
        
  

        # Handle bidirectional relationships
        if direction == "<->":
            # Determine owner and mapped side
            

            if cardinality1 == "1" and cardinality2 == "*":
                mapped_entity = entity1_lower
                mapped_annotation = f'@OneToMany(cascade = CascadeType.ALL, mappedBy="{mapped_entity}")'
                mapped_field_type = f"List<{entity2}>" 
                mapped_field_name = f"{entity2_lower}s"
                mapped_json_annotations = "@ToString.Exclude\n    @JsonIgnore\n"  
                result.append({
                    "entity name": entity1,
                    "jointure code": f"    {mapped_annotation}\n    {mapped_json_annotations}    private {mapped_field_type} {mapped_field_name};",
                    "assign code": ""
                })

                owner_field_type =  entity1
                owner_field_name = entity1_lower
                owner_annotation = f"@ManyToOne"
                owner_json_annotations =  "" 
                result.append({
                    "entity name": entity2,
                    "jointure code": f"    {owner_annotation}\n    private {owner_field_type} {owner_field_name};",
                     "assign code":generate_affectation(entity2,entity1,"set",project_path,actions)
                })



            elif cardinality1 == "*" and cardinality2 == "*":
                
                mapped_entity = f"{entity2_lower}s"
                mapped_attributes = ", ".join(filter(None, [f'mappedBy = "{mapped_entity}"']))
                mapped_annotation = f"@ManyToMany({mapped_attributes})" 
                mapped_field_type = f"List<{entity1}>" 
                mapped_field_name = f"{entity1_lower}s"
                mapped_json_annotations = "@ToString.Exclude\n    @JsonIgnore\n"  
                result.append({
                    "entity name": entity2,
                    "jointure code": f"    {mapped_annotation}\n    {mapped_json_annotations}    private {mapped_field_type} {mapped_field_name};",
                    "assign code": ""
                })

                owner_field_type =  f"List<{entity2}>" 
                owner_field_name = f"{entity2_lower}s"
                owner_annotation = f"@ManyToMany"
                owner_json_annotations =  "@ToString.Exclude\n    @JsonIgnore\n"  
                result.append({
                    "entity name": entity1,
                    "jointure code": f"    {owner_annotation}\n    {owner_json_annotations}    private {owner_field_type} {owner_field_name};",
                    "assign code":generate_affectation(entity1,entity2,"add",project_path,actions)
                })



            else:
                assign_type = "add" if annotation in ["@ManyToMany", "@OneToMany"] else "set"
                cascade = "cascade = CascadeType.ALL" if flip_annotation(annotation) in ["@OneToOne", "@OneToMany"] else None
                mapped_entity = entity2_lower
                mapped_annotation = f'{flip_annotation(annotation)}(cascade = CascadeType.ALL, mappedBy="{mapped_entity}")'
                mapped_attributes = ", ".join(filter(None, [f'mappedBy = "{mapped_entity}"', cascade]))
                mapped_field_type = f"List<{entity1}>" if flip_annotation(annotation) in ["@ManyToMany", "@OneToMany"] else entity1
                mapped_field_name = f"{entity1_lower}s" if flip_annotation(annotation) in ["@ManyToMany", "@OneToMany"] else entity1_lower
                mapped_json_annotations = "@ToString.Exclude\n    @JsonIgnore\n" if flip_annotation(annotation) in ["@ManyToMany", "@OneToMany"] else "" 
                result.append({
                    "entity name": entity2,
                    "jointure code": f"{mapped_annotation}\n    {mapped_json_annotations}    private {mapped_field_type} {mapped_field_name};",
                    "assign code": ""
                })

                cascade = "cascade = CascadeType.ALL" if annotation in ["@OneToOne", "@OneToMany"] else None
                owner_field_type = f"List<{entity2}>" if annotation in ["@ManyToMany", "@OneToMany"] else entity2
                owner_field_name = f"{entity2_lower}s" if annotation in ["@ManyToMany", "@OneToMany"] else entity2_lower
                owner_attributes = ", ".join(filter(None, [cascade]))
                owner_annotation = f"{annotation}({owner_attributes})" if owner_attributes else annotation
                owner_json_annotations = "@ToString.Exclude\n    @JsonIgnore\n" if annotation in ["@ManyToMany", "@OneToMany"] else "" 
                result.append({
                    "entity name": entity1,
                    "jointure code": f"    {owner_annotation}\n    {owner_json_annotations}    private {owner_field_type} {owner_field_name};",
                    "assign code":generate_affectation(entity1,entity2,assign_type,project_path,actions)
                })






        elif direction in ["<-", "->"]:
            cascade = "cascade = CascadeType.ALL" if annotation in ["@OneToOne", "@OneToMany"] else None

            # Handle unidirectional relationships
            if direction == "<-":
                annotation = flip_annotation(annotation)
                field_type = f"List<{entity1}>" if annotation in ["@ManyToMany", "@OneToMany"] else entity1
                
                field_name = f"{entity1}s" if "List" in field_type else entity1_lower
                owning_entity = entity2
                other_entity = entity1
            else:
                field_type = f"List<{entity2}>" if annotation in ["@ManyToMany", "@OneToMany"] else entity2
                
                field_name = f"{entity2_lower}s" if "List" in field_type else entity2_lower
                owning_entity = entity1
                other_entity = entity2

            assign_type = "add" if annotation in ["@ManyToMany", "@OneToMany"] else "set"
            json_annotations = "\n    @ToString.Exclude\n    @JsonIgnore" if annotation in ["@ManyToMany", "@OneToMany"] else ""
            attributes = ", ".join(filter(None, [cascade]))
            join_annotation = f"{annotation}({attributes})" if attributes else annotation
            field_declaration = f"{json_annotations}\n    {join_annotation}\n    private {field_type} {field_name};"

            result.append({
                "entity name": owning_entity,
                "jointure code": field_declaration,
                "assign code": generate_affectation(owning_entity, other_entity, assign_type, project_path,actions) 
            })

    return result



def generate_affectation(parent: str, child: str, association: str, project_path: str, actions: list[str]) -> dict:
    attribute = {"functions": "", "imports": "", "services": "", "repos": ""}
    functions = "" 
    services = ""
   
    r=r"}"
    l = r"{"
    imports = f"""import {project_path}.repository.{child}Repository;
    import {project_path}.entity.{child};
    """
    
    # Generating imports for affect
    repos = f"""
    private {child}Repository {first_char_lower(child)}Repo;
    """
    # Handle "affect" action
    if "affect" in actions:
        if association == "set":
            # Generating function for service (affect)
            services += f"""
        public {parent} affect{child}To{parent}(Long {first_char_lower(parent)}Id, Long {first_char_lower(child)}Id) {{
            {parent} {first_char_lower(parent)} = {first_char_lower(parent)}Repo.findById({first_char_lower(parent)}Id).orElseThrow(() -> new RuntimeException("{parent} not found"));
            {child} {first_char_lower(child)} = {first_char_lower(child)}Repo.findById({first_char_lower(child)}Id).orElseThrow(() -> new RuntimeException("{child} not found"));
            {first_char_lower(parent)}.set{child}({first_char_lower(child)}); // Set {child} on {parent}
            return {first_char_lower(parent)}Repo.save({first_char_lower(parent)});
        }}
    """ 
        else:
            services += f"""
        public {parent} affect{child}To{parent}(Long {first_char_lower(child)}Id, Long {first_char_lower(parent)}Id) {{
            {parent} {first_char_lower(parent)} = {first_char_lower(parent)}Repo.findById({first_char_lower(parent)}Id).get();
            {child} {first_char_lower(child)} = {first_char_lower(child)}Repo.findById({first_char_lower(child)}Id).get();
            // Add the child to the parent's list
            {first_char_lower(parent)}.get{child}s().add({first_char_lower(child)}); 
            return {first_char_lower(parent)}Repo.save({first_char_lower(parent)});
        }}
    """
        
        
        # Generating function for controller
        functions += f"""
        @PutMapping("affect{child}To{parent}/{l}{parent.lower()}-id{r}/{l}{child.lower()}-id{r}")
        public {parent} affect{child}To{parent}(
                @PathVariable("{parent.lower()}-id") long {first_char_lower(parent)}Id,
                @PathVariable("{child.lower()}-id") long {first_char_lower(child)}Id
        ) {{
            return service.affect{child}To{parent}({first_char_lower(parent)}Id, {first_char_lower(child)}Id);
        }}
    """
        
        
    # Handle "desaffect" action
    if "desaffect" in actions:
        if association == "set":
            # Generating function for desaffect (set to null)
            services += f"""
        public {parent} desaffect{child}From{parent}(Long {first_char_lower(parent)}Id) {{
            {parent} {first_char_lower(parent)} = {first_char_lower(parent)}Repo.findById({first_char_lower(parent)}Id).orElseThrow(() -> new RuntimeException("{parent} not found"));
            {first_char_lower(parent)}.set{child}(null); // Remove {child} from {parent}
            return {first_char_lower(parent)}Repo.save({first_char_lower(parent)});
        }}
    """
        else:
            services += f"""
        public void desaffect{child}From{parent}(Long {first_char_lower(parent)}Id, Long {first_char_lower(child)}Id) {{
            {parent} {first_char_lower(parent)} = {first_char_lower(parent)}Repo.findById({first_char_lower(parent)}Id).get();
            {child} {first_char_lower(child)} = {first_char_lower(child)}Repo.findById({first_char_lower(child)}Id).get();
            // Remove {child} from parent's list
            {first_char_lower(parent)}.get{child}s().remove({first_char_lower(child)}); 
            {first_char_lower(parent)}Repo.save({first_char_lower(parent)});
        }}
    """
        
        # Adding function for desaffect in the controller
        functions += f"""
        @PutMapping("desaffect{child}From{parent}/{l}{parent.lower()}-id{r}/{l}{child.lower()}-id{r}")
        public {parent} desaffect{child}From{parent}(
                @PathVariable("{parent.lower()}-id") long {first_char_lower(parent)}Id,
                @PathVariable("{child.lower()}-id") long {first_char_lower(child)}Id
        ) {{
            return service.desaffect{child}From{parent}({first_char_lower(parent)}Id, {first_char_lower(child)}Id);
        }}
    """

    # Handle "add-affect" action
    if "add-affect" in actions:
        if association == "set":
            # Generating function for add-affect (create new child entity and assign it using set)
            services += f"""
            public {parent} add{child}AndAssign{child}To{parent}({child} {first_char_lower(child)}, Long {first_char_lower(parent)}Id) {{
                {parent} {first_char_lower(parent)} = {first_char_lower(parent)}Repo.findById({first_char_lower(parent)}Id).orElseThrow(() -> new RuntimeException("{parent} not found"));
                {first_char_lower(parent)}.set{child}({first_char_lower(child)}); // Set {child} on {parent}
                return {first_char_lower(parent)}Repo.save({first_char_lower(parent)});
            }}
        """
        else:
            # Generating function for add-affect (create new child entity and add it to a collection)
            services += f"""
            public {parent} add{child}AndAssign{child}To{parent}({child} {first_char_lower(child)}, Long {first_char_lower(parent)}Id) {{
                {parent} {first_char_lower(parent)} = {first_char_lower(parent)}Repo.findById({first_char_lower(parent)}Id).orElseThrow(() -> new RuntimeException("{parent} not found"));
                {first_char_lower(parent)}.get{child}s().add({first_char_lower(child)}); // Add {child} to the list of {parent}
                return {first_char_lower(parent)}Repo.save({first_char_lower(parent)});
            }}
        """
            
            # Adding the function for handling the body (adding a new child and linking it to the parent)
        functions += f"""
            @PostMapping("/add{child}/{l}{parent.lower()}-id{r}")
            public {parent} add{child}AndAssignTo{parent}(
                @RequestBody {child} {first_char_lower(child)}, 
                @PathVariable("{parent.lower()}-id") Long {first_char_lower(parent)}Id) {{
                return service.add{child}AndAssign{child}To{parent}( {first_char_lower(child)}, {first_char_lower(parent)}Id);
            }}
        """
    else:
        imports =""
        repos = ""
    
        
    # Returning the dictionary with generated functions, imports, and services
    attribute = {"functions": functions, "imports": imports, "services": services, "repos": repos}
    
    return attribute


def get_jointure(entity_name, jointure_list):
    # Create dictionaries to store jointure and assignment codes
    jointures = {}
    affect_functions = {}
    affect_imports = {}
    affect_services = {}
    affect_repos = {}

    for jointure in jointure_list:
        if jointure["entity name"] == entity_name:
            # Collect jointure codes
            jointures[entity_name] = jointures.get(entity_name, "") + "\n" + jointure["jointure code"]

            # Collect affectation codes
            assign_code = jointure.get("assign code", {})
            if assign_code:
                affect_functions[entity_name] = affect_functions.get(entity_name, "") + "\n" + assign_code.get("functions", "")
                affect_imports[entity_name] = affect_imports.get(entity_name, "") + "\n" + assign_code.get("imports", "")
                affect_services[entity_name] = affect_services.get(entity_name, "") + "\n" + assign_code.get("services", "")
                affect_repos[entity_name] = affect_repos.get(entity_name, "") + "\n" + assign_code.get("repos", "")

    # Return jointure and affectation codes
    return {
        "jointure": jointures.get(entity_name, ""),
        "functions": affect_functions.get(entity_name, ""),
        "imports": affect_imports.get(entity_name, ""),
        "services": affect_services.get(entity_name, ""),
        "repos": affect_repos.get(entity_name,"")
    }

def first_char_lower(s: str) -> str:
    return s[0].lower() + s[1:] if s else s

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

