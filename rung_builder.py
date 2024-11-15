import csv

def build_rung(rung_data):
    old_pos = (0,0)
    cur_pos = (rung_data[0][0][1],rung_data[0][0][2])

    rung_str = ""

    for item in rung_data:
        cur_pos = (item[0][1],item[0][2])
        old_branch = old_pos[0] 
        old_level = old_pos[1] 
        cur_branch = cur_pos[0]
        cur_level = cur_pos[1]

        if old_branch > cur_branch:
            rung_str = rung_str + ']' + item[1]
        elif old_branch < cur_branch:
            rung_str = rung_str + '[' + item[1] + ' '
        else:
            if old_level > cur_level:
                rung_str = rung_str + ']' + item[1]
            elif old_level < cur_level:
                rung_str = rung_str + ',' + item[1] + ' '
            else:
                rung_str = rung_str + item[1] + " "

        old_pos = cur_pos

    while cur_branch > 0:
        rung_str = rung_str + ']'
        cur_branch -= 1
    rung_str = rung_str + ';'

    return rung_str  
            
def routine_handler(filename):
    '''     
    Description
    -------
    Loops through file and returns list of rungs
    
    Parameters
    ----------
    fp of type filepointer

    Returns
    -------
    L of type list
        list of tuples
    '''
    #filename = "csv_testing.csv"
    fp = open(filename)
    
    routine = []

    comment = ""
    new_rung = True
    got_comment = False
    raw_rung_data = list()
    
    reader = csv.reader(fp) # attaches a reader to the file fp
    next(reader, None) # skips a line, such as a header line
    
    for line in reader:
        if len(line) == 1:
            new_rung = True
            got_comment = False
            routine.append((build_rung(raw_rung_data), comment))
            raw_rung_data = []
            continue

        if new_rung:
            new_rung = False
            comment = line[1]
            got_comment = True
            continue

        if got_comment:
            position = list(map(int, line[0].split(',')))
            function_type = line[1]

            argument_holder = []
            for i in line[2:]:
                #for i in range(2, len(line)):
                argument_holder.append(i)

            arguments = ",".join(argument_holder)
            function = f"{function_type}({arguments})"

            raw_rung_data.append((position, function))

    for item in raw_rung_data:
        print(item)
    
    fp.close()
    return routine
