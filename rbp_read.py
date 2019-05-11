import pandas as pd

df = pd.read_csv("C:\\Users\\MeanMachine\\Downloads\\RBPs.txt", sep="\t")

a = """AARS     
AGGF1     
AKAP8L   
AUH      
BCCIP    
CPSF6    
CSTF2T   
DDX3X    
DDX42    
DDX55    
DDX6     
DGCR8    
DKC1     
DROSHA   
EFTUD2   
EIF3D    
EIF4G1   
EIF4G2   
EWSR1    
FAM120A  
FASTKD2  
FKBP4    
FMR1     
FUS      
FXR1     
FXR2     
GRSF1    
GTF2F1   
HLTF     
HNRNPA1  
HNRNPC   
HNRNPK   
HNRNPM   
HNRNPU   
HNRNPUL1 
IGF2BP1  
IGF2BP2  
IGF2BP3  
ILF3     
KHDRBS1  
KHSRP    
LARP4    
LARP7    
LIN28B   
LSM11    
METAP2   
MTPAP    
NCBP2    
NKRF     
NOL12    
NONO     
NPM1     
PCBP2    
PPIL4    
PRPF8    
PTBP1    
PUM2     
QKI      
RBFOX2   
RBM15    
RBM22    
RBM27    
RPS11    
RPS5     
SAFB2    
SBDS     
SF3A3    
SF3B4    
SFPQ     
SLBP     
SLTM     
SMNDC1   
SND1     
SRSF1    
SRSF7    
SRSF9    
TAF15    
TARDBP   
TBRG4    
TIA1     
TIAL1    
TNRC6A   
TRA2A    
TROVE2   
U2AF1    
U2AF2    
UPF1     
XRCC6    
XRN2     
YWHAG    
ZNF622   
ZRANB2"""

new = []

for i in a.split("\n"):
    new.append(i.strip())


df_dic =  {}

for i in range(len(df)):
    df_dic[df["HGNC_Gene_Symbol"][i]] = df["ENSEMBL_Gene_ID"][i]

print(df_dic)

master = {}

for i in range(len(new)):
    if new[i] in df_dic.keys():
        master[new[i]] = df_dic[new[i]]
    else:
        print(new[i])

print(len(master))

master["AARS"] = "ENSG00000090861"
master["AGGF1"] = "ENSG00000164252"
master["AUH"] = "ENSG00000148090"
master["DGCR8"] = "ENSG00000128191"

print(master)
print(master["UPF1"])