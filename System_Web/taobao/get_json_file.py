from MyModel.models import Analyse
from MyModel.models import Spider
from MyModel.models import Taobao
from django.shortcuts import render
from django.http import HttpResponse
import requests
import re
import random
import math


def get_barjson(taobao_id):
    try:
        analyse = Analyse.objects.get(analyse_id=taobao_id)
        return analyse.analyse_positive_prob
    except Analyse.DoesNotExist:
        print("情感倾向查询不存在")
        return None


def get_piejson(taobao_id):
    try:
        spider = Spider.objects.get(spider_id=taobao_id)
        return spider.spider_detail_Common
    except Spider.DoesNotExist:
        print("总体评价查询不存在")
        return None


def get_taobao(taobao_id):
    try:
        taobao = Taobao.objects.get(taobao_id=taobao_id)
        return taobao.taobao_name, taobao.taobao_price_now, taobao.taobao_time
    except Taobao.DoesNotExist:
        print("宝贝名称、价格、时间查询不存在")
        return None, None, None


def get_history_price(taobao_id):
    taobao_url = "http://www.xitie.com/tmall.php?no=" + taobao_id
    r = requests.get(taobao_url, allow_redirects=False)
    text = r.text
    error_text = "您输入的编号有错误"
    if error_text in text:
        return None, None
    data = re.findall(r"data: \[(.+?)\]", text)
    time = re.findall(r"categories: \[(.+?)\]", text)

    datas = data[0].split(',')

    newlist = []
    for i in datas:
        newlist.append(float(i))

    min_data = math.floor(min(newlist) / pow(10, len(str(math.floor(min(newlist)))) - 1)) * pow(10, len(
        str(math.floor(min(newlist)))) - 1)
    max_data = math.ceil(max(newlist) / pow(10, len(str(math.ceil(max(newlist)))) - 1)) * pow(10, len(
        str(math.ceil(max(newlist)))) - 1)

    newlist.append(min_data)
    newlist.append(max_data)
    print(newlist)

    return str(newlist), str(time)[2:-2]


def get_json_url(request):
    if request.GET:
        taobao_id = request.GET['taobao_id']
        print(taobao_id)

    json = get_barjson(taobao_id)

    if json:
        return HttpResponse(json)
    else:
        return HttpResponse(taobao_id)


def get_iframe_html(request):
    context = {}
    context['hello'] = 'Hello World!'
    if request.GET:
        taobao_id = request.GET['taobao_id']
        print("get_id：" + taobao_id)
        if taobao_id == None:
            return HttpResponse("未获取ID")

        # 准备宝贝名称、价格、时间
        taobao_name, taobao_price, taobao_time = get_taobao(taobao_id)
        if taobao_name == None:
            print("无效ID")
            return HttpResponse("无效ID")
        print(taobao_name, taobao_price, taobao_time)

        context['taobao_id'] = taobao_id

        context['taobao_name'] = taobao_name
        context['taobao_price'] = taobao_price
        context['taobao_time'] = taobao_time

        # 准备图表数据
        json_bar = get_barjson(taobao_id)
        if json_bar == None:
            return HttpResponse("柱状图ID错误")
        # 转list，排序
        json_bar = re.sub(' ', '', json_bar[1:-1]).split(",")
        json_bar.sort(key=None, reverse=False)
        # 转str
        barstr = ",".join(json_bar)

        if barstr == "":
            context['empty_bar'] = "柱状图没有有效的评论数据"
            print("正向情感数组为空")
        else:
            print("正向情感数组：" + barstr)
        context['barlables'] = context['bardata'] = barstr
