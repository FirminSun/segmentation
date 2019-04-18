#!/usr/bin/python3

"""
Copyright 2018-2019  Firmin.Sun (fmsunyh@gmail.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# -----------------------------------------------------
# @Time    : 4/17/2019 4:55 PM
# @Author  : Firmin.Sun (fmsunyh@gmail.com)
# @Software: ZJ_AI
# -----------------------------------------------------
# -*- coding: utf-8 -*-
import csv
import os

filename_1 = 'data_processing/C300/data/C300商品信息表.csv'
filename_2 = 'data_processing/C300/data/商品表0417.csv'
result_path = 'data_processing/C300/data/compare_result.csv'

project_path = os.path.join(os.path.dirname(__file__), '../../')

print(project_path)

# def compare(src, dst):
#     with open(src) as f:
#         reader = csv.reader(f)
#         data = list(reader)
#         print(data)

def compare(src, dst):
    result = []
    with open(src,encoding='utf-8-sig') as src_f:
        src_reader = csv.DictReader(src_f)
        src_data = [row for row in src_reader]
    with open(dst,encoding='utf-8-sig') as dst_f:
        dst_reader = csv.DictReader(dst_f)
        dst_data = [row for row in dst_reader]

    for s_row in src_data:
        flag = True
        for d_row in dst_data:
            if s_row['商品条形码'] == d_row['商品条形码']:
                flag = False
                break

        if flag == True:
            result.append(s_row)

    return result


def save_result(data, path):
    headers = ['商品条形码','商品名称']
    with open(path, 'w', newline='') as f:
        # 标头在这里传入，作为第一行数据
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        print('save result to ', path)

if __name__ == '__main__':

    src = os.path.join(project_path, filename_2)
    dst = os.path.join(project_path, filename_1)
    path = os.path.join(project_path, result_path)

    result = compare(src, dst)
    save_result(result, path)