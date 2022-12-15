# TODO 1 : 시 / 군 / 구 선택 가능하도록 변경
    # ㄴ 시 선택 이후 title=city + "/"
# TODO 2 : 직접 입력 / 선택 function화

# SYSTEMS
import cmd
import time, os, sys, re
import ctypes

# STYLE
from pyfiglet import Figlet

# ARROW OPTION (curses)
import pick

# DATA
import pandas as pd
from tqdm import tqdm

# GRAPH
import matplotlib.pyplot as plt
import matplotlib


def cursorPos():
    OldStdinMode = ctypes.wintypes.DWORD()
    OldStdoutMode = ctypes.wintypes.DWORD()
    kernel32 = ctypes.windll.kernel32
    kernel32.GetConsoleMode(kernel32.GetStdHandle(-10), ctypes.byref(OldStdinMode))
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
    kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), ctypes.byref(OldStdoutMode))
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    try:
        _ = ""
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()
        while not (_ := _ + sys.stdin.read(1)).endswith('R'):
            True
        res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)
    finally:
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), OldStdinMode)
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), OldStdoutMode)
    if(res):
        return (res.group("x"), res.group("y"))
    return (-1, -1)

def moveCursor(x, y):
    print("\033[%d;%dH" % (y, x))

def arrowOption(arr, title, multi=False):
    _arr = [' '.join(list(v)) for v in arr]
    _title = " ".join(list(title)).strip()
    option, index = pick.pick(_arr, _title, indicator='>', default_index=0, multiselect=multi)
    return option, index

# 한글 사용 가능하도독 폰트 설정
matplotlib.rcParams['font.family'] = 'Malgun Gothic'

# DO NOT TOUCH
global df
data_path = 'C:/Users/gram/Desktop/Temp/Python project/data/'
data_list = os.listdir(data_path)[1:]
city_list = []
industry_list = []

# 콘솔 편집
os.system("mode con cols=150 lines=40")


def load():

    # PRINT FIGLET
    f = Figlet(font='slant')
    print (f.renderText('Python Project'))

    time.sleep(1)

    global data_path
    global df
    global city_list
    global industry_list
    data_path = 'C:/Users/gram/Desktop/Temp/Python project/data/'
    # 불러올 파일 선택
    option, idx = arrowOption(data_list, "파일 선택")
    data_path += data_list[idx]
    city_list = []
    industry_list = []

    # Using tqdm module for pandas, Load file
    print("Loading File from " + data_path)
    tqdm.pandas()
    df = pd.concat([chunk for chunk in tqdm(pd.read_csv(data_path, chunksize=10000), unit=" 항목", desc="파일을 불러오는 중")])
    row, column = df.shape
    print("\n\n" + str(row) + "행 " + str(column) + "열 의 데이터를 불러왔습니다.")
    df.head()

    time.sleep(0.5)
    os.system("cls")

    print("\n\n시군구명 업데이트 중..\n")
    tem = list(set(df['시군구명'].tolist()))
    index = 0
    for city in tqdm(tem, unit="개"):
        if not city_list or city > city_list[-1]:
            city_list.append(city)
        else:
            while city > city_list[index] and len(city_list):
                index += 1
            city_list.insert(index, city)
    print("\n")
    for city in city_list:
        print("-", city)

    time.sleep(0.5)

    print("\n\n업종 종류 업데이트 중..\n")
    tem = list(set(df['상권업종대분류명'].tolist()))
    index = 0
    for industry in tqdm(tem, unit="개"):
        if not industry_list or industry > industry_list[-1]:
            industry_list.append(industry)
        else:
            while industry > industry_list[index] and len(industry_list):
                index += 1
            industry_list.insert(index, industry)
    print("\n")
    for industry in industry_list:
        print("-", industry)

    time.sleep(0.5)

    os.system("cls")

    print("지역 상권 분석 프로그램 <%s>\n\n" % (data_list[idx].split("_")[2]))

    Main()

# # # # # SCREEN # # # # #
# 메인 스크린
def Main():
    opt, idx = arrowOption(["업종별 지역 순위\n", "지역별 업종 순위\n", "나가기", "기록보기", "파일 변경"], "< 옵션 선택 >")
    option(idx)


# 이전 기록
def prevResult():
    print("[Enter] 키를 눌러 옵션으로 이동", end="")
    re = input()
    if re != 'q':
        x, y = cursorPos()
        moveCursor(0, int(y)-2)
        print("\r", end="")
        print(" "*30, "\r", end="")
        Main()
    print('프로그램을 종료합니다.')
    exit()


