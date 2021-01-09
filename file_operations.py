
def read_file(fileName):
  reader = open(fileName, 'r')
  lines = reader.readlines()
  reader.close()
  return lines

def save_file(fileName, fileContent):
  writer = open(fileName, 'w')
  writer.writelines(fileContent)
  writer.close()
