title = input('파일명을 입력하세요')
while True :
    txt = input('작성하실 텍스트를 입력하세요')
    if txt == "!q" :
        break
    with open(title+'.txt', 'at') as f :
        f.write(txt+'\n')