def option(num):
    if num==0:
        print_area_ranking_by_Industry()
    if num==1:
        print_Industry_ranking()
    elif num==2:
        print('프로그램을 종료합니다.')
        exit()
    elif num==3:
        prevResult()
    elif num==4:
        print("파일 변경 페이지로 이동합니다.")
        time.sleep(1)
        os.system("cls")
        load()
    else:
        print("\n잘못된 입력입니다.")
        time.sleep(2)
        Main()


def showCircleGraph(columns, column1, column2, re_row1, re_row2, title, options):
    list = []
    colList = df[columns].tolist()
    if options:
        for idx, data in tqdm(enumerate(colList), unit="개", desc="전체 "+str(len(colList))+"개 중"):
            list.append(idx)
        column1 = "전체"
    else:
        for idx, data in tqdm(enumerate(colList), unit="개",  desc="전체 "+str(len(colList))+"개 중"):
            if data == column1:
                list.append(idx)
    temp = df.loc[list]
    obj = {}
    for category in temp[column2]:
        if category in obj:
            obj[category] += 1
        else:
            obj[category] = 1
    sortedObj = sorted(obj.items(), key=lambda x: x[1], reverse=True)
    print(column1 + " 중 " + column2)
    print("---------------\n\t" + re_row1 + "\t\t" + re_row2)
    for cnt, category in enumerate(sortedObj):
        if cnt > 4:
            break
        print(str(cnt+1) + "위: \t" + category[0], end="")
        if len(category[0]) <= 4:
            print("\t", end="")
        print("\t" + str(category[1]))
    print("\n---------------\n")

    ratio = []
    labels = []
    counter = 0
    for key, value in sortedObj:
        ratio.append(value)
        labels.append(key)
        counter += 1
        if counter == 5:
            break

    plt.pie(ratio, labels=labels, autopct='%.1f%%')
    plt.title(title)
    plt.show()

# # # # # FEATUER # # # # #

# 지역별 업종 순위 입력
def print_Industry_ranking():
    option, index = arrowOption(["직접입력", "선택", "뒤로가기"], "지역별 업종 순위")
    city = ""
    if index == 0:
        city = input("확인하고자 하는 지역을 입력하세요: ")
    elif index == 1:
        city_option = sorted(city_list[0:])
        city_option.insert(0, "뒤로가기")
        city_option.insert(1, "전체")
        cityName, index = arrowOption(city_option, "지역 선택")
        city = "".join(cityName.split(" "))
    elif index == 2:
        Main()
    
    if city in city_list:
        Industry_ranking(city)
    elif city == "0" or city == "뒤로가기":
        Main()
    elif city == "전체":
        Industry_ranking(None)
    else:
        print("지역 \"" + city + "\" (이)가 존재하지 않습니다. 다시 입력하세요.")
        print_Industry_ranking()

# 업종별 지역 순위 입력
def print_area_ranking_by_Industry():
    option, index = arrowOption(["직접입력", "선택", "뒤로가기"], "업종별 지역 순위")
    industry = ""
    if index == 0:
        industry = input("확인하고자 하는 업종을 입력하세요: ")
    elif index == 1:
        industry_option = sorted(industry_list[1:])
        industry_option.insert(0, "뒤로가기")
        industry_option.insert(1, "전체")
        industryName, index = arrowOption(industry_option, "지역 선택")
        industry = "".join(industryName.split(" "))
    elif index == 2:
        Main()

    if industry in industry_list:
        area_ranking_by_Industry(industry)
    elif industry=="0" or industry=="뒤로가기":
        Main()
    elif industry=="전체":
        area_ranking_by_Industry(None)
    else:
        print("업종 \"" + industry + "\" (이)가 존재하지 않습니다. 다시 입력하세요.")
        print_Industry_ranking()


# # # # # ALGORITHM # # # # #

# 지역별 업종 순위 데이터
def Industry_ranking(city):
    if city == None:
        showCircleGraph("시군구명", city, "상권업종대분류명", "업종", "업종수", city, True)
    else:
        showCircleGraph("시군구명", city, "상권업종대분류명", "업종", "업종수", city, False)
    print_Industry_ranking()


# 업종별 지역 순위 데이터
def area_ranking_by_Industry(industry):
    if industry == None:
        showCircleGraph("상권업종대분류명", industry, "시군구명", "지역", ("업종 수"), "전체", True)
    else:
        showCircleGraph("상권업종대분류명", industry, "시군구명", "지역", ("업종 수"), industry, False)
    print_area_ranking_by_Industry()


# load
load()