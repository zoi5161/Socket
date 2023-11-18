# java -jar test-mail-server-1.0.jar -s 2225 -p 3335 -m ./
import socket
import os
import base64

# Prepare account email:
sender = input("Username: ")
# password = input("Password: ")
mailserver = "127.0.0.1" # input("MailServer: ")
smtp = input("SMTP: ")
pop3 = input("POP3: ")
# autoload = input("Autoload: ")

receiver = "vantai327@gmail.com"
pass_recv = "123tai"

list_TO = []
list_CC = []
list_BCC = []
list_File = []

list_sender = []
list_subject = []

subject = None
content = None

FORMAT = "utf8"
SERVER_PORT_SMTP = int(smtp)
SERVER_PORT_POP3 = int(pop3)
MAX_SIZE = 1024 * 3

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Send TO
def send_TO(attachment_path):
    # Send HELO command and print server response.
    heloCommand = 'EHLO [127.0.0.1]\r\n'
    clientSocket.send(heloCommand.encode(FORMAT))
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)

    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    send = 'MAIL FROM:<' + sender + '>\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();
    print(recv);

    if (recv[:3] != '250'):
        print('250 reply not received from server.');
        
    for i in list_TO:
        send = 'RCPT TO:<' + i + '>\r\n';
        clientSocket.send(send.encode(FORMAT));
        recv = clientSocket.recv(1024).decode();
        print(recv);
    
    send = 'DATA\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();
    print(recv);

    if (recv[:3] != '354'):
        print('354 reply not received from server');

    #goi du lieu mail: 
    for i in list_TO:
        clientSocket.send(b'To:' + i.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'From:' + sender.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject:' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type:multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type:text/plain;charset=UTF-8;format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')

    recv = clientSocket.recv(1024).decode()
    print(recv)

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()
    print(recv_quit)
    
# Send CC
def send_CC(attachment_path):
    # Send HELO command and print server response.
    heloCommand = 'EHLO [127.0.0.1]\r\n'
    clientSocket.send(heloCommand.encode(FORMAT))
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)

    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    send = 'MAIL FROM:<' + sender + '>\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();
    print(recv);

    if (recv[:3] != '250'):
        print('250 reply not received from server.');
        
    for i in list_CC:
        send = 'RCPT TO:<' + i + '>\r\n';
        clientSocket.send(send.encode(FORMAT));
        recv = clientSocket.recv(1024).decode();
        print(recv);
    
    send = 'DATA\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();
    print(recv);

    if (recv[:3] != '354'):
        print('354 reply not received from server');

    # Data mail: 
    for i in list_CC:
        clientSocket.send(b'CC:' + i.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'From:' + sender.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject:' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type:multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type:text/plain;charset=UTF-8;format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')
    recv = clientSocket.recv(1024).decode()
    print(recv)

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()
    print(recv_quit)
    
