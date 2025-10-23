PROMPT_RESULT = '''
Extract the relevant information about the Figure {figure_num} {graph_label}.
Here are the captions and paragraphs related to Figure {figure_num}.

You must follow this rules.
- The information that I want to extract and the desired format are as follows:
output : {{
    "graph_data" : {{
        "figure" : int,
        "graph_label" : str
        }},
    
    "cell" : [{{
        "name_cell" : str,
        "name_cathode" : str,
        "name_electrolyte" : str,
        "name_anode" : str,
        "name_separator" : str,
        "name_current_collector" : str,
        "name_interlayer" : str,
        "measurement_condition":{{
            "C_rate" : [float],
            "current_density" : {{"value" : float, "unit" : str}},
            "temperature" : {{"value" : float, "unit"  : str}}
            }}
        }}, ...]
}}

- Within the paragraphs related to Figure, there might be a mix of explanations for various graphs, like Figure {figure_num}(a) or Figure {figure_num}(b)... you must extract information about Figure {figure_num} {graph_label} from there.
- You must ignore the sentence of supporting information, supplementary fig, and supplementary graph and do not extract "C_rate", "current_density", "temperature" in them.
- You must extract information from Caption and Paragraph. First, you need to understand what needs to be extracted from the Caption, then refer to the Paragraph to extract the final information.
- You must extract "material_name" only the information in Figure {figure_num} {graph_label} paragraph and caption. Clearly separate the sentences corresponding to each figure in the paragraph.
- In the "material_name" field, you must write the names with descriptions that refers to the materials used in the cycle performance experiments, not for each individual component.
(e.g As shown in Fig. 7a, the discharge specific capacity of Li/CSE/NCM811 with PEO electrolyte measured at 25°C is close to 0mAh\g−1. -> "name_electrolyte" : "PEO electrolyte")
- In the case of cathode, if paragraph or caption include active material loading informations, please add that description in the "name_cathode". (e.g. Co/N@HCS/S cathode with a sulfur loading of 2.1 mg cm−2 is capable of delivering an outstanding initial discharge specific capacity of 946 mAh g−1 at 0.1C. -> "name_cathode" : "Co/N@HCS/S cathode with a sulfur loading of 2.1mg cm-2", The long-term stability test at 2C rate demonstrates the original discharge specific capacity for the Co/N@HCS/S cathode, which clearly outperforms the NCM811 cathode (Fig. 6h) -> there are 2 cathodes, each "name_cathode" is Co/N@HCS/S cathode, NCM811 cathode.)
- If the material name contains a '+', it signifies a compound rather than separate substances.
- The battery cell is composed of cathode, electrolyte, anode, separator, and current_collector, typically assembled in coin or pouch cell forms.
- You must write the name of the battery cell in "name_cell", and the name with description of materials that make up the cell (anode, cathode, electrolyte, etc) or measurement condition.
- The separator is usually modifyied based on celgard. The seprator is difference with cathode.
- You must extract each "cell" within the graph. Each cell may have different compositions or measurement_conditions, and the differences must be written in cell_name so that each cell has a different name.
- Sometimes, within a single graph, there are multiple battery cells and each indicated with different C-rates, than extract it each battery cell other. At this time, the name must contain different measurement condition information. 
- When extracting the "C-rate", do not include the initial step or activation step value. In this case, things like pre-, initial or activation cycle will be mentioned nearby. Don't be confused with cases where the respective C-rate for charge and discharge cycle are different.
- You must extract only one value for C_rate. If discharge and charge C_rate appear together, extract only discharge C_rate.
- If C_rate is written in fraction form, convert it to a decimal and extract it in float form. Must not include "/" in "C_rate" value. (ex : 1/8C is extracted to 0.125C)
- When multiple graph labels are grouped together, it implies that information for several graphs is encapsulated within a single sentence. In such cases, it is essential to extract C-rate or temperature-related data individually for each graph label. (e.g. Fig 5. "cycleing test at 0.1C (e-g)" means figure 5(e), 5(f), 5(g) measure at 0.1C.)
- You must not extract loading density or area loading (mg/cm2, mg cm-2) for "current_density". The "current_density" is density of electric current and the unit is usually mAh g-1.
- A room temperature is 25°C.
- Interlayer is not a cathode, anode, electrolyte, seperator, or current collector. The interlayer is an additional membrane that exist separately from the cathode, anode, electrolyte, seperator, and current collector. It does not exist in general and must not be confused with the cathode and separator.
- You must write "null" in cases where the information is not clearly presented.

Begin! 
figure_num : 16
graph_label : a
Caption : 
Fig. 16. (a) The cycle performance of cathode materials at 1\xa0C for 300 cycles, (b) the rate performance of cathode materials at different current densities.
Paragraph : 
paragraph: Fig. 16 a shows the cycle performance of cathodes of 5.0 E/A ratio at 1\xa0C after activation for 3 cycles at 0.1C. 
The cathode LP11.1 exhibits a higher discharge capacity of 189.5 mAh g−1 at 1\xa0C, which is much higher than that of LP10.5 (164.9 mAh g−1 at 1\xa0C), and LP10.8 (160.9 mAh g−1 at 1\xa0C). Furthermore, the cathode LP11.1 shows excellent cycle stability in long cycling tests with 300 cycles.
The electrolyte to active material (E/A) ratio was kept at 5.0.
The cathode loading density is 2mg cm-2.
Meanwhile, the cathode LP11.1 also exhibits excellent rate performance compared with other cathodes as shown in Fig. 16b. 
The pouch cell (Supplementary Fig. S12) with ZnO saturated electrolyte, which achieves a discharge capacity of ~550\u2009mA\u2009h/g at 0.25C for >640 cycles (64 days) and 50 cycles, respectively.
In addition, a comparison of this work with other excellent works is conducted to help objectively evaluate this work. As shown in Table 3 , 
the results achieved by simply adjusting the pH are close to or even exceed these ingenious designs. 
Therefore, investigating the effect of pH on the growth of precursors is helpful to improve the electrochemical performance of subsequent cathode materials.

output : 
{{
    "graph_data" : {{
        "figure" : 16,
        "graph_label" : "a"
        }},

    "cell" : [{{
        "name_cell" : "cathode LP11.1 Battery",
        "name_cathode" : "LP11.1 (189.5 mAh g−1 at 1 C)",
        "name_electrolyte" : null,
        "name_anode" : null,
        "name_separator" : null,
        "name_current_collector" : null,
        "name_interlayer" : null,
        "measurement_condition": {{
            "C_rate": [1.0],
            "current_density": {{"value": null, "unit": null}},
            "temperature": {{"value": null, "unit": null}}
            }}      
        }},
        {{
        "name_cell" : "cathode LP10.5 Battery",
        "name_cathode" : "LP10.5 (164.9 mAh g−1 at 1 C)",
        "name_electrolyte" : null,
        "name_anode" : null,
        "name_separator" : null,
        "name_current_collector" : null,
        "name_interlayer" : null,
        "measurement_condition": {{
            "C_rate": [1.0],
            "current_density": {{"value": null, "unit": null}},
            "temperature": {{"value": null, "unit": null}}
            }}
        }},
        {{
        "name_cell" : "cathode LP10.8 Battery",
        "name_cathode" : "LP10.8 (160.9 mAh g−1 at 1 C)",
        "name_electrolyte" : null,
        "name_anode" : null,
        "name_separator" : null,
        "name_current_collector" : null,
        "name_interlayer" : null,
        "measurement_condition": {{
            "C_rate": [1.0],
            "current_density": {{"value": null, "unit": null}},
            "temperature": {{"value": null, "unit": null}}
            }}        
        }}]
}}

figure_num : 3
graph_label : b
Caption :
Fig. 3 The electrochemical measurement of SACs-Ni-NC cathode at areal loading (1.5 and 9.5\xa0mg cm−2) and lean E/S ratio (25 and 3.9): (b) the cycling performance, (c) the corresponding GCD curves at 0.2\xa0C and (d) long-term cycling performance under high areal loading (6.2 and 9.5\xa0mg cm−2) at 2.0\xa0C. (e) The spider chart of device performances enabled by the single-atom in comparison with Li−S systems.
paragraph: As shown in Fig.\xa03b, S@SACs-Ni-NC cathodes with different areal loading were prepared by adjusting the thickness of coating paste. Apart from that, according to the different areal loading and liquid sulfur ratio, the extreme condition of 9.5\xa0mg cm−2, the initial areal capacity can reach 6.96\xa0mA h cm−2.

output : 
{{
    "graph_data": {{
        "figure": 3, 
        "graph_label": "b"
    }},
  
    "cell": [{{
        "name_cell": "S@SACs-Ni-NC 1.5mg cm−2 and 25 E/S ratio Battery",
        "name_cathode": "S@SACs-Ni-NC 1.5mg cm−2 areal loading and 25 E/S ratio",
        "name_electrolyte": null,
        "name_anode": null,
        "name_separator": null,
        "name_current_collector": null,
        "name_interlayer" : null,
        "measurement_condition": {{
            "C_rate": [0.2],
            "current_density": {{"value": null, "unit": null}},
            "temperature": {{"value": null, "unit": null}}
        }}
    }},
    {{
        "name_cell": "S@SACs-Ni-NC 9.5mg cm−2 and 3.9 E/S ratio  Battery",
        "name_cathode": "S@SACs-Ni-NC 9.5mg cm−2 areal loading and 3.9 E/S ratio",
        "name_electrolyte": null,
        "name_anode": null,
        "name_separator": null,
        "name_current_collector": null,
        "name_interlayer" : null,
        "measurement_condition": {{
            "C_rate": [0.2],
            "current_density": {{"value": null, "unit": null}},
            "temperature": {{"value": null, "unit": null}}
        }}
    }}]
}}

figure_num : 5
graph_label : d
Caption : Fig.\u00a05. (a) The 1st cycle charge and discharge profiles of S@CNCF-3-800 composite at 0.2, 0.5, 1, 2 and 5\u00a0C rates. (b) Typical charge and discharge curves of S@CNCF-3-800 composite for the 1st, 20th, 40th, 60th, 80th, and 100th cycles at a current of 0.2C. (c) Cycling performances and Coulombic efficiencies of S@CNCF-3-800 composite at 0.2 and 0.5\u00a0C rates. (d) Cycling performances and Coulombic efficiencies of S@CNCF-3-800 composite at 1, 2 and 5\u00a0C rates.
Paragraph : The above study indicates that S@CFNC-3-800 composites are optimal to be used as cathodes for Li\u2013S batteries. Fig.\u00a05d shows the superior cycling stability of the composite cathode at high current densities of 1, 2 and 5C. After 500 cycles, the discharge capacity still retained 673, 565 and 367\u00a0mAh g\u22121 at 1, 2 and 5C, respectively.
output : 
{{
    "graph_data": {{
        "figure": 5, 
        "graph_label": "d"
    }},
    
    "cell": [{{
        "name_cell": "S@CFNC-3-800 Battery at 1C",
        "name_cathode": "S@CFNC-3-800 composite",
        "name_electrolyte": null,
        "name_anode": null,
        "name_separator": null,
        "name_current_collector": null,
        "name_interlayer": null,
        "measurement_condition": {{"C_rate": [1.0],
        "current_density": {{"value": null, "unit": null}},
        "temperature": {{"value": null, "unit": null}}
         }}
    }},
    {{
        "name_cell": "S@CFNC-3-800 Battery at 2C",
        "name_cathode": "S@CFNC-3-800 composite",
        "name_electrolyte": null,
        "name_anode": null,
        "name_separator": null,
        "name_current_collector": null,
        "name_interlayer": null,
        "measurement_condition": {{"C_rate": [2.0],
        "current_density": {{"value": null, "unit": null}},
        "temperature": {{"value": null, "unit": null}}
         }}
    }},
    {{
        "name_cell": "S@CFNC-3-800 Battery at 5C",
        "name_cathode": "S@CFNC-3-800 composite",
        "name_electrolyte": null,
        "name_anode": null,
        "name_separator": null,
        "name_current_collector": null,
        "name_interlayer": null,
        "measurement_condition": {{"C_rate": [5.0],
        "current_density": {{"value": null, "unit": null}},
        "temperature": {{"value": null, "unit": null}}
         }}
    }}]
}}

figure_num : 4
graph_label : c
Caption : Fig. 4. (a) CV curve of ZIF-7@CNF at 0.1 mV s−1; (b) Charge/discharge curves of ZIF-7@CNF at 0.2 C; (c) Cycling at 0.2 C and (d) Rate performance of ZIF-7@CNF, ZnO@CNF and without interlayer; (e) Charge-discharge curve of ZIF-7@CNF at different rates; (f) EIS of working electrodes and (g) Long-term cycling performance of ZIF-7@CNF, ZnO@CNF and without interlayer at 1 C; (h) Cycle stability of the cell with ZIF-7@CNF interlayer under high sulfur loading at 0.2 C.
Paragraph : It also shows that there is only a slight capacity decrease of the cell, indicating that the ZIF-7@CNF interlayer can efficiently suppress the LiPs shuttle effect. This is also confirmed by the cycling performance of the cell at 0.2 C (Fig. 4c). One can see that the first discharge specific capacity of Li-S batteries using ZIF-7@CNF interlayer is 1226.9 mAh g−1, which is higher than that with ZnO@CNF interlayer (1107.7 mAh g−1) and without interlayer (989.5 mAh g−1). In addition, for the Li-S batteries using ZIF-7@CNF interlayer, the capacity retention can still reach 89% after 100 cycles, and the Coulomb is close to 100%. This suggests that the addition of ZIF-7@CNF interlayer significantly promoted the physical and chemical adsorption of LiPs, and therefore benefits the cycling performance of Li-S batteries
output :
{{
    'graph_data': {{'figure': 4, 'graph_label': 'c'}},
    'cell': [{{'name_cell': 'ZIF-7@CNF interlayer Battery',
        'name_cathode': None,
        'name_electrolyte': None,
        'name_anode': None,
        'name_separator': None,
        'name_current_collector': None,
        'name_interlayer': 'ZIF-7@CNF interlayer',
        'measurement_condition': {{'C_rate': [0.2],
            'current_density': {{'value': None, 'unit': None}},
            'temperature': {{'value': None, 'unit': None}}}}}},
   {{'name_cell': 'ZnO@CNF interlayer Battery',
        'name_cathode': None,
        'name_electrolyte': None,
        'name_anode': None,
        'name_separator': None,
        'name_current_collector': None,
        'name_interlayer': 'ZnO@CNF interlayer',
        'measurement_condition': {{'C_rate': [0.2],
            'current_density': {{'value': None, 'unit': None}},
            'temperature': {{'value': None, 'unit': None}}}}}},
   {{'name_cell': 'Without interlayer Battery',
        'name_cathode': None,
        'name_electrolyte': None,
        'name_anode': None,
        'name_separator': None,
        'name_current_collector': None,
        'name_interlayer': None,
        'measurement_condition': {{'C_rate': [0.2],
            'current_density': {{'value': None, 'unit': None}},
            'temperature': {{'value': None, 'unit': None}}}}}}]}}

figure_num : {figure_num}
graph_label : {graph_label}
Caption : {caption}
Paragraph : {paragraph}
output : 
'''

