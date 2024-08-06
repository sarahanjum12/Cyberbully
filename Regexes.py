# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 05:51:37 2024

@author: prath
"""

from models import ToxicRemover, ToxicRemoverList
import re

with open("html.txt", "r") as f:
    A = f.read()

A = A.replace("\n", "")

def RegexHero(text):
    patt = "(<p>|<p .*?>)(.*?)(<\/p>)"
    Final = ""
    Match = re.split(patt, text)
    y = re.split(patt, text)
    
    if(len(Match) < 2):
        return text
    
    SplitScreen = []
    i = 2
    while(i < len(Match)-1):
        SplitScreen.append(Match[i])
        i+=4
    print(SplitScreen)
    SplitScreen = ToxicRemoverList(SplitScreen)
    print(SplitScreen)
    
    i = 2
    while(i < len(Match)-1):
        if(len(SplitScreen) == 0):
            break
        Match[i] = SplitScreen[0]
        SplitScreen = SplitScreen[1:]
        i+=4
        
    for m in Match:
        Final += m
    return Final
    
    
    