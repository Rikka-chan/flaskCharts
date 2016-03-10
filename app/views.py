from app import app
from flask import render_template, request, redirect,url_for
import search
from datetime import datetime, date, time, timedelta
import chart


def values_by_soap(soap,buckets):
    res=[]
    for bucket in buckets:
        buff=None

        for buck in bucket['3']['buckets']:
            if buck['key'] == soap:
                buff=buck['1']['value']

        res.append(buff)
    return res



def doc_count_by_soap(soap,buckets):
    res=[]
    for bucket in buckets:
        buff=0

        for buck in bucket['3']['buckets']:
            if buck['key'] == soap:
                buff=buck['doc_count']

                if buff!=0:
                    buff=float(buck['1']['value'])*100/float(buff)
        res.append(buff)
    return res



@app.route('/')
@app.route('/index/', methods=["GET","POST"])
def index():
    types_of_graph=['average_duration','error_count','error_soap']
    time_of_beginning=dict.fromkeys(types_of_graph,\
                                    (int(datetime.now().strftime("%s")) -3600) * 1000)
    time_of_end = int(datetime.now().strftime("%s"))  * 1000
    interval=dict.fromkeys(types_of_graph,'10m')
    if request.method=="POST":
        for type in types_of_graph:
            if request.form.get('interval_'+type)=='1d':
                time_of_beginning[type] =(int(datetime.now().strftime("%s")) -86400) * 1000
                interval[type]='1h'

            if request.form.get('interval_'+type)=='7d':
                time_of_beginning [type] =(int(datetime.now().strftime("%s")) -604800) * 1000
                interval[type]='1d'
    soap_calls=['getDoctorsInfo','createAppointment','getAvailableResourcesScheduleInfo',
                'cancelAppointment','digitalPrescription','getAppointmentReceptionsByPatient','getSpecialitiesInfo',
                'shiftAppointment','getAllLpusInfo']



    buckets=search.soapDurationBuckets(time_of_beginning['average_duration'], time_of_end,
                                       (datetime.now()+timedelta(hours=3)).strftime("%Y.%m.%d"),interval['average_duration'])
    duration_chart=chart.build_chart('Line',soap_calls, buckets,values_by_soap,
                                     title='Average duration by soap',interval=interval['average_duration'])


    buckets=search.soapErrorCounter(time_of_beginning['error_count'],time_of_end,
                                    (datetime.now()+timedelta(hours=3)).strftime("%Y.%m.%d"), interval['error_count'])#datetime.now().strftime("%Y.%m.%d")
    error_chart=chart.build_chart('StackedBar',soap_calls,buckets,values_by_soap,
                                  rounded_bars=4,title='Count errors by soap',interval=interval['error_count'])

    buckets=search.soapErrorCounter(time_of_beginning['error_soap'],time_of_end,
                                    (datetime.now()+timedelta(hours=3)).strftime("%Y.%m.%d"), interval['error_soap'])
    temp_chart=chart.build_chart('Line',soap_calls,buckets,doc_count_by_soap,title='Errors relative success (%)',
                                 y_labels=[0,10,20,30,40,50,60,70,80,90,100],interval=interval['error_soap'])

    return render_template("index.html",
                           avarage_dur_graph=duration_chart.render_data_uri(),
                           error_count_graph=error_chart.render_data_uri(),
                           error_soap_graph=temp_chart.render_data_uri())

