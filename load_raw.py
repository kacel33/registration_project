import json
import nrrd
import argparse
import numpy as np
from glob import glob
from oct2py import Oct2Py
import matplotlib.pyplot as plt

def extract_num_from_raw():
    name = args.raw
    extract_num = name.split('.')[1]
    extract_num = extract_num.split('x')
    extract_num = list(map(int, extract_num))
    return extract_num
def matlab_raw_read():
    #----matlab raw read-----  matlab and ppython have different raw file load results
    oc = Oct2Py()
    fid = oc.fopen(args.raw, 'r')
    num = extract_num_from_raw()
    I = oc.fread(fid, num[0]*num[1]*num[2], 'uint8')
    z = oc.reshape(I, [num[0], num[1], num[2]])
    z = np.asarray(z).astype(np.uint8)
    return z

def load_json():
    with open(args.json) as f:
        data = json.load(f)
    return data

def extract_roi_info(json_data):
    roi_dict = {'x1' : 0, 'x2' : 0, 'y1' : 0, 'y2' : 0, 'z1' : 0, 'z2' : 0}
    roi_info = json_data['dimension']['maskVOI'].replace('-', ',').replace('(', '').replace(')', '')
    roi_info = np.array(roi_info.split(',')).astype(np.int32).reshape(2, 3)
    roi_info = np.transpose(roi_info, (1, 0))
    roi_dict['x1'], roi_dict['x2'] = roi_info[0][0], roi_info[0][1]
    roi_dict['y1'], roi_dict['y2'] = roi_info[1][0], roi_info[1][1]
    roi_dict['z1'], roi_dict['z2'] = roi_info[2][0], roi_info[2][1]
    return roi_dict

def change_nrrd_roi(nrrd_data, roi_info, roi):
    R = roi_info
    zero_data = np.zeros_like(nrrd_data).astype(np.int16)
    zero_data[R['x1']:R['x2'], R['y1']:R['y2'], R['z1']:R['z2']] = roi
    zero_data = np.where(nrrd_data == 255, 1, 0)
    return zero_data

def write_changed_nrrd(nrrd_data, roi_info, roi):
    change_nrrd_data = change_nrrd_roi(nrrd_data, roi_info, roi)
    nrrd.write(args.nrrd, change_nrrd_data, nrrd_header)
    print('write nrrd done')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--nrrd', type=str, help='write nrrd file path')
    parser.add_argument('--json', type=str, help='write json file path')
    parser.add_argument('--raw', type=str, help='write raw file path')
    args = parser.parse_args()
    print(args)

    roi = matlab_raw_read()
    json_data = load_json()
    roi_info = extract_roi_info(json_data)
    print('roi info : {}'.format(roi_info))

    nrrd_data, nrrd_header = nrrd.read(args.nrrd)
    write_changed_nrrd(nrrd_data, roi_info, roi)














