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
kansuji_figure = (
    ("〇", 0),
    ("一", 1),
    ("二", 2),
    ("三", 3),
    ("四", 4),
    ("五", 5),
    ("六", 6),
    ("七", 7),
    ("八", 8),
    ("九", 9),
)
kansuji_kurai = (
    ("", 1),
    ("十", 10),
    ("百", 100),
    ("千", 1000),
)
"""
じゅう
ひゃく
せん
まん
おく
ちょう
けい
がい
じょ
じょう
こう
かん
せい
さい
ごく
こうがしゃ
あそうぎ
なゆた
ふかしぎ
むりょうたいすう
"""
kansuji_big = [
    ("", 1, ""),
    ("万", 10000, "まん,"),
    ("億", 100000000, "おく,"),
    ("兆", 1000000000000, "ちょう,"),
    ("京", 10000000000000000, "けい,"),
    ("垓", 100000000000000000000, "がい,"),
    ("𥝱", 1000000000000000000000000, "じょ,"),
    ("穣", 10000000000000000000000000000, "じょう,"),
    ("溝", 100000000000000000000000000000000, "こう,"),
    ("澗", 1000000000000000000000000000000000000, "かん,"),
    ("正", 10000000000000000000000000000000000000000, "せい,"),
    ("載", 100000000000000000000000000000000000000000000, "さい,"),
    ("極", 1000000000000000000000000000000000000000000000000, "ごく,"),
    ("恒河沙", 10000000000000000000000000000000000000000000000000000, "こうがしゃ,"),
    ("阿僧祇", 100000000000000000000000000000000000000000000000000000000, "あそうぎ,"),
    ("那由他", 1000000000000000000000000000000000000000000000000000000000000, "なゆた,"),
    ("不可思議", 10000000000000000000000000000000000000000000000000000000000000000, "ふかしぎ,"),
    ("無量大数", 100000000000000000000000000000000000000000000000000000000000000000000, "むりょうたいすう,"),
]
argv = sys.argv
argc = len(argv)
# print("argv:{argv}\nargc:{argc}\nargv[argc-1]:{argv1}".format(argv=argv,argc=argc,argv1=argv[argc-1]))
# ----- options -----
options = {"mixed": False, "debug": False, "all": False, "for_speech": False}
if "--stdin" in argv:
    intmp = sys.stdin.read()
else:
    intmp = argv[argc - 1]
if "--mixed" in argv or "-m" in argv:
    options["mixed"] = True
elif "--all-kansuji" in argv or "-a" in argv:
    options["all"] = True
if "--for-speech" in argv or "-s" in argv:
    options["for_speech"] = True
    for i in range(len(kansuji_big)):
        kansuji_big[i] = tuple(reversed(kansuji_big[i]))
if "--debug" in argv:
    print(
        "argv:{argv}\nargc:{argc}\nargv[argc-1]:{argv1}".format(argv=argv, argc=argc, argv1=argv[argc - 1]),
        file=sys.stderr,
    )
    options["debug"] = True
if "-h" in argv:
    print("conv-suji [options...] [number]")
    print("-m, --mixed       :漢数字と算用数字の折衷表記 例 1234万5678")
    print("-a, --all-kansuji :完全な漢数字表記 例 千百三十四万五千六百七十八")
    print("-s, --for-speech  :単位をひらがな表記 (a/mどちらかと一緒に指定してください)")
    print("-e, --eval        :numberをeval()で評価する")
    print("--stdin           :パイプで送られてきた入力を処理する")
    print("--debug           :デバッグ表示をオンにする")
    print("-h, --help        :このヘルプを表示して終了する")
    sys.exit(0)

if "-e"in argv or "--eval" in argv:
    import math
    intmp=f"{eval(intmp)}"

checked = re.search('[^0-9.,]', intmp)

if options["debug"] == True:
    print("intmp:{intmp}".format(intmp=intmp), file=sys.stderr)
    print(checked, file=sys.stderr)

if checked != None and checked.group(0) != '\n':
    print("数の入力には数字と小数点しか使えません。", file=sys.stderr)
    sys.exit(1)
if re.search(r'\.', intmp) == None:
    bigger_than_1 = True
else:
    bigger_than_1 = False
result_tmp = ""
kurai = 0
kurai_bigger = 0
num_zeros = 0
for cnow in reversed(intmp):
    # print(num_zeros)
    if cnow == "\n" or cnow == ",":
        continue
    if bigger_than_1 == False and cnow != '.':
        result_tmp += cnow
    elif bigger_than_1 == False and cnow == '.':
        result_tmp += cnow
        bigger_than_1 == True
    elif bigger_than_1 == True:
        if kurai_bigger < len(kansuji_big):
            if kurai % 4 == 0:
                if num_zeros == 4:
                    result_tmp = result_tmp.replace((kansuji_big[kurai_bigger - 1][0])[::-1], '')
                    if options["mixed"] == True:
                        result_tmp = result_tmp[: len(result_tmp) - 4]
                num_zeros = 0
                if cnow == '0':
                    if options["all"] == True:
                        result_tmp += (kansuji_big[kurai_bigger][0])[::-1]
                    else:
                        result_tmp += (kansuji_big[kurai_bigger][0])[::-1] + cnow
                    num_zeros += 1
                elif cnow == '1':
                    if options["all"] == True:
                        cnow = kansuji_figure[int(cnow)][0]
                    result_tmp += (kansuji_big[kurai_bigger][0])[::-1] + cnow
                else:
                    if options["all"] == True:
                        cnow = kansuji_figure[int(cnow)][0]
                    result_tmp += (kansuji_big[kurai_bigger][0])[::-1] + cnow
                kurai += 1
                kurai_bigger += 1
            else:
                if options["mixed"] == False or options["all"] == True:
                    if cnow == '0':
                        num_zeros += 1
                        # (1+1==3)==True
                    elif cnow == '1':
                        result_tmp += kansuji_kurai[kurai % 4][0]
                    else:
                        cnow = kansuji_figure[int(cnow)][0]
                        result_tmp += kansuji_kurai[kurai % 4][0] + cnow
                elif cnow == '0':
                    result_tmp += cnow
                    num_zeros += 1
                else:
                    result_tmp += cnow
                kurai += 1
        else:
            if kurai%4==0:
                result_tmp+=","
            result_tmp +=cnow
            kurai += 1
result = result_tmp[::-1]
print(result)
