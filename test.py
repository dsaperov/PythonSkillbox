def generator(file):
    prev_line = None
    prev_line_count = None

    cur_line = True
    while cur_line:
        cur_line = file.readline()
        if ' OK' not in cur_line:
            cur_line = cur_line[1:17]
            if cur_line != prev_line:
                if prev_line:
                    yield prev_line, prev_line_count
                prev_line, prev_line_count = cur_line, 1
            else:
                prev_line_count += 1

file_to_parse = r'D:\PycharmProjects\PythonSkillbox\lesson_009\events.txt'

print(dir(generator))
