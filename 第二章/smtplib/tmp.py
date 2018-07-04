HOST = "smtp.g-i.asia"
SUBJECT = "Test email from Python"
TO = "1028190073@qq.com"
FROM = "heyue@g-i.asia"
Text = "Python rules them all!"
fag = "\r\n"
str1 = ("From:"+FROM, "To:"+TO, "Subject:"+SUBJECT, "Text:"+Text)
BODY = fag.join(str1)
print(BODY)