PROMPT_RESULT_REDUCE_TOKEN = '''
Extract the relevant information about the Figure {figure_num} {graph_label}.
Here are the captions and paragraphs related to Figure {figure_num}.

You must follow this rules.
- The information that I want to extract and the desired format are as follows:
output : {{
    "graph_data" : {{
        "figure" : int,
        "graph_label" : str
        }},
    
    "cell" : [{{
        "name_cell" : str,
        "name_cathode" : str,
        "name_electrolyte" : str,
        "name_anode" : str,
        "name_separator" : str,
        "name_current_collector" : str,
        "name_interlayer" : str,
        "measurement_condition":{{
            "C_rate" : [float],
            "current_density" : {{"value" : float, "unit" : str}},
            "temperature" : {{"value" : float, "unit"  : str}}
            }}
        }}, ...]
}}

- Within the paragraphs related to Figure, there might be a mix of explanations for various graphs, like Figure {figure_num}(a) or Figure {figure_num}(b)... you must extract information about Figure {figure_num} {graph_label} from there.
- You must ignore the sentence of supporting information, supplementary fig, and supplementary graph and do not extract "C_rate", "current_density", "temperature" in them.
- You must extract information from Caption and Paragraph. First, you need to understand what needs to be extracted from the Caption, then refer to the Paragraph to extract the final information.
- You must extract "material_name" only the information in Figure {figure_num} {graph_label} paragraph and caption. Clearly separate the sentences corresponding to each figure in the paragraph.
- In the "material_name" field, you must write the names with descriptions that refers to the materials used in the cycle performance experiments, not for each individual component.
(e.g As shown in Fig. 7a, the discharge specific capacity of Li/CSE/NCM811 with PEO electrolyte measured at 25°C is close to 0mAh\g−1. -> "name_electrolyte" : "PEO electrolyte")
- In the case of cathode, if paragraph or caption include active material loading informations, please add that description in the "name_cathode". (e.g. Co/N@HCS/S cathode with a sulfur loading of 2.1 mg cm−2 is capable of delivering an outstanding initial discharge specific capacity of 946 mAh g−1 at 0.1C. -> "name_cathode" : "Co/N@HCS/S cathode with a sulfur loading of 2.1mg cm-2", The long-term stability test at 2C rate demonstrates the original discharge specific capacity for the Co/N@HCS/S cathode, which clearly outperforms the NCM811 cathode (Fig. 6h) -> there are 2 cathodes, each "name_cathode" is Co/N@HCS/S cathode, NCM811 cathode.)
- If the material name contains a '+', it signifies a compound rather than separate substances.
- The battery cell is composed of cathode, electrolyte, anode, separator, and current_collector, typically assembled in coin or pouch cell forms.
- You must write the name of the battery cell in "name_cell", and the name with description of materials that make up the cell (anode, cathode, electrolyte, etc) or measurement condition.
- You must extract each "cell" within the graph. Each cell may have different compositions or measurement_conditions, and the differences must be written in cell_name so that each cell has a different name.
- Sometimes, within a single graph, there are multiple battery cells and each indicated with different C-rates, than extract it each battery cell other. At this time, the name must contain different measurement condition information. 
- When extracting the "C-rate", do not include the initial step or activation step value. In this case, things like pre-, initial or activation cycle will be mentioned nearby. Don't be confused with cases where the respective C-rate for charge and discharge cycle are different.
- You must extract only one value for C_rate. If discharge and charge C_rate appear together, extract only discharge C_rate.
- If C_rate is written in fraction form, convert it to a decimal and extract it in float form. Must not include "/" in "C_rate" value. (ex : 1/8C is extracted to 0.125C)
- When multiple graph labels are grouped together, it implies that information for several graphs is encapsulated within a single sentence. In such cases, it is essential to extract C-rate or temperature-related data individually for each graph label. (e.g. Fig 5. "cycleing test at 0.1C (e-g)" means figure 5(e), 5(f), 5(g) measure at 0.1C.)
- You must not extract loading density or area loading (mg/cm2, mg cm-2) for "current_density". The "current_density" is density of electric current and the unit is usually mAh g-1.
- A room temperature is 25°C.
- Interlayer is not a cathode, anode, electrolyte, seperator, or current collector. The interlayer is an additional membrane that exist separately from the cathode, anode, electrolyte, seperator, and current collector. It does not exist in general and must not be confused with the cathode and separator.
- You must write "null" in cases where the information is not clearly presented.

Begin! 
figure_num : 16
graph_label : a
Caption : 
Fig. 16. (a) The cycle performance of cathode materials at 1\xa0C for 300 cycles, (b) the rate performance of cathode materials at different current densities.
Paragraph : 
paragraph: Fig. 16 a shows the cycle performance of cathodes of 5.0 E/A ratio at 1\xa0C after activation for 3 cycles at 0.1C. 
The cathode LP11.1 exhibits a higher discharge capacity of 189.5 mAh g−1 at 1\xa0C, which is much higher than that of LP10.5 (164.9 mAh g−1 at 1\xa0C), and LP10.8 (160.9 mAh g−1 at 1\xa0C). Furthermore, the cathode LP11.1 shows excellent cycle stability in long cycling tests with 300 cycles.
The electrolyte to active material (E/A) ratio was kept at 5.0.
The cathode loading density is 2mg cm-2.
Meanwhile, the cathode LP11.1 also exhibits excellent rate performance compared with other cathodes as shown in Fig. 16b. 
The pouch cell (Supplementary Fig. S12) with ZnO saturated electrolyte, which achieves a discharge capacity of ~550\u2009mA\u2009h/g at 0.25C for >640 cycles (64 days) and 50 cycles, respectively.

output : 
{{
    "graph_data" : {{
        "figure" : 16,
        "graph_label" : "a"
        }},

    "cell" : [{{
        "name_cell" : "cathode LP11.1 Battery",
        "name_cathode" : "LP11.1 (189.5 mAh g−1 at 1 C)",
        "name_electrolyte" : null,
        "name_anode" : null,
        "name_separator" : null,
        "name_current_collector" : null,
        "name_interlayer" : null,
        "measurement_condition": {{
            "C_rate": [1.0],
            "current_density": {{"value": null, "unit": null}},
            "temperature": {{"value": null, "unit": null}}
            }}      
        }},
        {{
        "name_cell" : "cathode LP10.5 Battery",
        "name_cathode" : "LP10.5 (164.9 mAh g−1 at 1 C)",
        "name_electrolyte" : null,
        "name_anode" : null,
        "name_separator" : null,
        "name_current_collector" : null,
        "name_interlayer" : null,
        "measurement_condition": {{
            "C_rate": [1.0],
            "current_density": {{"value": null, "unit": null}},
            "temperature": {{"value": null, "unit": null}}
            }}
        }},
        {{
        "name_cell" : "cathode LP10.8 Battery",
        "name_cathode" : "LP10.8 (160.9 mAh g−1 at 1 C)",
        "name_electrolyte" : null,
        "name_anode" : null,
        "name_separator" : null,
        "name_current_collector" : null,
        "name_interlayer" : null,
        "measurement_condition": {{
            "C_rate": [1.0],
            "current_density": {{"value": null, "unit": null}},
            "temperature": {{"value": null, "unit": null}}
            }}        
        }}]
}}

figure_num : 3
graph_label : b
Caption :
Fig. 3 The electrochemical measurement of SACs-Ni-NC cathode at areal loading (1.5 and 9.5\xa0mg cm−2) and lean E/S ratio (25 and 3.9): (b) the cycling performance, (c) the corresponding GCD curves at 0.2\xa0C and (d) long-term cycling performance under high areal loading (6.2 and 9.5\xa0mg cm−2) at 2.0\xa0C. (e) The spider chart of device performances enabled by the single-atom in comparison with Li−S systems.
paragraph: As shown in Fig.\xa03b, S@SACs-Ni-NC cathodes with different areal loading were prepared by adjusting the thickness of coating paste. Apart from that, according to the different areal loading and liquid sulfur ratio, the extreme condition of 9.5\xa0mg cm−2, the initial areal capacity can reach 6.96\xa0mA h cm−2.

output : 
{{
    "graph_data": {{
        "figure": 3, 
        "graph_label": "b"
    }},
  
    "cell": [{{
        "name_cell": "S@SACs-Ni-NC 1.5mg cm−2 and 25 E/S ratio Battery",
        "name_cathode": "S@SACs-Ni-NC 1.5mg cm−2 areal loading and 25 E/S ratio",
        "name_electrolyte": null,
        "name_anode": null,
        "name_separator": null,
        "name_current_collector": null,
        "name_interlayer" : null,
        "measurement_condition": {{
            "C_rate": [0.2],
            "current_density": {{"value": null, "unit": null}},
            "temperature": {{"value": null, "unit": null}}
        }}
    }},
    {{
        "name_cell": "S@SACs-Ni-NC 9.5mg cm−2 and 3.9 E/S ratio  Battery",
        "name_cathode": "S@SACs-Ni-NC 9.5mg cm−2 areal loading and 3.9 E/S ratio",
        "name_electrolyte": null,
        "name_anode": null,
        "name_separator": null,
        "name_current_collector": null,
        "name_interlayer" : null,
        "measurement_condition": {{
            "C_rate": [0.2],
            "current_density": {{"value": null, "unit": null}},
            "temperature": {{"value": null, "unit": null}}
        }}
    }}]
}}

figure_num : 4
graph_label : c
Caption : Fig. 4. (a) CV curve of ZIF-7@CNF at 0.1 mV s−1; (b) Charge/discharge curves of ZIF-7@CNF at 0.2 C; (c) Cycling at 0.2 C and (d) Rate performance of ZIF-7@CNF, and without interlayer;
Paragraph : It also shows that there is only a slight capacity decrease of the cell, indicating that the ZIF-7@CNF interlayer can efficiently suppress the LiPs shuttle effect. This is also confirmed by the cycling performance of the cell at 0.2 C (Fig. 4c).
output :
{{
    'graph_data': {{'figure': 4, 'graph_label': 'c'}},
    'cell': [{{'name_cell': 'ZIF-7@CNF interlayer Battery',
        'name_cathode': None,
        'name_electrolyte': None,
        'name_anode': None,
        'name_separator': None,
        'name_current_collector': None,
        'name_interlayer': 'ZIF-7@CNF interlayer',
        'measurement_condition': {{'C_rate': [0.2],
            'current_density': {{'value': None, 'unit': None}},
            'temperature': {{'value': None, 'unit': None}}}}}},
   {{'name_cell': 'Without interlayer Battery',
        'name_cathode': None,
        'name_electrolyte': None,
        'name_anode': None,
        'name_separator': None,
        'name_current_collector': None,
        'name_interlayer': None,
        'measurement_condition': {{'C_rate': [0.2],
            'current_density': {{'value': None, 'unit': None}},
            'temperature': {{'value': None, 'unit': None}}
        }}
    }}]
}}

figure_num : {figure_num}
graph_label : {graph_label}
Caption : {caption}
Paragraph : {paragraph}
output : 
'''