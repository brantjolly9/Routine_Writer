def parse_funtion_block(cur_pos=list(), cur_block=str()):
    position_found = False
    function_pos = cur_pos.copy()

    while position_found == False:
        first_char = cur_block[0]
        match first_char:
            case '[':
                function_pos[1] += 1
                cur_block = cur_block.lstrip('[')
            case ']':
                function_pos[1] -= 1
                function_pos[2] -= 1
                cur_block = cur_block.lstrip(']')
            case ',':
                function_pos[2] += 1
                cur_block = cur_block.lstrip(',')
            case _:
                position_found = True

    block_holder = cur_block.split('(')
    function = [block_holder[0]]
    arg_holder = block_holder[1].split(',')

    for item in arg_holder:
        function.append(item)

    return [function_pos, function]


def parse_routine(raw_routine_data=list()):
    '''
    Description
    -------
    Handles the parsing of LX5 plaintext routine data

    Parameters
    ----------
    raw_routine_data of type list

    Returns
    -------
    parsed_routine_data of type list
    '''
    parsed_routine_data = []
    rung_num = 0
    for rung in raw_routine_data: #Loops through all rungs in routine
        #clean up the string for formatting
        temp_rung = rung[0].rstrip(';')
        temp_rung = temp_rung.rstrip(']')
        temp_rung = temp_rung.replace(' ', '')
        raw_rung_data = temp_rung.split(')')
        raw_rung_data.pop()

        parsed_rung_data = []
        position = [rung_num, 0, 0]
        for item in raw_rung_data: #Loops through function blocks in rung
            raw_function = item
            parsed_function = parse_funtion_block(position, raw_function)
            position = parsed_function[0].copy()
            parsed_rung_data.append(parsed_function)

        rung_comment = ["Rung Comment:", rung[1]]
        idk_anymore = [parsed_rung_data.copy(), rung_comment]
        #parsed_rung_data.append(rung_comment)
        #print(parsed_rung_data)
        parsed_routine_data.append(idk_anymore)
        rung_num += 1

    return parsed_routine_data
