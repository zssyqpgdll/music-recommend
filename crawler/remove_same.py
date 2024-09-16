def file_remove_same(input_file_name, output_file_name):
    with open(input_file_name, 'r', encoding='utf-8') as input, open(output_file_name, 'a', encoding='utf-8') as output:
        input_lines = []
        for line in input:
            if line not in input_lines:
                input_lines.append(line)
                output.write(line)
                output.flush()
        input.close()
        output.close()

#去重
# file_remove_same('./dataset/user_info_init.txt', './dataset/user_info.txt')
file_remove_same('./dataset/song_info.txt', './dataset/song_info_remove.txt')