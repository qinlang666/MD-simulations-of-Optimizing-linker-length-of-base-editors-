# MD-simulations-of-Optimizing-linker-length-of-base-editors-
This is the code of MD simulations of paper "Optimizing linker length of base editors for precise crop breeding and gene therapy"
The main contents of this library include the processing flow of different linker base editors, tpr files of molecular dynamics simulation, start commands and analysis commands

1. Predicted protein model:
We use alphafold3 to predict base editor's model. The setting is total protein's pTM greater than 0.7, core part of the protein ‘s plDDT greater than 90. All protein structure were analyzed the Ramachandran plots using  SAVESv6.1 to ensure that all models exhibited good quality, with amino acids falling into the disallowed region accounting for less than 5%. The model_0 selected as the optimal  starting structure for MD simulations using GROMACS (v2024.4, CUDA)

2. Protein model pretreatment:
The Amber99BSC1 force field and TIP3P water model were used for MD. The complex was centered in a cubic box (15 A buffer), treatment with Na⁺/Cl⁻ (0.15 M), and simulated using particle mesh Ewald for electrostatics (14 A cut-off) and LINCS for H-bond constraints under periodic boundary conditions. The pH of the simulated system was normal physiological pH (pH = 7.35). And the model will be suffer energy minimization (steepest descent, ≤ 2,500 steps or force <1,000 kJ mol⁻¹ nm⁻¹),the system underwent 100 ps NVT (310 K, V-rescale) and 100 ps NPT (1.0 bar, Parrinell–Rahman) equilibration

3. MD simulations： we use runmd.slurm for MD simulations #本文的分子动力学模拟均在华南农业大学大学的算力集群中进行300ns的模拟，使用slurm调度系统脚本运行。

4. Results Analysis:

4.1 Solvent Accessible Surface Area(SASA):
   first, we use trjconvcomand to get the equilibration system:
   gmx trjconv -f md.xtc -s md.tpr -o 100ns.gro -dump 100000  （ps） #提取150ns稳定后的构象
   then, we use SASA comand to get SASA
   gmx sasa -s md.tpr -f md.xtc -o area.xvg -or resarea.xvg -oa atomarea.xvg #提取SASA
   
4.2 Root Mean Square Deviation(RMSD): gmx rms -s md.tpr -f noPBC.xtc -o rmsd_pro.xvg #提取RMSD

4.3 Range of gyration(Rg):gmx gyrate -f noPBC.xtc -s md.tpr -o Rg.xvg #提取Rg

4.4 Root Mean Square Fluctuation(RMSF):gmx rmsf -s md.tpr -f noPBC.xtc -res -o rmsf.xvg #提取RMSF

4.5 free energy landscape(FEL):
   first, we combined the Rg and RMSD with the code combineRg_RMSD.py #合并Rg和RMSD
   then, we use the sham command for FEL:
   gmx sham -f combined.xvg -ls gibbs.xpm #构建自由能形貌图
   finally, we use plotly to Output FEL.
   
4.6 convert command: gmx convert-tpr -s md.tpr -extend 200000 -o md.tpr #用于延长MD模拟时间，200000ps为200ns 
 
