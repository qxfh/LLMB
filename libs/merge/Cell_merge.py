import copy

class Merge:
    def __init__(self, cell_summary, material_summary):
        self.cell_summary = cell_summary
        self.material_summary = material_summary
        self.merge_summary = self.merge_cell_material_summary()
    
    def merge_cell_material_summary(self):
        # Helper function to create a dictionary for faster lookup
        def create_lookup_dict(material_summary, material_type, cell_summary):
            lookup_dict = {}
            if material_type == 'current_collector':
                for material in material_summary[material_type]:
                    key = material['name_cell']
                    lookup_dict[key] = material
                    
            elif material_summary[material_type] == []:
                pass
            
            elif material_summary[material_type][0].get('name_cell'):
                for material in material_summary[material_type]:
                    key = material['name_cell']
                    material_new = copy.deepcopy(material)
                    material_new.pop('name_cell', None)
                    lookup_dict[key] = material_new
                    
            else:
                for material in material_summary[material_type]:
                    key = material[f'name_{material_type}']
                    lookup_dict[key] = material
            return lookup_dict

        # Create lookup dictionaries for each material type
        lookup_dicts = {material_type: create_lookup_dict(self.material_summary, material_type, self.cell_summary) 
                    for material_type in ['cathode', 'electrolyte', 'anode', 'separator', 'current_collector']}

        # Initialize the merged summary
        merged_summary = {}

        # Iterate over each cell in self.cell_summary
        for figure_data in self.cell_summary:
            figure_label = f"{figure_data['graph_data']['figure']}_{figure_data['graph_data']['graph_label']}"
            merged_summary[figure_label] = []

            for cell in figure_data['cell']:
                # Initialize merged cell data
                merged_cell_data = {'name_cell': cell['name_cell']}
                # Merge cathode, electrolyte, anode, and separator based on material name
                for material_type in ['cathode', 'electrolyte', 'anode', 'separator']:
                    name_key = f'name_{material_type}'
                    if cell.get(name_key):
                        material_data = lookup_dicts[material_type].get(cell[name_key])
                        if material_data:
                            merged_cell_data[material_type] = material_data
                        else:
                            merged_cell_data[material_type] = cell[f'name_{material_type}']
                    else:    # Merger None material in cell_summary based on name_cell
                        material_data = lookup_dicts[material_type].get(cell['name_cell'])
                        if material_data:
                            merged_cell_data[material_type] = material_data
                
                # Special case for current_collector
                collector_data = lookup_dicts['current_collector'].get(cell['name_cell'])
                
                if collector_data:
                    merged_cell_data['current_collector'] = {
                        'collector1': collector_data['collector1'],
                        'collector2': collector_data['collector2']
                    }
                else:
                    merged_cell_data['current_collector'] = cell['name_current_collector']
                merged_cell_data["interlayer"] = cell["name_interlayer"]
                merged_cell_data['measurement_condition'] = cell['measurement_condition']
                merged_summary[figure_label].append(merged_cell_data)
        return merged_summary