PROMPT_CELL = '''
Here, you need to find {num_of_cells} Lithium metal battery cells. The information provided in each battery cell is listed respectively based on their content.
Extract the material informations {none} related to the battery cell listed in {cell_name} from the given paragraph.
This particular cell is depicted in Fig. {figure_num}_{graph_label}. 
The battery cells comprise {exist} components, and what you need to find is {none}.
Extract the names and descriptions of {none} materials in the following format.

There are guildlines for Json format output:
[
    {{
        "name_cell" : {cell_name[0]},
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
    }}, ...
]

You must follow rules belows:
- The battery cell is composed of cathode, electrolyte, anode, separator, and current_collector, typically assembled in coin or pouch cell forms.
- You must extract each name and description of the parts only when it is exist. Each name must be written the name of each part with description of materials that make up.
- You must refer to {cell_name} and {exist} and extract accordingly.
- The example of the name of Li battery cells are "LiS full cells", "Li||NCM811 pouch cells", "...full cell", "...half cell", etc.
- You must write the name of the battery cell, and the name and description of materials that make up the cell (anode, cathode, electrolyte, etc.).
- You must extract only half-cell (with lithium metal as the counter electrode) or full cell battery configurations not symmetric cells(e.g. Li||Li, SS||SS, ...).
- The separator is a blocking layer.
- You must write the name of the cathode in "name_cathode", and the name with description of materials that make up the cathode. If various cathodes are exist in the paragraph, please include differences between each cathode in the "name_cathode" refer to "name_cell" and paragraph. If the "name_cell" contains informations of the cathode, you must include that in "name_cathode".
- If the information of part doesn't exist in paragraph, please extract null.

- You must extract measurement_condition property refer to the temperature and C rate (current density) when the sentence containing condition property is related to capacity-cycling test.
- You must extract measurement_condition property when the sentence containing condition property is related to cycling test. It is same as electrochemical cycling, cycling performance, cycle-capacity performance, cycle stability test, galvanostatically cycle, galvanostatic charge discharge test, etc.
- You must not extract measurement_condition property about another measurement(rate capability test, Electrochemical Impedance Spectroscopy, Cycle Voltametry test, Li stripping/plating measurement, galvanostatic Li plating/stripping test, charge-discharge profiles, ...).
- Only one of the information, C_rate or current_density, will exist in paragraph, and you need to extract the information of that exist. Vary occasionally, if both exist, please write both information.
- When extracting the "C-rate", do not include the initial step or activation step value. In this case, things like pre-, initial or activation cycle will be mentioned nearby. Don't be confused with cases where the respective C-rate for charge and discharge cycle are different. 
- If there are 2 or more capacity-cycling performance in the paragraph, extract the condition properties corresponding to each.
- If C_rate is written in fraction form, convert it to a decimal and extract it in float form. Must not include "/" in "C_rate" value. (ex : 1/8C is extracted to 0.125C)
- When several graph labels are grouped together, it's possible for multiple pieces of information to be presented within a single sentence. In such instances, there may be multiple C-rate or temperature-related data that needs to be extracted individually for each graph label.
- You must extract "temperature" only when temperature of cycle test is mentioned in the given paragraph. If not mentioned, you have to extract null in "temperature".
- If cycling test is conducted at room temperature, you must extract {{"value" : 25, "unit"  : "°C"}} in "temperature".
- For unknown information, use the value null.

Begin!

paragraph:
Electrochemical characteristics of the prepared nanofibers were evaluated using 2032R type coin cells. A Celgard 2300 membrane served as a separator. A liquid electrolyte with the composition 1\xa0M LiPF6 in ethyl carbonate/diethyl carbonate + 10% fluoroethylene carbonate + 1% vinyl carbonate [14] was purchased from DodoChem Co. Ltd. Asymmetric cells were assembled using Cu foil, Cu@Au foil, or PI@Au film as the working electrode and Li foil as the counter/reference electrode. The plating process was controlled by the electrode capacity while Li stripping was limited by a cut-off potential of 1.0 V. Symmetric Li||Li-type cells were assembled using PI@Au–Li or Cu–Li (pre-deposited at a Li areal capacity of 5 mAh cm−2) as both the working and counter/reference electrodes. The fabricated asymmetric and symmetric cells were cycled at various current densities and plating/stripping areal capacities using a Neware battery test system (Shenzhen, China). An NCM811 cathode with an active material mass fraction of 96% was purchased from Guangdong Canrd New Energy Technology Co., Ltd., and an Al foil CC with a thickness of 8 μm was employed. The mass loading of NCM811 was 32.0 mg cm−2, which corresponded to a high areal capacity of 6.4 mAh cm−2. AF–LMB cells were assembled using the NCM811 cathode and PI@Au film or Cu foil as the anode. Owing to the ultrahigh areal capacity of the cathode, a moderate amount of the electrolyte (10.0 μL mAh−1) was utilized. Galvanostatic charge/discharge tests of the AF–LMB cells were conducted in the voltage range 3.0–4.3 V at 60\xa0°C
num_of_cells: 2
cell_name: 
["AF–LMB with PI@Au Battery", "AF–LMB with Cu Battery"]
exist: 
["name_cathode: NCM811, name_measurement_condition[C_rate]: [1.0]", "name_cathode: NCM811, name_measurement_condition[C_rate]: [2.0]"]
none: 
["name_electrolyte, name_anode, name_separator, name_current_collector, name_measurement_condition[current_density, temperature]", "name_electrolyte, name_anode, name_separator, name_current_collector, name_measurement_condition[current_density, temperature]"]
Json:
[
    {{
        "name_cell" : "AF–LMB with PI@Au Battery",
        "name_cathode" : "NCM811",
        "name_electrolyte" : "liquid electrolyte of 1 M LiPF6 in ethyl carbonate/diethyl carbonate + 10% fluoroethylene carbonate + 1% vinyl carbonate",
        "name_anode" : "PI@Au film",
        "name_separator" : "Celgard 2300 membrane",
        "name_current_collector" : "Al foil",
        "name_interlayer" : null,
        "measurement_condition" : {{
            "C_rate" : [1.0],
            "current_density" : {{"value" : null, "unit" : null}},
            "temperature" : {{"value" : 60, "unit"  : "°C"}}
        }}
    }},
    {{
        "name_cell" : "AF–LMB with Cu Battery",
        "name_cathode" : "NCM811",
        "name_electrolyte" : "liquid electrolyte of 1 M LiPF6 in ethyl carbonate/diethyl carbonate + 10% fluoroethylene carbonate + 1% vinyl carbonate",
        "name_anode" : "Cu foil",
        "name_separator" : "Celgard 2300 membrane",
        "name_current_collector" : "Al foil",
        "name_interlayer" : null,
        "measurement_condition" : {{
            "C_rate" : [2.0],
            "current_density" : {{"value" : null, "unit" : null}},
            "temperature" : {{"value" : 60, "unit"  : "°C"}}
        }}
    }}
]

paragraph: The hierarchical macroporous carbon (MPC) was synthesized as previously reported [31], [32]. Sulfur-loaded MPC (S/MPC) was prepared via calcination of the ball-milled mixture of sulfur and MPC with a mass ratio of 7:3 at 155 °C for 4 h in N2 atmosphere [16]. Coin cells (CR2025) were assembled in an Ar-filled glove box by using a lithium foil as the counter electrode and Celgard 2400 membrane as the separator. The working electrode was prepared by casting the electrode slurry on an Al foil before drying at 60 °C for 12 h in vacuum. The slurry was composed of S/MPC (70 wt.%), super P (20 wt.%), and prepared binder (10 wt.%) in NMP. The sulfur content in cathode was 49 wt.%, measured by the thermogravimetric analyzer.
num_of_cells: 2
cell_name: ["PVDF Binder Batter", "Li+-Nafion Binder Battery"]
exist: ["name_electrolyte: lithiumbis(trifluoromethane sulfonimide) (LiTFSI: 1 mol L−1) and LiNO3 (1 wt.%) in a DOL-DME solution (1:1 ratio in volume, DOL: 1,3-dioxolane, DME: 1,2-dimethoxyethane), name_anode: lithium foil, name_separator: Celgard 2400 membrane, name_current_collector: Al foil, name_interlayer: None, measurement_condition[C_rate: [0.2], temperature: {{value: 25, unit: °C}}]", "name_electrolyte: lithiumbis(trifluoromethane sulfonimide) (LiTFSI: 1 mol L−1) and LiNO3 (1 wt.%) in a DOL-DME solution (1:1 ratio in volume, DOL: 1,3-dioxolane, DME: 1,2-dimethoxyethane), name_anode: lithium foil, name_separator: Celgard 2400 membrane, name_current_collector: Al foil, name_interlayer: None, measurement_condition[C_rate: [0.2], temperature: {{value: 25, unit: °C}}]"]
none: ["name_cathode, name_interlayer, name_measurement_condition[current_density]","name_cathode, name_interlayer, name_measurement_condition[current_density]"]
Json:
[
    {{
        "name_cell" : "PVDF Binder Batter",
        "name_cathode" : "S/MPC with PVDF Binder cathode",
        "name_electrolyte" : "lithiumbis(trifluoromethane sulfonimide) (LiTFSI: 1 mol L−1) and LiNO3 (1 wt.%) in a DOL-DME solution (1:1 ratio in volume, DOL: 1,3-dioxolane, DME: 1,2-dimethoxyethane)",
        "name_anode" : "lithium foil",
        "name_separator" : "Celgard 2400 membrane",
        "name_current_collector" : "Al foil",
        "name_interlayer" : null,
        "measurement_condition" : {{
            "C_rate" : [0.2],
            "current_density" : {{"value" : null, "unit" : null}},
            "temperature" : {{"value" : 25, "unit"  : "°C"}}
        }}
    }},
    {{
        "name_cell" : "Li+-Nafion Binder Battery",
        "name_cathode" : "S/MPC with Li+-Nafion Binder cathode",
        "name_electrolyte" : "lithiumbis(trifluoromethane sulfonimide) (LiTFSI: 1 mol L−1) and LiNO3 (1 wt.%) in a DOL-DME solution (1:1 ratio in volume, DOL: 1,3-dioxolane, DME: 1,2-dimethoxyethane)",
        "name_anode" : "lithium foil",
        "name_separator" : "Celgard 2400 membrane",
        "name_current_collector" : "Al foil",
        "name_interlayer" : null,
        "measurement_condition" : {{
            "C_rate" : [0.2],
            "current_density" : {{"value" : null, "unit" : null}},
            "temperature" : {{"value" : 25, "unit"  : "°C"}}
        }}
    }}
]

paragraph: {paragraph}
num_of_cells: {num_of_cells}
cell_name: {cell_name}
exist: {exist}
none: {none}
Json:
'''

