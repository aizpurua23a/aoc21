import numpy as np





def rotate():
    for rot in _3d_rotations():
        print(rot)
        print(np.linalg.det(rot))


if __name__ == '__main__':
    rotate()
