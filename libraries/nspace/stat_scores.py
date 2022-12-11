import pandas as pd
import numpy as np
import statistics as stat
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.preprocessing import StandardScaler,normalize

class Normalization():
    @classmethod
    def normalize(cls,x,columns,index):
        x_norm = normalize(x)
        x_norm = pd.DataFrame(x_norm,columns = columns,index = index) 
        return x_norm
    @classmethod    
    def scaler(cls,x,columns,index):
        scaler = StandardScaler().fit(x)
        x_scaler = scaler.fit_transform(x)
        
        x_scaler = pd.DataFrame(x_scaler,columns = columns,index = index) 
        return x_scaler
        
class RegressionAnalysis():
    
    def __init__(self,x,y,y_pred,ddof) -> None:
        self.x = x
        self.y = y
        self.n =len(self.x)
        self.ddof =ddof 
        self.y_pred = y_pred
        self.residuals = self.y -self.y_pred
        self.std_error = np.sqrt(self.MSE(self.ddof))
    def t_analysis(self,p,n,ddof= 2):
        x = self.x
        y = self.y
        correlation = x.corr()
        t_score = self.t_score_slope(x,correlation)
        t_inter = self.t_score_intercept()
        delta_a =self.delta_a_calc() 
        delta_b = self.delta_b_calc()
        delta_y = self.delta_y_calc()
        t_crit = stats.t.ppf(p,df=n - ddof)
        f_crit= stats.f.ppf(p,df=n - ddof)
        return t_score,t_inter,delta_a,delta_b,delta_y,t_crit,f_crit
    
    
    def MSE(self,ddof = 2):
        squared_error = (self.y_pred - self.y) ** 2
        sum_squared_error = np.sum(squared_error)
        mse = sum_squared_error / self.y.size - ddof
        return(mse)


    def t_score_slope (self,corr = None,n = None,slope = None, MSE = None, method = "corr"):
        if method == "corr":
            return corr* ((n-2)**0.5)/(1-corr)**0.5
        else:
            return slope/(MSE**0.5)/ np.sum((self.x - np.mean(self.x))**2)**0.5
    
    def t_score_intercept(self,a,b,t_score,var,mean):
        return a/b*(t_score/((var**2) +mean**2 ))
    
    def delta_b_calc(self,MSE,t,n):
        return t*(MSE**0.5)*(np.sum(self.x**2)/n*(np.sum((self.x - np.mean(x))**2)))**0.5
    
    def delta_a_calc(self,t,MSE):
        return t* (MSE **0.5)

    def delta_y_calc(self,n,t,MSE):
        return t *((MSE**0.5)/(n**0.5))*(np.sum(self.x**2)/(n*np.sum(self.x**2)-(np.sum(self.x)**2)))**0.5
    
   
    def normality_test(self,res,y,x):
        plt.hist(x)
        plt.hist(y)
        # Check normality assumption
        plt.hist(self.residuals)
        # Check homoscedaticite assumption
        plt.scatter(self.y_pred,self.residuals)
        plt.show()
        plt.clf()


    def variance_validation(self,data_role,column=None):
        df = self.x if data_role =='predictor'else self.y
        if column is not None:
            series = df[column]
            df =series
        variance_coeff = stats.variation(df,axs=1,ddof=1)
        if type(df) == pd.Series:
            df= pd.DataFrame(df,columns = df.name,index = df.index)
        for col in df.columns:
            col_zscore = col + "_zscore"
            df[col_zscore] = (df[col] - df[col].mean())/df[col].std(ddof=0)
            series_outlier =(abs(df["Data_zscore"]) > 3).astype(int) 
            df[col + "_outlier"] = series_outlier
        return df 
    def custom_prediction(self):
        y_min = np.mean(self.y)-(self.std_error*stats.t.ppf(1-.05/2, df = self.n-self.ddof-1))
        y_max = np.mean(self.y)+(self.std_error*stats.t.ppf(1-.05/2, df = self.n-self.ddof-1))
        return y_min,y_max

        
            
            

