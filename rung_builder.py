import csv

def build_rung(rung_data):
    old_pos = (0,0)
    cur_pos = (rung_data[0][0][1],rung_data[0][0][2])

    temp = "[MOVE('CABLL',Param.BuildingName) MOVE('SL-0001',Param.SorterName) MOVE(5,Param.TotalNumberOfBelts) MOVE(5,Param.ConveyorNumberOfSorter[0]) ,OTL(Param.AcbPresent) OTL(Param.OutboundSorter) OTL(Param.SmallsSorter) OTL(Param.HytrolSorter) OTL(Param.ShoesPresortLeft) OTL(Param.DoubleSidedSorter) ,MOVE(75,Param.NumberOfDestinations) MOVE(75,Param.OverflowDestination) MOVE(3,Param.MinimumDivertLength) ,MOVE(22,Param.MaximumDivertLength) MOVE(10,Param.AverageParcelLength) MOVE(4,Param.WrongSorterDestination) MOVE(4,Param.CameraNoReadDestination) MOVE(3000,Param.ChuteNumberingOffset) ,MOVE(86,Param.PresortingDivertOffset) MOVE(5,Param.PresortingBuffer) MOVE(4,Param.PresortDivertInterlockingBelt) MOVE(3,Param.ShoeLength) ,MOVE(2,Param.ShoeOutOfPositionBelt) MOVE(20,Param.ShoeOutOfPositionOffset) ,MOVE(415,Param.SorterFpmSpeed) MOVE(415,Param.SorterHslaSpeed) MOVE(415,Param.SorterNonHslaSpeed) ,XIC(EmulatorActive) MOVE(10,Param.PlcChatIpAddress[0]) MOVE(71,Param.PlcChatIpAddress[1]) MOVE(168,Param.PlcChatIpAddress[2]) MOVE(131,Param.PlcChatIpAddress[3]) ,XIC(EmulatorActive) MOVE(192,Param.XleIpAddress[0]) MOVE(168,Param.XleIpAddress[1]) MOVE(10,Param.XleIpAddress[2]) MOVE(114,Param.XleIpAddress[3]) ,XIC(EmulatorActive) MOVE(Param.XleIpAddress[0],Param.ChatIpAddress[0]) MOVE(Param.XleIpAddress[1],Param.ChatIpAddress[1]) MOVE(Param.XleIpAddress[2],Param.ChatIpAddress[2]) MOVE(Param.XleIpAddress[3],Param.ChatIpAddress[3]) ,XIO(EmulatorActive) MOVE(10,Param.XleIpAddress[0]) MOVE(86,Param.XleIpAddress[1]) MOVE(80,Param.XleIpAddress[2]) MOVE(154,Param.XleIpAddress[3]) ,XIO(EmulatorActive) MOVE(10,Param.PlcChatIpAddress[0]) MOVE(86,Param.PlcChatIpAddress[1]) MOVE(80,Param.PlcChatIpAddress[2]) MOVE(156,Param.PlcChatIpAddress[3]) ,MOVE(10,Param.PrimaryCameraIpAddress[0]) MOVE(86,Param.PrimaryCameraIpAddress[1]) MOVE(80,Param.PrimaryCameraIpAddress[2]) MOVE(163,Param.PrimaryCameraIpAddress[3]) ,MOVE(10,Param.BackupCameraIpAddress[0]) MOVE(86,Param.BackupCameraIpAddress[1]) MOVE(80,Param.BackupCameraIpAddress[2]) MOVE(164,Param.BackupCameraIpAddress[3]) ];"
    temp = "[MOVE('CABLL',Param.BuildingName) MOVE('SL-0001',Param.SorterName) MOVE(5,Param.TotalNumberOfBelts) MOVE(5,Param.ConveyorNumberOfSorter[0]) ,OTL(Param.AcbPresent) OTL(Param.OutboundSorter) OTL(Param.SmallsSorter) OTL(Param.HytrolSorter) OTL(Param.ShoesPresortLeft) OTL(Param.DoubleSidedSorter) ,MOVE(75,Param.NumberOfDestinations) MOVE(75,Param.OverflowDestination) MOVE(3,Param.MinimumDivertLength) ,MOVE(22,Param.MaximumDivertLength) MOVE(10,Param.AverageParcelLength) MOVE(4,Param.WrongSorterDestination) MOVE(4,Param.CameraNoReadDestination) MOVE(3000,Param.ChuteNumberingOffset) ,MOVE(86,Param.PresortingDivertOffset) MOVE(5,Param.PresortingBuffer) MOVE(4,Param.PresortDivertInterlockingBelt) MOVE(3,Param.ShoeLength) ,MOVE(2,Param.ShoeOutOfPositionBelt) MOVE(20,Param.ShoeOutOfPositionOffset) ,MOVE(415,Param.SorterFpmSpeed) MOVE(415,Param.SorterHslaSpeed) MOVE(415,Param.SorterNonHslaSpeed) ,XIC(EmulatorActive) MOVE(10,Param.PlcChatIpAddress[0]) MOVE(71,Param.PlcChatIpAddress[1]) MOVE(168,Param.PlcChatIpAddress[2]) MOVE(131,Param.PlcChatIpAddress[3]) ,XIC(EmulatorActive) MOVE(192,Param.XleIpAddress[0]) MOVE(168,Param.XleIpAddress[1]) MOVE(10,Param.XleIpAddress[2]) MOVE(114,Param.XleIpAddress[3]) ,XIC(EmulatorActive) MOVE(Param.XleIpAddress[0],Param.ChatIpAddress[0]) MOVE(Param.XleIpAddress[1],Param.ChatIpAddress[1]) MOVE(Param.XleIpAddress[2],Param.ChatIpAddress[2]) MOVE(Param.XleIpAddress[3],Param.ChatIpAddress[3]) ,XIO(EmulatorActive) MOVE(10,Param.XleIpAddress[0]) MOVE(86,Param.XleIpAddress[1]) MOVE(80,Param.XleIpAddress[2]) MOVE(154,Param.XleIpAddress[3]) ,XIO(EmulatorActive) MOVE(10,Param.PlcChatIpAddress[0]) MOVE(86,Param.PlcChatIpAddress[1]) MOVE(80,Param.PlcChatIpAddress[2]) MOVE(156,Param.PlcChatIpAddress[3]) ,MOVE(10,Param.PrimaryCameraIpAddress[0]) MOVE(86,Param.PrimaryCameraIpAddress[1]) MOVE(80,Param.PrimaryCameraIpAddress[2]) MOVE(163,Param.PrimaryCameraIpAddress[3]) ,MOVE(10,Param.BackupCameraIpAddress[0]) MOVE(86,Param.BackupCameraIpAddress[1]) MOVE(80,Param.BackupCameraIpAddress[2]) MOVE(164,Param.BackupCameraIpAddress[3]) ];"

    rung_str = ""

    for item in rung_data:
        cur_pos = (item[0][1],item[0][2])
        old_branch = old_pos[0] 
        old_level = old_pos[1] 
        cur_branch = cur_pos[0]
        cur_level = cur_pos[1]
        
        branch_change = str()
        level_change = str()

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



def open_file():
    '''     
    Description
    -------
    Prompts user for filename until a valid one is provided and open it.
    
    Parameters
    ----------
    None

    Returns
    -------
    fp of type filepointer
    '''

    fp = open("csv_testing.csv")
    '''
    continue_check = True
    while continue_check: #Loop until valid file provided
        try:
            #filename = "map0.csv"
            filename = input('Enter the file name: ')
            fp = open(filename)
            continue_check = False #Ends loop
            
        except FileNotFoundError:
            print('\nFile not found.! Try again.')
    ''' 
    return fp      
            
def read_file(fp):
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
           
    return routine

def routine_handler():
    L = read_file(open_file())






def main():
    routine_handler()

if __name__=='__main__':
    main()