from tkinter import  messagebox
import os
from jointure_logic import generate_jointure, get_jointure


ENUM_TEMPLATE = """package {package_path}.entity;

public enum {enum_name} {{
    {enum_values}
}}
"""


ENTITY_TEMPLATE = """package {package_path}.entity;
import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.*;

import java.util.Date;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "{entity_name_lower}")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class {entity_name} {{
    @Id
    @GeneratedValue(strategy = GenerationType.{id_type})
    private {id_class_type} {id_name};

{fields}
{jointure}
}}
"""

CONTROLLER_TEMPLATE = """package {package_path}.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;
import {package_path}.entity.{entity_name};
import {package_path}.service.{entity_name}Service;

import java.util.List;

@Tag(name = "Gestion {entity_name}")
@RestController
@AllArgsConstructor
@RequestMapping("/{entity_name_lower}")
public class {entity_name}Controller {{
    private {entity_name}Service service;

    @Operation(description = "Ajout d'un {entity_name} dans la base de données")
    @PostMapping
    public {entity_name} add{entity_name}(@RequestBody {entity_name} {entity_name_lower}) {{
        return service.add{entity_name}({entity_name_lower});
    }}

    @Operation(description = "Récupérer tous les {entity_name}s de la base de données")
    @GetMapping
    public List<{entity_name}> retrieveAll{entity_name}s() {{
        return service.retrieveAll{entity_name}s();
    }}

    @Operation(description = "Modifier un {entity_name} dans la base de données")
    @PutMapping
    public {entity_name} modify{entity_name}(@RequestBody {entity_name} {entity_name_lower}) {{
        return service.modify{entity_name}({entity_name_lower});
    }}

    @Operation(description = "Supprimer un {entity_name} dans la base de données")
    @DeleteMapping("/{id}")
    public void remove{entity_name}(@PathVariable("id") {id_class_type} id) {{
        service.remove{entity_name}(id);
    }}

    @Operation(description = "Rechercher un {entity_name} dans la base de données")
    @GetMapping("/{id}")
    public {entity_name} retrieve{entity_name}(@PathVariable("id") {id_class_type} id) {{
        return service.retrieve{entity_name}(id);
    }}
}}"""

REPOSITORY_TEMPLATE = """package {package_path}.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import {package_path}.entity.{entity_name};

@Repository
public interface {entity_name}Repository extends JpaRepository<{entity_name}, {id_class_type}> {{
    // Add custom queries if needed
}}"""

SERVICE_TEMPLATE = """package {package_path}.service;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import {package_path}.entity.{entity_name};
import {package_path}.repository.{entity_name}Repository;

import java.util.List;

@Service
@AllArgsConstructor
public class {entity_name}Service implements I{entity_name}Service {{
    private {entity_name}Repository repo;

    @Override
    public {entity_name} add{entity_name}({entity_name} {entity_name_lower}) {{
        return repo.save({entity_name_lower});
    }}

    @Override
    public {entity_name} modify{entity_name}({entity_name} {entity_name_lower}) {{
        return repo.save({entity_name_lower});
    }}

    @Override
    public void remove{entity_name}({id_class_type} id) {{
        repo.deleteById(id);
    }}

    @Override
    public {entity_name} retrieve{entity_name}({id_class_type} id) {{
        return repo.findById(id).orElse(null);
    }}

    @Override
    public List<{entity_name}> retrieveAll{entity_name}s() {{
        return repo.findAll();
    }}
}}"""

ISERVICE_TEMPLATE = """package {package_path}.service;

import {package_path}.entity.{entity_name};

import java.util.List;

public interface I{entity_name}Service {{
    List<{entity_name}> retrieveAll{entity_name}s();
    {entity_name} retrieve{entity_name}({id_class_type} id);
    {entity_name} add{entity_name}({entity_name} {entity_name_lower});
    void remove{entity_name}({id_class_type} id);
    {entity_name} modify{entity_name}({entity_name} {entity_name_lower});
}}"""


def extract_package_path(project_path):
    """Extract the package path from the given project path."""
    java_index = project_path.find("java") + len("java")
    package_path = project_path[java_index:].strip(os.sep)
    return package_path.replace(os.sep, ".")




def generate_entities(self,project_path):
    """Generate entity files based on the collected entities."""

    generated_join =  generate_jointure(self.join_blocks)
    

    for entity in self.entities:
        entity_name = entity["name"]
        fields_content = ""

        # Generate entity fields
        for attr in entity["attributes"]:
            attr_name = attr["name"].get()
            attr_type = attr["type"].get()
            if attr_type == "Date":
                fields_content += f"    @Temporal(TemporalType.DATE)\n    private {attr_type} {attr_name};\n"
            elif attr_type not in ["String", "int", "Date", "boolean", "List", "Long"] :
                fields_content += f"    @Enumerated(EnumType.STRING)\n     private {attr_type} {attr_name};\n"
            
        selected_id_type = entity["id_type_combobox"].get()
        id_class_type = "String" if selected_id_type in ["UUID", "AUTO"] else "Long"

        code_for_jointure = get_jointure(entity_name,generated_join)


        # Generate files
        for template, folder, file_suffix in [
            (ENTITY_TEMPLATE, "entity", f"{entity_name}.java"),
            (CONTROLLER_TEMPLATE, "controller", f"{entity_name}Controller.java"),
            (REPOSITORY_TEMPLATE, "repository", f"{entity_name}Repository.java"),
            (SERVICE_TEMPLATE, "service", f"{entity_name}Service.java"),
            (ISERVICE_TEMPLATE, "service", f"I{entity_name}Service.java"),
        ]:
            file_content = template.format(
                package_path=extract_package_path(project_path),
                jointure=code_for_jointure,
                entity_name=entity_name,
                entity_name_lower=entity_name.lower(),
                id_class_type=id_class_type,
                id_type=selected_id_type,
                id_name=entity["id_name_entry"].get(),
                fields=fields_content,
                id=r"{id}",  # Add the missing `id` placeholder

            )
            file_path = os.path.join(project_path, f"{folder}/{file_suffix}")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(file_content)
    for enum_block in self.enums:
        enum_name = enum_block["name"]
        enum_values = ",\n    ".join([field["name"].get() for field in enum_block["fields"]])
        
        enum_content = ENUM_TEMPLATE.format(
            package_path=extract_package_path(project_path),
            enum_name=enum_name,
            enum_values=enum_values,
        )

        enum_file_path = os.path.join(project_path, f"entity/{enum_name}.java")
        os.makedirs(os.path.dirname(enum_file_path), exist_ok=True)
        with open(enum_file_path, "w") as enum_file:
            enum_file.write(enum_content)

    messagebox.showinfo("Success", "Entities and associated files generated successfully!")

def generate_enum(self, project_path):
    """Generate enum files based on the collected enums."""
    for enum_block in self.enums:
        enum_name = enum_block["name"]
        enum_values = ",\n    ".join([field["name"].get() for field in enum_block["fields"]])
        
        enum_content = ENUM_TEMPLATE.format(
            package_path=extract_package_path(project_path),
            enum_name=enum_name,
            enum_values=enum_values,
        )

        enum_file_path = os.path.join(project_path, f"enum/{enum_name}.java")
        os.makedirs(os.path.dirname(enum_file_path), exist_ok=True)
        with open(enum_file_path, "w") as enum_file:
            enum_file.write(enum_content)

    messagebox.showinfo("Success", "Enum files generated successfully!")