PROMPT_MAJOR_CATEGORIZE = '''You must decide type of paragraph that it should be one or more listed in
["material", "synthesis", "measurement", "else"].

You must follow rules below.
- You must return ["material"] only when the paragraph includes information about "cathode", "anode", "electrolyte", "separator", or "current_collector" that constitute a battery cells.
- You must determine that information about the cathode or electrolyte exists only when there is composition information about the cathode or electrolyte.
- Li foil is commercial anode in Lithium metal battery.
- You must return ["material"] when the paragraph includes information about "Slurry preparation".
- You must return ["synthesis"] only when the paragraph includes several chemical synthesis process and material purchasing.
- Paragraph can have ["material"] and ["synthesis"] simultaneously because they are not independent.
- You must return ["measurement"] only when the paragraph includes measurement of the Electrochemical Impedance Spectroscopy (EIS) and cycling test. Cycling test is same as cycle-capacity performance, cycle stability test, galvanostatically cycle, galvanostatic charge discharge test, etc. 
- When the paragraph does not include material, synthesis and measurement, it means that there is no information. In this case, you must return ["else"].
- You must return ["material"], when the paragraph include sulfur composite material or synthesis.

Begin!

Paragraph: The composite cathode slurry consisted of 80\u00a0wt% HCNF-S composite, 10\u00a0wt% acetylene black and 10\u00a0wt% polyvinylidene fluoride (PVDF) dissolved in N-methyl pyrrolidinone (NMP). The slurry of the cathode was pressed onto a sheet of aluminum foil, dried at 60\u00a0\u00b0C overnight, then the cathode were cut into pellets with a diameter of 1.0\u00a0cm and dried for 12\u00a0h in a vacuum oven at 60\u00a0\u00b0C. The electrolyte used was 1\u00a0M bis(trifluoromethane) sulfonamide lithium salt (LiTFSI, Sigma Aldrich) in a mixed solvent of 1,3-dioxolane (DOL, Acros Organics) and 1,2-dimethoxyethane (DME, Acros Organics) with a volume ratio of 1: 1, including 0.1\u00a0M LiNO3 as an electrolyte additive. Lithium metal was used as counter electrode and reference electrode and celgard-2400 was used as separator. Specific capacity was corrected based on the mass of sulfur, and the typical sulfur mass loading on the electrode was about 1.5\u00a0mg cm\u22122.
List: ["material"]

Paragraph: Slurry preparation was conducted in several steps as summarized in Fig. 1. Firstly, NMC811 and conductive carbon (LITX, Cabot Corporation) powders were submitted to heating treatment at 400 °C for 1 h and 140 °C for 2 h, respectively, under argon atmosphere to remove residual water molecules. Then, NMC811 and conductive carbon (C) were homogeneously mixed in a planetary ball-mill equipment (Retsch, PM 100) using two spheres of 10 mm diameter. Polyvinylidene fluoride (PVDF) binder solution was prepared dissolving PVDF powder (HSV 1810, Arkema) into anhydrous N-methylpyrrolidone (NMP, 99.5 %, Sigma-Aldrich) at 50 °C under magnetically stirring. To reach an optimal dissolution, the PVDF was added slowly into the NMP solution. The weight ratio NMC:C:PVDF used in this work was 90:5:5 and solids: solvent was 1:1 (w/w). The resulting solution was cooled down to room temperature and transferred to a 50 mL mixing vessel.
List: ["material", "synthesis"]

Paragraph: The cycling performances of Li/SSEs/LFP full cells at 1 C were obtained at 30\u2103 with the voltage range from 2.5 to 4.2\u00a0V and the corresponding rate performance was measured from 0.1 C to 1.0 C at 30 \u2103. The cycling performances of Li/SSEs/NCM523 full cells at 1 C were obtained at 30 \u2103 with the voltage range from 3.0 to 4.4\u00a0V. All the electrochemical measurements of the full cell were tested on the LAND CT2001A measurement system.
List: ["measurement"]

Paragraph: Preparation of Ag NWs-modified 3D carbon cloth (Ag NWs/CC): The carbon cloth (CC) was cleaned by ultrasonication with acetone, ethanol and deionized water for 20\u00a0min and dried in a vacuum oven at 80\u00a0\u00b0C. The Ag NWs/EtOH suspension (2\u00a0mg\u00a0mL\u22121) was vacuum-filtrated through CC, in which the CC was used as a filter membrane with a plane size of 2.5\u00a0\u00d7\u00a02.5\u00a0cm. The mass loading of Ag NWs on CC was controlled by varying the volume of Ag NWs/EtOH suspension. Finally, the Ag NWs/CC was dried in vacuum oven at 80\u00a0\u00b0C for 12h.
List: ["synthesis"]

Paragraph: The carbon cloth with the thickness of 0.36\u00a0mm was purchased from Carbon Energy Technology Co., Ltd. Li foil was bought from Guangdong Canrd New Energy Technology Co., Ltd.) Silver nitrate (AgNO3, AR) was purchased from Tianjin YingDa Chemical Reagents Co., Ltd. Copper chloride (CuCl2\u22c52H2O, AR) and polyvinylpyrrolidone (PVP, Mw\u00a0=\u00a058000) were purchased from Macklin. Ethylene glycol (EG, 99.5%) and ethanol (99.7%) were purchased from Tianjin FuChen Chemical Reagents Co., Ltd. Deionized water was prepared by UPT ultrapure water dispenser (UPT-II-20T, Chengdu Chaochun Technology Co., Ltd.). All chemicals in this work were used without further purification.
List: ["synthesis"]

Paragraph: To investigate the electrochemical stability of electrolytes, stainless-steel electrode-based symmetric cells with dmlSPE and SPE were assembled and a linear sweep voltammetry test was conducted. The electrochemical stabilities of dmlSPE and SPE were measured with linear sweep voltammetry at a scanning rate of 1\u00a0mV s\u22121 from 1 to 5.5\u00a0V at 25\u00a0\u00b0C. To evaluate ionic conductivity and Li ion transference number of SPE and dmlSPE, galvanostatic polarization and electrochemical impedance spectrum (EIS, Chenghua, Shanghai) were conducted with stainless steel-based symmetric cells. Then cells were tested by electrochemical impedance spectroscopy with an amplitude voltage adjusted of 5\u00a0mV over the frequency range 105\u20131\u00a0Hz and a temperature range from 0 to 60\u00a0\u00b0C.
List: ["measurement"]

Paragraph: We have employed density functional theory (DFT) calculations to study the absorption of PMTFPS monomer onto Li. A four-layer Li 4 × 4 slab of 15 Å vacuum spacing was constructed to simulate the electrode surface, with the bottom 2.0 layers fixed during structural relaxation. The Perdew-Burke-Ernzerhof methods implemented in the Castep software of Materials Studio was employed. The energy cutoff for expanding electronic wave function and Monkhorst-Pack k-point mesh are 400 eV and 1 × 1 × 1, respectively. The structures were relaxed until all atomic residual forces were no greater than 0.02 eV/Å. The binding energy (Eb) used to determine the adsorbing ability was defined as the difference between the total energy of the monomer molecule-adsorbed system energy (ELi-monomer) and the sum of an isolated monomer molecule (Emonomer) and a clean Li substrate (ELi), i.e., Eb = ELi-monomer − (Emonomer + ELi). The magnitude of the molecular binding energy indicates the interaction between the PMTFPS monomer and Li (110) surfaces. Thus, the more negative the binding energy is, the higher the adoptability of the Li surface to the molecular adsorbate.
List: ["else"]

Paragraph: {paragraph}
List:
'''

PROMPT_SUB_CATEGORIZE = '''
You must decide type of paragraph that it should be one or more listed in 
["cathode", "electrolyte", "anode", "current_collector", "separator", "else"].

You must follow rules below.
- If you find same type in the paragraph, please include once.
- Please extract only the information of lithium metal battery components. 
- Cathode and Anode are a electrode of battery. Cathode is composed by active material, conductive additive, and binder.
- You must extract ["cathode"], when a slurry preparation which contain cathode active material such as NMC, NCM, sulfur, LFP,...
- You must include ["cathode"] or ["electrolyte"] only when composition informations of cathode or electrolyte are mentioned in.
- You must return ["Cathode"], when the paragraph include sulfur composite material or synthesis.
- You must include ["electrolyte"] when the paragraph includes "electrolyte" which consiste of Li-salts and solvents.
- ["current collector"] is the metal foil based on Copper or Aluminium foil which is included in the fabrication of a cell, along with the other components(anode, cathode ...).
- Synthesized anodes or cathodes are typically coated or stacked on the current collector.(e.g. The resulting slurry was cast on the Al foil then dried at 60 °C)
- You must include ["separator"] when cellgard is mentioned in. 
- When the paragraph does not include any of the cathode, electrolyte, anode, current_collector, and separator, it means that there is no information. In this case, you must return ["else"].

Begin!
paragraph: 
In a typical synthesis of MnCO3 microspheres, 0.1352 g MnSO4·H2O was dissolved into the mixed solution of 20 mL deionized water and 5 mL ethanol with vigorous stirring.
At the same time, 0.672 g NaHCO3 was dissolved into 25 mL deionized water. After that, both of two solutions were mixed with stirring for 4 h at room temperature. 
Finally, the product was obtained after washing with distilled water and ethanol for several times. 
To obtain the porous MnO microspheres, the as-prepared MnCO3 microspheres were annealed in an argon atmosphere at 500 °C for 4 h with a heating rate of 5 °C/min.
In a typical synthesis of MnO@C, two steps were taken. The as-obtained MnO was firstly mixed with the oleic acid with a proportion of 0.1 g/mL. 
Then, the mixture was kept stirring magnetically for 24 h at room temperature, and then annealed at 500 °C for 2 h with a heating rate of 5 °C/min in argon atmosphere.
output: ["else"]

paragraph:
Electrochemical measurements of the three electrolytes were conducted in a glove box with 2032-type coin half-cells that had lithium foil as the counter electrode.
The working NCM811 electrodes (supplied by an industrial manufacturer) were prepared as follows: 
a slurry containing 80\u00a0wt% active cathode material, 10\u00a0wt% carbon black (Super P) and 10\u00a0wt% polyvinylidene fluoride (PVDF) in N-methyl-2-pyrrolidone (NMP) was stirred overnight before being coated on aluminum foil and then dried under vacuum at 120\u00a0\u00b0C for 10\u00a0h. 
Finally, cathode sheets with a diameter of 12\u00a0mm were obtained by punching disks.
output: ["anode", "cathode", "current_collector"]

paragraph: 
A Celgard 2400 microporous polypropylene membrane was used as a separator. The carbonate-based electrolyte contained a solution of 1 M LiPF6 in ethylene carbonate/dimethyl carbonate/diethyl carbonate (1:1:1, by wt%). 
These cells were assembled in the glovebox (Super 1220/750, Switzerland) filled with highly pure argon gas (O2 and H2O levels less than 1 ppm). 
The cells were aged for 12 h before the electrochemical measurements to ensure percolation of the electrolyte to electrodes. 
output: ["separator", "electrolyte"]

paragraph: 
The electrochemical measurements of the final cathodes were executed at room temperature by assembling CR2025 coin-type cells. 
The process of preparation for NCM811 cathode included the following steps: 
dissolving polyvinylidene fluoride (PVDF) into N-methyl-2-pyrrolidone (NMP), casting a slurry of 80\xa0wt% active material,
10\xa0wt% Super P carbon black and 10\xa0wt% PVDF onto an aluminum foil, drying the aluminum foil with the coating slurry at 60\xa0°C for 12\xa0h, 
and cutting the aluminum foil into a disk-shape electrode with a diameter of 14\xa0mm. 
The coin-type cells were assembled in a glove box (Vigor LG1200/750\xa0TS) filled with argon, and lithium metal foil was used as the counter electrode.
The separator was a Celgard 2400 polymer membrane. The electrolyte was 1.0\xa0mol\xa0L−1 LiPF6 dissolved in a mixture of ethylene carbonate (EC),
dimethyl carbonate (DMC) and ethyl methyl carbonate (EMC) at a volume ratio of EC: DMC: EMC\xa0=\xa01 : 1: 1. 
To test the cycling performance, cells were galvanostatically cycled between 3.0 and 4.2\u00a0V at 1 C. with the same voltage range, the coin cells were galvanostatically cycled at 0.1 C, 0.5 C, 1 C, 2 C, 5 C, 10 C, and 5 C for the rate performance testing.
output: ["cathode", "anode", "separator", "electrolyte", "current_collector"]

paragraph: {paragraph}
output:
'''

