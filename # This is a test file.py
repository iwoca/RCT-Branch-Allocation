# This is a test file
list1 = []
text = '''
testuser1@example.com
testuser2@example.com
testuser3@example.com
testuser4@example.com
testuser5@example.com
testuser6@example.com
testuser7@example.com
testuser8@example.com
testuser9@example.com
testuser10@example.com
testuser11@example.com
testuser12@example.com
testuser13@example.com
testuser14@example.com
testuser15@example.com
testuser16@example.com
testuser17@example.com
testuser18@example.com
testuser19@example.com
testuser20@example.com
testuser21@example.com
testuser22@example.com
testuser23@example.com
testuser24@example.com
testuser25@example.com
testuser26@example.com
testuser27@example.com
testuser28@example.com
testuser29@example.com
testuser30@example.com
testuser31@example.com
testuser32@example.com
testuser33@example.com
testuser34@example.com
testuser35@example.com
testuser36@example.com
testuser37@example.com
testuser38@example.com
testuser39@example.com
testuser40@example.com
testuser41@example.com
testuser42@example.com
testuser43@example.com
testuser44@example.com
testuser45@example.com
testuser46@example.com
testuser47@example.com testuser48@example.com
testuser49@example.com
testuser50@example.com
'''
word = ''
for i in text:
    if i not in ['\n', '\t', '\r', ' ']:
        word += i
    else:
        if word:
            list1.append(word)
            word = ''

# Append the last word if it exists
if word:
    list1.append(word)

print(list1)
