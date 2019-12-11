import tensorflow as tf
from tensorflow import keras
import numpy as np
import xlrd, string

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Machine Learning
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


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

        if iso3_code is None or disaster_type is None or displacement is None or displacement == '':
            continue
        disaster_type = string.capwords(disaster_type.lower())

        iso3_index = region_dict[iso3_code]
        disaster_index = disaster_dict[disaster_type]

        region_arr = np.zeros(196)
        disaster_arr = np.zeros(12)

        region_arr[iso3_index] = 1
        disaster_arr[disaster_index] = 1

        x_train.append(np.concatenate((region_arr, disaster_arr)))
        y_train.append(displacement)

    x = np.asarray(x_train)
    y = np.asarray(y_train)

    return x, y


def main():
    region_dict = create_mapped_dict('../Resources/indexedRegions.xlsx')
    disaster_dict = create_mapped_dict('../Resources/indexedDisasters.xlsx')

    X, y = build_train_set(region_dict, disaster_dict)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

    svc_class = SVC(kernel='sigmoid')
    svc_class.fit(X_train, y_train)
    print(svc_class.score(X_test, y_test))
    print(svc_class.predict(X_test))
    print(y_test)


if __name__ == '__main__':
    main()
