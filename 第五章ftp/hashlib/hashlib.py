import hashlib

def getHash(f):
    line = f.readline()
    hash = hashlib.md5()
    while (line):
        hash.update(line)
        line = f.readline()
    return hash.hexdigest()

def IsHashEqual(f1, f2):
    str1 = getHash(f1)
    str2 = getHash(f2)
    return str1 == str2

if __name__ == '__main__':
    f1 = open("../ftplib/gi-logo.jpg", "rb")
    f2 = open("../ftplib/gi-logo.jpg", "rb")
    print(IsHashEqual(f1, f2))
