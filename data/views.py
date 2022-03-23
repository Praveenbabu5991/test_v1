from django.shortcuts import render
import pandas as pd
import io
import xlsxwriter
from django.http import HttpResponse
import xlwt
import datetime
from .inference import *
obj=SentimentInference('Trainings.xlsx','myModel.h5')


def home(request):
    if request.method=="POST":
        file=request.FILES["myfile"]
        csv=pd.read_csv(file)
    return render(request, 'index.html')

def result(request):
    if request.method=="POST":
        file=request.FILES["myfile"]
        csv=pd.read_excel(file)
        print(csv.shape)
        print("###################################################")
        #csv = csv.drop_duplicates()
        print("############################################")
        csv=csv.dropna()
        #csv['Text'] = csv.fillna({'Text':''})
        print(csv.shape)
        print(csv.isnull().sum().sum()
)
        l=list(csv["Text"])
        f=obj.predict(l)
        print("####################################################")
        response=HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition']='attachment; filename=Predictionresult' +\
        str(datetime.datetime.now())+'.xls'
        wb=xlwt.Workbook(encoding="utf-8")
        ws=wb.add_sheet('s1')
        row_num=0
        font_style=xlwt.XFStyle()
        font_style.font.bold=True
        columns=["Timestamp","I was satisfied with the content of the Training (1 strongly disagree and 4 strongly agree)","The content was presented in a logically and easy-to-follow manner (1 strongly disagree and 4 strongly agree)","Trainer was able to hold my interest  (1 strongly disagree and 4 strongly agree)","I was satisfied with the training method (1 strongly disagree and 4 strongly agree)","The speed of the training was appropriate (1 strongly disagree and 4 strongly agree)","I can use new information/knowledge in my daily work (1 strongly disagree and 4 strongly agree)","Rate your overall impression of the training (1= unsatisfying, 2 = not very good, 3 = good, 4 = excellent)","What did you enjoy from the training and why? If nothing, leave the answer blank.","What did you not like about the training and why? If nothing, leave the answer blank.","What you would suggest to the trainer? If nothing, leave the answer blank."]
        for col_num in range(len(columns)):
            ws.write(row_num,col_num,columns[col_num],font_style)
        font_style=xlwt.XFStyle()
        rows=csv.values.tolist()
        for row in rows:
            row_num+=1
            for col_num in range(len(row)):
                ws.write(row_num,col_num,str(row[col_num]),font_style)
        ###############################
        ws=wb.add_sheet('s2')
        row_num=0
        font_style=xlwt.XFStyle()
        font_style.font.bold=True
        columns=["Text","Prediction"]
        for col_num in range(len(columns)):
            ws.write(row_num,col_num,columns[col_num],font_style)
        font_style=xlwt.XFStyle()
        nd=pd.DataFrame()
        nd["Text"]=l
        nd["Prediction"]=f
        print(nd.head(5))
        rows=nd.values.tolist()
        for row in rows:
            row_num+=1
            for col_num in range(len(row)):
                ws.write(row_num,col_num,str(row[col_num]),font_style)

        wb.save(response)

        print("++++++++++++++++++++++++++")
        return response





    return render(request, 'result.html',{"csvf":csv})
