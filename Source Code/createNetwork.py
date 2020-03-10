import string
from joblib import dump, load
import pickle
import numpy as np
import xlrd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import sys


def create_mapped_dict(filepath):
    workbook = xlrd.open_workbook(filepath)
    sheet = workbook.sheet_by_index(0)

    mapped_dict = {}

    for i in range(0, sheet.nrows):
        key = sheet.cell(i, 0).value
        val = int(sheet.cell(i, 1).value)

        mapped_dict[key] = val

    return mapped_dict


def build_train_set(region_dict, disaster_dict):
    workbook = xlrd.open_workbook('../Resources/idmc_disaster_all_dataset.xlsx')
    sheet = workbook.sheet_by_index(0)

    x_train = []
    y_train = []

    for i in range(2, sheet.nrows):
        iso3_code = sheet.cell(i, 0).value
        disaster_type = sheet.cell(i, 6).value
        displacement = sheet.cell(i, 7).value
        timeframe = sheet.cell(i, 3).value
        #
        # if (displacement < 1000):
        #     continue

        #print(timeframe[5:7])

        month_idx = np.asarray([int(timeframe[5:7])])

       # print(one_hot_target)

        if iso3_code is None or disaster_type is None or disaster_type == '' or displacement is None or displacement == '':
            continue
        disaster_type = string.capwords(disaster_type.lower())

        iso3_index = region_dict[iso3_code]
        disaster_index = disaster_dict[disaster_type]

        reg = [iso3_index]
        region_arr = np.asarray(reg)
 #       print(region_arr)

        dis = [disaster_index]
        disaster_arr = np.asarray(dis)
#        print(disaster_arr)

        total_input = np.concatenate((region_arr, disaster_arr, month_idx))

        x_train.append(total_input)
        y_train.append(displacement)

    x = np.asarray(x_train)
    y = np.asarray(y_train)

    return x, y


def main():
    region_dict = create_mapped_dict('../Resources/indexedRegions.xlsx')
    disaster_dict = create_mapped_dict('../Resources/indexedDisasters.xlsx')

    X, y = build_train_set(region_dict, disaster_dict)

    # nsamples, nx, ny = X.shape
    # d2_X = X.reshape((nsamples, nx*ny))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

    svc_class = SVC(gamma='auto')
    svc_class.fit(X_train, y_train)

    # for i in range(len(X_test)):
    #     print(y_test[i], svc_class.predict([X_test[i]]))

    dump(svc_class, '../Resources/model.joblib', compress=3)


if __name__ == '__main__':
    main()
