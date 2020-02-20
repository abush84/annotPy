#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 11:52:56 2020

@author: ao622
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Annotate.py module of WarblePy. 

This module provides functions to work with annotation tables. 

@author: Alan Bush
"""

#cargo paquetes estandar
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import os.path
import math
import collections
import warnings
import pdb

class Error(Exception): pass


# def consolidate(annot_db,when,additive='all'):
#     """
#     Consolidate annotation rows. Combines together contiguous annotation rows of a record when a criteria is met.
    
#     annot_db - pandas DataFrame with required columns 
#     when - str or callable
#         criteria to define when to consolidate two or more annotations
#         The criteria should evaluate to True or False on the candidate consolidated annotation row
#         if callable, should accept a pandas.Series and return a boolean
#         if str, should be a condition that evaluates to True or False when evaluated on a pandas.Series. 
#     additive - list of str or 'all'
#         indicates which variables should be treated as 'additive'.
#         If 'all', all the variables not required will be treated as additive
        
#     returns a pandas DataFrame with columns 'record_id', 'annot_id', 'start', 'end', 
#         'comment', 'duration', 'consolidated_duration', the additive variables and all other varibles 
#         unmodified with respect to the seed row. 
#     """
#     cols=['record_id','annot_id','start','end','comment','duration','datetime']

#     if set(['start','end']).issubset(annot_db.columns.values) and 'duration' not in annot_db.columns.values:
#         annot_db['duration']=annot_db.end-annot_db.start
#     if not set(cols).issubset(annot_db.columns.values):
#         raise Error("Columns 'record_id', 'annot_id', 'start', 'end', 'comment', 'duration' and 'datetime' required in annot_db")
#     if str(additive).lower()=='all':
#         additive=list(set(annot_db.columns.values).difference(cols))
#     if not isinstance(additive,collections.Iterable):
#         raise Error("additive should be a list or 'all'")
#     if isinstance(when,str): #when='(c_duration/duration)>0.5'
#         when_f = lambda s: eval(when,dict(s))
#     else:
#         when_f = when

#     annot_db[['record_id','annot_id']] = annot_db[['record_id','annot_id']].astype(np.int64)
#     annot_db.set_index(['record_id','annot_id'],drop=False,inplace=True,verify_integrity=True)

#     def consolidate_record(annot_db):
#         cons_db = pd.DataFrame()         
#         annot_db=annot_db.copy()
#         annot_db.sort_values('start',inplace=True) 
#         i=0; j=1;
#         while i < len(annot_db)-1:
#             if j==1:
#                 curr_s=annot_db.iloc[i].copy()
#                 curr_s['consolidated_duration']=curr_s.duration
#                 merge_s=annot_db.iloc[i].copy()
#             merge_s.end=annot_db.iloc[i+j].end
#             merge_s.duration=merge_s.end-merge_s.start
#             merge_s['consolidated_duration']=curr_s.consolidated_duration+annot_db.iloc[i+j].duration
#             merge_s.comment=curr_s.comment+annot_db.iloc[i+j].comment
#             merge_s.datetime=curr_s.datetime

#             for var in additive:
#                 #var='vS_energy'
#                 merge_s[var]=curr_s[var]+annot_db.iloc[i+j][var]
#             if when_f(merge_s):
#                 curr_s = merge_s.copy()
#                 j+=1
#                 if i + j >= len(annot_db):
#                     cons_db=cons_db.append(curr_s.copy())
#                     i=len(annot_db)
#             else:
#                 cons_db=cons_db.append(curr_s.copy())
#                 i+=j
#                 j=1
#                 if i + 1 == len(annot_db): #adding last register
#                     curr_s=annot_db.iloc[i].copy()
#                     curr_s['consolidated_duration']=curr_s.duration
#                     cons_db=cons_db.append(curr_s.copy())
#         return cons_db
        
#     cons_db=annot_db.groupby('record_id').apply(consolidate_record)

#     cols.append('consolidated_duration')
#     cols += [c for c in annot_db.columns.values if c not in cols]
#     cons_db=cons_db.reindex(cols,axis=1)
#     cons_db[['record_id','annot_id']] = cons_db[['record_id','annot_id']].astype(np.int64)
#     cons_db.set_index(['record_id','annot_id'],drop=False,inplace=True,verify_integrity=True)
   
#     return cons_db

    
# def difference(x,y):
#     """
#     Calculates the difference between annotations DataFrames
    
#     x - Pandas DataFrame
#     y - Pandas DataFrame
    
#     x and y should have columns 'record_id','annot_id','start' and 'end'.
    
#     returns a pandas data with annotations corresponding to the difference of 
#     annotations on x and y (x-y)
#     """
#     #rid=20170323183253
#     #x=w.annot['QC']
#     #y=w.annot['sound1']
#     cols=['record_id','annot_id','start','end']

#     if hasattr(x, 'name'):
#         x_name=x.name
#     else:
#         x_name='x'

#     if not set(cols).issubset(x.columns.values):
#         raise Error("Columns '"+"', '".join(cols)+"' required in x DataFrame")
#     if not set(cols).issubset(y.columns.values):
#         raise Error("Columns '"+"', '".join(cols)+"' required in y DataFrame")
        
#     annot_db=pd.DataFrame(columns=cols + ["x_id"])
#     for rid in x.record_id:
#         if rid in set(y.record_id):
#             annot_rec=_difference_(x.ix[rid].copy(),y.ix[rid].copy())
#             annot_rec.insert(0,'record_id',int(rid))
#             annot_db=annot_db.append(annot_rec, ignore_index=True, verify_integrity=True)    
#         else:
#             annot_rec=x.ix[rid,cols].copy()
#             annot_rec["x_id"]=annot_rec.annot_id
#             annot_db=annot_db.append(annot_rec, ignore_index=True, verify_integrity=True)  
            
