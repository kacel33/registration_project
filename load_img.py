import nrrd
import argparse
import numpy as np
import SimpleITK as sitk

def load_img():
    img = sitk.ReadImage(args.img)
    t1 = sitk.GetArrayFromImage(img)
    trans = np.transpose(t1, (2, 1, 0))
    trans = np.flip(trans, 1)
    print('ROI img shape : {}'.format(trans.shape))
    return trans

def write_changed_nrrd():
    nrrd_data, nrrd_header = nrrd.read(args.nrrd)
    trans = load_img()
    nrrd.write(args.output, trans, nrrd_header)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--nrrd', type=str, help='write nrrd file path')
    parser.add_argument('--img', type=str, help='write img file path')
    parser.add_argument('--output', type=str, help='write output file path')
    args = parser.parse_args()
    print(args)

    write_changed_nrrd()