###############################################################
        # 新的评论分析图
        newjson_bar = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in json_bar:
            i = float(i)
            if 0 <= i < 0.1:
                newjson_bar[0] += 1
            if 0.1 <= i < 0.2:
                newjson_bar[1] += 1
            if 0.2 <= i < 0.3:
                newjson_bar[2] += 1
            if 0.3 <= i < 0.4:
                newjson_bar[3] += 1
            if 0.4 <= i < 0.5:
                newjson_bar[4] += 1
            if 0.5 <= i < 0.6:
                newjson_bar[5] += 1
            if 0.6 <= i < 0.7:
                newjson_bar[6] += 1
            if 0.7 <= i < 0.8:
                newjson_bar[7] += 1
            if 0.8 <= i < 0.9:
                newjson_bar[8] += 1
            if 0.9 <= i <= 1.0:
                newjson_bar[9] += 1
        sum = len(json_bar)
        for i in range(10):
            newjson_bar[i] = round(newjson_bar[i] / sum * 100)
        context['newbarlables'] = "'0-0.1','0.1-0.2','0.2-0.3','0.3-0.4','0.4-0.5','0.5-0.6','0.6-0.7','0.7-0.8','0.8-0.9','0.9-1.0'"
        context['newbardata'] = str(newjson_bar)

        newbarcolor = ""
        for col in range(0,5):
            co_color = "'rgba({0}, {1}, {2}, 0.8)',".format(255, 0, math.floor(col * 255 / 10))
            newbarcolor = newbarcolor.__add__(co_color)
        for col in range(5,11):
            co_color = "'rgba({0}, {1}, {2}, 0.8)',".format(0, 255, math.floor(col * 255 / 10))
            newbarcolor = newbarcolor.__add__(co_color)
        context['newbarcolor'] = newbarcolor
#################################################################

        # 准备图表颜色
        barcolor = ""
        ran_num = round(random.uniform(0, 255))
        for co in json_bar:
            co = round(float(co) * 255)
            co_color = "'rgba({0}, {1}, {2}, 0.8)',".format(255 - co, co, ran_num)
            barcolor = barcolor.__add__(co_color)
        context['barcolor'] = barcolor

        # 准备评价饼图数据
        json_pie = get_piejson(taobao_id)
        if json_pie == None:
            return HttpResponse("饼图ID错误")

        pie_title = re.findall(r"\"title\":\"(.+?)\"", json_pie)
        pie_value = re.findall(r"\{\"count\":(.+?),\"", json_pie)
        if len(pie_value) == 0:
            context['empty_pie'] = "总体评价饼图没有有效的评价数据"
            print("总体评价数组为空")
        else:
            print("总体评价分类：" + str(pie_title))
            print("总体评价数值：" + str(pie_value))
        context['pielables'] = pie_title
        context['piedata'] = pie_value
        # 准备评价饼图颜色
        piecolor = ""
        for lo in range(len(pie_value)):
            lo = round(random.uniform(0, 0.1) * 2550)
            lo_color = "'rgba({0}, {1}, {2}, 0.8)',".format(round(255 - lo / 2) % 255, lo * 2 % 255, lo % 255)
            piecolor = piecolor.__add__(lo_color)
        context['piecolor'] = piecolor

        # 准备好中差评数据
        pie_good_data = re.findall(r"\"good\":(.+?),\"", json_pie)
        pie_normal_data = re.findall(r"\"normal\":(.+?),\"", json_pie)
        pie_bad_data = re.findall(r"\"bad\":(.+?),\"", json_pie)
        threedata = pie_good_data + pie_normal_data + pie_bad_data
        if len(threedata) != 3:
            context['empty_three'] = "好中差评饼图没有有效的评价数据"
            print("好评、中评、差评数组为空")
        else:
            print("好中差评数据：" + str(threedata))
        context['threelables'] = ['好评', '中评', '差评']
        context['threedata'] = threedata
        # 准备好中差评饼图颜色
        # threecolor = ""
        # for ro in range(3):
        #     ro = round(random.uniform(0, 0.1) * 2550)
        #     ro_color = "'rgba({0}, {1}, {2}, 0.8)',".format(ro % 255, ro * 2 % 255, round(255 - ro / 2) % 255)
        #     threecolor = threecolor.__add__(ro_color)
        threecolor = "'rgba(255, 0, 0, 0.8)','rgba(0, 255, 0, 0.8)','rgba(0, 0, 255, 0.8)'"
        print(threecolor)
        context['threecolor'] = threecolor

        # 准备历史价格数据
        context['pointdata'], context['pointlables'] = get_history_price(taobao_id)
        if context['pointdata'] == None or context['pointlables'] == None:
            context['empty_point'] = "商品没有有效的历史价格数据"
        ho = round(random.uniform(0, 0.1) * 2550)
        context['pointcolor'] = "'rgba({0}, {1}, {2}, 0.8)',".format(ho % 255, ho * 2 % 255, round(255 - ho / 2) % 255)

        return render(request, 'get_more_analyse.html', context)
    return HttpResponse("请使用正确GET参数")
