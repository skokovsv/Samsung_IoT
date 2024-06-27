
# import socket
# def get_ip():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:
#         # doesn't even have to be reachable
#         s.connect(('10.255.255.255', 1))
#         IP = s.getsockname()[0]
#     except:
#         IP = '127.0.0.1'
#     finally:
#         s.close()
#     return IP
#
# print(get_ip())



# номер 6
# year = int(input('Введите год: '))
#
# if year % 4 == 0 and year % 100 != 0:
#     print('Високосный')
# elif year % 400 == 0:
#     print('Високосный')
# else:
#     print('Невисокосный')


# номер 22
# n = int(input('Введите размер массива: '))
# mas = []
# for i in range(n):
#     mas.append(int(input('Элемент массива: ')))
# print(mas)
#
# min_el = mas[0]
# for i in range(1,n):
#     if mas[i] < min_el:
#         min_el = mas[i]
#
# print(f'Минимальный элемент: {min_el}')


#номер 44

class Stack:
    def __init__(self):
        self.stack=[]

    def push(self,item):
        self.stack.append(item)

    def pop(self):
        if len(self.stack) == 0:
            print("Stack is empty")
            return -1
        else:
            return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def isEmpty(self):
        if len(self.stack)==0:
            return True
        else:
            return False


