import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import pickle
import pandas as pd

def save_inventory(Diction):
    filename = 'inventory.text'
    outfile = open(filename,'wb')
    pickle.dump(Diction,outfile)
    outfile.close()

def open_inventory(_dict):
    filename = 'inventory.text'
    infile = open(filename,'rb')
    new_dict = pickle.load(infile)
    infile.close()
    return _dict.update(new_dict)

def scan(diction):
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    diction = {}
    shopping = []
    while True:
        success, img = cap.read()
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
        for barcode in decode(img):
            myData = barcode.data.decode('utf-8')
            print(myData)
            shopping.append(myData)
            pts = np.array([barcode.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(img,[pts],True,(255,0,255),5)
            time.sleep(3)
            diction[myData] = shopping.count(myData)
            name_converter(diction)
        cv2.imshow('Result',img)
        cv2.waitKey(1)

    return diction

def name_converter(con_dic):
    for key in con_dic.keys():
        if key == '4088600140872':
            con_dic["Mixed Beans in water(Four Seasons)"] = con_dic.pop('4088600140872')
        if key == '4088600140902':
            con_dic["Chick Peas in water(Four Seasons)"] = con_dic.pop('4088600140902')
        if key == '4088600140865':
            con_dic["Butter Beans in water(Four Seasons)"] = con_dic.pop('4088600140865')
        if key == '4088600247571':
            con_dic["Green Lentils in water(Four Seasons)"] = con_dic.pop('4088600247571')
        if key == '4088600140841':
            con_dic["Red Kidney Beans in water(Four Seasons)"] = con_dic.pop('4088600140841')
    return con_dic

def shop(diction):
    Shop = scan(diction)
    Final_Shop = name_converter(Shop)
    return Final_Shop

def merge(Dict1, Dict2):
    for a in list(Dict1.keys()):
        for b in list(Dict2.keys()):
            if a == b:
                Dict2[b] = Dict1[a] + Dict2[b]
                Dict1.pop(a)
    Dict1.update(Dict2)
    save_inventory(Dict1)
    return Dict1

inventory = {}
open_inventory(inventory)
shopping_list = {}
shopping_list = shop(shopping_list)
inventory = merge(inventory, shopping_list)
shop1 = list(inventory.keys())
shop2 = list(inventory.values())
invent_Dict = {'item': shop1,
               'Amount': shop2}
data = pd.DataFrame(invent_Dict, columns=['item', 'Amount'])
print(data)
