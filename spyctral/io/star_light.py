import re
import pandas as pd
import numpy as np
from spyctral import core
from astropy.table import QTable
import astropy.units as u

SL_GET_TITLE_VALUE = re.compile(r"\[")
SL_REPLACE_AND = re.compile(r"&")
SL_GET_MULTIPLE_VALUES = re.compile(r',')
SL_GET_DATE = re.compile(r'\b\d{2}/[a-zA-Z]{3}/\d{4}\b')
PATRON = re.compile(r'#(.*?)(?:(?=\n)|$)')

def read_star_light(path):
    with open(path) as starfile:
        summary_dict = {}
        blocks = []
        tab = []
        block_titles=[]
        for d ,starline in enumerate(starfile):
            # Gets all the lines that contains '[' that means: all the summarized information.
            if re.findall(SL_GET_TITLE_VALUE, starline) :
                #Cleaning of the string.
                if re.findall(SL_GET_DATE,starline):
                    summary_dict['Date']  = re.findall(SL_GET_DATE,starline)[0]
                starline = re.sub(r'\s{2,}',' ',starline.replace("&", ',').replace(']\n','')).replace('/','_')

                #Handles string with multiple values on the same line.
                if  re.findall(SL_GET_MULTIPLE_VALUES, starline) :
                    starline_list = starline.split('[')
                    try:
                        temp_dict = dict(zip(starline_list[1].strip().replace(' ','').split(','),float(starline_list[0].strip().split(' '))))
                    except:
                        temp_dict = dict(zip(starline_list[1].strip().replace(' ','').split(','),starline_list[0].strip().split(' ')))
                    summary_dict = { **summary_dict, **temp_dict}

                #Handles string with SN titles that repeats and overlaps if not handled.
                elif re.findall(r'\[S_N', starline): 
                    starline_list = starline.split('[')
                    try:
                        summary_dict[starline_list[1].split(' ')[0]+str(d)] = float(starline_list[0])
                    except:
                        summary_dict[starline_list[1].split(' ')[0]+str(d)] = starline_list[0]

                ##Adds all the other normal values that do not contain any exeption 
                else:
                    starline_list= starline.replace('-','_').replace('#','').split('[')
                    try:
                        summary_dict[starline_list[1].split(' ')[0]] = float(starline_list[0].strip())
                    except:
                        summary_dict[starline_list[1].split(' ')[0]] = starline_list[0].strip()

            ## This part procces the tables 
            if re.search(SL_GET_TITLE_VALUE, starline) is None and re.match('##', starline) is None  :
               starline = starline.replace('\n','')
               # Filters the titles of the tables 
               if re.search(r'# ', starline):
                   block_titles.append(starline) 
               # Filters the empty spaces 
               elif  starline != '':
                    starline= re.sub('\s{2,}',' ',starline.strip())
                    tab.append(starline.split(' '))
                # Generates a block for each empty line that founds and if the block is larger it appends it 
               else:
                    if len(tab)>1:
                        blocks.append(tab)
                        tab=[]

        blocks.append(tab)
        tab=[]
    first_title = re.sub('\s{2,}',' ',block_titles[0][1:]).replace('.','').replace('?','').strip()
    spectra_dict = {
        "synthetic_spectrum": QTable(
            rows=blocks[4], names=["l_obs", "f_obs", "f_syn", "weights"]
        ),
        "synt_results": QTable(rows=blocks[0],names= first_title.split(' ')),
        "qtable_1": QTable(rows=blocks[1]),
        "qtable_2": QTable(rows=blocks[2]),
        "qtable_3": QTable(
            rows=np.array(blocks[3]).T[1:],
            names=np.array(blocks[3]).T[0],
        ),
    }

    return summary_dict, spectra_dict

