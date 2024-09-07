import os
# import markdown

def get_instruction_dictionary():
    instruction_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instruction_data")
    instruction_files = [f for f in os.listdir(instruction_dir) if f.endswith('.md') and f != 'compiled_instructions.md']
    
    instructions = {}
    compiled_content = ""

    for file in instruction_files:
        with open(os.path.join(instruction_dir, file), 'r') as f:
            content = f.read()
            key = file[:-3]  # Remove .md extension
            instructions[key] = content
            compiled_content += f"# {key.capitalize()}\n\n{content}\n\n"

    # Save compiled instructions
    with open(os.path.join(instruction_dir, 'compiled_instructions.md'), 'w') as f:
        f.write(compiled_content)

    return instructions


# │   ├── navigation.md
# │   ├── data_presentation.md
# │   ├── authentication.md
# │   ├── marketplace_order_data.md
# │   ├── player_inventory_profile.md
# │   └── generate_instructions.py
