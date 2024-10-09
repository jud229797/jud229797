from collections import defaultdict
import paramiko
import time

# 服务器信息
host = '111.230.53.161'
port = 22
username = 'zhu'
password = 'zxd12345'

# 本地文件路径和远程文件路径
local_path_circle = '/home/aidlux/2024.4.27first.connect/output_circle.jpg'
remote_path_circle = '/home/zhu/picture_circle.jpg'
local_path_ill = '/home/aidlux/2024.4.27first.connect/output_ill.jpg'
remote_path_ill = '/home/zhu/picture_ill.jpg'
local_path_bigdata = '/home/aidlux/2024.4.27first.connect/bigdata.txt'
remote_path_bigdata = '/home/zhu/bigdata_remote.txt'


# def upload_file(host, port, username, password, local_path_circle, remote_path_circle,local_path_ill, remote_path_ill):
#     # 创建两个SSH对象
#     ssh_circle = paramiko.SSHClient()
#     ssh_circle.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh_ill = paramiko.SSHClient()
#     ssh_ill.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
#     try:
#         ssh_circle.connect(host, port, username, password)
#         ssh_ill.connect(host, port, username, password)
#         while True:
#             # 使用SCP上传文件
#             scp_circle = paramiko.SFTPClient.from_transport(ssh_circle.get_transport())
#             scp_circle.put(local_path_circle, remote_path_circle)
#             print(f"Uploaded {local_path_circle} to {remote_path_circle}")
#             scp_ill = paramiko.SFTPClient.from_transport(ssh_ill.get_transport())
#             scp_ill.put(local_path_ill, remote_path_ill)
#             print(f"Uploaded {local_path_ill} to {remote_path_ill}")
#             scp_circle.close()
#             scp_ill.close()
#             time.sleep(10)  # 等待10秒再次上传
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         ssh_circle.close()
#         ssh_ill.close()


# def upload_file(host, port, username, password, local_path_circle, remote_path_circle,local_path_ill, remote_path_ill, local_path_bigdata, remote_path_bigdata):
#     # 创建两个SSH对象
#     ssh_circle = paramiko.SSHClient()
#     ssh_circle.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh_ill = paramiko.SSHClient()
#     ssh_ill.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh_bigdata = paramiko.SSHClient()
#     ssh_bigdata.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     try:
#         ssh_circle.connect(host, port, username, password)
#         ssh_ill.connect(host, port, username, password)
#         ssh_bigdata.connect(host, port, username, password)
#         while True:
#             # 使用SCP上传文件
#             scp_circle = paramiko.SFTPClient.from_transport(ssh_circle.get_transport())
#             scp_circle.put(local_path_circle, remote_path_circle)
#             print(f"Uploaded {local_path_circle} to {remote_path_circle}")
#             scp_ill = paramiko.SFTPClient.from_transport(ssh_ill.get_transport())
#             scp_ill.put(local_path_ill, remote_path_ill)
#             print(f"Uploaded {local_path_ill} to {remote_path_ill}")

#             # 调用send_bigdata函数获取要上传的数据
#             # combined_info = send_bigdata()
#             combined_info = "success!!!"
#             with open(local_path_bigdata, 'w') as file:
#                 file.write(combined_info)
#             scp_bigdata = paramiko.SFTPClient.from_transport(ssh_bigdata.get_transport())
#             scp_bigdata.put(local_path_bigdata, remote_path_bigdata)
#             print(f"Uploaded {local_path_bigdata} to {remote_path_bigdata}")

#             scp_circle.close()
#             scp_ill.close()
#             scp_bigdata.close()
#             time.sleep(10)  # 等待10秒再次上传
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         ssh_circle.close()
#         ssh_ill.close()
#         scp_bigdata.close()



def upload_file(host, port, username, password, local_path_circle, remote_path_circle, 
                local_path_ill, remote_path_ill, local_path_bigdata, remote_path_bigdata):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, port, username, password)
        
        with paramiko.SFTPClient.from_transport(ssh.get_transport()) as sftp:
            while True:
                # 上传图片文件
                sftp.put(local_path_circle, remote_path_circle)
                print(f"Uploaded {local_path_circle} to {remote_path_circle}")
                sftp.put(local_path_ill, remote_path_ill)
                print(f"Uploaded {local_path_ill} to {remote_path_ill}")

                # 获取要上传的大数据显示数据
                combined_info = "6666666666"  # 确保send_bigdata函数已定义并返回数据
                with open(local_path_bigdata, 'w') as file:
                    file.write(combined_info)
                
                # 上传大数据文本文件
                sftp.put(local_path_bigdata, remote_path_bigdata)
                print(f"Uploaded {local_path_bigdata} to {remote_path_bigdata}")
                
                time.sleep(10)  # 等待10秒再次上传
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ssh.close()





if __name__ == "__main__":
    upload_file(host, port, username, password, local_path_circle, remote_path_circle,local_path_ill, remote_path_ill, local_path_bigdata, remote_path_bigdata)