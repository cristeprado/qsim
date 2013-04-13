import custom_file_reader

fileStream = open("qsim-config.txt","r")
currFile=custom_file_reader.CustomFileReader(fileStream,'horizontal','str')
dd=currFile.get_dict()
print dd