#     annot_db["x_id"] = annot_db["x_id"].astype(int)
#     annot_db.rename(index=str, columns={"x_id": x_name + "_annot_id"},inplace=True)
#     annot_db[['record_id','annot_id']] = annot_db[['record_id','annot_id']].astype(np.int64)    

#     annot_db.sort_values(['record_id','start'],inplace=True) 
#     annot_db.set_index(['record_id','annot_id'],drop=False,inplace=True,verify_integrity=True)
#     return annot_db
    
# def _difference_(x,y):
#     #x=w.annot['QC'].query("record_id==20170412113127")    
#     #y=w.annot['sound1'].query("record_id==20170412113127")
#     #x,y=(x.ix[rid],y.ix[rid])  
#     i=0
#     j=0
#     annot_db = pd.DataFrame(columns=['start','end','x_id']) 
#     while i<len(x) and j<len(y):
#         x_start=x.start.iloc[i] 
#         x_end=x.end.iloc[i]
#         x_id=int(x.annot_id.iloc[i]) 
#         y_start=y.start.iloc[j]
#         y_end=y.end.iloc[j]
#         if y_start <= x_start < x_end <= y_end:
#             #     xxxxxxxxxxxx
#             #  yyyyyyyyyyyyyyyyyy
#             i+=1
            
#         elif x_start < y_start < y_end < x_end:
#             #     xxxxxxxxxxxx
#             #        yyyyy  
#             annot_db.loc[len(annot_db)]=[x_start,y_start,x_id]
#             x.set_value(x.index[i],'start',y_end)
#             j+=1

#         elif x_start < y_start < x_end <= y_end:
#             #     xxxxxxxxxxxx
#             #         yyyyyyyyyyyy
#             annot_db.loc[len(annot_db)]=[x_start,y_start,x_id]
#             i+=1
            
#         elif y_start <= x_start < y_end < x_end:
#             #     xxxxxxxxxxxx
#             # yyyyyyyyy
#             x.set_value(x.index[i],'start',y_end)
#             j+=1
        
#         elif x_end <= y_start:    
#             #    xxxxxxxxxxxxx
#             #                    yyyyyyyy
#             annot_db.loc[len(annot_db)]=[x_start,x_end,x_id]     
#             i+=1
            
#         elif y_end <= x_start:   
#             #       xxxxxxxxxxx
#             # yyyy   
#             j+=1
#             # if last row in y, x should be added to result
            
#         else:
#             raise Error("Should never get here")
   
#     while i<len(x):
#         annot_db.loc[len(annot_db)]=[x.start.iloc[i],x.end.iloc[i],int(x.annot_id.iloc[i])]
#         i+=1             
                     
#     annot_db.sort_values(by='start',ascending=True,inplace=True)
#     annot_db.insert(0,'annot_id',np.arange(len(annot_db)))         
#     return annot_db    
    
    
    
def intersect(x,y):
    """
    Intersects annotations DataFrames
    
    x - Pandas DataFrame
    y - Pandas DataFrame
    
    x and y should have columns 'id','starts' and 'ends'.
    If x and y have 'name' attributes, these are used to define the x/y_id column name
    
    returns a pandas dataframe with annotations corresponding to the intersection of 
    annotations on x and y
    """
    
    cols=['id','starts','ends']

    if isinstance(x, pd.Series):
        x = x.to_frame(0).T

    if isinstance(y, pd.Series):
        y = x.to_frame(0).T

    if not set(cols).issubset(x.columns.values):
        raise Error("Columns '"+"', '".join(cols)+"' required in x DataFrame")
    if not set(cols).issubset(y.columns.values):
        raise Error("Columns '"+"', '".join(cols)+"' required in y DataFrame")
        
    if hasattr(x, 'name') and type(x.name) is str:
        x_name=x.name
    else:
        x_name='x'
        
    if hasattr(y, 'name') and type(y.name) is str:
        y_name=y.name
    else:
        y_name='y'

    i=0
    j=0
    annot_db = pd.DataFrame(columns=['starts','ends','x_id','y_id']) 
    while i<len(x) and j<len(y):
        if x.starts.iloc[i]<y.ends.iloc[j] and x.ends.iloc[i]>y.starts.iloc[j]:
            annot_db.loc[len(annot_db)]=[\
                max(x.starts.iloc[i],y.starts.iloc[j]),\
                min(x.ends.iloc[i],y.ends.iloc[j]),\
                int(x.id.iloc[i]),\
                int(y.id.iloc[j])]
            if x.ends.iloc[i]<y.ends.iloc[j] or j+1==len(y):
                i+=1
                j=0
            else:
                j+=1
        elif x.ends.iloc[i] <= y.starts.iloc[j] or j+1==len(y):
            i+=1
            j=0
        elif x.starts.iloc[i] >= y.ends.iloc[j]:
            j+=1
        else:
            raise Error("unsorted input DataFrames")

    #pdb.set_trace()
    
    annot_db.sort_values(by='starts',ascending=True,inplace=True)
    annot_db.insert(0,'id',np.arange(len(annot_db)))         

    annot_db[["x_id","y_id"]] = annot_db[["x_id","y_id"]].astype(int)
    annot_db.rename(columns={"x_id": x_name + "_id", "y_id": y_name + "_id"},inplace=True)
    annot_db[['id']] = annot_db[['id']].astype(int)
    
    annot_db.sort_values(['id','starts'],inplace=True) 
    annot_db.set_index(['id'],drop=False,inplace=True,verify_integrity=True)
    return annot_db
    


