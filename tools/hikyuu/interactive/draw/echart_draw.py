#!/usr/bin/python
# -*- coding: utf8 -*-
# cp936
#
# The MIT License (MIT)
#
# Copyright (c) 2010-2017 fasiondog
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#===============================================================================
# history:
# 1. 20171121, Added by fasiondog
#===============================================================================

import sys
import datetime
import numpy as np

from hikyuu import *
from hikyuu.indicator import Indicator, MACD, CLOSE
from hikyuu.trade_manage import BUSINESS 
from hikyuu.trade_sys.system import getSystemPartName

from pyecharts import Overlap, Line, Kline, Bar
from .common import get_draw_title

g_overlap = None

def gca():
    global g_overlap
    if g_overlap is None:
        g_overlap = Overlap(width=800, height=450)
    return g_overlap

def create_one_axes_figure(figsize=(800,450)):
    """生成一个仅含有1个坐标轴的figure，并返回其坐标轴对象
    
    :param figsize: (宽, 高)
    :return: ax
    """
    global g_overlap
    g_overlap = Overlap(width=figsize[0], height=figsize[1])
    return g_overlap

def create_figure(n=1, figsize=(800,450)):
    """生成含有指定坐标轴数量的窗口，最大只支持4个坐标轴。

    :param int n: 坐标轴数量
    :param figsize: (宽, 高)
    :return: (ax1, ax2, ...) 根据指定的坐标轴数量而定，超出[1,4]个坐标轴时，返回None
    """
    if n == 1:
        return create_one_axes_figure(figsize)
    elif n == 2:
        pass
        #return create_two_axes_figure(figsize)
    elif n == 3:
        pass
        #return create_three_axes_figure(figsize)
    elif n == 4:
        pass
        #return create_four_axes_figure(figsize)
    else:
        #print("Max support axes number is 4!")
        return None
    

def iplot(indicator, new=False, axes=None, 
          legend_on=False, text_on=False, text_color='k',  
          zero_on=False, label=None, *args, **kwargs):
    """绘制indicator曲线
    
    :param Indicator indicator: indicator实例
    :param axes:            指定的坐标轴
    :param new:             pyecharts中无效
    :param legend_on:       是否打开图例
    :param text_on:         是否在左上角显示指标名称及其参数
    :param text_color:      指标名称解释文字的颜色，默认为黑色
    :param zero_on:         是否需要在y=0轴上绘制一条直线
    :param str label:       label显示文字信息，text_on 及 legend_on 为 True 时生效
    :param args:            pylab plot参数
    :param kwargs:          pylab plot参数，如：marker（标记类型）、
                             markerfacecolor（标记颜色）、
                             markeredgecolor（标记的边缘颜色）
    """
    if not indicator:
        print("indicator is None")
        return
    
    if not axes:
        axes = gca()
    
    if not label:
        label = "%s %.2f" % (indicator.long_name, indicator[-1])

    x_list = [i for i in range(len(indicator))]
    y_list = [ '-' if x == constant.null_price else round(x,3) for x in indicator]
    line = Line()
        
    line.add(label, x_list, y_list, 
             is_datazoom_show=True, yaxis_min=min(indicator),
             is_legend_show=legend_on,
             *args, **kwargs)
    
    axes.add(line)
        
    return axes  


def ibar(indicator, new=False, axes=None, 
          legend_on=False, text_on=False, text_color='k',  
          zero_on=False, label=None, *args, **kwargs):
    """绘制indicator曲线
    
    :param Indicator indicator: indicator实例
    :param axes:            指定的坐标轴
    :param new:             pyecharts中无效
    :param legend_on:       是否打开图例
    :param text_on:         是否在左上角显示指标名称及其参数
    :param text_color:      指标名称解释文字的颜色，默认为黑色
    :param zero_on:         是否需要在y=0轴上绘制一条直线
    :param str label:       label显示文字信息，text_on 及 legend_on 为 True 时生效
    :param args:            pylab plot参数
    :param kwargs:          pylab plot参数，如：marker（标记类型）、
                             markerfacecolor（标记颜色）、
                             markeredgecolor（标记的边缘颜色）
    """
    if not indicator:
        print("indicator is None")
        return
    
    if not axes:
        axes = gca()
    
    if not label:
        label = "%s %.2f" % (indicator.long_name, indicator[-1])

    x_list = [i for i in range(len(indicator))]
    y_list = [ '-' if x == constant.null_price else round(x,3) for x in indicator]
    bar = Bar()
        
    bar.add(label, x_list, y_list, 
             is_datazoom_show=True, yaxis_min=min(indicator),
             is_legend_show=legend_on,
             *args, **kwargs)
    
    axes.add(bar)
        
    return axes  


def kplot(kdata, new=True, axes=None, 
          colorup='r', colordown='g', width=0.6, alpha=1.0):
    """绘制K线图
    
    :param KData kdata: K线数据
    :param bool new:    是否在新窗口中显示，只在没有指定axes时生效
    :param axes:        指定的坐标轴
    :param colorup:     the color of the rectangle where close >= open
    :param colordown:   the color of the rectangle where close < open
    :param width:       fraction of a day for the rectangle width
    :param alpha:       the rectangle alpha level, 透明度(0.0~1.0) 1.0为不透明
    """
    if not kdata:
        print("kdata is None")
        return
    
    if not axes:
        axes = gca()
        
    title = get_draw_title(kdata)
    last_record = kdata[-1]
    text = u'%s 开:%.2f 高:%.2f 低:%.2f 收:%.2f 涨幅:%.2f%%' % (
        last_record.datetime.number/10000, 
        last_record.openPrice, last_record.highPrice,
        last_record.lowPrice,  last_record.closePrice,
        100*(last_record.closePrice-kdata[-2].closePrice)/kdata[-2].closePrice)
    
    date_list = kdata.getDatetimeList()
    if kdata.getQuery().kType == KQuery.DAY:
        x_list = [d.date() for d in date_list]
    else:
        x_list = [d.datetime() for d in date_list]
        
    y_list = [[k.openPrice, k.closePrice, k.lowPrice, k.highPrice] for k in kdata] 

    kline = Kline(title, text, title_pos='center', subtitle_color='#FF0000')
    kline.add(None, x_axis=x_list, y_axis=y_list, is_datazoom_show=True,
              mark_line=["max"], mark_line_symbolsize=0, 
              mark_line_valuedim='highest')
    axes.add(kline)
    
    return axes  

def mkplot(kdata, new=True, axes=None, colorup='r', colordown='g', ticksize=3):
    """绘制美式K线图
    
    :param KData kdata: K线数据
    :param bool new:    是否在新窗口中显示，只在没有指定axes时生效
    :param axes:        指定的坐标轴
    :param colorup:     the color of the lines where close >= open
    :param colordown:   the color of the lines where close < open
    :param ticksize:    open/close tick marker in points
    """
    print('Pyecharts暂不支持美式K线图')
    return None