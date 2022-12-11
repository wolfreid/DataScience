import matplotlib.pyplot as plt
import random
import statsmodels.api as sm
import seaborn as sns
import stat_scores as stcores
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from numpy import inf


def single_linear_regression (data,X_train, Y_train,save,separate =False):
    alpha = 0.05
    section_name = "./redesign_results/single_linear_regression/unweighted"
    name_single = "OLS-single"
    name_multiple = "OLS-multivar"
    
    params = {}; summaries = {};results = {}
    predictions_arr = {}
    data =data 
    X_train= X_train.drop(columns = {'const'})
    n = X_train.columns.size

    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                for i in range(n)]
    plt.figure(figsize=(10, 10), dpi=80)
    length = 0
    while n-length !=0:
        x = X_train[X_train.columns[length]]
        y = Y_train

        model = sm.OLS.from_formula('{} ~ {}'.format(y.name,x.name),data )
        result = model.fit()
        predictions = result.get_prediction(X_train).summary_frame(alpha)
        param = result.params
        summary = result.summary()
        f, ax = plt.subplots()
        # ax.set_xlim(0-100, max(x[x.notna()]+100))
        if separate:
            sns.regplot(x = x.name,y = y.name,data = data)
        else:
            plt.scatter(x,y,c=color[length],label =x.name,marker='x' )
            plt.plot(x,result.predict(x))
        f.tight_layout()
        if separate:
            sign = '+' if result.params[0] > 0 else '-'
            plt.text(0.55, 0.15, '$y = %.2f x_1 %s %.2f $' % (result.params[1],sign, abs(result.params[0])), fontsize=17, transform=ax.transAxes)
            plt.xlabel(x.name)
            plt.ylabel(y.name)
            plt.title(x.name+ "~"+ y.name, fontsize=15)
            plt.legend(loc='upper right')
            plt.savefig("./"+section_name +"/"+ name_single + "_"+x.name+ "_"+ y.name +"."+save)
            plt.show()
            plt.clf()    
        length+=1
        params.update({x.name:param})
        summaries.update({x.name:summary})
        results.update({x.name:result})
        predictions = x.reset_index().join(predictions).join(y.reset_index(drop = True))
        predictions_arr.update({x.name:predictions})
    else:
        if not separate:
            plt.xlabel(x.columns.to_list().join("+"), fontsize=14)
            plt.ylabel(y.name, fontsize=14)
            plt.legend(loc='upper right')
            plt.savefig("./"+section_name +"/"+ name_multiple +"."+save)
            plt.show()
            plt.clf()
    return params,summaries,result,predictions_arr

def single_linear_compare_regr(X_train, Y_train,sample_w,save): 
    section_name = "./redesign_results/single_linear_regression/weighted"
    name_single = "OLS-single"
    for col in X_train.columns[1:]:
        x = np.array(X_train[col].fillna(0)).reshape(-1,1)
        y = np.array(X_train.fillna(0)).reshape(-1,1)
        s_w = np.array(sample_w[col].fillna(0))
        # The weighted model
        regr = LinearRegression()
        result_w = regr.fit(x,y ,s_w )
        plt.plot(x, result_w.predict(x), color='green', linewidth=4, label='Weighted model')

        # The unweighted model 
        regr = LinearRegression()
        result_unw = regr.fit(x, y)
        plt.plot(x, result_unw.predict(x), color='red', linewidth=3, label='UnWeighted model', linestyle='dashed')
        plt.xticks(());plt.yticks(())
        plt.scatter(X_train[col], Y_train, c='grey', edgecolor='black')
        plt.legend(title = 'col')
        plt.savefig("./"+section_name +"/"+ name_single +".", save)
        plt.show()        
        plt.clf()
        
