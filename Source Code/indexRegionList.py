import xlsxwriter
import xlrd

workbook = xlrd.open_workbook('../Resources/idmc_disaster_all_dataset.xlsx')
sheet = workbook.sheet_by_index(0)
region_list = []
for i in range(2, sheet.nrows):
    region = sheet.cell(i, 0).value

    if region is not None:
        region = region.upper()
        if region not in region_list:
            region_list.append(region)


workbook = xlsxwriter.Workbook('../Resources/indexedRegions.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0
counter = 0

for iso3 in region_list:
    worksheet.write(row, col, iso3)
    worksheet.write(row, col + 1, counter)
    row += 1
    counter += 1

workbook.close()
