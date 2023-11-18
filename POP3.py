import socket
import os
import base64


FORMAT = "utf8";
SERVER_PORT_POP3 = 3335;

MAX_SIZE = 1024 * 3

mailserver = '127.0.0.1';
receiver = "vantai327@gmail.com"
pass_recv = "123tai"

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
clientSocket.connect((mailserver, SERVER_PORT_POP3))

# nhận thông báo từ mail server:
response = clientSocket.recv(1024).decode();
print(response)
if (response[:3] != '+OK'):
    print('TEST MAIL SERVER NOT REQUIRED');

# gửi lệnh USER để xác thực:
clientSocket.send(b'USER ' + receiver.encode(FORMAT) + b'\r\n')
response = clientSocket.recv(1024).decode()
print(response)
if (response[:3] != '+OK'):
    print('USER NOT REQUIRED')

# gửi lệnh pass để xác thực:
clientSocket.send(b'PASS ' + pass_recv.encode(FORMAT) + b'\r\n')
response = clientSocket.recv(1024).decode()
print(response);
if (response[:3] != '+OK'):
    print('PASS NOT REQUIRED')

# gửi lệnh STAT -> lấy số byte có trong mail:
clientSocket.send('STAT\r\n'.encode(FORMAT))
response = clientSocket.recv(1024).decode();
print(response);
if (response[:3] != '+OK'):
    print('STAT NOT REQUIRED')

# gửi lệnh LIST để lấy danh sách email
clientSocket.send('LIST\r\n'.encode(FORMAT))
response = clientSocket.recv(1024).decode()
print(response)
if (response[:3] != '+OK'):
    print('LIST NOT REQUIRED')

# gửi lệnh UIDL
clientSocket.send('UIDL\r\n'.encode(FORMAT))
response = clientSocket.recv(1024).decode()
print(response)
if (response[:3] != '+OK'):
    print('UILD NOT RESPONSE')

num_Email = response.count('.msg')
# gửi lệnh RETR để lấy nội dung email theo số thứ tự
for i in range(1, num_Email + 1):
    clientSocket.send(('RETR ' + str(i) + '\r\n').encode(FORMAT))
    response = b''  # Sử dụng bytes để nắm bắt dữ liệu nhận được

    while True:
        part = clientSocket.recv(1024)
        response += part
        if b'\r\n.\r\n' in part:
            break
        
    response = response.decode()
    print('NOI DUNG MAIL: ')

    # Vì sử dụng 1 lệnh response = clientSocket.recv(1024).decode() -> không thể lấy hết được dữ liệu 1 lần trên đường truyền -> dùng vòng while để lấy đủ dữ liệu -> bỏ vào file

    # lấy subject và ng gửi
    

    # lấy nội dung email:
    data_idx = response.find('Content-Type:text/plain;charset=UTF-8;format=flowed') + len('Content-Type:text/plain;charset=UTF-8;format=flowed\r\n\r\n')
    if (response.find('Content-Transfer-Encoding: base64') != -1): # có file đính kèm
        data_idx_end = response.find('--boundary', data_idx);
        data_res = response[data_idx : data_idx_end]
        print(data_res)
    else: # không có file đính kèm
        data_idx_end = response.find('--boundary--', data_idx)
        data_res = response[data_idx : data_idx_end]
        print(data_res)


    # xác định nếu có file đính kèm và lấy thong tin file:
    attachment_start = response.find('Content-Transfer-Encoding: base64')
    if attachment_start != -1: # có file
        idx_start = response.find('Content-Transfer-Encoding: base64') + len('Content-Transfer-Encoding: base64\r\n\r\n'); # cho \r\n\r\n
        idx_end = response.find('--boundary--')
        res = response[idx_start : idx_end]

        #tên file đính kèm:
        attachment_file = ''
        if (response.find('Content-Type:application/octet-stream') != -1):
            attachment_file = 'download.txt'
        elif (response.find('Content-Type:application/pdf') != -1):
            attachment_file = 'download.pdf'
        elif(response.find('Content-Type:application/msword') != -1):
            attachment_file = 'download.docx'
        elif (response.find('Content-Type:image/jpeg') != -1):
            attachment_file = 'download.jpg'
        elif (response.find('Content-Type:application/zip') != -1):
            attachment_file = 'download.zip'

        # kiểm tra -> tạo file -> ghi dữ liệu vào:
        if not os.path.exists(attachment_file):
            with open(attachment_file, "xb") as attachment_file: # xb : kiểm tra nếu chưa có file đó thì tạo ra file mới tự động, còn có rồi thì kh thực hiện
                attachment_file.write(base64.b64decode(res))
        else:
            print('file alredy exist');

# # Gửi lệnh DELE để đánh dấu email đã tải
# clientSocket.send(b'DELE 1\r\n')

# Send QUIT command and get server response.
clientSocket.send(b'QUIT\r\n')
recv_quit = clientSocket.recv(1024).decode()
print(recv_quit)