# python3 main.py ros_version path_to_file

import ros1_extract
import ros2_extract
import sys


def main():
    ros_ver = sys.argv[1]
    # path_to_file = 'rosbag2_2022_05_25-1/rosbag2_2022_05_25-15_53_16' #/2022-07-01-06-30-52.bag'
    if ros_ver == 'ros1':
        path_to_file = sys.argv[2]
        ros1_extract.main(path_to_file)
    elif ros_ver == 'ros2':
        path_to_file = sys.argv[2]
        ros2_extract.main(path_to_file)
    else:
        print("ROS version does not exist, please enter either 'ros1' or 'ros2'.")
        sys.exit()


if __name__ == '__main__':
    main()