PROMPT_SUB_MEASUREMENT = '''
You must decide type of electrical measurement paragraph that it should be one or more listed in 
["cycle_performance", "EIS", "else"].

You must follow rules below.
- You must return ["EIS"] only when the paragraph include Electrochemical Impedance Spectroscopy (EIS).
- EIS is a technique that measures the impedance of an electrochemical system over a range of frequencies, providing insights into the system's electrical behavior and characteristics. It is commonly used to study the interface between electrodes and electrolytes in batteries. EIS is same as Nyquist plot.

- You must return ["cycle_performance"] only when the paragraph include cycle test.
- The cycle test is a electrochemical performance that measures the charge or discharge capacity of a battery cell in each cycle. It is same as cycle-capacity performance, cycle stability test, galvanostatically cycle, galvanostatic charge discharge test, etc.
- In lithium metal battery, only half-cell (with lithium metal as the counter electrode) or full cell configurations are conducted cycle test.
- Do not confuce with another electrical measurement(rate capability test, Cycle Voltametry test(CV), Li stripping/plating measurement ...) that are not cycle-capacity performance and EIS.
- You must return ["else"] When the paragraph does not include any information of "EIS" and "cycle_performance".

paragraph:
Electrochemical impedance spectroscopy (EIS) was conducted in the frequency range of 105–10−2 Hz with an amplitude of 5 mV characterized by using a CHI 660C instrument. Galvanostatically cycle test was conducted everty cells in 0.1C. All battery testing was conducted at room temperature.
output: ["EIS", "cycle_performance"]

paragraph:
Electrochemical cycling performance of LiFePO4 and NCM811 electrodes (12mm diameter) are all with an areal capacity of 2 mAh cm−2 tested with lithium metal foils with a thickness of 50 μm as counter electrode. Li||NMC811 cells were electrochemically cycled between 2.8 and 4.3 V under a 0.1 C rate for three cycles before cycling at 0.333C rate (1 C = 180mAg−1).
output: ["cycle_performance"]

paragraph:
Li||LiFePO4 cells were cycled in the galvanostatic mode, whereas a voltage range of 2.5–5.0 V was used to gauge the oxidation stabilities of the different electrolytes for which LiFePO4 cathode doesn’t show the extra redox reaction from Fe2+ to Fe3+ above ~3.8 V. For electrochemical rate capabilities of Li||Li4Ti5O12 and Li||NMC811 cells, the areal capacity of 2 mAh cm−2 for Li4Ti5O12 (12mm diameter) and capacity of 2 mAh cm−2 for NMC811 were used with lithium metal foils having a thickness of 250 μm as counter electrode.
output: ["else"]

paragraph: {paragraph}
output:
'''

PROMPT_CELL_TYPE = '''
Extract the relevant information about the cell type mentioned in the paragraph.
There are guildlines for  Json format:
[
    {{
        "name_cell" : str,
        "type" : str, #coin or pouch
    }},...
]

You must follow rules belows:
- For unknown information, use the value null
- The battery only has coin or pouch cell types.
- If the electrode is in a disk or chip form, it is a coin-type cell, and if it is in film form, it is a pouch cell.
- you must write the name of the battery cell, excluding the materials that make up the cell (anode, cathode, electrolyte, etc.), in the name_cell field.

Begin!
paragraph:
To evaluate the electrochemical performance of MnO@C composites and pure MnO, coin-type cells were assembled in an argon-filled glove box. 
For preparing the working electrodes, the active material, carbon black and carboxyl methyl cellulose (CMC) were mixed by a weight ratio of 80:10:10, 
which were dissolved in deionized water and absolute alcohol mixture. The mixture was stirred at a constant speed for 24 h in order to form homogeneous slurry, 
and then uniformly spread on a copper foil. The coated copper foil was cut into round pieces with a diameter of 1 cm, after dried at 60 °C in vacuum overnight.
Json: 
[
    {{
        "name_cell" : "MnO@C composites",
        "type" : "coin"
    }},
    {{
        "name_cell" : "pure MnO",
        "type" : "coin"
    }}
]

paragraph: {paragraph}
output:
'''

PROMPT_CATHODE = '''
Extract the relevant information about the cathode with the names {name_material} mentioned in the paragraph.
There are {name_cell} name of cells are exist.

There are guildlines for output Json format:
[
    {{
        "name_cathode" : {name_material[0]},
        "active_material" : {{"material" : [str,...], "ratio_of_active_material" : [float,...]}},
        "conductive_additive" : str,
        "binder" : str,
        "ratio_of_cathode_weight" : [float, float, float],
        "area loading of active material" : {{"value" : float, "unit" : str}}
    }}, ...
]

You must follow rules belows:
- The "name_cathode" is one of the {name_material}, representing the name of the cathode. You are required to thoroughly investigate all the cathode present here without missing any.
- The cathode is one of the components that make up a battery cell.
- You must refer to everything written in the paragraph and extract the output.
- If the cathode is a sulfur composite material (in a Lithium Sulfur battery), the active material of the cathode consists of sulfur encapsulated within the host material (S@host_material). You must return both components (sulfur and the host material) as the active material. And the ratio_of_active_material is the weight % ratio of each components of sulfur composite, not a ratio of cathode slurry components, such as {{"active_material" : ["S", "host material"], "ratio_of_active_material" : [S weight%, host material weight%]}}. Please extract "ratio_of_active_material" as null when there are no information of ratio_of_active_material. If sulfur composite is synthesized by various synthesizing, each ratio must be calculated complexly to extract the final "ratio_of_active_material".
- Do not confuse host material and conductive additive in lithium sulfur battery. A carbon material such as Kejen black (KB), Super P (SP), carbon black (CB), conductive carbon (C), etc can be used as host material or conductive additive both but the host material encapsulate sulfur using methods such as melt diffusion. ("70 wt% S and 30 wt% cb were mixed and heated at 155°C for 24 h." This heating method is melt diffusion. Extract host material in active material only when it contain sulfur by melt diffusion.) The sulfur cathode is composed of sulfur composite (active material), conductive additive, and binder, and may not contain conductive material (if there are no ratio information of conductive additive, ratio_of_cathode_weight is extracted as active material wt%:0:binder wt%).
- Lithium nickel manganese cobalt oxides is same as NCM or NMC. (e.g. LiNi0.5Mn0.3Co0.2O2 is same with NMC-532, NCM-523, NMC532, NCM523. You must extract LiNi0.5Mn0.3Co0.2O2 in active material field.)
- In cases where two or more constituents appear in the cathode material, a separate cathode was fabricated for each scenario.
- If many active materials are include in paragraph, than there are a number of active materials cathode is exist.
- Binders are typically made of polymers.
- "ratio_of_activate_material" refers to the ratio of active mateiral substances constituting the active material. In the case of sulfur cathode, the ratio must be extracted in that order of sulfur:host material. (e.g. S/CeO2/MXene was mixed CeO2/MXene with S at a mass ratio of 3:7. -> "active_material": {{"material": ["S", "CeO2/MXene"], "ratio_of_active_material": [0.7, 0.3]}})
- The "ratio_of_activate_material" of NCM or NMC active material must be extracted in that order of nickel:manganese:cobalt ratio (e.g. NCM721 -> [0.7:0.1:0.2], NMC721 -> [0.7:0.2:0.1], LiCoO2 (LCO) -> [0:0:1]). NMC811 cathode means the "active material" is LiNi0.8Mn0.1Co0.1O2 and the "ratio_of_active_material" is [0.8,0.1,0.1].
- The "ratio_of_active_material" of LFP (LiFePO4) is 1.
- "ratio_of_cathode_weight" is a mass ratio of the active material, conductive catbon, and binder. And the ratio must be extracted in that order of active material:conductive additive:binder. For substances that do not exist, enter 0 in the ratio. If only active material is exist without conductive additive and binder, the "ratio_of_cathode_weight" is [1:0:0].
- If the "area loading of active material" value is not given as a specific value but is given as a range such as 0.5-2.0 mg/cm2, please return the average value (e.g. The sulfur loading of 1.3-1.5mg\cm2 -> "area loading of active material" : {{"value" : 1.4, "unit" : "mg\cm2"}}).
- If the "area loading of active material" value is mentioned multiple times, extract each with a different cathode.
- active material loading (* mg cm-2) and sulfur ratio (* wt%) is different.
- You must not extract additional layers which coated on the cathode. (e.g. The solution coated on as prepared CNT@S cathode via doctor blade to form ZB/G hybrid layer coated cathode. -> don't extract about ZB/G materials.)
- For unknown information, write null.

Begin!

name_cathode: ['LFP cathode of 3.5mg cm-2 loading', 'NCM721 cathode of 1.5mg cm-2 loading']
Paragraph: The pristine LiFePO4 (LFP) and LiNi0.7Co0.2Mn0.1O2 (NCM721) electrode was prepared as follows: the active material (LFP or NCM721,
80 wt%), acetylene black (AB) (10 wt%) and PVDF (10 wt%) were mixed in NMP. Then, the slurry was spread on aluminum foil, and dried at 80℃
for 12 h.
output: 
[
    {{
        "name_cathode" : "LFP cathode of 3.5mg cm-2 loading",
        "active_material" : {{"material" : ["LiFePO4"], "ratio_of_active_material" : [1]}},
        "conductive_additive" : "acetylene black",
        "binder" : "PVDF",
        "ratio_of_cathode_weight" : [0.8,0.1,0.1],
        "area loading of active material" : {{"value" : 3.5, "unit" : "mg cm-2"}}
    }},
    {{
        "name_cathode" : "LiNi0.7Co0.2Mn0.1O2 (NCM721) electrode",
        "active_material" : {{"material" : "LiNi0.7Co0.2Mn0.1O2 (NCM721)", "ratio_of_active_material" : [0.7,0.1,0.2]}},
        "conductive_additive" : "acetylene black",        
        "binder" : "PVDF",
        "ratio_of_cathode_weight" : [0.8,0.1,0.1],
        "area loading of active material" : {{"value" : null, "unit" : null}}
    }}
]

name_cathode: ['NMC cathode with 5.72 mg cm-2 loading']
Paragraph: The NMC electrode were prepared by mixing NMC-532, carbon black and poly(vinylidene difluoride) in the weight ratio of 8:1:1. The active material loading of the NMC-532 cathode was controlled to be \u223c5.72\u202fmg\u202fcm\u22122.
output:
[
    {{
        "name_cathode": "NMC cathode with 5.72 mg cm-2 loading",
        "active_material": {{"material": ["Li(Ni0.5Mn0.3Co0.2)O2"], "ratio_of_active_material": [0.5, 0.3, 0.2]}},
        "conductive_additive": "carbon black",
        "binder": "poly(vinylidene difluoride)",
        "ratio_of_cathode_weight": [0.8, 0.1, 0.1],
        "area loading of active material": {{"value": 5.72, "unit": "mg cm-2"}}
    }}
]

name_cathode: ["S/PPy composite (1051 mAh g\u22121 at 0.1 C) cathode"]
Paragraph: The S/PPy composites were prepared via a simple ball-milling followed by a low-temperature heat treatment. Typically, 0.2\u00a0g of as prepared PPy was mixed with 4\u00a0g of nano-sulfur aqueous suspension (US Nanomaterials, 10\u00a0wt%) by ball-milling at 600\u00a0rpm for 3\u00a0h, and then dried at 60\u00a0\u00b0C overnight to remove the solvent. The resulting mixture was heated at 150\u00a0\u00b0C for 3\u00a0h in argon gas to obtain a desired S/PPy composite. The composite cathode was prepared by mixing 80\u00a0wt% S/PPy composite, 10\u00a0wt% polyvinylidene fluoride (PVDF) (Kynar, HSV900) as a binder and 10\u00a0wt% acetylene black (MTI, 99.5% purity) conducting agent in 1-methyl-2-pyrrolidinone (NMP, Sigma-Aldrich, \u226599.5% purity). The resultant slurry was uniformly spread onto aluminum foil using a doctor blade. The sulfur loading in each electrode was about 4\u00a0mg\u00a0cm\u22122. The chemical analysis of the composite has confirmed a high sulfur content of 60\u00a0wt%. 
output: 
[
    {{
        "name_cathode": "S/PPy composite (1051 mAh g\u22121 at 0.1 C) cathode",
        "active_material": {{"material": ["S", "PPy"], "ratio_of_active_material": [0.6, 0.4]}},
        "conductive_additive": "acetylene black",
        "binder": "PVDF",
        "ratio_of_cathode_weight": [0.8, 0.1, 0.1],
        "area loading of active material": {{"value": 4,"unit": "mg cm-2"}}
    }}
]

name_cathode: ['S/KB cathode']
Paragraph: Preparation of the cathode. Sulfur powder and Ketjen Black (KB) (mass ratio: S/C=7/3) were evenly ground and mixed, then calcined in a tubular furnace at 155\u00a0\u00b0C under argon atmosphere for 12\u00a0h, insuring the tight connection of sulfur and KB. After that, S/KB mixture and polyvinylidenefluoride (PVDF) (mass ratio: S/KB:PVDF\u00a0=\u00a09:1) were ground evenly, a proper amount of N-methyl-2-pyrrolidone (NMP) was added to obtain slurry then coated on the carbon fiber membrane to form a dense and uniform sulfur layer. They were put into oven to obtain cathode with sulfur loading of 0.8\u20131.2\u00a0mg\u00a0cm\u22122.
output:
[    
    {{
        "name_cathode": "S/KB cathode",
        "active_material": {{"material": ["S", "KB"], "ratio_of_active_material": [0.7, 0.3]}},
        "conductive_additive": null,
        "binder": "polyvinylidenefluoride (PVDF)",
        "ratio_of_cathode_weight": [0.9, 0, 0.1],
        "area loading of active material": {{"value": 0.8, "unit": "mg cm-2"}}
    }}
]                

name_cathode: ["S-HTC@pDA cathode"]
Paragraph: the hierarchical tower-shaped carbon was prepared and denoted as HTC. S-HTC was synthesized by melt-diffusion method. HTC was mixed with sulfur (C/S\u202f=\u202f4:7) by milling in a mortar for 0.5\u202fh. Preparation of S-HTC@pDA: 200\u202fmg S-HTC and 50\u202fmg dopamine hydrochloride were dispersed in 100\u202fml deionized water. S-HTC@pDA, carbon black and polyvinylidene fluoride (PVDF) were mixed uniformly in N-methyl-2-pyrrolidinone (NMP) at a mass ratio of 70:20:10 to make cathode slurry. The typical areal sulfur loading was \u223c1.2\u202fmg\u202fcm\u22122. 
output:
[
    {{
            "name_cathode": "S-HTC@pDA cathode",
            "active_material": {{"material": ["S", "HTC", "pDA"], "ratio_of_active_material": [0.509, 0.291, 0.2]}},
            "conductive_additive": "carbon black",
            "binder": "PVDF",
            "ratio_of_cathode_weight": [0.7, 0.2, 0.1],
            "area loading of active material": {{"value": 1.2, "unit": "mg cm-2"}}
    }}
]

name_cathode: ["GC/(Fe3C)x@SSe cathode"]
Paragraph: The materials of GC/(Fe3C)x@SSe was prepared by vacuum melting method. Sulfur powder and selenium powder (with a molar ratio of 94: 6) were evenly mixed with GC at a ratio of 7: 3, and then transferred to a 25 mL reactor, and the treated reactor was reacted in a muffle furnace at 2 °C min−1 to 260 °C for 12 h to obtain the GC@SSe. The preparation method of GC/(Fe3C)x@SSe were the same as that of GC@SSe. GC/(Fe3C)2.7@S was prepared by the same method as above except that selenium powder is not added. The electrode was prepared by mixing the active material, conductive carbon black (Super-P) and polyvinylidene fluoride (PVDF) at a mass ratio of 7: 2: 1. The actual sulfur content of the electrodes was about 0.9 mg cm−2
output:
[
    {{
                        "name_cathode": "GC/(Fe3C)x@SSe cathode",
                        "active_material": {{"material": ["S", "Se", "GC/(Fe3C)x"], "ratio_of_active_material": [0.658, 0.042, 0.3]}},
                        "conductive_additive": "Super-P",
                        "binder": "PVDF",
                        "ratio_of_cathode_weight": [0.7, 0.2, 0.1],
                        "area loading of active material": {{"value": 0.9, "unit": "mg cm-2"}}
    }}
]

name_cathode: ["h-SP-S cathode"]
Paragraph: The cathodes for Li-S batteries were prepared from slurries based on N-methyl-2-pyrrolidone, which had composition ratio of sulfur, h-SP, and polyvinylidene fluoride (PVDF) with 60:20:20 (wt.%). Hollow SP was used as conductive agents and/or reaction sites, while PVDF was used as a binder. The electrode slurry was cast onto electrochemical grade aluminum foil with ∼20-μm thickness and ∼1-mgsulfur/cm2 loading.
output:
[
    {{
                        "name_cathode": "h-SP-S cathode",
                        "active_material": {{"material": ["S"], "ratio_of_active_material": [1, 0]}},
                        "conductive_additive": "hollow SP",
                        "binder": "PVDF",
                        "ratio_of_cathode_weight": [0.6, 0.2, 0.2],
                        "area loading of active material": {{"value": 1, "unit": "mg cm-2"}}
    }}
]

name_cathode: ["HSC-0.1 cathode"]
Paragraph: To fabricate conventional carbon/sulfur (C/S) composite cathodes, MWCNTs and S were first ball-milled with PVDF binder at a weight ratio of 9:1 in NMP to obtain a slurry. Three kinds of sulfur cathodes with different sulfur contents were prepared by regulating the sulfur to carbon ratio in the C/S composites including cathodes with routine sulfur content (RSC) of 64 wt%, high sulfur content (HSC) of 76 wt%, and ultra-high sulfur content (UHSC) of 82 wt%. The above sulfur contents are calculated based on the whole sulfur cathode including S, C, and PVDF.
output:
[
    {{
                        "name_cathode": "HSC-0.1 cathode",
                        "active_material": {{"material": ["S"], "ratio_of_active_material": [1]}},
                        "conductive_additive": "MWCNT",
                        "binder": "PVDF",
                        "ratio_of_cathode_weight": [0.76, 0.14, 0.1],
                        "area loading of active material": {{"value": null, "unit": null}}
    }}
]
description:
# the weight ratio of conductive additive, 0.14, is 0.9-0.76=0.14
 
name_cathode: {name_material}
Paragraph: {paragraph}
output:
'''

