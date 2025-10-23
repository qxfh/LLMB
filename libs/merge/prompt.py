PROMPT_MATCHING_GROUP1_ = '''
Now, you are an expert in the material science, especially specialized in battery.
You must to match "graph_legend" and "cell_name" that refer to the same battery cell.
"graph_legend" and "cell_name" will be given as lists, and the output should be a list of tuples in the form of [index of graph_legend, index of the matching cell_name].

Here is the input
graph_legend: ["graph_legend_1", "graph_legend_2", ...]
cell_name: ["cell_name_1", "cell_name_2", ...]

There is guideline for output below:
output: [[int, int], ...]

You must follow the rules below:
- You must write down each matched index in the output list.
- There may be typos in the given "graph_legend" and "cell_name".
- so Each graph_legend index must be included in the output. 
- Each cell_name must match one graph_legend and must not be duplicated.
- The number of graph_legend is larger than cell_name, so if there is no cell_name similar to a graph_legend, return [graph_legend_index, null].
- There are often cases where the meaning of "@" and "-" in cell_name and fiugre_legend are different. In this case, "@" means chemical composite and "-" means mixture. (CNT@NEC -> CNT,NEC composite, CNT-NEC -> CNT,NEC mixture)

Begin!
graph_legend: ["ZW-COF@CNT", "COF@CNT"]
cell_name: ["S/ZW-COF@CNT Battery at 1C", "S/COF@CNT Battery at 1C", "S/ZW-COF Battery at 1C"]
output: [[0,0],[1,1],[null, 2]]

graph_legend: ["MWCNTs/POW11Mo","MWCNTs","MWCNTs/PW12","MWCNTs/PW10Mo2","PW10Mo2"]
cell_name: ["MWCNTs/PW10Mo2 interlayer Battery","MWCNTs/PW11Mo interlayer Battery","MWCNTs/PW12 interlayer Battery"]
output: [[0,1],[1, null],[2,2],[3,0],[4,null]]

graph_legend: ["0.2C","0.3C","0.5C"]
cell_name: ["CoMoS3.13/SnO2 nanocomposites Battery","pure CoMoS3.13 Battery"]
output: [[0,null],[1,null],[2,null]]

graph_legend: ["1.5LiBOB","Baseline"]
cell_name: ["NC94 cathode with LiBOB additive Battery"]
output: [[0,0],[1,null]]

graph_legend: ["PTFE","PANI","LA132"]
cell_name: ["C-S composite with polyaniline binder Battery","C-S composite with LA132 binder Battery"]
output: [[0,null],[1,0],[2,1]]

graph_legend: {graph_legend}
cell_name: {cell_name}
output:
'''

PROMPT_MATCHING_GROUP3_ = '''
Now, you are an expert in the material science, especially specialized in battery.
You must to match "graph_legend" and "cell_name" that refer to the same battery cell.
"graph_legend" and "cell_name" will be given as lists, and the output should be a list of tuples in the form of [index of graph_legend, index of the matching cell_name].

Here is the input
graph_legend: ["graph_legend_1", "graph_legend_2", ...]
cell_name: ["cell_name_1", "cell_name_2", ...]

There is guideline for output below:
output: [[int, int], ...]

You must follow the rules below:
- You must write down each matched index in the output list.
- There may be typos in the given "graph_legend" and "cell_name".
- Each cell_name index must be included in the output.
- Each graph_legend must match one cell_name and must not be duplicated.
- The number of cell_name is larger than graph_legend, so if there is no graph_legend similar to a cell_name, return [null, cell_name_index].
- There are often cases where the meaning of "@" and "-" in cell_name and fiugre_legend are different. In this case, "@" means chemical composite and "-" means mixture. (CNT@NEC -> CNT,NEC composite, CNT-NEC -> CNT,NEC mixture)

Begin!

graph_legend: ["BDDP/PP","PP"]
cell_name: ["LSBs with PP separators Battery","LSBs with DBDPE/PP separators Battery","LSBs with BDDP/PP separators Battery"]
output: [[0,2],[1,0],[null,1]]

graph_legend: ["BC/S-II"]
cell_name: ["BC/S-III Battery","BC/S-II Battery","BC/S-I Battery"]
output: [[0,1],[null,0],[null,2]]

graph_legend: ["NC-Mg",NC"]
cell_name: ["Mg-doped Ni-rich NC94–Mg Battery","Al-doped LiNi0.92Co0.06Al0.02O2 Battery","F-doped LiNi0.9Co0.05Mn0.05O2−zFz Battery"]
output: [[0,0],[null,1],[null,2]]

graph_legend: ["LiPF6-EC/DEC"]
cell_name: ["S/UMC-3 in carbonate-based electrolyte Battery","S/UMC-3 in ether-based electrolyte Battery"]
output: [[0,1],[null,0]]

graph_legend: ["disharge"]
cell_name: ["Li-Cu Battery","Li-LFP Battery"]
output: [[0,null],[null,null]]

graph_legend: {graph_legend}
cell_name: {cell_name}
output:
'''

PROMPT_MATCHING_GROUP4_ = '''
Now, you are an expert in the material science, especially specialized in battery.
You must to match "graph_legend" and "cell_name" that refer to the same battery cell.
"graph_legend" and "cell_name" will be given as lists, and the output should be a list of tuples in the form of [index of graph_legend, index of the matching cell_name].

Here is the input
graph_legend: ["graph_legend_1", "graph_legend_2", ...]
cell_name: ["cell_name_1", "cell_name_2", ...]

There is guideline for output below:
output: [[int, int], ...]

You must follow the rules below:
- You must write down each matched index in the output list.
- There may be typos in the given "graph_legend" and "cell_name".
- Each cell_name index must be included in the output.
- Each graph_legend must match one cell_name and must not be duplicated.
- The number of cell_name is same as graph_legend
- If there is no graph_legend similar to a cell_name, return [null, cell_name_index]. [same as cell_name]
- There are often cases where the meaning of "@" and "-" in cell_name and fiugre_legend are different. In this case, "@" means chemical composite and "-" means mixture. (CNT@NEC -> CNT,NEC composite, CNT-NEC -> CNT,NEC mixture)

Begin!
graph_legend: ["chargo.490.mm", "charge,740.mm"]
cell_name: ["490 nm PMMA particles Battery", "740 nm PMMA particles Battery"]
output: [[0,0],[1,1]]

graph_legend: [["S/CB", "S/CB-in"]
cell_name: ["VN-NWs interlayer Battery", "Without interlayer Battery"]
output: [[0,1],[1,0]]

graph_legend: ["FT","CVE","SiFT"]
cell_name: ["3x excess Li||NCM811 Battery with SiFT electrolyte","3x excess Li||NCM811 Battery with FT electrolyte","3x excess Li||NCM811 Battery with CVE electrolyte"]
output: [[0,1],[1,2],[2,0]]

graph_legend: ["Li foil","Li@NCNT-3DG"]
cell_name: ["Li@NCNT-3DG||S@3DG Battery","Li||S@3DG Battery"]
output: [[0,1],[1,0]]

graph_legend: ["liquid alloy","pristine electrolyte"]
cell_name: ["Li||LFP Battery with GaSnIn electrolyte additive","Li||LFP Battery with standard carbonate electrolyte"]
output: [[0,0],[1,1]]

graph_legend: {graph_legend}
cell_name: {cell_name}
output:
'''