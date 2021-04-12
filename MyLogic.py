# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 00:41:28 2021

@author: vf199
"""

import csv

#將開盤價與最後一天收盤價存至 all_price
def get_price(prediction):
    all_price = [] #價格
    for price in prediction:
        all_price.append(float(price[0]))
    else:
        #all_price.append(float(prediction[19][3]))#加入最後一天收盤價
        pass
    return all_price
    
#將價差紀錄下來
def get_spread(all_price):    
    spread = [] #記錄價差
    for k in range(len(all_price)-1):
        spread.append(all_price[k+1]-all_price[k])
    return spread
        
def get_sum_spread(spread):
    #將價差正負區間加總
    a = 0
    b = 0
    c = 0
    l1 = 0
    sum_spread = []
    index_spread_a = []
    index_spread_b = []
    index_spread_c = []
    for l in spread:
        if l > 0:
            a = a + l
            index_spread_a.append(c)
            if l1 * l < 0:
                sum_spread.append([b, index_spread_b])
            elif l1 * l == 0 and l != spread[0]:
                sum_spread.append([0, index_spread_c])
            b = 0
            index_spread_b = []
            index_spread_c = []
        elif l < 0:
            b = b + l
            index_spread_b.append(c)
            if l1 * l < 0:
                sum_spread.append([a, index_spread_a])
            elif l1 * l == 0 and l != spread[0]:
                sum_spread.append([0, index_spread_c])
            a = 0
            index_spread_a = []
            index_spread_c = []
        elif l == 0:#假設漲跌兩邊都不算
            index_spread_c.append(c)
            if l1 > 0:
                sum_spread.append([a, index_spread_a])
                a = 0
                index_spread_a = []
            elif l1 < 0:
                sum_spread.append([b, index_spread_b])
                b = 0
                index_spread_b = []
        l1 = l
        c = c + 1
    else:
        if a != 0:
            sum_spread.append([a, index_spread_a])
        elif b != 0:
            sum_spread.append([b, index_spread_b])
    return sum_spread

#買賣
def buy (unit, output):#買
    if unit != 1:
        unit = unit + 1
        output.append(1)
        print("購買後剩餘： "+ str(unit) + " 單位")
    else:
        print("Buy Error")
        output.append(0)
    return unit, output

def sell (unit, output):#賣
    if unit != -1:
        unit = unit - 1
        #output.append(-1)
        output.append(2)
        print("賣出後剩餘： "+ str(unit) + " 單位")
    else:
        print("Sell Error")
        output.append(0)
    return unit, output

def merchandise (unit, output, profit, sum_profit, next_spread): #交易
    if unit == 1:
        unit, output, sum_profit = sell(unit, output, profit, sum_profit)
    elif unit == -1:
        unit, output, sum_profit = buy(unit, output, profit, sum_profit)
    elif unit == 0:
        if abs(profit) < abs(next_spread):
            if next_spread > 0:
                unit, output, sum_profit = buy(unit, output, profit, sum_profit)
            elif next_spread < 0:
                unit, output, sum_profit = sell(unit, output, profit, sum_profit)
        elif abs(profit) > abs(next_spread):
            output.append(0)
    return unit, output, sum_profit

def mylogic (spread, sum_spread):
    output = [] #初始輸出設定
    unit = 0 #初始持有數為零
    for j in range(len(sum_spread)):
        ind_day = sum_spread[j][1]
        for i in ind_day:
            print(i)
            if i == 0:#第一天
                if spread[i]*spread[i+1] > 0:#若為連續漲跌
                    if spread[i] > 0:#若即將漲價
                        unit, output = buy(unit, output)#買入
                    elif spread[i] < 0:#若即將跌價
                        unit, output = sell(unit, output)#賣出
                elif spread[i]*spread[i+1] < 0 and spread[i+1]*spread[i+2] > 0:#若為單次漲跌，但下段為連續漲跌
                    if abs(spread[i]) > abs(sum_spread[j+1][0]):#若本單次漲跌大於下段連續漲跌總和
                        if spread[i] > 0:#若即將漲價
                            unit, output = buy(unit, output)#買入
                        elif spread[i] < 0:#若即將跌價
                            unit, output = sell(unit, output)#賣出
                    elif abs(spread[i]) <= abs(sum_spread[j+1][0]):#若本單次漲跌未大於下段連續漲跌總和
                        if abs(spread[i]) > abs(spread[sum_spread[j+1][1][0]]):#若本單次漲跌大於下段連續漲跌的第一小段漲跌
                            if spread[i] > 0:#若即將漲價
                                unit, output = buy(unit, output)#買入
                            elif spread[i] < 0:#若即將跌價
                                unit, output = sell(unit, output)#賣出
                        elif abs(spread[i]) <= abs(spread[sum_spread[j+1][1][0]]):#若本單次漲跌未大於(小於)下段連續漲跌的第一小段漲跌
                            output.append(0)
                elif spread[i]*spread[i+1] < 0 and spread[i+1]*spread[i+2] < 0:#若為單次漲跌，但下段也為單次漲跌 ##########
                    one_change = [] #紀錄單次變化的資訊
                    for k in range(j,len(sum_spread),1): #計算有連續幾次單次漲跌
                        if len(sum_spread[k][1]) != 1:
                            one_change.append([spread[int(sum_spread[k-1][1][0])+1],[int(sum_spread[k-1][1][0])+1]])#將接續的連續漲跌區間的第一段收益加進去
                            break
                        one_change.append(sum_spread[k])
                        
                    if len(one_change) >= 3: #連續單漲跌區間的最後一個單漲跌
                        if unit == 0: #手上無持股
                            if spread[i] > 0:#若即將漲價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = buy(unit, output)#買入
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小等於下一漲跌區間收益
                                    if abs(one_change[1][0]) > abs(one_change[2][0]): #下一單漲跌區間收益大於下一連續漲跌區間第一段收益
                                        output.append(0)#甚麼都不做
                                    elif abs(one_change[1][0]) <= abs(one_change[2][0]): #下一單漲跌區間收益小於下一連續漲跌區間第一段收益
                                        unit, output = buy(unit, output)#買入
                            elif spread[i] < 0:#若即將跌價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = sell(unit, output)#賣出
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    if abs(one_change[1][0]) > abs(one_change[2][0]): #下一單漲跌區間收益大於下一連續漲跌區間第一段收益
                                        output.append(0)#甚麼都不做
                                    elif abs(one_change[1][0]) <= abs(one_change[2][0]): #下一單漲跌區間收益小於下一連續漲跌區間第一段收益
                                        unit, output = sell(unit, output)#賣出
                        elif unit == 1: #持有1張
                            if spread[i] > 0:#若即將漲價
                                #print("ERROR")
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    #例外狀況，應該不會發生
                                    output.append(0)#甚麼都不做
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    if abs(one_change[1][0]) > abs(one_change[2][0]): #下一單漲跌區間收益大於下一連續漲跌區間第一段收益
                                        unit, output = sell(unit, output)#賣出
                                    elif abs(one_change[1][0]) <= abs(one_change[2][0]): #下一單漲跌區間收益小於下一連續漲跌區間第一段收益
                                        #例外狀況，應該不會發生
                                        output.append(0)#甚麼都不做
                            elif spread[i] < 0:#若即將跌價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = sell(unit, output)#賣出
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    if abs(one_change[1][0]) > abs(one_change[2][0]): #下一單漲跌區間收益大於下一連續漲跌區間第一段收益
                                        unit, output = sell(unit, output)#賣出
                                    elif abs(one_change[1][0]) <= abs(one_change[2][0]): #下一單漲跌區間收益小於下一連續漲跌區間第一段收益
                                        unit, output = sell(unit, output)#賣出
                        elif unit==-1: #持有-1張
                            if spread[i] > 0:#若即將漲價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = buy(unit, output)#買進
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    if abs(one_change[1][0]) > abs(one_change[2][0]): #下一單漲跌區間收益大於下一連續漲跌區間第一段收益
                                        unit, output = buy(unit, output)#買進
                                    elif abs(one_change[1][0]) <= abs(one_change[2][0]): #下一單漲跌區間收益小於下一連續漲跌區間第一段收益
                                        unit, output = buy(unit, output)#買進
                            elif spread[i] < 0:#若即將跌價
                                #print("ERROR")
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    #例外狀況，應該不會發生
                                    output.append(0)#甚麼都不做
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    if abs(one_change[1][0]) > abs(one_change[2][0]): #下一單漲跌區間收益大於下一連續漲跌區間第一段收益
                                        #例外狀況，應該不會發生
                                        unit, output = buy(unit, output)#買進
                                    elif abs(one_change[1][0]) <= abs(one_change[2][0]): #下一單漲跌區間收益小於下一連續漲跌區間第一段收益
                                        #例外狀況，應該不會發生
                                        output.append(0)#甚麼都不做
                    elif len(one_change) == 2: #最後2天單漲跌區間
                        if unit == 0: #手上無持股
                            if spread[i] > 0:#若即將漲價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = buy(unit, output)#買進
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    output.append(0)#甚麼都不做
                            elif spread[i] < 0:#若即將跌價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = sell(unit, output)#賣出
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    output.append(0)#甚麼都不做
                        elif unit == 1: #持有1張
                            if spread[i] > 0:#若即將漲價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    output.append(0)#甚麼都不做
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    unit, output = sell(unit, output)#賣出
                            elif spread[i] < 0:#若即將跌價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = sell(unit, output)#賣出
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    output.append(0)#甚麼都不做
                        elif unit==-1: #持有-1張
                            if spread[i] > 0:#若即將漲價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = buy(unit, output)#買進
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    output.append(0)#甚麼都不做
                            elif spread[i] < 0:#若即將跌價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    output.append(0)#甚麼都不做
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    unit, output = buy(unit, output)#買進
                elif spread[i] ==  0: #若本區間持平
                    output.append(0) #甚麼都不做
                    
            elif i == len(spread)-1:#最後一天
                if unit ==0: #手上無持股
                    if spread[i] > 0:#若即將漲價
                        unit, output = buy(unit, output)#買入
                    elif spread[i] < 0:#若即將跌價
                        unit, output = sell(unit, output)#賣出
                    elif spread[i] ==  0: #若本區間持平
                        output.append(0) #甚麼都不做
                elif unit == 1: #持有1張
                    if spread[i] > 0:#若即將漲價
                        output.append(0)
                    elif spread[i] < 0:#若即將跌價
                        unit, output = sell(unit, output)#賣出
                    elif spread[i] ==  0: #若本區間持平
                        output.append(0) #甚麼都不做
                elif unit==-1: #持有-1張
                    if spread[i] > 0:#若即將漲價
                        unit, output = buy(unit, output)#買入
                    elif spread[i] < 0:#若即將跌價
                        output.append(0)
                    elif spread[i] ==  0: #若本區間持平
                        output.append(0) #甚麼都不做
            else: #其他裝況
                if j == len(sum_spread)-1: #若為最後一段漲跌區間
                    day_last = ind_day[-1] #高點或低點前一天
                    day_first = ind_day[0] #高點或低點當天
                    day_second = ind_day[1] #高點或低點隔天
                    if i != day_last and i != day_first and i != day_second: #除了漲/跌區間前後外不進行任何操作(正確)
                        output.append(0)
                    else: #若為該區間高點或低點以及高點或低點後一天
                        if unit == 0: #手上無持股
                            if spread[i] > 0:#若即將漲價
                                unit, output = buy(unit, output)#買入
                            elif spread[i] < 0:#若即將跌價
                                unit, output = sell(unit, output)#賣出
                            elif spread[i] ==  0: #若本區間持平
                                output.append(0) #甚麼都不做
                        elif unit == 1: #持有1張
                            if spread[i] > 0:#若即將漲價
                                output.append(0)#甚麼都不做
                            elif spread[i] < 0:#若即將跌價
                                unit, output = sell(unit, output)#賣出
                            elif spread[i] ==  0: #若本區間持平
                                output.append(0) #甚麼都不做
                        elif unit == -1:
                            if spread[i] > 0:#若即將漲價
                                unit, output = buy(unit, output)#買入
                            elif spread[i] < 0:#若即將跌價
                                output.append(0)#甚麼都不做
                            elif spread[i] ==  0: #若本區間持平
                                output.append(0) #甚麼都不做
                            
                elif len(ind_day) >= 2: #若為連續漲跌區間
                    day_last = ind_day[-1] #高點或低點前一天
                    day_first = ind_day[0] #高點或低點當天
                    day_second = ind_day[1] #高點或低點隔天
                    if i != day_last and i != day_first and i != day_second: #除了漲/跌區間前後外不進行任何操作
                        output.append(0)
                        
                    elif i == day_first: #若為該區間高點或低點
                        if unit == 0: #手上無持股
                            if spread[i] > 0:#若即將漲價
                                unit, output = buy(unit, output)#買入
                            elif spread[i] < 0:#若即將跌價
                                unit, output = sell(unit, output)#賣出
                            elif spread[i] ==  0: #若本區間持平
                                output.append(0) #甚麼都不做
                        elif unit == 1: #持有1張
                            if spread[i] > 0:#若即將漲價
                                output.append(0)#甚麼都不做
                            elif spread[i] < 0:#若即將跌價
                                unit, output = sell(unit, output)#賣出
                            elif spread[i] ==  0: #若本區間持平
                                unit, output = sell(unit, output)#賣出
                        elif unit == -1:
                            if spread[i] > 0:#若即將漲價
                                unit, output = buy(unit, output)#買入
                            elif spread[i] < 0:#若即將跌價
                                output.append(0)#甚麼都不做
                            elif spread[i] ==  0: #若本區間持平
                                unit, output = buy(unit, output)#買入
                                
                    elif i == day_last: #若為下一區間高點或低點前一天
                        if abs(sum_spread[j+1][0]) > abs(spread[day_last]): #若下一漲/跌區間收益大於此區間最後一段收益
                            if abs(spread[day_last+1]) > abs(spread[day_last]): #若下一漲/跌區間第一段收益大於此區間最後一段收益
                                if unit == 0: #手上無持股
                                    #例外狀況，應該不會發生
                                    if spread[i] > 0:#若即將漲價
                                        output.append(0)#甚麼都不做
                                    elif spread[i] < 0:#若即將跌價
                                        output.append(0)#甚麼都不做
                                    elif spread[i] == 0:#若本區間持平
                                        output.append(0)#甚麼都不做
                                elif unit == 1: #持有1張
                                    if spread[i] > 0:#若即將漲價
                                        unit, output = sell(unit, output)#賣出
                                    elif spread[i] < 0:#若即將跌價
                                        #例外狀況，應該不會發生
                                        unit, output = sell(unit, output)#賣出
                                    elif spread[i] == 0:#若本區間持平
                                        #例外狀況，應該不會發生
                                        unit, output = sell(unit, output)#賣出
                                elif unit == -1:
                                    if spread[i] > 0:#若即將漲價
                                        #例外狀況，應該不會發生
                                        unit, output = buy(unit, output)#買入
                                    elif spread[i] < 0:#若即將跌價
                                        unit, output = buy(unit, output)#買入
                                    elif spread[i] == 0:#若本區間持平
                                        #例外狀況，應該不會發生
                                        unit, output = buy(unit, output)#買入
                            elif abs(spread[day_last+1]) <= abs(spread[day_last]): #若下一漲/跌區間第一段收益小於此區間最後一段收益
                                #至高點或低點在做買賣
                                output.append(0)#甚麼都不做
                        elif abs(sum_spread[j+1][0]) <= abs(spread[day_last]): #若下一漲/跌區間收益小於等於此區間最後一段收益
                            #至高點或低點在做買賣
                            output.append(0)#甚麼都不做
                            
                    elif i == day_second: #若為該區間高點或低點隔天
                        if unit ==0: #手上無持股
                            #在高點或低點當天或前一天沒有進行買賣
                            if spread[i] > 0:#若即將漲價
                                unit, output = buy(unit, output)#買入
                            elif spread[i] < 0:#若即將跌價
                                unit, output = sell(unit, output)#賣出
                            elif spread[i] == 0:#若本區間持平
                                output.append(0)
                        elif unit == 1: #持有1張
                            #在高點或低點當天或前一天已經進行買賣
                            if spread[i] > 0:#若即將漲價
                                output.append(0)
                            elif spread[i] < 0:#若即將跌價
                                output.append(0)
                            elif spread[i] == 0:#若本區間持平
                                unit, output = sell(unit, output)#賣出
                        elif unit==-1: #持有-1張
                            #在高點或低點當天或前一天已經進行買賣
                            if spread[i] > 0:#若即將漲價
                                output.append(0)
                            elif spread[i] < 0:#若即將跌價
                                output.append(0)
                            elif spread[i] == 0:#若本區間持平
                                unit, output = buy(unit, output)#買入
                                       
                elif len(ind_day) == 1 and len(sum_spread[j+1][1]) >= 2: #若本段為單漲跌區間，下一段為連續漲跌區間
                    if abs(spread[i]) > abs(sum_spread[j+1][0]):#若本單次漲跌大於下段連續漲跌總和
                        if unit == 0:#手上無持股
                            if spread[i] > 0:#若即將漲價
                                unit, output = buy(unit, output)#買入
                            elif spread[i] < 0:#若即將跌價
                                unit, output = sell(unit, output)#賣出
                            elif spread[i] == 0:#若本區間持平
                                output.append(0)
                        elif unit == 1: #持有1張
                            if spread[i] > 0:#若即將漲價
                                output.append(0)
                            elif spread[i] < 0:#若即將跌價
                                #例外狀況，應該不會發生
                                unit, output = sell(unit, output)#賣出
                            elif spread[i] == 0:#若本區間持平
                                #例外狀況，應該不會發生
                                unit, output = sell(unit, output)#賣出
                        elif unit==-1: #持有-1張
                            if spread[i] > 0:#若即將漲價
                                #例外狀況，應該不會發生
                                unit, output = buy(unit, output)#買入
                            elif spread[i] < 0:#若即將跌價
                                output.append(0)
                            elif spread[i] == 0:#若本區間持平
                                #例外狀況，應該不會發生
                                unit, output = buy(unit, output)#買入
                        
                    elif abs(spread[i]) <= abs(sum_spread[j+1][0]):#若本單次漲跌未大於(小於)下段連續漲跌總和
                        if abs(spread[i]) > abs(spread[sum_spread[j+1][1][0]]):#若本單次漲跌大於下段連續漲跌的第一小段漲跌
                            if unit == 0:#手上無持股
                                if spread[i] > 0:#若即將漲價
                                    unit, output = buy(unit, output)#買入
                                elif spread[i] < 0:#若即將跌價
                                    unit, output = sell(unit, output)#賣出
                                elif spread[i] == 0:#若本區間持平
                                    output.append(0)
                            elif unit == 1: #持有1張
                                if spread[i] > 0:#若即將漲價
                                    output.append(0)
                                elif spread[i] < 0:#若即將跌價
                                    #例外狀況，應該不會發生
                                    unit, output = sell(unit, output)#賣出
                                elif spread[i] == 0:#若本區間持平
                                    #例外狀況，應該不會發生
                                    unit, output = sell(unit, output)#賣出
                            elif unit==-1: #持有-1張
                                if spread[i] > 0:#若即將漲價
                                    #例外狀況，應該不會發生
                                    unit, output = buy(unit, output)#買入
                                elif spread[i] < 0:#若即將跌價
                                    output.append(0)
                                elif spread[i] == 0:#若本區間持平
                                    #例外狀況，應該不會發生
                                    unit, output = buy(unit, output)#買入
                                
                        elif abs(spread[i]) <= abs(spread[sum_spread[j+1][1][0]]):#若本單次漲跌未大於(小於)下段連續漲跌的第一小段漲跌
                            if unit == 0:#手上無持股
                                output.append(0)
                            elif unit == 1: #持有1張
                                if spread[i] > 0:#若即將漲價
                                    unit, output = sell(unit, output)#賣出
                                elif spread[i] < 0:#若即將跌價
                                    #例外狀況，應該不會發生
                                    unit, output = sell(unit, output)#賣出
                                elif spread[i] == 0:#若本區間持平
                                    #例外狀況，應該不會發生
                                    unit, output = sell(unit, output)#賣出
                            elif unit==-1: #持有-1張
                                if spread[i] > 0:#若即將漲價
                                    #例外狀況，應該不會發生
                                    unit, output = buy(unit, output)#買入
                                elif spread[i] < 0:#若即將跌價
                                    unit, output = buy(unit, output)#買入
                                elif spread[i] == 0:#若本區間持平
                                    #例外狀況，應該不會發生
                                    unit, output = buy(unit, output)#買入
                
                
                elif len(ind_day) == 1 and len(sum_spread[j+1][1]) == 1: #若本段為單漲跌區間，下一段也為單漲跌區間
                    one_change = [] #紀錄單次變化的資訊
                    for k in range(j,len(sum_spread),1): #計算有連續幾次單次漲跌
                        if len(sum_spread[k][1]) != 1:
                            one_change.append([spread[int(sum_spread[k-1][1][0])+1],[int(sum_spread[k-1][1][0])+1]])#將接續的連續漲跌區間的第一段收益加進去
                            break
                        one_change.append(sum_spread[k])
                        
                    if len(one_change) >= 3: #連續單漲跌區間的最後一個單漲跌
                        if unit == 0: #手上無持股
                            if spread[i] > 0:#若即將漲價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = buy(unit, output)#買入
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    if abs(one_change[1][0]) > abs(one_change[2][0]): #下一單漲跌區間收益大於下一連續漲跌區間第一段收益
                                        output.append(0)#甚麼都不做
                                    elif abs(one_change[1][0]) <= abs(one_change[2][0]): #下一單漲跌區間收益小於下一連續漲跌區間第一段收益
                                        unit, output = buy(unit, output)#買入
                            elif spread[i] < 0:#若即將跌價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = sell(unit, output)#賣出
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    if abs(one_change[1][0]) > abs(one_change[2][0]): #下一單漲跌區間收益大於下一連續漲跌區間第一段收益
                                        output.append(0)#甚麼都不做
                                    elif abs(one_change[1][0]) <= abs(one_change[2][0]): #下一單漲跌區間收益小於下一連續漲跌區間第一段收益
                                        unit, output = sell(unit, output)#賣出
                            elif spread[i] == 0:#若本區間持平
                                output.append(0)#甚麼都不做
                        elif unit == 1: #持有1張
                            if spread[i] > 0:#若即將漲價
                                #print("ERROR")
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    #例外狀況，應該不會發生
                                    output.append(0)#甚麼都不做
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    if abs(one_change[1][0]) > abs(one_change[2][0]): #下一單漲跌區間收益大於下一連續漲跌區間第一段收益
                                        unit, output = sell(unit, output)#賣出
                                    elif abs(one_change[1][0]) <= abs(one_change[2][0]): #下一單漲跌區間收益小於下一連續漲跌區間第一段收益
                                        #例外狀況，應該不會發生
                                        output.append(0)#甚麼都不做
                            elif spread[i] < 0:#若即將跌價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = sell(unit, output)#賣出
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    if abs(one_change[1][0]) > abs(one_change[2][0]): #下一單漲跌區間收益大於下一連續漲跌區間第一段收益
                                        unit, output = sell(unit, output)#賣出
                                    elif abs(one_change[1][0]) <= abs(one_change[2][0]): #下一單漲跌區間收益小於下一連續漲跌區間第一段收益
                                        output.append(0)#甚麼都不做
                            elif spread[i] == 0:#若本區間持平
                                unit, output = sell(unit, output)#賣出
                        elif unit==-1: #持有-1張
                            if spread[i] > 0:#若即將漲價
                                #print("ERROR")
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = buy(unit, output)#買進
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    if abs(one_change[1][0]) > abs(one_change[2][0]): #下一單漲跌區間收益大於下一連續漲跌區間第一段收益
                                        unit, output = buy(unit, output)#買進
                                    elif abs(one_change[1][0]) <= abs(one_change[2][0]): #下一單漲跌區間收益小於下一連續漲跌區間第一段收益
                                        unit, output = buy(unit, output)#買進
                            elif spread[i] < 0:#若即將跌價
                                #print("ERROR")
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    #例外狀況，應該不會發生
                                    output.append(0)#甚麼都不做
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    if abs(one_change[1][0]) > abs(one_change[2][0]): #下一單漲跌區間收益大於下一連續漲跌區間第一段收益
                                        #例外狀況，應該不會發生
                                        unit, output = buy(unit, output)#買進
                                    elif abs(one_change[1][0]) <= abs(one_change[2][0]): #下一單漲跌區間收益小於下一連續漲跌區間第一段收益
                                        #例外狀況，應該不會發生
                                        output.append(0)#甚麼都不做
                            elif spread[i] == 0:#若本區間持平
                                #例外狀況，應該不會發生
                                unit, output = buy(unit, output)#買進
                    elif len(one_change) == 2: #最後2天單漲跌區間
                        if unit == 0: #手上無持股
                            if spread[i] > 0:#若即將漲價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = buy(unit, output)#買進
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    output.append(0)#甚麼都不做
                            elif spread[i] < 0:#若即將跌價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = sell(unit, output)#賣出
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    output.append(0)#甚麼都不做
                            elif spread[i] == 0:#若本區間持平
                                output.append(0)#甚麼都不做
                        elif unit == 1: #持有1張
                            if spread[i] > 0:#若即將漲價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    output.append(0)#甚麼都不做
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    unit, output = sell(unit, output)#賣出
                            elif spread[i] < 0:#若即將跌價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = sell(unit, output)#賣出
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    output.append(0)#甚麼都不做
                            elif spread[i] == 0:#若本區間持平
                                unit, output = sell(unit, output)#賣出
                        elif unit==-1: #持有-1張
                            if spread[i] > 0:#若即將漲價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    unit, output = buy(unit, output)#買進
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    output.append(0)#甚麼都不做
                            elif spread[i] < 0:#若即將跌價
                                if abs(one_change[0][0]) > abs(one_change[1][0]):#漲跌區間收益大於下一漲跌區間收益
                                    output.append(0)#甚麼都不做
                                elif abs(one_change[0][0]) <= abs(one_change[1][0]):#漲跌區間收益小於下一漲跌區間收益
                                    unit, output = buy(unit, output)#買進
                            elif spread[i] == 0:#若本區間持平
                                unit, output = buy(unit, output)#買進
    return output

def creat_csv(output, file_name):
    with open(file_name,'w',newline='') as csvfile:
        csv_write=csv.writer(csvfile)
        
        for i in output:
            csv_write.writerow([i])
    print("Csv File is created!")
    
def write_csv(output, file_name):
    with open(file_name,'a',newline='') as csvfile:
        csv_write=csv.writer(csvfile)
        
        for i in output:
            csv_write.writerow([i])
    print("Csv file is writed!")
    
def load_csv(file_name):
    data=[]#建立空矩陣，之後用來儲存CSV檔中的資料
    with open(file_name,newline='',encoding="utf-8") as csvfile:
        rows=csv.reader(csvfile)
        
        for row in rows:
            data.append(row)
    print("Csv file is loaded")
    return data

def calculation(output, all_price):
    profit = 0
    #最後一天將所有持有股票出清
    if sum(output) == 1:
        output.append(-1)
    elif sum(output) == -1:
        output.append(1)
    elif sum(output) == 0:
        output.append(0)
    
    for i in range(len(output)):
        profit = profit + output[i] * all_price[i] * (-1)
    return output, profit
  
def final_day(output):
    one = 0
    two = 0
    for i in output:
        if i == 1:
            one = one + 1
        elif i == 2:
            two = two + 1
            
    if one - two == 1:
        output.append(2)
    elif one - two == -1:
        output.append(1)
    elif one - two == 0:
        output.append(0)
    return output
    
def testing_first_day(output):
    output.append(0)
    return output