import socket

host = '127.0.0.1'
port = 7000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)

print(f'Server listening on {host}:{port}')
while True:
    conn,addr = server.accept()
    print(f'Connected by {addr}')

    data = conn.recv(1024).decode()
    num1, operator, num2 = data.split()
    num1, num2 = int(num1), int(num2)

    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        result = num1 // num2 if num2 != 0 else 'Error: Division by zero'
    elif operator == '%':
        result = num1 % num2 if num2 != 0 else 'Error: Division by zero'
    else:
        result = 'Error: Invalid operator'

    conn.send(str(result).encode())
    print(f'Calculated: {num1} {operator} {num2} = {result}')
    conn.close()