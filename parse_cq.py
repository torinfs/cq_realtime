import csv
import os.path


def parseCQtoCSV(filename):
    '''
    Parses a Chronus Quantum real-time tddft output file and stores the results in a 
    .csv formatted file

    INPUTS:
    * filename (string), name of cq.out file.

    OUTPUTS:
    * "filename + _dipole.csv", file written to current directory.
    '''

    # expression to find in CQ.out file  
    expr = 'Dipole (X)'

    with open(filename) as file_obj:
        #file_contents = file.read()
        lines = file_obj.read().split("\n")


        for i, line in enumerate(lines):
            if expr in line:
                dipoles = lines[i+3:-1]
                break

    # Remove MMUT lines without dipole data
    mmut_line = '  *** Restarting MMUT ***'
    mmut_remove = lambda x: x != mmut_line
    dipoles = list(filter(mmut_remove, dipoles))

    # remove CQ job end line if there including blank lines
    dipoles = list(filter(None, dipoles))
    if str(dipoles[-1][0]) == 'C':
        dipoles.pop()

    # Trim white space in list of lists
    clean_dipoles = [[0.0] * 5] * len(dipoles)
    for i in range(len(dipoles)):
        clean_dipoles[i] = [float(i) for i in dipoles[i].split()]

    # Write dipole to .csv file ("filename"_data.csv)
    basename = os.path.splitext(filename)[0]
    with open(basename + "_dipole.csv", "w") as newfile:
        writer = csv.writer(newfile)
        writer.writerows(clean_dipoles)


parseCQtoCSV('benzene_gto_Y.out')