PROMPT_SEPARATOR = '''
Extract the relevant information about the separator with the names {name_material} mentioned in the paragraph.
There are {name_cell} name of cells are exist.
There are guildlines for output Json format:
[
    {{
        "name_separator" : {name_material[0]},
        "separator_material" : [str,...]
    }},...
]

You must follow rules below:
- The "name_separator" is one of the {name_material}, representing the name of the separator. You are required to thoroughly investigate all the separator present here without missing any.
- The separator is same as blocking layer and it is a solid film and is not composed of a liquid solution. Do not extract solvent such as "NMP" or "H2O" in "separator_material".
- If the paragraph mentions a specific separator by name, please include it in the name_separator field.
- You must represent them all in list, When multiple separators are present.
- You must not mention any materials other than the separator.
- If there are multiple materials used in the separator, you must list them all in sepator_material field.
- Celgard is a commercial separator that typically used which is a polymer film. If only celgard name is mentioned without polymer type, extract celgard name. (e.g. "name_separator: celgard-2450" -> "separator_material": ["celgard-2450"])

Begin!

name_separator: ["UiO-66 MOF-coated separator", "UiO-66-NH2 MOF-coated separator", "PPseparator"]
Paragraph : Prepare UiO-66/PP and UiO-66-NH2/PP separators.
The as-prepared UiO-66 or UiO-66-NH2 and PVDF (8 wt%) were dispersed into mixed solution of NMP. Afterward, the samples were ball milled for 1 h at room temperature to form uniform slurry. 
The formed uniform slurry was coated on the PP separator and vacuum-dried at 60℃ for 12 h to evaporate the solvent. 
After that, the MOF-coated separator and PP separator were punched into disks with a diameter of 16 mm and with a mass loading of ≈0.13 mg cm 2.
output: 
[
    {{
        "name_separator" : "UiO-66 MOF-coated separator",
        "separator_material" : ["Uio-66", "PVDF", "PP", "NMP"]
    }},
    {{
        "name_separator" : "UiO-66-NH2 MOF-coated separator",
        "separator_material" : ["Uio-66-NH2", "PVDF", "PP", "NMP"]
    }},
    {{
        "name_separator" : "PP separator",
        "separator_material" : ["PP"]
    }},...
]

name_separator: ['NSPC/Celgard 2400']
Paragraph: Lithium metal was employed as anode and NSHPC sample was coated on Celgard 2400 separator to be used as interlayer.
output:
[
    {{
        "name_separtor" : "NSPC/Celgard 2400",
        "separator_material" : ["NSHPC", "Celgard 2400"]
    }}
]

name_separator: ["microporous polypropylene membrane (Celgard 2400)"]
Paragraph: The batteries (type CR2032) were assembled in the glove box (MIKROUNA, Universal), the contents of water and oxygen in the glove box were less than 0.01 PPM. The prepared CNF, Co\u2013PCNF sandwich electrode and aluminum foil collector electrode were respectively used for the cathode, and metal Li as the anode. A microporous polypropylene membrane (Celgard 2400) was used as the separator. 1 M LiTFSI in a mixture of DOL/DME (v/v\u00a0=\u00a01:1) with 2\u00a0wt % LiNO3 additives were used as the electrolyte, and the average E/S ratio is 20\u00a0\u03bcL\u00a0mg\u22121.
output:
[
    {{
            "name_separator" : "microporous polypropylene membrane (Celgard 2400)",
            "separator_material" : ["polypropylene"]
    }}
]

name_separator: {name_material}
Paragraph: {paragraph}
output:
'''

PROMPT_ANODE = '''
Extract the relevant information about the anodes {name_material} mentioned in the paragraph. 
There are {name_cell} name of cells are exist.
Anode is consisted of Li metal.

There are guildlines for output Json format:
[
    {{
        "name_anode" : {name_material[0]},
        "thickness" : float,
        "unit" : str,
        "additional_layer" : str
    }},...
]

You must follow rules below:
- The "name_anode" is one of the {name_material}, representing the name of the anode. You are required to thoroughly investigate all the anode present here without missing any.
- The anode is one of the components that make up a battery cell.
- You must write the thickness of the Li metal, foli or chip in the "thickness" field.
- additional layer is the layer that is coated or doping only on the Li metal and may be not present.
- You must not include the materials that are not related to anode.(material that coated in the separtor..)
- If you're uncertain, return with null.

Begin!

name_anode: ['Li metal foil']
Paragraph: The thickness and diameter of Li metal foil were 500 μm and 16.0 mm, respectively.
Json: 
[
    {{
        "name_anode" : "Li metal foil",
        "thickness":500, 
        "unit":"μm", 
        "additional_layer": null
    }}
]

name_anode: ["Lithium metal"]
Paragraph : Lithium metal was employed as anode and NSHPC sample was coated on Celgard 2400 separator to be used as interlayer.
Json:
[
    {{
        "name_anode" : "Lithium metal",
        "thickness":null, 
        "unit": null, 
        "additional_layer": null
    }}
]

name_anode: {name_material}
Paragraph: {paragraph}
Json:
'''

