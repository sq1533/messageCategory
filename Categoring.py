import os
import json
import pandas

#데이터 불러오기
simplePayMessagePath = os.path.join(os.path.dirname(__file__),"DB","1.json")
pgMessagesPath = os.path.join(os.path.dirname(__file__),"DB","2.json")
musinsaMessagesPath = os.path.join(os.path.dirname(__file__),"DB","3.json")
zeroOneZeroPayMessagesPath = os.path.join(os.path.dirname(__file__),"DB","4.json")
myaccountMessagesPath = os.path.join(os.path.dirname(__file__),"DB","5.json")
zeroOneZeroCheckMessagesPath = os.path.join(os.path.dirname(__file__),"DB","6.json")
with open(simplePayMessagePath, 'r', encoding='utf-8') as f:
    simplePay = json.load(f)
with open(pgMessagesPath, 'r', encoding='utf-8') as f:
    PG = json.load(f)
with open(musinsaMessagesPath, 'r', encoding='utf-8') as f:
    musinsa = json.load(f)
with open(zeroOneZeroPayMessagesPath, 'r', encoding='utf-8') as f:
    zeroOneZeroPay = json.load(f)
with open(myaccountMessagesPath, 'r', encoding='utf-8') as f:
    myaccount = json.load(f)
with open(zeroOneZeroCheckMessagesPath, 'r', encoding='utf-8') as f:
    zeroOneZeroCheck = json.load(f)

#데이터 분류
ignoreMessage = ["검수 시작","검수 완료"]
D = []
T = []
messages = []

#간편결제 처리
for i in range(len(simplePay["messages"])):
    message = simplePay["messages"][i]["text"]
    if any(j in message for j in ignoreMessage):
        pass
    elif message == "":
        pass
    else:
        date = simplePay["messages"][i]["date"].split("T")
        Day = date[0]
        time = date[1]
        D.append(Day)
        T.append(time)
        messages.append(message)
#PG 처리
for i in range(len(PG["messages"])):
    message = PG["messages"][i]["text"]
    if message == "":
        pass
    else:
        date = PG["messages"][i]["date"].split("T")
        Day = date[0]
        time = date[1]
        D.append(Day)
        T.append(time)
        messages.append(message)
#무신사 처리
for i in range(len(musinsa["messages"])):
    message = musinsa["messages"][i]["text"]
    if message == "":
        pass
    else:
        date = musinsa["messages"][i]["date"].split("T")
        Day = date[0]
        time = date[1]
        D.append(Day)
        T.append(time)
        messages.append(message)
#010PAY 처리
for i in range(len(zeroOneZeroPay["messages"])):
    message = zeroOneZeroPay["messages"][i]["text"]
    if message == "":
        pass
    else:
        date = zeroOneZeroPay["messages"][i]["date"].split("T")
        Day = date[0]
        time = date[1]
        D.append(Day)
        T.append(time)
        messages.append(message)
#내통장결제 처리
for i in range(len(myaccount["messages"])):
    message = myaccount["messages"][i]["text"]
    if message == "":
        pass
    else:
        date = myaccount["messages"][i]["date"].split("T")
        Day = date[0]
        time = date[1]
        D.append(Day)
        T.append(time)
        messages.append(message)
#010Checkcard 처리
for i in range(len(zeroOneZeroCheck["messages"])):
    message = zeroOneZeroCheck["messages"][i]["text"]
    if message == "":
        pass
    else:
        date = zeroOneZeroCheck["messages"][i]["date"].split("T")
        Day = date[0]
        time = date[1]
        D.append(Day)
        T.append(time)
        messages.append(message)

results = pandas.DataFrame(data={"DAY":D,"TIME":T,"message":messages})

PGresults = results[results["message"].str.contains("[PG",na=False,regex=False)]
MSresults = results[results["message"].str.contains("[Musinsa",na=False,regex=False)]
_010results = results[results["message"].str.contains("[010페이",na=False,regex=False)]
MCresults = results[results["message"].str.contains("[내통장결제",na=False,regex=False)]
results1 = results[results["message"].str.contains("[서버",na=False,regex=False)]
results2 = pandas.concat([PGresults,MSresults],ignore_index=True)
results3 = pandas.concat([_010results,MCresults],ignore_index=True)

writer = pandas.ExcelWriter(path=os.path.join(os.path.dirname(__file__),"results.xlsx"),engine='openpyxl')

results1.to_excel(excel_writer=writer,sheet_name="simplePAY",index=False,engine="openpyxl")
results2.to_excel(excel_writer=writer,sheet_name="PG",index=False,engine="openpyxl")
results3.to_excel(excel_writer=writer,sheet_name="010PAY",index=False,engine="openpyxl")

writer.close()