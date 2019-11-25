import xlrd, string

workbook = xlrd.open_workbook('idmc_disaster_all_dataset.xlsx')
sheet = workbook.sheet_by_index(0)


category_list = []
disaster_type_list = []

for i in range(2, sheet.nrows):
   disaster_type = sheet.cell(i, 1).value

   if disaster_type is not None:
       disaster_type = string.capwords(disaster_type.lower())
       if disaster_type not in disaster_type_list:
           disaster_type_list.append(disaster_type)



    # Export to ui/ui2.py in order to link data with neural network.

print(category_list)
print(disaster_type_list)