PROMPT_MEASUREMENT_CONDITION = '''
Extract the relevant information about measurement condition about cycling performance in the paragraph. 
There are {name_cell} name of cells are exist in the paragraph.
Condition property include C_rate or current_density or temperature.
There are guildlines for output Json format:
- You must write like 
[
    {{
        "name_cell" : {name_cell[0]},
        "C_rate" : [float],
        "current_density" : {{"value" : float, "unit" : str}},
        "temperature" : {{"value" : float, "unit"  : str}}
    }},...
]

You must follow rules below:
- The "name_cell" is one of the {name_cell} which is the name of the battery cells.
- If there are no float value in the paragraph, please do not include that property.
- You must not extract about symmetric cell.
- You must extract condition property refer to the temperature and C rate (current density) at which the cycling test is conducted.
- You must extract condition property when the sentence containing condition property is related to cycling test. It is same as electrochemical cycling, cycling performance, cycle-capacity performance, cycle stability test, galvanostatically cycle, galvanostatic charge discharge test, etc.
- You must extract condition property only when conducting cycling tests on either half-cell (with lithium metal as the counter electrode) or full cell configurations. 
- You must not extract condition property about another measurement(rate capability test, Electrochemical Impedance Spectroscopy, Cycle Voltametry test, Li stripping/plating measurement, galvanostatic Li plating/stripping test, charge-discharge profiles, ...).
- Only one of the information, C_rate or current_density, will exist, and you need to extract the information of that exist. Vary occasionally, if both exist, please write both information.
- Even if C_rate or current_density are mentioned in the paragraph, do not blindly include them. If the condition property is not related to cycling performance, do not include it.
- Do not include free cycling condtion property.
- If there are 2 or more capacity-cycling performance in the paragraph, extract the condition properties corresponding to each.
-If you're uncertain, please return null.

Begin!

name_cell: {name_cell}
Paragraph: {paragraph}
Json:
'''

PROMPT_CURRENT_COLLECTOR = '''
Extract the relevant information about the current collector mentioned in the paragraph.
There are {name_cell} name of cells are exist in the paragraph.
There are guildlines for output Json format:
[{{
    "name_cell" : {name_cell[0]},
    "collector1": str, 
    "collector2": str
}},...]

You must follow rules below:
- The "name_cell" is one of the {name_cell} which is the name of the battery cells.
- The current collector is one of the components that make up a battery cell.
- The current collector combined with the cathode should be returned to collector1, and the current collector combined with the anode should be returned to collector2.
- The anode, such as Li metal foil or Li metal composite is not a current collector. Do not extract Li metal as current collector.
- Current collector is typically made of metal foil (not Li foil) and comercially Al and Cu foil are used as "collector1", "collector2", respectively.
- If current collector is carbon coated, you must extract carbon coated information too.
- Please do not extract NMP or water which is a solvent to use in 
- For unknown information, write null.

Begin!

name_cell: ["LFP cathode Battery"]
Paragraph: The 2032-type battery cell, Celgard 2320 separator, glassfiber separator, copper foil (14 μm), aluminum foil (14 μm), lithium anode with the thinness of 450 μm and LiFePO4 (LFP) cathode with the active material loading of 10.52 mg⋅cm􀀀 2 and areal capacity of 1.578 mAh⋅cm2 were all purchased from Guangdong Canrd New Energy Technology Co., Ltd.
Json: 
[
    {{
        "name_cell" : "LFP cathode Battery",
        "collector1" : "aluminum foil", 
        "collector2" : "copper foil"
    }}
]

name_cell: ['7 wt.% DMMP Battery']
Paragraph: The cathode was fabricated by mixing 70 wt.% PAN/S composite, 20 wt.% Super P and 10 wt.% PTFE as binder, and distilled water as dispersant. The slurry was stirred for 4h and then uniformly coated onto a thin Al foil (with a carbon coating), dried and cut into small disks with weight loads of ca. 0.5\u20132mgcm\u22122. The 1M LiPF6/EC+EMC (1:1, v/v) was used as baseline electrolyte, in which DMMP was directly added at the ratios of 0, 7, 11, 15, 21 wt.%. With lithium foil as anode and PE film as separator, 2016 type coin cells were assembled in a glove box (MBraun, Germany).
Json:
[
    {{
        "name_cell" : "7 wt.% DMMP Battery",
        "collector1" : "Al foil with carbon coating", 
        "collector2" : null
    }}
]



name_cell: {name_cell}
Paragraph: {paragraph}
Json:
'''

PROMPT_ELECTROLYTE = '''
Extract the relevant information about electrolyte {name_material} mentioned in the paragraph.
There are {name_cell} name of cells are exist.
Electroltye is consisted of Li salts and solvents.

There are guildlines for output Json format:
- You must write like 
[
    {{
        "name_electrolyte" : {name_material[0]},
        "Li_salt" : {{ "material": [str, str,...], "concentration":[float, float,...],"unit": [str, str ...]}}, 
        "solvent" : {{ "material": [str, str,...], "solvent_volume_ratio":[float, float, ...], "unit": [str, str, ...]}},
        "EA_ratio" : float
    }},...
]

You must follow rules below:
- The "name_electrolyte" is one of the {name_material}, representing the name of the electrolyte. You are required to thoroughly investigate all the electrolyte present here without missing any.
- The electrolyte is one of the components that make up a battery cell.
- If there are 2 or more electrolyte combinations exist in paragraph, you must extract all electrolytes.
- If there are additive salt in paragraph, it is same as Li salt and you must include "Li_salt" once.
- "EA_ratio" is ratio of electrolyte(in mL) and active materials(in mg). In Lithium sulfur battery, it is same as ES ratio.
- If the "EA_ratio" value is mentioned multiple times, extract each with a different electrolyte.
- The "unit" of "solvent" is typically v, v% or wt%, each means volume, volume% and weight%.
- If you're uncertain, fill "null".

Begin!

name_electrolyte: ["DD of 1.0 M LiTFSI in DOL/DME (v:v = 1:1)", "DD-N of 1.0 M LiTFSI in DOL/DME (v:v = 1:1) with 5wt% LiNO3"]
Paragraph: The electrolyte of DD was 1.0 M LiTFSI in DOL/DME (v:v = 1:1) and DD-N was DD with 5wt% LiNO3.
Json:
[
    {{
        "name_electrolyte" : "DD of 1.0 M LiTFSI in DOL/DME (v:v = 1:1)",
        "Li_salt":{{ "material": ["LiTFSI"], "concentration":[1.0],"unit": ["M"]}}, 
        "solvent":{{ "material": ["DOL", "DME"], "solvent_volume_ratio":[1,1], "unit": ["v", "v"]}},
        "EA_ratio": null
    }},
    {{
        "name_electrolyte" : "DD-N of 1.0 M LiTFSI in DOL/DME (v:v = 1:1) with 5wt% LiNO3",
        "Li_salt":{{ "material": ["LiTFSI", "LiNO3"], "concentration":[1.0, 5],"unit": ["M", "wt%"]}}, 
        "solvent":{{ "material": ["DOL", "DME"], "solvent_volume_ratio":[1,1], "unit": ["v", "v"]}},
        "EA_ratio": null
    }}
]

name_electrolyte: ["electrolyte of a mixture of 0.6mol L-1(M) LiFSI-DME", "electroltye of a mixture of 0.6M LiTFSI-DME", "electrolyte of a mixture of 0.6M LiDFOB-DME", "electrolyte of a mixture of 0.36M LiNO3-DME", "HE-DME of a mixture of 0.15MLiFSI, 0.15MLiTFSI, 0.15MLiDFOB and 0.15MLiNO3 into DME solvent with the total concentration of lithium ion to be 0.6M", "5-component 0.6M HE-DME of a mixture of 0.15M LiFSI, 0.10M LiTFSI, 0.10M LiBFTI, 0.10M LiDFOB and 0.15M LiNO3 into DME solvent with the total concentration of lithium to be 0.6M"]
Paragraph: All the electrolytes were prepared by dissolving the specific amount of different lithium salts in DME solvent in an Ar-filled glove box (H2O<0.1ppm, O2 < 0.1 ppm). 
0.6mol L-1(M) LiFSI-DME, 0.6M LiTFSI-DME, 0.6M LiDFOB-DME and 0.36M LiNO3-DME electrolytes denote that the corresponding concentration of different salts are dissolved in DME, 
where 0.6MLiNO3-DME electrolyte can’t be prepared because of the relatively low salt solubility. HE-DME electrolyte was prepared by dissolving 0.15MLiFSI, 0.15MLiTFSI, 
0.15MLiDFOB and 0.15MLiNO3 into DME solvent with the total concentration of lithium ion to be 0.6M.
5-component 0.6M HE-DME electrolyte was prepared by dissolving 0.15M LiFSI, 0.10M LiTFSI, 0.10M LiBFTI, 
0.10M LiDFOB and 0.15M LiNO3 into DME solvent with the total concentration of lithium to be 0.6M.
Json: 
[
    {{
        "name_electrolyte" : "electrolyte of a mixture of 0.6mol L-1(M) LiFSI-DME"
        "Li_salt":{{ "material": ["LiFSI"], "concentration":[0.6],"unit": ["M"]}}, 
        "solvent":{{ "material": ["DME"], "solvent_volume_ratio":null, "unit": null}},
        "EA_ratio": null
    }}, 
    {{
        "name_electrolyte" : "electroltye of a mixture of 0.6M LiTFSI-DME",
        "Li_salt":{{ "material": ["LiTFSI"], "concentration":[0.6],"unit": ["M"]}}, 
        "solvent":{{ "material": ["DME"], "solvent_volume_ratio":null, "unit": null}},
        "EA_ratio": null
    }}, 
    {{
        "name_electrolyte" : "electrolyte of a mixture of 0.6M LiDFOB-DME"
        "Li_salt":{{ "material": ["LiDFOB"], "concentration":[0.6],"unit": ["M"]}},
        "solvent":{{ "material": ["DME"], "solvent_volume_ratio":null, "unit": null}},  
        "EA_ratio": null
    }}, 
    {{
        "name_electrolyte" : "electrolyte of a mixture of 0.36M LiNO3-DME"
        "Li_salt":{{ "material": ["LiNO3"], "concentration":[0.36],"unit": ["M"]}},
        "solvent":{{ "material": ["DME"], "solvent_volume_ratio":null, "unit": null}},  
        "EA_ratio": null
    }}, 
    {{
        "name_electrolyte" : "HE-DME of a mixture of 0.15MLiFSI, 0.15MLiTFSI, 0.15MLiDFOB and 0.15MLiNO3 into DME solvent with the total concentration of lithium ion to be 0.6M"
        "Li_salt":{{ "material": ["LiFSI", "LiTFSI", "LiDFOB", "LiNO3"], "concentration":[0.15, 0.15, 0.15, 0.15],"unit": ["M", "M", "M", "M"]}},
        "solvent":{{ "material": ["DME"], "solvent_volume_ratio":null, "unit": null}}, 
        "EA_ratio": null
    }}, 
    {{
        "name_electrolyte" : "5-component 0.6M HE-DME of a mixture of 0.15M LiFSI, 0.10M LiTFSI, 0.10M LiBFTI, 0.10M LiDFOB and 0.15M LiNO3 into DME solvent with the total concentration of lithium to be 0.6M"
        "Li_salt":{{ "material": ["LiFSI", "LiTFSI", "LiBFTI", "LiDFOB", "LiNO3"], "concentration":[0.15, 0.10, 0.10, 0.10, 0.15],"unit": ["M", "M", "M", "M", "M"]}},
        "solvent":{{ "material": ["DME"], "solvent_volume_ratio":null, "unit": null}}, 
        "EA_ratio": null
    }}
]

name_electrolyte: ["electrolyte of a mixture of DOL/DME with 1 M LiTFSI and 1 wt% LiNO3."]
Paragraph : 
The electrolyte was 1 M lithium bis(trifluoromethanesulfonyl)imide (LiTFSI) in mixed solvent of 1,2-dimethoxyethane (DME): 1,3-dioxolane (DOL) (1:1 in volume) with 2wt% lithium nitrate (LiNO3) additive.
Json:
[
    {{
        "name_electrolyte" : "electrolyte of a mixture of DOL/DME with 1 M LiTFSI and 1 wt% LiNO3.",
        "Li_salt":{{ "material": ["LiTFSI", "LiNO3"], "concentration":[1, 2],"unit": ["M", "wt%"]}}, 
        "solvent":{{ "material": ["DME", "DOL"], "solvent_volume_ratio":[1,1], "unit": ["v", "v"]}},
        "EA_ratio": null
    }}
]

name_electrolyte: {name_material}
Paragraph: {paragraph}
Json:
'''

