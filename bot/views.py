from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from json import loads
from bot.models import Card
import re
import requests
import random
import time

g_id = 683423349


def print_to_private(msg: str):
    requests.post('http://127.0.0.1:5700/send_private_msg', data={'user_id': 1445031625, 'message': msg})


def print_to_group(msg: str):
    requests.post('http://127.0.0.1:5700/send_group_msg', data={'group_id': g_id, 'message': msg})


def pop(star: int):
    cards = Card.objects.filter(star=star)
    time.sleep(0.01)
    x = random.randint(0, len(cards) - 1)
    return cards[x].cid


def draw():
    x = random.randint(1, 1000)
    if x <= 25:
        return pop(3)
    elif x <= 205:
        return pop(2)
    else:
        return pop(1)


def draw_s():
    x = random.randint(1, 1000)
    if x <= 25:
        return pop(3)
    else:
        return pop(2)


def draw_10():
    string = '抽卡结果为：'
    for i in range(9):
        card = Card.objects.get(cid=draw())
        string += '\n' + '★' * card.star + '  ' + card.name
    card = Card.objects.get(cid=draw_s())
    string += '\n' + '★' * card.star + '  ' + card.name
    return string


def draw_300():
    string = '一井共抽出不重复三星：'
    lst = [0] * 70
    for i in range(1, 301):
        if i % 10:
            lst[draw() - 1001] = 1
        else:
            lst[draw_s() - 1001] = 1
    cards = Card.objects.all()
    for i in cards:
        if i.star == 3 and lst[i.cid - 1001]:
            string += '\n' + i.name
    return string


# Create your views here.
@require_http_methods('POST')
def sever(request):
    data = loads(request.body)
    m_type = data['message'][0]['type']
    if m_type != 'text':
        return JsonResponse({})
    text = data['message'][0]['data'].get('text')
    print(data)
    res = re.search('#(.*)', text)
    if not res:
        return JsonResponse({})
    srh_card = re.search('#查询 角色(.*)', text)
    draw_cards = re.search('#抽卡 (.*)', text)
    if srh_card:
        if not srh_card.group(1):
            cards = Card.objects.values('name')
            string = '目前角色有：'
            for i in cards:
                string += '\n' + i['name']
            print_to_group(string)
        else:
            card = Card.objects.filter(name=srh_card.group(1)[1:])
            if card:
                print_to_group(card[0].print())
            else:
                print_to_group('不存在该角色')
    elif draw_cards:
        if draw_cards.group(1) == '十连':
            print_to_group(draw_10())
        elif draw_cards.group(1) == '一井':
            print_to_group(draw_300())
        else:
            print_to_group('不存在该命令')
    print(res)
    return JsonResponse({})