def multiple_linear_regression(_dm,X_train, Y_train,func,weights = None, weighting = False,simple_WLS = True,hasconst = False):
    alpha = 0.05
    x = X_train
    y = Y_train
    data =X_train.join(Y_train)
    if func =='WLS':
        if simple_WLS:
            result = sm.WLS(y,x,weights = weights,missing='drop').fit()
        else:
            temp_result = sm.OLS(y,x,missing='drop').fit()
            wt = 1/sm.OLS.from_formula('temp_result.resid.abs() ~ temp_result.fittedvalues', data=data).fit().fittedvalues**2
            result = sm.WLS(y,x,weights = wt,hasconst = hasconst).fit()
    elif func == 'OLS':
        if weighting:
            result = sm.OLS(y,x,weights).fit()
        else:
            result = sm.OLS(y,x).fit()
    predictions = result.get_prediction(x).summary_frame(alpha)
    predictions = _dm.join(predictions)
    summary = result.summary()
    param = result.params
    return param,summary,result,predictions

def MakeNormalizeALL(x,y,projects,save,show,method):
    for project in projects:
        MakeNormalize(x[project],y,save,show = show,method = method)
    return 0

def MakeNormalize(pred,resp,save,show,method ="scaler"):
    section_name = "./redesign_results/"
    y = resp
    x = pred.copy()
    nrm =  stcores.Normalization()
    matrix_x = []

    if method in ['all','sknormalize','scaler']:
        if len(x.shape)==1:
            columns = [x.name]
            x = x.dropna()
            index = x.index 
            x= x.to_numpy().reshape(-1, 1)
        else:
            columns = x.columns
            index = x.index     
        if  method=='all':    
            x_norm = nrm.normalize(x = x,columns = columns,index = index)
            x_scaler = nrm.scaler(x = x,columns = columns,index = index)
            matrix_x= [x,x_norm,x_scaler]
        elif method == 'sknormalize':
            x_norm = nrm.normalize(x = x,columns = columns,index = index)
            x = x_norm
        elif method =='scaler':
            x_scaler = nrm.scaler(x = x,columns = columns,index = index)
            x = x_scaler
    if show in ['all','one'] :
        if show == 'one':      
            y = pd.concat([x,y],join='inner',axis= 1)['economy']             
            ShowNormalize(x,y,'png',method = method )
            return x 
        elif show == 'all':
            name = 'compare_scaling'
            fig = plt.figure(figsize=(12,8),dpi=80)
            fig.subplots_adjust(hspace=0.5)
            for i in  list(range(1,4)):
                ax = plt.subplot(1,3,i)
                ax.scatter(matrix_x[i-1],y, marker='*')
                ax.legend()
            plt.savefig("./"+section_name +"/"+ name +"." + save)
            plt.show()
            
            return {'scaler':x_scaler,'sknormalize':x_norm,'standart':x}
    else:
        if  method in ['scaler','sknormalize','none']:
            return x
        else:
            return {'scaler':x_scaler,'sknormalize':x_norm,'standart':pred}

def ShowNormalize(x,y,save,method ="scaler"):
    if type(x) == pd.Series:
        name = "_".join(["Normalize",method,x.name])
    else:
        name = "_".join(["Normalize",method,x.columns[0]])    
    section_name = "./redesign_results/"
    plt.scatter(x,y, marker='*')
    plt.savefig("./"+section_name +"/"+ name +"." + save)
    plt.show()
    plt.clf

def WLS_weight_func(sample,operation = "mean",pow_ =1):
    sample['product'] = sample.apply(operation,axis = 1,skipna = True )**pow_
    a = pd.DataFrame((sample['product']))
    a.loc[a['product'] == inf,'product'] = 1
    return a


def ProcModel(table,column_x,column_y,prefix_y, get = None):
    response = [col for col in table.columns if prefix_y in col]
    pred_columns = column_x
    resp_columns = response
    data_model = table[pred_columns+resp_columns]
    data_model_pred,data_model_resp = data_model[pred_columns],data_model[resp_columns]
    pred =  data_model_pred
    resp = data_model_resp[column_y]
    resp = resp.rename("economy")
    if get == None:
        return
    elif get =='pred':
        return pred
    elif get == 'resp':
        return resp
    else:
        return pred.join(resp)

    