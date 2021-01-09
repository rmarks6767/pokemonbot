import os



def read_file(fileName):
  reader = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),fileName), 'r')
  lines = reader.readlines()
  reader.close()
  return lines

def save_file(fileName, fileContent):
  writer = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),fileName), 'w')
  writer.writelines(fileContent)
  writer.close()