PROMPT_INTERLAYER = '''
Extract the relevant information about the interlayer mentioned in the paragraph.
There are {name_cell} name of cells are exist in the paragraph.
There are guildlines for output Json format:
[{{
    "name_cell" : {name_cell[0]},
    "interlayer": str
}},...]

You must follow rules below:
- The "name_cell" is one of the {name_cell} which is the name of the battery cells.
-The interlayer is an additional layer in lithium metal battery.
- For unknown information, write null.

Begin!

name_cell: ["LFP cathode Battery"]
Paragraph: The 2032-type battery cell, Celgard 2320 separator, glassfiber separator, copper foil (14 μm), aluminum foil (14 μm), lithium anode with the thinness of 450 μm and LiFePO4 (LFP) cathode with the active material loading of 10.52 mg⋅cm􀀀 2 and areal capacity of 1.578 mAh⋅cm2 were all purchased from Guangdong Canrd New Energy Technology Co., Ltd.

Json : 
[
    {{
        "name_cell" : "LFP cathode Battery",
        "interlayer": null
    }}
]

name_cell: {name_cell}
Paragraph: {paragraph}
Json:
'''

PROMPT_CATHODE_NOT_MENTIONED = '''
Extract the relevant information about the cathode mentioned in the paragraph.
There are {name_cell} name of cells are exist in the paragraph.

There are guildlines for output Json format:
[
    {{
        "name_cell" : {name_cell[0]},
        "name_cathode" : str,
        "active_material" : {{"material" : [str,...], "ratio_of_active_material" : [float,...]}},
        "conductive_additive" : str,
        "binder" : str,
        "ratio_of_cathode_weight" : [float, float, ...],
        "area loading of active material" : {{"value" : float, "unit" : str}}
    }}, ...
]

You must follow rules belows:
- The cathode is one of the components that make up a battery cell.
- You must refer to everything written in the paragraph and extract the output.
- If the cathode is a sulfur composite material (in a Lithium Sulfur battery), the active material of the cathode consists of sulfur encapsulated within the host material (S@host_material). You must return both components (sulfur and the host material) as the active material. And the ratio_of_active_material is the weight % ratio of each components of sulfur composite, not a ratio of cathode slurry components, such as {{"active_material" : ["S", "host material"], "ratio_of_active_material" : [S weight%, host material weight%]}}. Please extract "ratio_of_active_material" as null when there are no information of ratio_of_active_material. If sulfur composite is synthesized by various synthesizing, each ratio must be calculated complexly to extract the final "ratio_of_active_material".
- Do not confuse host material and conductive additive in lithium sulfur battery. A carbon material such as Kejen black (KB), Super P (SP), carbon black (CB), conductive carbon (C), etc can be used as host material or conductive additive both but the host material encapsulate sulfur using methods such as melt diffusion. ("70 wt% S and 30 wt% cb were mixed and heated at 155°C for 24 h." This heating method is melt diffusion. Extract host material in active material only when it contain sulfur by melt diffusion.) The sulfur cathode is composed of sulfur composite (active material), conductive additive, and binder, and may not contain conductive material (if there are no ratio information of conductive additive, ratio_of_cathode_weight is extracted as active material wt%:0:binder wt%).
- Lithium nickel manganese cobalt oxides is same as NCM or NMC. (e.g. LiNi0.5Mn0.3Co0.2O2 is same with NMC-532, NCM-523, NMC532, NCM523. You must extract LiNi0.5Mn0.3Co0.2O2 in active material field.)
- In cases where two or more constituents appear in the cathode material, a separate cathode was fabricated for each scenario.
- If many active materials are include in paragraph, than there are a number of active materials cathode is exist.
- Binders are typically made of polymers.
- "ratio_of_activate_material" refers to the ratio of active mateiral substances constituting the active material. In the case of sulfur cathode, the ratio must be extracted in that order of sulfur:host material. (e.g. S/CeO2/MXene was mixed CeO2/MXene with S at a mass ratio of 3:7. -> "active_material": {{"material": ["S", "CeO2/MXene"], "ratio_of_active_material": [0.7, 0.3]}})
- The "ratio_of_activate_material" of NCM or NMC active material must be extracted in that order of nickel:manganese:cobalt ratio (e.g. NCM721 -> [0.7:0.1:0.2], NMC721 -> [0.7:0.2:0.1]). NMC811 cathode means the "active material" is LiNi0.8Mn0.1Co0.1O2 and the "ratio_of_active_material" is [0.8,0.1,0.1].
- The "ratio_of_active_material" of LFP (LiFePO4) is 1.
- "ratio_of_cathode_weight" is a mass ratio of the active material, conductive catbon, and binder. And the ratio must be extracted in that order of active material:conductive additive:binder. For substances that do not exist, enter 0 in the ratio. If only active material is exist without conductive additive and binder, the "ratio_of_cathode_weight" is [1:0:0].
- If the "area loading of active material" value is not given as a specific value but is given as a range such as 0.5-2.0 mg/cm2, please return the average value (e.g. The sulfur loading of 1.3-1.5mg\cm2 -> "area loading of active material" : {{"value" : 1.4, "unit" : "mg\cm2"}}).
- If the "area loading of active material" value is mentioned multiple times, extract each with a different cathode.
- active material loading (* mg cm-2) and sulfur ratio (* wt%) is different.
- You must not extract additional layers which coated on the cathode. (e.g. The solution coated on as prepared CNT@S cathode via doctor blade to form ZB/G hybrid layer coated cathode. -> don't extract about ZB/G materials.)
- For unknown information, write null.

Begin!
Paragraph: The pristine LiFePO4 (LFP) and LiNi0.7Co0.2Mn0.1O2 (NCM721) electrode was prepared as follows: the active material (LFP or NCM721,
80 wt%), acetylene black (AB) (10 wt%) and PVDF (10 wt%) were mixed in NMP. Then, the slurry was spread on aluminum foil, and dried at 80℃
for 12 h.
output: 
[
    {{
        "name_cell" : null,
        "name_cathode" : "The pristine LiFePO4 (LFP) cathode",
        "active_material" : {{"material" : "LiFePO4 (LFP)", "ratio_of_active_material" : [1]}},
        "conductive_additive" : "acetylene black",
        "binder" : "PVDF",
        "ratio_of_cathode_weight" : [0.8,0.1,0.1],
        "area loading of active material" : {{"value" : null, "unit" : null}}
    }},
    {{
        "name_cell" : null,
        "name_cathode" : "LiNi0.7Co0.2Mn0.1O2 (NCM721) cathode",
        "active_material" : {{"material" : "Li(Ni0.7Co0.2Mn0.1)O2", "ratio_of_active_material" : [0.7,0.1,0.2]}},
        "conductive_additive" : "acetylene black",        
        "binder" : "PVDF",
        "ratio_of_cathode_weight" : [0.8,0.1,0.1],
        "area loading of active material" : {{"value" : null, "unit" : null}}
    }}
]

Paragraph: The NMC electrode were prepared by mixing NMC-532, carbon black and poly(vinylidene difluoride) in the weight ratio of 8:1:1. The active material loading of the NMC-532 cathode was controlled to be \u223c5.72\u202fmg\u202fcm\u22122.
output:
[
    {{
        "name_cell" : null,
        "name_cathode": "NMC cathode with 5.72 mg cm-2 loading",
        "active_material": {{"material": ["Li(Ni0.5Mn0.3Co0.2)O2"], "ratio_of_active_material": [0.5, 0.3, 0.2]}},
        "conductive_additive": "carbon black",
        "binder": "poly(vinylidene difluoride)",
        "ratio_of_cathode_weight": [0.8, 0.1, 0.1],
        "area loading of active material": {{"value": 5.72, "unit": "mg cm-2"}}
    }}
]

Paragraph: The S/PPy composites were prepared via a simple ball-milling followed by a low-temperature heat treatment. Typically, 0.2\u00a0g of as prepared PPy was mixed with 4\u00a0g of nano-sulfur aqueous suspension (US Nanomaterials, 10\u00a0wt%) by ball-milling at 600\u00a0rpm for 3\u00a0h, and then dried at 60\u00a0\u00b0C overnight to remove the solvent. The resulting mixture was heated at 150\u00a0\u00b0C for 3\u00a0h in argon gas to obtain a desired S/PPy composite. The composite cathode was prepared by mixing 80\u00a0wt% S/PPy composite, 10\u00a0wt% polyvinylidene fluoride (PVDF) (Kynar, HSV900) as a binder and 10\u00a0wt% acetylene black (MTI, 99.5% purity) conducting agent in 1-methyl-2-pyrrolidinone (NMP, Sigma-Aldrich, \u226599.5% purity). The resultant slurry was uniformly spread onto aluminum foil using a doctor blade. The sulfur loading in each electrode was about 4\u00a0mg\u00a0cm\u22122. The chemical analysis of the composite has confirmed a high sulfur content of 60\u00a0wt%.
output: 
[
    {{
        "name_cell" : null,
        "name_cathode": "S/PPy composite cathode",
        "active_material": {{"material": ["S", "PPy"], "ratio_of_active_material": [0.6, 0.4]}},
        "conductive_additive": "acetylene black",
        "binder": "PVDF",
        "ratio_of_cathode_weight": [0.8, 0.1, 0.1],
        "area loading of active material": {{"value": 4,"unit": "mg cm-2"}}
    }}
]

Paragraph: Preparation of the cathode. Sulfur powder and Ketjen Black (KB) (mass ratio: S/C=7/3) were evenly ground and mixed, then calcined in a tubular furnace at 155\u00a0\u00b0C under argon atmosphere for 12\u00a0h, insuring the tight connection of sulfur and KB. After that, S/KB mixture and polyvinylidenefluoride (PVDF) (mass ratio: S/KB:PVDF\u00a0=\u00a09:1) were ground evenly, a proper amount of N-methyl-2-pyrrolidone (NMP) was added to obtain slurry then coated on the carbon fiber membrane to form a dense and uniform sulfur layer. They were put into oven to obtain cathode with sulfur loading of 0.8\u20131.2\u00a0mg\u00a0cm\u22122.

output:
[    
    {{
        "name_cell" : null,
        "name_cathode": "S/KB cathode",
        "active_material": {{"material": ["S", "KB"], "ratio_of_active_material": [0.7, 0.3]}},
        "conductive_additive": null,
        "binder": "polyvinylidenefluoride (PVDF)",
        "ratio_of_cathode_weight": [0.9, 0, 0.1],
        "area loading of active material": {{"value": 0.8, "unit": "mg cm-2"}}
    }}
]               

Paragraph: the hierarchical tower-shaped carbon was prepared and denoted as HTC. S-HTC was synthesized by melt-diffusion method. HTC was mixed with sulfur (C/S\u202f=\u202f4:7) by milling in a mortar for 0.5\u202fh. Preparation of S-HTC@pDA: 200\u202fmg S-HTC and 50\u202fmg dopamine hydrochloride were dispersed in 100\u202fml deionized water. S-HTC@pDA, carbon black and polyvinylidene fluoride (PVDF) were mixed uniformly in N-methyl-2-pyrrolidinone (NMP) at a mass ratio of 70:20:10 to make cathode slurry. The typical areal sulfur loading was \u223c1.2\u202fmg\u202fcm\u22122. 

output:
[
    {{
            "name_cell" : null,
            "name_cathode": "S-HTC@pDA cathode",
            "active_material": {{"material": ["S", "HTC", "pDA"], "ratio_of_active_material": [0.509, 0.291, 0.2]}},
            "conductive_additive": "carbon black",
            "binder": "PVDF",
            "ratio_of_cathode_weight": [0.7, 0.2, 0.1],
            "area loading of active material": {{"value": 1.2, "unit": "mg cm-2"}}
    }}
]

Paragraph: The cathodes for Li-S batteries were prepared from slurries based on N-methyl-2-pyrrolidone, which had composition ratio of sulfur, h-SP, and polyvinylidene fluoride (PVDF) with 60:20:20 (wt.%). Hollow SP was used as conductive agents and/or reaction sites, while PVDF was used as a binder. The electrode slurry was cast onto electrochemical grade aluminum foil with ∼20-μm thickness and ∼1-mgsulfur/cm2 loading.
output:
[
    {{
            "name_cell" : null,
            "name_cathode": "h-SP-S cathode",
            "active_material": {{"material": ["S"], "ratio_of_active_material": [1, 0]}},
            "conductive_additive": "hollow SP",
            "binder": "PVDF",
            "ratio_of_cathode_weight": [0.6, 0.2, 0.2],
            "area loading of active material": {{"value": 1, "unit": "mg cm-2"}}
    }}
]

Paragraph: The materials of GC/(Fe3C)x@SSe was prepared by vacuum melting method. Sulfur powder and selenium powder (with a molar ratio of 94: 6) were evenly mixed with GC at a ratio of 7: 3, and then transferred to a 25 mL reactor, and the treated reactor was reacted in a muffle furnace at 2 °C min−1 to 260 °C for 12 h to obtain the GC@SSe. The preparation method of GC/(Fe3C)x@SSe were the same as that of GC@SSe. GC/(Fe3C)2.7@S was prepared by the same method as above except that selenium powder is not added. The electrode was prepared by mixing the active material, conductive carbon black (Super-P) and polyvinylidene fluoride (PVDF) at a mass ratio of 7: 2: 1. The actual sulfur content of the electrodes was about 0.9 mg cm−2
output:
[
    {{
            "name_cell": null,
            "name_cathode": "GC/(Fe3C)x@SSe cathode",
            "active_material": {{"material": ["S", "Se", "GC/(Fe3C)x"], "ratio_of_active_material": [0.658, 0.042, 0.3]}},
            "conductive_additive": "Super-P",
            "binder": "PVDF",
            "ratio_of_cathode_weight": [0.7, 0.2, 0.1],
            "area loading of active material": {{"value": 0.9, "unit": "mg cm-2"}}
    }}
]

Paragraph: To fabricate conventional carbon/sulfur (C/S) composite cathodes, MWCNTs and S were first ball-milled with PVDF binder at a weight ratio of 9:1 in NMP to obtain a slurry. Three kinds of sulfur cathodes with different sulfur contents were prepared by regulating the sulfur to carbon ratio in the C/S composites including cathodes with routine sulfur content (RSC) of 64 wt%, high sulfur content (HSC) of 76 wt%, and ultra-high sulfur content (UHSC) of 82 wt%. The above sulfur contents are calculated based on the whole sulfur cathode including S, C, and PVDF.
output:
[
    {{
            "name_cell": null,
            "name_cathode": "HSC-0.1 cathode",
            "active_material": {{"material": ["S"], "ratio_of_active_material": [1]}},
            "conductive_additive": "MWCNT",
            "binder": "PVDF",
            "ratio_of_cathode_weight": [0.76, 0.14, 0.1],
            "area loading of active material": {{"value": null, "unit": null}}
    }}
]
description:
# the weight ratio of conductive additive, 0.14, is 0.9-0.76=0.14

Paragraph: {paragraph}
output:
'''

