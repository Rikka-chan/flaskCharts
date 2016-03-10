import requests
import json

def request_wrapper(data):
    headers={
        "kbn-version":"4.3.1"
            }

    r=requests.post(
            "http://192.168.20.3/elasticsearch/_msearch?timeout=0&ignore_unavailable=true&preference=1457214241738",
            data=data,
            headers=headers
    ).json()
    ret=r['responses'][0]['aggregations']['2']['buckets']
    return ret


def soapDurationBuckets(time_of_beginning,time_of_end,now,interval):#change the date in index. it is cause of trouble of empty response
    dat='{"index":["logstash-emias-backend-'+now +'"],"search_type":"count","ignore_unavailable":true}'+'\n'+\
'{"size":0,"query":{"filtered":{"query":{"query_string":{"analyze_wildcard":true,"query":"*"}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"gte":'+str(time_of_beginning)+',"lte":'+str(time_of_end)+',"format":"epoch_millis"}}}],"must_not":[]}}}},"aggs":{"2":{"date_histogram":{"field":"@timestamp","interval":"'+interval+'","time_zone":"Europe/Minsk","min_doc_count":1,"extended_bounds":{"min":'+str(time_of_beginning)+',"max":'+str(time_of_end)+'}},"aggs":{"3":{"terms":{"field":"soap_call.raw","size":15,"order":{"1":"desc"}},"aggs":{"1":{"avg":{"field":"soap_duration"}}}}}}}}\n'

    return request_wrapper(dat)

def soapErrorCounter(time_of_beginning, time_of_end, now, interval):
    dat='{"index":["logstash-emias-backend-'+now +'"],"search_type":"count","ignore_unavailable":true}'+'\n'+\
        '{"size":0,"query":{"filtered":{"query":{"query_string":{"analyze_wildcard":true,"query":"*"}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"gte":'+str(time_of_beginning)+',"lte":'+str(time_of_end)+',"format":"epoch_millis"}}}],"must_not":[]}}}},"aggs":{"2":{"date_histogram":{"field":"@timestamp","interval":"'+interval+'","time_zone":"Europe/Minsk","min_doc_count":1,"extended_bounds":{"min":'+str(time_of_beginning)+',"max":'+str(time_of_end)+'}},"aggs":{"3":{"terms":{"field":"soap_call.raw","size":15,"order":{"1":"desc"}},"aggs":{"1":{"cardinality":{"field":"soap_error.raw"}}}}}}}}\n'

    return request_wrapper(dat)