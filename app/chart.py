
import pygal
from pygal.style import NeonStyle, DarkStyle
import arrow


def get_time_range(buckets,interval='minutes'):
    res=[]
    for bucket in buckets:

        temp_time=arrow.get(bucket['key_as_string']).datetime
        if interval=='10m' or interval=='1h':
            res.append(str(temp_time.hour)+':'+str(temp_time.minute))
        if interval=='1d':
            res.append(temp_time.strftime('%Y.%m.%d'))
    return  res


def build_chart(type, soap_calls, buckets, get_values,style=DarkStyle,rounded_bars=0,y_labels=[],title="some chart",interval='10m'):
    chart = pygal.Line(style=style)
    if type=='Line' or type=='line':
        chart = pygal.Line(style=style)

    if type=='Bar' or type=='bar':
        chart = pygal.Bar(style=style)

    if type=='Pie' or type=='pie':
        chart = pygal.Pie(style=style)

    if type=='StackedBar' or type=='stacked_bar':
        chart = pygal.StackedBar(style=style)

    chart.title = title
    print('build_chart')
    chart.x_labels = get_time_range(buckets,interval)
    if(y_labels):
        chart.y_labels=y_labels
    for soap in soap_calls:
        chart.add(soap, get_values(soap, buckets),rounded_bars=rounded_bars)
    return chart