# Convert to SMILES (PubChem base) 
import pubchempy as pcp
import json

class Get_smiles:
    def __init__(self, name_list):
        self.name_list = name_list
        self.smiles_list, self.smiles_dict, self.none_smiles_list = self.get_smiles_dict()
        #self.smiles_dict = self.get_smiles_dict()[1]
    
    def get_smiles_dict(self):
        cid_list = [] 
        smiles_list = []
        smiles_dict = {}
        none_smiles_name_list = []
        exception_smiles_dict = get_exception_smiles_dict()
        #exception_name = exception_smiles_dict.keys()
        exception_names = exception_smiles_dict.keys()
        for name in self.name_list:
            try:
                name_lower = name.lower()

            except:
                if name == None:
                    smiles_list.append(None)
                    smiles_dict[name] = None
                    continue
            
            if name_lower in exception_names:
                smile = exception_smiles_dict[name_lower]
                smiles_list.append(smile)
                smiles_dict[name] = smile                

            else:
                try:
                    mol = pcp.get_compounds(name, namespace='name')
                    if mol == []:
                        raise
                    cid = mol[0].cid
                    cid_list.append(cid)
                
                    cmpnd = pcp.Compound.from_cid(cid)
                    smile = cmpnd.canonical_smiles
                    smiles_list.append(smile)
                    smiles_dict[name] = smile
    
                except:
                    print("molecule name is not appropriate.")
                    smiles_list.append(None)
                    smiles_dict[name] = None
                    none_smiles_name_list.append(name)
        
        return smiles_list, smiles_dict, none_smiles_name_list
    
def get_exception_smiles_dict():
    with open('SMILES/smiles_dict.json', 'r') as file:
        exception_smiles_dict = json.load(file)
    exception_smiles_dict_lower = {key.lower(): value for key, value in exception_smiles_dict.items()}
    return exception_smiles_dict_lower
