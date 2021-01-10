import os

def read_file(file_name):
  reader = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),file_name), 'r')
  lines = reader.readlines()
  reader.close()
  return lines

def save_file(file_name, file_content):
  writer = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),file_name), 'w')
  writer.writelines(file_content)
  writer.close()
  
def update_file(file_name, update_item):
  previous_content = read_file(file_name)
  split_update = update_item.split('[:]')
  file = []
  for line in previous_content:
    split_line = line.split('[:]')
    if (split_line[0] == split_update[0] and split_line[2] == split_update[2]
    ) or(split_line[0] == split_update[2] and split_line[2] == split_update[0]):
      file.append(update_item)
    else:
      file.append(line)
  save_file(file_name, file)