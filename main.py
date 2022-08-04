# python3 main.py ros_version path_to_file

import ros1_extract
import ros2_extract
import sys
from datetime import datetime
from rosbags.rosbag2 import Reader


def date_to_datetime(time):
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S")


def main():
    path_to_file = sys.argv[1]

    start = sys.argv[2]
    end = sys.argv[3]

    with Reader(path_to_file) as reader:
        bag_start = datetime.fromtimestamp(reader.start_time // 1000000000)
        bag_end = datetime.fromtimestamp(reader.end_time // 1000000000)
        print("The bagfile STARTS at：", bag_start, " and ENDS at: ", bag_end)

    if start == 'start':
        start_t = bag_start
    else:
        if date_to_datetime(start) < bag_start or date_to_datetime(start) > bag_end:
            print("Please input a valid start time.")
            sys.exit()
        else:
            start_t = date_to_datetime(start)

    if end == 'end':
        end_t = bag_end
    else:
        if date_to_datetime(end) > bag_end or date_to_datetime(end) < bag_start:
            print("Please input a valid end time.")
            sys.exit()
        else:
            end_t = date_to_datetime(end)

    ros2_extract.main(path_to_file, start_t, end_t)


    #
    # while True:
    #     option = input("Do you want to extract the graph from a specific time window? (y/n)  ")
    #     if option != 'y' and option != 'n':
    #         continue
    #     break
    # if option == 'y':
    #     while True:
    #         start_t = input("Enter the preferred START-time: (yyyy-mm-dd xx:xx:xx) ")
    #         if date_to_datetime(start_t) < bag_start or date_to_datetime(start_t) > bag_end:
    #             print("Please input a valid start time.")
    #             continue
    #         else: break
    #     while True:
    #         end_t = input("Enter the preferred END-time: (yyyy-mm-dd xx:xx:xx) ")
    #         if date_to_datetime(end_t) > bag_end or date_to_datetime(end_t) < bag_start:
    #             if date_to_datetime(end_t) < date_to_datetime(start_t):
    #                 print("Please input a valid end time.")
    #                 continue
    #         else: break
    #     print("Start extracting the graph from ", start_t, " to ", end_t)
    #     ros2_extract.main(path_to_file,
    #                       date_to_datetime(start_t),
    #                       date_to_datetime(end_t))
    # else:
    #     print("Start extracting the graph from ", bag_start, " to ", bag_end)
    #     ros2_extract.main(path_to_file, bag_start, bag_end)
    # else:
    #     print("ROS version does not exist, please enter either 'ros1' or 'ros2'.")
    #     sys.exit()


if __name__ == '__main__':
    main()