# Send BCC
def send_BCC(bcc, attachment_path):
    # Send HELO command and print server response.
    heloCommand = 'EHLO [127.0.0.1]\r\n'
    clientSocket.send(heloCommand.encode(FORMAT))
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)

    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    send = 'MAIL FROM:<' + sender + '>\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();
    print(recv);

    if (recv[:3] != '250'):
        print('250 reply not received from server.');
    send = 'RCPT TO:<' + bcc + '>\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();
    print(recv);

    send = 'DATA\r\n';
    clientSocket.send(send.encode(FORMAT));
    recv = clientSocket.recv(1024).decode();
    print(recv);

    if (recv[:3] != '354'):
        print('354 reply not received from server');

    # Data mail: 
    clientSocket.send(b'BCC:' + bcc.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'From:' + sender.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Subject:' + subject.encode(FORMAT) + b'\r\n');
    clientSocket.send(b'Content-Type:multipart/mixed; boundary="boundary"\r\n\r\n')

    # Gửi phần text của email
    clientSocket.send(b'--boundary\r\n')
    clientSocket.send(b'Content-Type:text/plain;charset=UTF-8;format=flowed\r\n\r\n')
    clientSocket.send(content.encode(FORMAT) + b'\r\n')

    # Đọc nội dung của file.txt và mã hóa base64
    if (attachment_path):
        send_File(attachment_path)

    # Kết thúc email
    clientSocket.send(b'--boundary--\r\n.\r\n')
    recv = clientSocket.recv(1024).decode()
    print(recv)

    # Send QUIT command and get server response.
    clientSocket.send(b'QUIT\r\n')
    recv_quit = clientSocket.recv(1024).decode()
    print(recv_quit)

# Send File
def send_File(attachment_path_list):
    size = 0
    # Có giới hạn dung lượng file gửi
    for attachment_path in attachment_path_list:
        if os.path.exists(attachment_path):
            size += os.path.getsize(attachment_path)
        else:
            print(f"File not found: {attachment_path}")
    size = size / 1024;
    if (size > MAX_SIZE): return ;

    # gửi file đính kèm
    for attachment_path in attachment_path_list:
        attachment_name = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as attachment_file:
            attachment_data = attachment_file.read()
        encoded_attachment = base64.b64encode(attachment_data).decode(FORMAT)  # Mã hóa base64

        last_three_char = attachment_name[-3:]
        if (last_three_char == 'txt'):
            # Gửi phần đính kèm *.txt của email
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type:application/octet-stream; name="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Disposition:attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

        elif (last_three_char == 'pdf'):
            # Gửi phần đính kèm *.pdf của email
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type:application/pdf; name="{attachment_name}"\r\n'.encode(FORMAT));
            clientSocket.send(f'Content-Disposition:attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

        elif (last_three_char == 'ocx'):
            #gửi phần đính kèm *.doc của email
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type:application/msword; name="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Disposition:attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # clientSocket.send(encoded_attachment.encode(FORMAT) + b'\r\n')

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

        elif (last_three_char == 'jpg'):
            #gửi phần đính kèm *.jpg của email
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type:image/jpeg; name="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Disposition:attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

        elif (last_three_char == 'zip'):
            #gửi phần đính kèm *.zip của email:
            clientSocket.send(b'--boundary\r\n')
            clientSocket.send(f'Content-Type:application/zip; name="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Disposition:attachment; filename="{attachment_name}"\r\n'.encode(FORMAT))
            clientSocket.send(f'Content-Transfer-Encoding: base64\r\n\r\n'.encode(FORMAT))

            # Chia nhỏ dữ liệu đính kèm thành các dòng nhỏ hơn
            chunk_size = 76  # Độ dài tối đa của mỗi dòng
            for i in range(0, len(encoded_attachment), chunk_size):
                clientSocket.send(encoded_attachment[i:i+chunk_size].encode(FORMAT) + b'\r\n')

while 1:
    print("Vui lòng chọn Menu:")
    print("1. Để gửi email")
    print("2. Để xem danh sách các email đã nhận")
    print("3. Thoát\n")
    choice = input("Bạn chọn: ")
    print()

    if choice == "1":
        print("Đây là thông tin soạn email: (nếu không điền vui lòng nhấn enter để bỏ qua)")
        answer = input()

        to = input("To: ")
        if not to:
            print("<enter>\n")
        else:
            list_TO = to.split(', ')
            print()
            
        cc = input("CC: ")
        if not cc:
            print("<enter>\n")
        else:
            list_CC = cc.split(', ')
            print()
            
        bcc = input("BCC: ")
        if not bcc:
            print("<enter>\n")
        else:
            list_BCC = bcc.split(', ')
            print()
        
        subject = input("Subject: ")
        content = input("Content: ")
        
        attachment = int(input("Có gửi kèm file (1. có, 2. không): "))
        if attachment == 1:
            num_File = int(input("Số lượng file muốn gửi: "))
            for i in range(1, num_File + 1):
                add = input("Cho biết đường dẫn file thứ " + str(i) + ": ")
                list_File.append(add)
                
        if to:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((mailserver, SERVER_PORT_SMTP))

            recv = clientSocket.recv(1024).decode()
            print(recv)
            if recv[:3] != '220':
                print('\n 220 reply not received from server.')
            send_TO(list_File)
        if cc:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            clientSocket.connect((mailserver, SERVER_PORT_SMTP))
            
            recv = clientSocket.recv(1024).decode()
            print(recv)
            if recv[:3] != '220':
                print('\n 220 reply not received from server.')
            send_CC(list_File)
        if bcc:
            for i in range(len(list_BCC)):
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                clientSocket.connect((mailserver, SERVER_PORT_SMTP))
                
                recv = clientSocket.recv(1024).decode()
                print(recv)
                if recv[:3] != '220':
                    print('\n 220 reply not received from server.')
                send_BCC(list_BCC[i], list_File)
    elif choice == "2":
        # Create socket called clientSocket and establish a TCP connection with mailserver
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        clientSocket.connect((mailserver, SERVER_PORT_POP3))

        # nhận thông báo từ mail server:
        response = clientSocket.recv(1024).decode();
        # print(response)
        # if (response[:3] != '+OK'):
        #     print('TEST MAIL SERVER NOT REQUIRED');

        # gửi lệnh USER để xác thực:
        clientSocket.send(b'USER ' + receiver.encode(FORMAT) + b'\r\n')
        response = clientSocket.recv(1024).decode()
        # print(response)
        # if (response[:3] != '+OK'):
        #     print('USER NOT REQUIRED')

        # gửi lệnh pass để xác thực:
        clientSocket.send(b'PASS ' + pass_recv.encode(FORMAT) + b'\r\n')
        response = clientSocket.recv(1024).decode()
        # print(response);
        # if (response[:3] != '+OK'):
        #     print('PASS NOT REQUIRED')

        # gửi lệnh STAT -> lấy số byte có trong mail:
        clientSocket.send('STAT\r\n'.encode(FORMAT))
        response = clientSocket.recv(1024).decode();
        # print(response);
        # if (response[:3] != '+OK'):
        #     print('STAT NOT REQUIRED')

        # gửi lệnh LIST để lấy danh sách email
        clientSocket.send('LIST\r\n'.encode(FORMAT))
        response = clientSocket.recv(1024).decode()
        # print(response)
        # if (response[:3] != '+OK'):
        #     print('LIST NOT REQUIRED')

        # gửi lệnh UIDL
        clientSocket.send('UIDL\r\n'.encode(FORMAT))
        response = clientSocket.recv(1024).decode()
        # print(response)
        # if (response[:3] != '+OK'):
        #     print('UILD NOT RESPONSE')

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
            
            from_start_idx = response.find('From:') + len('From:')
            from_end_idx = response.find('Subject:')
            list_sender.append(response[from_start_idx : (from_end_idx - len('\r\n'))])
            
            subject_start_idx = response.find('Subject:') + len('Subject:')
            subject_end_idx = response.find('Content')
            list_subject.append(response[subject_start_idx : (subject_end_idx - len('\r\n'))])
            
            
            # print('NOI DUNG MAIL: ')

            # Vì sử dụng 1 lệnh response = clientSocket.recv(1024).decode() -> không thể lấy hết được dữ liệu 1 lần trên đường truyền -> dùng vòng while để lấy đủ dữ liệu -> bỏ vào file

            # lấy subject và ng gửi
            

            # lấy nội dung email:
            # data_idx = response.find('Content-Type:text/plain;charset=UTF-8;format=flowed') + len('Content-Type:text/plain;charset=UTF-8;format=flowed\r\n\r\n')
            # if (response.find('Content-Transfer-Encoding: base64') != -1): # có file đính kèm
            #     data_idx_end = response.find('--boundary', data_idx);
            #     data_res = response[data_idx : data_idx_end]
            #     print(data_res)
            # else: # không có file đính kèm
            #     data_idx_end = response.find('--boundary--', data_idx)
            #     data_res = response[data_idx : data_idx_end]
            #     print(data_res)


            # # xác định nếu có file đính kèm và lấy thong tin file:
            # attachment_start = response.find('Content-Transfer-Encoding: base64')
            # if attachment_start != -1: # có file
            #     idx_start = response.find('Content-Transfer-Encoding: base64') + len('Content-Transfer-Encoding: base64\r\n\r\n'); # cho \r\n\r\n
            #     idx_end = response.find('--boundary--')
            #     res = response[idx_start : idx_end]

            #     #tên file đính kèm:
            #     attachment_file = ''
            #     if (response.find('Content-Type:application/octet-stream') != -1):
            #         attachment_file = 'download.txt'
            #     elif (response.find('Content-Type:application/pdf') != -1):
            #         attachment_file = 'download.pdf'
            #     elif(response.find('Content-Type:application/msword') != -1):
            #         attachment_file = 'download.docx'
            #     elif (response.find('Content-Type:image/jpeg') != -1):
            #         attachment_file = 'download.jpg'
            #     elif (response.find('Content-Type:application/zip') != -1):
            #         attachment_file = 'download.zip'

            #     # kiểm tra -> tạo file -> ghi dữ liệu vào:
            #     if not os.path.exists(attachment_file):
            #         with open(attachment_file, "xb") as attachment_file: # xb : kiểm tra nếu chưa có file đó thì tạo ra file mới tự động, còn có rồi thì kh thực hiện
            #             attachment_file.write(base64.b64decode(res))
            #     else:
            #         print('file alredy exist');

        # # Gửi lệnh DELE để đánh dấu email đã tải
        # clientSocket.send(b'DELE 1\r\n')

        # Send QUIT command and get server response.
        clientSocket.send(b'QUIT\r\n')
        recv_quit = clientSocket.recv(1024).decode()
        # print(recv_quit)
        
        print(list_sender)
        print(list_subject)
    elif choice == "3":
        break
    
# Đóng socket
clientSocket.close()




