#!/usr/bin/python3
import sys
import re
"""
kansuji_small={
    "分"
    厘
    毛

    }
"""
kansuji_kurai=(
    (""        ,1),
    ("十"      ,10),\
    ("百"      ,100),\
    ("千"      ,1000),\
    )
kansuji_big=(
    (""        ,1),\
    ("万"      ,10000),\
    ("億"      ,100000000),\
    ("兆"      ,1000000000000),\
    ("京"      ,10000000000000000),\
    ("垓"      ,100000000000000000000),\
    ("𥝱"      ,1000000000000000000000000),\
    ("穣"      ,10000000000000000000000000000),\
    ("溝"      ,100000000000000000000000000000000),\
    ("澗"      ,1000000000000000000000000000000000000),\
    ("正"      ,10000000000000000000000000000000000000000),\
    ("載"      ,100000000000000000000000000000000000000000000),\
    ("極"      ,1000000000000000000000000000000000000000000000000),\
    ("恒河沙"  ,10000000000000000000000000000000000000000000000000000),\
    ("阿僧祇"  ,100000000000000000000000000000000000000000000000000000000),\
    ("那由他"  ,1000000000000000000000000000000000000000000000000000000000000),\
    ("不可思議",10000000000000000000000000000000000000000000000000000000000000000),\
    ("無量大数",100000000000000000000000000000000000000000000000000000000000000000000)\
    )
argv=sys.argv
argc=len(argv)
print("argv:{argv}\nargc:{argc}\nargv[argc-1]:{argv1}".format(argv=argv,argc=argc,argv1=argv[argc-1]))
intmp=argv[argc-1]
checked=re.search('[^\d.]',intmp)
print(checked) 
if checked != None and  checked.group(0) != '\n':
    print("数の入力には数字と小数点しか使えません。")
    sys.exit(1)
if re.search('\.',intmp) == None: 
    bigger_than_1=True
else:
    bigger_than_1=False
result_tmp=""
kurai=0
kurai_bigger=0
for cnow in reversed(intmp):
    if bigger_than_1==False and cnow != '.':
        result_tmp+=cnow
    elif bigger_than_1==False and cnow == '.':
        result_tmp+=cnow
        bigger_than_1==True
    elif bigger_than_1==True:
        if kurai_bigger<=len(kansuji_big):
            if kurai%4==0:
                if cnow == '0':
                    result_tmp+=(kansuji_big[kurai_bigger][0])
                elif cnow == '1':
                    result_tmp+=(kansuji_big[kurai_bigger][0])
                else:
                    result_tmp+=(kansuji_big[kurai_bigger][0]+cnow)
                kurai+=1
                kurai_bigger+=1
            else:
                if cnow == '0':
                    result_tmp+=''
                elif cnow == '1':
                    result_tmp+=(kansuji_kurai[kurai%4][0])
                else:
                    result_tmp+=(kansuji_kurai[kurai%4][0]+cnow)
                kurai+=1
        else:
            result_tmp+=cnow
            kurai+=1
result=result_tmp[::-1]
print(result)
