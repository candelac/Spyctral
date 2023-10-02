import pandas as pd 
import re


def get_data_starligth(path: str):
    f = open(path, 'r')
    l_obs = list()
    f_obs = list()
    f_syn = list()
    wei = list()
    count = 0
    for lines in f.readlines():
        if (re.search('Best Model', lines)) is not None:   #hace que comience a leer desde best model 
            count = count + 1
        if (count >= 1):

            if(re.search('[Nl_obs]', lines)) is not None:  # tiene una segunda linea que especifica el numero total de obs esto hace que la saltee

                count = count + 1
            else:
                if (count >= 2):
                    count = count + 1
                    listline = re.findall('\d+.\d+\w', lines)
                    l_obs.append(float(listline[0]))
                    f_obs.append(float(listline[1]))
                    f_syn.append(float(listline[2]))
                    wei .append(float(listline[3]))


    data= pd.DataFrame([l_obs, f_obs, f_syn, wei], index = ['l_obs', 'f_obs', 'f_syn', 'wei']).T
    return data