PROMPT_SEPARATOR_NOT_MENTIONED = '''
There are {name_cell} name of cells are exist in the paragraph.
Extract the relevant information about the {name_cell} cell's separators mentioned in the paragraph.
There are guildlines for output format:
[
    {{
        "name_cell" : {name_cell[0]},
        "name_separator" : str,
        "separator_material" : [str,...]
    }},...
]


You must follow rules belows:
- The separator is one of the components that make up a battery cell.
- For the "name_cell", if the name of the cell is not mentioned, please return null.
- You extract "separator_material" must only that associated with "name_cell".
- The separator is same as blocking layer and it is a solid film and is not composed of a liquid solution. Do not extract solvent such as "NMP" or "H2O" in "separator_material".
- If the paragraph mentions a specific separator by name, please include it in the name_separator field.
- You must represent them all in list, When multiple separators are present.
- You must not mention any materials other than the separator.
- If there are multiple materials used in the separator, you must list them all in sepator_material field.
- Celgard is a commercial separator that typically used which is a polymer film. If only celgard name is mentioned without polymer type, extract celgard name. (e.g. "name_separator: celgard-2450" -> "separator_material": ["celgard-2450"])

Begin!
Paragraph : Prepare UiO-66/PP and UiO-66-NH2/PP separators.
The as-prepared UiO-66 or UiO-66-NH2 and PVDF (8 wt%) were dispersed into mixed solution of NMP. Afterward, the samples were ball milled for 1 h at room temperature to form uniform slurry. 
The formed uniform slurry was coated on the PP separator and vacuum-dried at 60℃ for 12 h to evaporate the solvent. 
After that, the MOF-coated separator and PP separator were punched into disks with a diameter of 16 mm and with a mass loading of ≈0.13 mg cm 2.
output: 
[
    {{
        "name_cell" : null,
        "name_separator" : "UiO-66 coated separator",
        "separator_material" : ["Uio-66", "PVDF", "PP", "NMP"]
    }},
    {{
        "name_cell" : null,
        "name_separator" : "UiO-66-NH2 coated separator",
        "separator_material" : ["Uio-66-NH2", "PVDF", "PP", "NMP"]
    }},
    {{ 
        "name_cell" : null,
        "name_separator" : "PP separator",
        "separator_material" : ["PP"]
    }}
]

name_cell: ["Lithium metal battery"]
Paragraph: Lithium metal was employed as anode and NSHPC sample was coated on Celgard 2400 separator to be used as interlayer.
output:
[
    {{
        "name_cell" : "Lithium metal battery",
        "name_separtor" : "Celgard 2400",
        "separator_material" : ["NSHPC", "Celgard 2400"]
    }}
]

name_cell: ["CNF sandwich electrode Battery", "Li–S battery with Co–PCNF sandwich electrode", "Li–S battery with CNF sandwich electrode"]
Paragraph: The batteries (type CR2032) were assembled in the glove box (MIKROUNA, Universal), the contents of water and oxygen in the glove box were less than 0.01 PPM. The prepared CNF, Co\u2013PCNF sandwich electrode and aluminum foil collector electrode were respectively used for the cathode, and metal Li as the anode. A microporous polypropylene membrane (Celgard 2400) was used as the separator. 1 M LiTFSI in a mixture of DOL/DME (v/v\u00a0=\u00a01:1) with 2\u00a0wt % LiNO3 additives were used as the electrolyte, and the average E/S ratio is 20\u00a0\u03bcL\u00a0mg\u22121.
output:
[
    {{
            "name_cell" : "CNF sandwich electrode Battery"
            "name_separator" : "microporous polypropylene membrane (Celgard 2400)",
            "separator_material" : ["polypropylene"]
    }},
    {{
            "name_cell" : "Li–S battery with Co–PCNF sandwich electrode"
            "name_separator" : "microporous polypropylene membrane (Celgard 2400)",
            "separator_material" : ["polypropylene"]
    }},
    {{
            "name_cell" : "Li–S battery with CNF sandwich electrode"
            "name_separator" : "microporous polypropylene membrane (Celgard 2400)",
            "separator_material" : ["polypropylene"]
    }}
]

name_cell: {name_cell}
Paragraph: {paragraph}
output:
'''

PROMPT_ANODE_NOT_MENTIONED = '''
Extract the relevant information about anode mentioned in the paragraph. 
There are {name_cell} name of cells are exist in the paragraph.
Anode is consisted of Li metal.

There are guildlines for output format:
[
    {{
        "name_cell" : {name_cell[0]},
        "name_anode" : str,
        "thickness" : float,
        "unit" : str,
        "additional_layer" : str
    }},...
]

You must follow rules below:
- The anode is one of the components that make up a battery cell.
- For the "name_cell", if the name of the cell is not mentioned, please return null.
- If the paragraph mentions a specific anode by name, please include it in the name_anode field.
- If you're uncertain, return with null.
- You must write the thickness of the Li metal, foli or chip in the "thickness" field.
- additional layer is the layer that is coated on or doping in the Li metal and may be not present.
- You must not include the materials that are not related to anode.(material that coated in the separtor..)

Begin!
Paragraph: The thickness and diameter of Li metal foil were 500 μm and 16.0 mm, respectively.
Json: 
[
    {{
        "name_cell" : null,
        "name_anode" : "Li metal foil",
        "thickness":500, 
        "unit":"μm", 
        "additional_layer": null
    }}
]

Paragraph : Lithium metal was employed as anode and NSHPC sample was coated on Celgard 2400 separator to be used as interlayer.
Json:
[
    {{
        "name_cell" : null,
        "name_anode" : "Lithium metal",
        "thickness":null, 
        "unit": null, 
        "additional_layer": null
    }}
]

name_cell: {name_cell}
Paragraph: {paragraph}
Json:
'''

PROMPT_CURRENT_COLLECTOR_NOT_MENTIONED = '''
Extract the relevant information about the current collector mentioned in the paragraph.
There are {name_cell} name of cells are exist in the paragraph.
There are guildlines for output Json format:
[{{
    "name_cell" : {name_cell[0]},
    "collector1": str, 
    "collector2": str
}},...]

You must follow rules below:
- The "name_cell" is one of the {name_cell} which is the name of the battery cells.
- The current collector is one of the components that make up a battery cell.
- The current collector combined with the cathode should be returned to collector1, and the current collector combined with the anode should be returned to collector2.
- Current collector is typically made of metal foil (not Li foil) and comercially Al and Cu foil are used as "collector1", "collector2", respectively.
- For unknown information, write null.

Begin!

name_cell: ["LFP cathode Battery"]
Paragraph: The 2032-type battery cell, Celgard 2320 separator, glassfiber separator, copper foil (14 μm), aluminum foil (14 μm), lithium anode with the thinness of 450 μm and LiFePO4 (LFP) cathode with the active material loading of 10.52 mg⋅cm􀀀 2 and areal capacity of 1.578 mAh⋅cm2 were all purchased from Guangdong Canrd New Energy Technology Co., Ltd.

Json : 
[
    {{
        "name_cell" : "LFP cathode Battery",
        "collector1" : "aluminum foil", 
        "collector2" : "copper foil"
    }}
]

name_cell: {name_cell}
Paragraph: {paragraph}
Json:
'''

