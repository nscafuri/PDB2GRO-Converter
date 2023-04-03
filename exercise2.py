# This script takes a PDB file or a GRO file as input and outputs a new file, by default output.pdb or output.gro, with only the atoms within a specified range of residue IDs specified by the user.
#
#
# Input File
# The protein_0.pdb file was rearranged using the pdb-tool script, so that the residue IDs start from 0 instead of -1 (the new file is protein_0.pdb)
# protein_0.gro  was generated from protein_0.pdb file by using "pdb2gmx" module implemented in GROMACS.
#
#
# Execution
# The script accepts either a PDB file or a GRO file as an argument: python3 exercise2.py protein_0.pdb (protein_0.gro)
# The script was tested with Python 3.8.10
#
# Dependencies
# sys
######################################################################################################################################################

# Import the sys module for reading command line arguments
import sys

# Define the `read_pdb` function to extract relevant information from a PDB file
def read_pdb(input_file):
    ATOM, atom, atom_type, res, chain, res_ID, = [],[], [], [], [], []  # Initialize lists to store the extracted information 
    x, y, z = [], [], [] 
    with open(input_file, "r") as f:                                    # Open the input file and read each line
         for line in f:
             if line.startswith("ATOM"):                                # If the line starts with "ATOM", extract the relevant information
                values = line.split()                                   # Split the string in substrings, separated by space by default
                ATOM.append(values[0])
                atom.append(int(values[1]))
                atom_type.append(values[2])
                res.append(values[3])
                chain.append(values[4])
                res_ID.append(int(values[5]))
                x.append(float(values[6]))
                y.append(float(values[7]))
                z.append(float(values[8]))

    return ATOM, atom, atom_type, res, chain, res_ID, x, y, z           # Return the extracted information


# Define the `read_gro` function to extract relevant information from a GRO file
def read_gro(input_file):
    residue_number, atom_type, atom = [], [], []                        # Initialize lists to store the extracted information
    x, y, z = [], [], []
    with open(input_file, "r") as f:                                    # Open the input file and read each line
         header = f.readline().strip() 
         N_atoms = int(f.readline().strip())
         for line in f: 
             values = line.split() 
             residue_number.append(values[0])
             atom_type.append(values[1]) 
             atom.append(values[2]) 
             x.append(float(values[3])) 
             y.append(float(values[4])) 
             z.append(float(values[5])) 


         residue_number = residue_number[:-1]                         # Remove values from the last line of the file, which contains information about the box vectors
         atom_type      = atom_type[:-1]
         atom           = atom[:-1]
         x              = x[:-1]
         y              = y[:-1]
         z              = z[:-1]
         
    res, res_ID = [], []
    for i in range(len(residue_number)):                              # Exctract res and res ID information that are merged in the gro file.   
        res.append(residue_number[i][-3:])                            # The "res_ID" is obtained by taking the last three characters of the string,
        res_ID.append(int(residue_number[i][:-3]))                    # while "res" is obtained by taking the rest.

         
    return N_atoms, res, res_ID, atom_type, atom, x, y, z


# Get the input file name from the command line argument
input_file = sys.argv[1]               

# Check if the input file is a PDB file
if input_file.endswith(".pdb"):
   ATOM, atom, atom_type, res, chain, res_ID, x, y, z = read_pdb(input_file)  # Call the read_pdb function to read the PDB file and extract the relevant information
else:
   N_atoms, res, res_ID, atom_type, atom, x, y, z     = read_gro(input_file)  # Call the read_gro function to read the GRO file and extract the relevant information

# Ask the user to input the first and last residue IDs
First_residue = int(input("Enter your first residue ID: "))
Last_residue  = int(input("Enter your final residue ID: "))

output_lines = []
for i in range(len(ATOM) if input_file.endswith(".pdb") else N_atoms):
    if (res_ID[i] >= First_residue) and (res_ID[i] <= Last_residue):
       if input_file.endswith(".pdb"):
          line = "{:4s}      {}  {:3s}   {:3s} {:1s} {}      {:.3f}   {:.3f}   {:.3f}\n".format(ATOM[i], atom[i], atom_type[i], res[i], chain[i], res_ID[i], x[i], y[i], z[i])
       else:
          line = "    {}{}      {:4s}  {:3s}   {:.3f}   {:.3f}   {:.3f} \n".format(res_ID[i], res[i], atom_type[i], atom[i], x[i], y[i], z[i])
       output_lines.append(line)
with open("output.pdb" if input_file.endswith(".pdb") else "output.gro", "w") as a:
   a.write("".join(output_lines))











