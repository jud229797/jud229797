import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

# 设置SMTP服务器信息
smtp_server = 'smtp.qq.com'
smtp_port = 587

# 发件人邮箱信息
sender_adress = '3272276406@qq.com'
authorization_code = 'vdxadcffmnrbchjb'  # 您的SMTP授权码
location = "A 区"
disease = "白粉病"

def send_email(recipient_email,disease,location):
    if disease=="angular_leafspot":
        disease="角斑病"
    elif disease=="leaf_spot":
        disease="叶斑病"
    elif disease=="powdery_mildew_fruit":
        disease="白粉病果"
    elif disease=="powdery_mildew_leaf":
        disease="白粉病叶"
    text_body = f"""
        <body>
            <h4>紧急通知:出现病虫害</h4>
            <br>
            <br>

            <div class="contact-info">
                <h1>尊敬的用户：</h1>
                
                <h4>系统发现您的草莓园{location}可能遭受了的{disease}侵袭。</h4>
                <h4>请您尽快确认并采取行动，以保护您的草莓作物。我们期待您的草莓园能够迅速恢复健康。</h4>
            </div>
            <br>
            <br>
        </body>
        """
    try:
        with smtplib.SMTP('smtp.qq.com', 587) as server:
            server.starttls()
            server.login('3272276406@qq.com', 'vdxadcffmnrbchjb')
            # 创建邮件内容
            msg = MIMEMultipart()
            head = Header("草莓魔法师", 'utf-8')
            head.append('3272276406@qq.com', 'ascii')
            msg['From'] = head
            msg['Subject'] = "草莓魔法师通知助手"
            msg["To"] = recipient_email
            msg.attach(MIMEText(text_body, "html"))

            server.sendmail('3272276406@qq.com', recipient_email, msg.as_string())
            print(f"成功发送邮件至 {recipient_email}")
    except Exception as e:
        print(f"发送邮件时发生错误: {e}")




if __name__ == "__main__":
    recipient_email = "2706736703@qq.com"
    # disease = "bad"
    # location = "A区f"
    send_email(recipient_email,disease,location)
