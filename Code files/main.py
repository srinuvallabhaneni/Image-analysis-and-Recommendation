from data_loading import DataLoading

from phase3_task1 import Phase3_task1
from phase3_task2 import Phase3_task2
from phase3_task3 import Phase3_task3
from phase3_task4 import Phase3_task4
from phase3_task_5ab import Phase3_Task_5ab
from phase3_task6a import Phase3_Task_6a
from phase3_task6b import Phase3_Task_6b

def print_menu():
    print('1. Task 1')
    print('2a. Task 2a')
    print('2b. Task 2b')
    print('3. Task 3')
    print('4. Task 4')
    print('5a. Task 5a')
    print('5b. Task 5b  RUN 5a before this to build index structure')
    print('6a. Task 6a With k')
    print('6aa Task 6aa without k')
    print('6b. Task 6b')
    print('8. Load data')
    print('0. Quit')


def main():
    while True:
        print_menu()
        option = input("Enter option: ")
        if option == '1':
            print('TASK 1')
            print('e.g: 10')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Phase3_task1()
            data = tasks.task1(int(ips[0]))
        elif option == '2a':
            print('TASK 2a - Spectral clustering')
            print('e.g: 5')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Phase3_task2()
            tasks.task_2a(data, int(ips[0]))
        elif option == '2b':
            print('TASK 2b - Normalised cut partitioning')
            print('e.g: 5')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Phase3_task2()
            tasks.task_2b(data, int(ips[0]))
        elif option == '3':
            print('TASK 3')
            print('Sample: 10')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Phase3_task3()
            tasks.task_3(data, int(ips[0]))
        elif option == '4':
            print('TASK 4')
            print('Sample: 10 2976144 3172496917 2614355710')
            inp = input("Input: ")
            ips = inp.split(' ')
            tasks = Phase3_task4()
            tasks.task_4(data, int(ips[0]), [ips[1], ips[2], ips[3]])
        elif option == '5a':
            print('TASK 5a')
            print("Sample: 5 7")
            inp = input("Input: <L> <K> ")
            ips = inp.split(' ')
            tasks_ = Phase3_Task_5ab()
            tasks_.task5a(int(ips[0]), int(ips[1]))
        elif option == '5b':
            print('TASK 5b')
            print("Sample: 4268828872 5")
            inp = input("Input: <Image Id> <t> ")
            ips = inp.split(' ')
            tasks_.task5b(int(ips[0]), int(ips[1]))
        elif option == '6a':
            print('6a Task 6a with k')
            print('Sample: task6.txt 4')
            inp = input('Input: <filename> <k>')
            ips = inp.split(' ')
            tasks = Phase3_Task_6a()
            tasks.task6a(ips[0],int(ips[1]))
        elif option == '6aa':
            print('6aa Task 6aa without k')
            print('Sample: task6.txt')
            inp = input('Input: <filename>')
            tasks = Phase3_Task_6a()
            tasks.task6a(inp)
        elif option == '6b':
            print('6b Task 6b')
            print('Sample: task6.txt')
            inp = input('Input: ')
            ips = inp.split(' ')
            tasks = Phase3_Task_6b()
            tasks.task6b(data, ips[0])
        elif option == '8':
            print('Load Data')
            path = input("Path: ")
            dt = DataLoading(path)
            dt.drop_database()
            dt.process_location_data()
            dt.process_users_textual_data()
            dt.process_images_textual_data()
            dt.process_locations_textual_data()
            dt.process_visual_data()
            dt.process_common_terms_data()
            # dt.generate_img_text_graph()
            dt.generate_img_img_vis_graph()
        elif option == '0':
            break
        else:
            print('Incorrect option.')
        input('Press any key to continue...')

if __name__ == "__main__":
    main()