PROMPT_ELECTROLYTE_NOT_MENTIONED = '''
Extract the relevant information about electrolyte mentioned in the paragraph. 
There are {name_cell} name of cells are exist in the paragraph.
Electroltye is consisted of Li salts and solvents.

There are guidlines for output format:
- You must write like 
[
    {{  
        "name_cell" : {name_cell[0]},
        "name_electrolyte" : str,
        "Li_salt" : {{ "material": [str, str,...], "concentration":[float, float,...], "unit": [str, str, ...]}}, 
        "solvent" : {{ "material": [str, str,...], "solvent_volume_ratio":[float, float, ...], "unit": [str, str, ...]}},
        "EA_ratio" : float
    }},...
]

You must follow rules below:
- The electrolyte is one of the components that make up a battery cell.
- For the "name_cell", if the name of the cell is not mentioned, please return null.
- You must extract information of electrolyte only that associated with "name_cell".
- You must extract the name of the electrolyte(e.g. carbonate electrolyte, liquid electrolyte, ether based electrolyte, ...) with description in the "name_electrolyte" field. 
- If there are 2 or more electrolyte combinations exist in paragraph, you must extract all electrolytes.
- If there are additive salt in paragraph, it is same as Li salt and you must include "Li_salt" once.
- "EA_ratio" is ratio of electrolyte(in mL) and active materials(in mg). In Lithium sulfur battery, it is same as ES ratio.
- If the "EA_ratio" value is mentioned multiple times, extract each with a different electrolyte.
- The "unit" of "solvent" is typically v, v% or wt%, each means volume, volume% and weight%.
- If you're uncertain, fill "null".

Begin!
Paragraph: The electrolyte of DD was 1.0 M LiTFSI in DOL/DME (v:v = 1:1) and DD-N was DD with 5wt% LiNO3.
Json:
[
    {{
        "name_cell" : null,
        "name_electrolyte" : "DD = 1.0 M LiTFSI in DOL/DME (v:v = 1:1)",
        "Li_salt":{{ "material": ["LiTFSI"], "concentration":[1.0],"unit": ["M"]}}, 
        "solvent":{{ "material": ["DOL", "DME"], "solvent_volume_ratio":[1,1], "unit": ["v", "v"]}},
        "EA_ratio": null
    }},
    {{
        "name_cell" : null,
        "name_electrolyte" : "DD-N = 1.0 M LiTFSI in DOL/DME (v:v = 1:1) with 5wt% LiNO3",
        "Li_salt":{{ "material": ["LiTFSI", "LiNO3"], "concentration":[1.0, 5],"unit": ["M", "wt%"]}}, 
        "solvent":{{ "material": ["DOL", "DME"], "solvent_volume_ratio":[1,1], "unit": ["v", "v"]}},
        "EA_ratio": null
    }}
]

Paragraph: All the electrolytes were prepared by dissolving the specific amount of different lithium salts in DME solvent in an Ar-filled glove box (H2O<0.1ppm, O2 < 0.1 ppm). 
0.6mol L-1(M) LiFSI-DME, 0.6M LiTFSI-DME, 0.6M LiDFOB-DME and 0.36M LiNO3-DME electrolytes denote that the corresponding concentration of different salts are dissolved in DME, 
where 0.6MLiNO3-DME electrolyte can’t be prepared because of the relatively low salt solubility. HE-DME electrolyte was prepared by dissolving 0.15MLiFSI, 0.15MLiTFSI, 
0.15MLiDFOB and 0.15MLiNO3 into DME solvent with the total concentration of lithium ion to be 0.6M.
5-component 0.6M HE-DME electrolyte was prepared by dissolving 0.15M LiFSI, 0.10M LiTFSI, 0.10M LiBFTI, 
0.10M LiDFOB and 0.15M LiNO3 into DME solvent with the total concentration of lithium to be 0.6M.
Json: 
[
    {{
        "name_cell" : null,
        "name_electrolyte" : "electrolyte = a mixture of 0.6mol L-1(M) LiFSI-DME"
        "Li_salt":{{ "material": ["LiFSI"], "concentration":[0.6],"unit": ["M"]}}, 
        "solvent":{{ "material": ["DME"], "solvent_volume_ratio":null, "unit": null}},
        "EA_ratio": null
    }}, 
    {{
        "name_cell" : null,
        "name_electrolyte" : "electroltye = a mixture of 0.6M LiTFSI-DME",
        "Li_salt":{{ "material": ["LiTFSI"], "concentration":[0.6],"unit": ["M"]}}, 
        "solvent":{{ "material": ["DME"], "solvent_volume_ratio":null, "unit": null}},
        "EA_ratio": null
    }}, 
    {{
        "name_cell" : null,
        "name_electrolyte" : "electrolyte = a mixture of 0.6M LiDFOB-DME"
        "Li_salt":{{ "material": ["LiDFOB"], "concentration":[0.6],"unit": ["M"]}},
        "solvent":{{ "material": ["DME"], "solvent_volume_ratio":null, "unit": null}},  
        "EA_ratio": null
    }}, 
    {{
        "name_cell" : null,
        "name_electrolyte" : "electrolyte = a mixture of 0.36M LiNO3-DME"
        "Li_salt":{{ "material": ["LiNO3"], "concentration":[0.36],"unit": ["M"]}},
        "solvent":{{ "material": ["DME"], "solvent_volume_ratio":null, "unit": null}},  
        "EA_ratio": null
    }}, 
    {{  
        "name_cell": null,
        "name_electrolyte" : "HE-DME = a mixture of 0.15MLiFSI, 0.15MLiTFSI, 0.15MLiDFOB and 0.15MLiNO3 into DME solvent with the total concentration of lithium ion to be 0.6M"
        "Li_salt":{{ "material": ["LiFSI", "LiTFSI", "LiDFOB", "LiNO3"], "concentration":[0.15, 0.15, 0.15, 0.15],"unit": ["M", "M", "M", "M"]}},
        "solvent":{{ "material": ["DME"], "solvent_volume_ratio":null, "unit": null}}, 
        "EA_ratio": null
    }}, 
    {{
        "name_cell": null,
        "name_electrolyte" : "5-component 0.6M HE-DME = a mixture of 0.15M LiFSI, 0.10M LiTFSI, 0.10M LiBFTI, 0.10M LiDFOB and 0.15M LiNO3 into DME solvent with the total concentration of lithium to be 0.6M"
        "Li_salt":{{ "material": ["LiFSI", "LiTFSI", "LiBFTI", "LiDFOB", "LiNO3"], "concentration":[0.15, 0.10, 0.10, 0.10, 0.15],"unit": ["M", "M", "M", "M", "M"]}},
        "solvent":{{ "material": ["DME"], "solvent_volume_ratio":null, "unit": null}}, 
        "EA_ratio": null
    }}
]

Paragraph : 
The electrolyte was 1 M lithium bis(trifluoromethanesulfonyl)imide (LiTFSI) in mixed solvent of 1,2-dimethoxyethane (DME): 1,3-dioxolane (DOL) (1:1 in volume) with 2wt% lithium nitrate (LiNO3) additive.
Json:
[
    {{
        "name_cell" : null,
        "name_electrolyte" : "electrolyte = a mixture of DOL/DME with 1 M LiTFSI and 1 wt% LiNO3.",
        "Li_salt":{{ "material": ["LiTFSI", "LiNO3"], "concentration":[1, 2],"unit": ["M", "wt%"]}}, 
        "solvent":{{ "material": ["DME", "DOL"], "solvent_volume_ratio":[1,1], "unit": ["v", "v"]}},
        "EA_ratio": null
    }}
]

name_cell: {name_cell}
Paragraph: {paragraph}
Json:
'''

PROMPT_NCM_LFP = '''
Now you have to extract the areal_capacity of cathode about the NMC or LFP cathode with the names {name_cathode_list} mentioned in the caption, result and experiment.
There are {cell_name_list} name of cells are exist and {name_cathode_list} name of cathodes are exist, respectively.

There are guildlines for output Json format:
{{
    {cell_index_list[0]}: {{"name_cathode" : {name_cathode_list[0]},        
                            "areal_capacity_of_cathode" : {{"value": float, "unit": str}}}}, ...
}}

You must follow rules belows:
- The areal capacity of a cathode is a unique value for that cathode and is usually expressed in units of mAh cm-2.
- First, find the value in mAh cm-2 from the caption, result, experiment and check if that value is the areal capcity of the cathode.
- The areal capcity value of the cathode corresponding to the name cathode must be extracted in mAh cm-2 units.
- You must only extract areal capacity of cathode, not the charge or discharge condition, and not the anode (Li).
- If areal capacity is written as a range, extract the average value.
- For unknown information, write null.

Begin!
cell_index_list: [0]
cell_name_list: ["LiFePO4 (LFP) cell at 1.0C"]
name_cathode_list: ["LiFePO4 (LFP)"]
caption:Fig. 2 | Electrochemical performance. a, b Galvanostatic charge/discharge curves of NCM811 cells in a 0.6M LiFSI-DME, b 0.6M HE-DME electrolytes within the voltage range of 2.8–4.3 V at a rate of 0.1 C (1 C = 180mA g−1). Cells were tested with a capacity of 2.0mAhcm−2 for NCM811 and 50 μm lithium metal foils, resulting in a N/P ratio of 5. f Cycling performance of LiFePO4 (LFP) cells cycled at a 0.2 C rate for three cycles before cycling at a 1.0 C rate.

result: The rate performance is evaluated in Li||NCM811 cells (Fig. 2c, d and SI Fig. 29). When charged at 6.0C (1080mAg−1) reflecting stable cycling. Cycling performance tests of the 0.6M HE-DME electrolyte in Li||NCM811 cells are performed at 0.3C (Fig. 2e), resulting in a capacity retention of over 82% after 100 cycles charged to 4.3 V. This is further demonstrated by the LiFePO4 cathodes cycled at 2.5–3.8 V which implies that a more stable interphase is formed with the 0.6M HE-DME electrolyte compared to the 0.6M LiFSI-DME electrolyte in the suitable voltage range (Fig. 2f).

experiment: The electrochemical cell was simultaneously controlled by a Maccor battery testing system. A plastic capsule cell made out of polyether ether ketone was used for the operando NMR experiments. The cells were assembled using LiFePO4 cathode (areal capacity is 2.0mAh cm−2) and Cu foils as working and counter electrodes with both a piece of Celgard and a piece of Glass fiber as separator. The operando capsule cellwas aligned in an Ag-coated Cu coil with LiFePO4 and Cu foil electrode oriented perpendicular to B0 and parallel with respect to the B1 rf-field. During the static 7Li NMR measurements, the cells were charged to the capacity of 1 mAh cm−2 at current density of 0.5mA cm−2. A charge cut-off capacity of 1mAh cm−2 was used for lithium metal plating on Cu foils and a discharge cut-off voltage of 2.0 V for stripping. Electrochemical cycling performance of LiFePO4 and NCM811 electrodes (12mm diameter) are all with an areal capacity of 2 mAh cm−2 tested with lithium metal foils with a thickness of 50 μm as counter electrode. Li||NMC811 cells were electrochemically cycled between 2.8 and 4.3 V under a 0.1 C rate for three cycles before cycling at 0.3C rate (1 C = 180mAg−1).

output: 
{{
    "0": {{"name_cathode" : "LiFePO4 (LFP)",        
           "areal_capacity_of_cathode" : {{"value": 2.0, "unit": mAh cm−2}}}}
}}

cell_index_list: {cell_index_list}
cell_name_list: {cell_name_list}
name_cathode_list: {name_cathode_list}
caption: {caption}
result: {result}
experiment: {experiment}
output:
'''