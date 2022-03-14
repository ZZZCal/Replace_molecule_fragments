import sys
import re
from ase import io

def operation_on_file(OperationFile, CoordinateFile):
    title = []
    operation = []
    data = []
    with open(OperationFile, 'r') as fx:
        for lines in fx:
            line = re.split('\s+', lines)
            line = [x for x in line if x != '']
            operation.append(line)

    with open(CoordinateFile, 'r') as fy:
        for lines in fy:
            line = re.split('\s+', lines)
            line = [x for x in line if x != '']
            if 3 < len(line) < 10:
                data.append(line)
            else:
                title.append(line)
    for i in range(len(operation)):
        for j in range(len(data)):
            if data[j][4] == operation[i][0]:
                if operation[i][1] == "replace":
                    data[j][0] = operation[i][2]
                elif operation[i][1] == "delete":
                    data[j][0] = "Del"
                # more operations can be added here
    return title, data

def write_xyzfile(filename, title, data):

    # count how many atoms are deleted:
    count = 0
    for i in range(len(data)):
        if data[i][0] == "Del":
            count += 1
    title[0][0] = str(int(title[0][0]) - count)

    # write xyz file title:
    with open(filename, 'w') as f:
        for line in title:
            line = re.sub("[][\',]", "", ("%s\n" % line))
            f.write(line)

    # write full xyz file:
    with open(filename, 'a') as fnew:
        for lineAdd in sorted(data):
            del lineAdd[4:]
            if lineAdd[0] != "Del":
                lineAdd = re.sub("[][\',]", "", ("%s\n" % lineAdd))
                fnew.write(lineAdd)

def convert_file(xyzfile, filetype):
    xyz = io.read(xyzfile)
    if filetype == "cif":
        name = xyzfile + ".cif"
        io.write(name, xyz)
    if filetype == "vasp":
        name = xyzfile + ".vasp"
        io.write(name, xyz)
    if filetype == "gjf":
        name = xyzfile + ".gjf"
        io.write(name, xyz)



if __name__ == "__main__":
    # title, data = operation_on_file("operation.txt", "test.xyz")
    # write_xyzfile("newFile.xyz", title, data)
    # convert_file('newFile.xyz', 'cif')

    title, data = operation_on_file(sys.argv[1], sys.argv[2])
    file_name = sys.argv[3]
    if file_name.endswith("xyz"):
        write_xyzfile(file_name, title, data)
    elif file_name.endswith("cif"):
        write_xyzfile("temp.xyz", title, data)





