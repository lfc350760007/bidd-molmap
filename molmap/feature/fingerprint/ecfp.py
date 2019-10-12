from rdkit.Chem import AllChem
from rdkit.Chem import  DataStructs
import numpy as np

def GetECFPs(mol, nBits=2048, radius = 4, return_bitInfo = False):
    
    bitInfo={}
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=radius, 
                                               bitInfo=bitInfo, nBits = nBits)
    arr = np.zeros((0,),  dtype=np.bool)
    DataStructs.ConvertToNumpyArray(fp, arr)
    
    if return_bitInfo:
        return arr, bitInfo
    return arr