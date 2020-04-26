import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
######################Importando os dados
local="/home/alexandre/Documentos/Artigo/COVID-19/SIR/Script/painel.xlsx"
dados=pd.read_excel(local)

###############OLS
######Casos
y=dados['Numero de Infectados']
x=np.column_stack((dados['Salário Médio'],dados['População Ocupada'],dados['Aeroporto'],dados['Esgotamento'],dados['Agência BB/Caixa']))


print(res1.params)
print(res1.bse)

OLS1= sm.OLS(y,x, family=sm.families.Binomial())
glm1_res=glm1.fit()


##########Taxa 1
y=dados['Taxa de Transmissão -B1']

res2 = sm.OLS(y,x).fit()
print(res2.params)
print(res2.bse)

glm2= sm.GLM(y,x, family=sm.families.Binomial())
glm2_res=glm2.fit()


###########Taxa 2
y=dados['Taxa de Transmissão -B2']
    
res3 = sm.OLS(y,x).fit()
print(res3.params)
print(res3.bse)
print(res3.summary())

glm3= sm.GLM(y,x, family=sm.families.Binomial())
glm3_res = glm3.fit()


##################################Testes
###########Auto correlação
db1=sm.stats.stattools.durbin_watson(res1.resid)
db2=sm.stats.stattools.durbin_watson(res2.resid)
db3=sm.stats.stattools.durbin_watson(res3.resid)

###########Jarque-Bera
jb1=sm.stats.stattools.jarque_bera(res1.resid)
jb2=sm.stats.stattools.jarque_bera(res2.resid)
jb3=sm.stats.stattools.jarque_bera(res3.resid)
jb4=sm.stats.stattools.jarque_bera(glm2_res.resid_anscombe)
jb5=sm.stats.stattools.jarque_bera(glm3_res.resid_anscombe)
###########Breuch-Godfrey
bg1=sm.stats.diagnostic.acorr_breusch_godfrey(res1)
bg2=sm.stats.diagnostic.acorr_breusch_godfrey(res2)
bg3=sm.stats.diagnostic.acorr_breusch_godfrey(res3)
#bg4=sm.stats.diagnostic.acorr_breusch_godfrey(glm2)
#bg5=sm.stats.diagnostic.acorr_breusch_godfrey(glm3)
###########Breuch-Pagan

bp1=sm.stats.diagnostic.het_breuschpagan(res1.resid,res1.model.exog)
bp2=sm.stats.diagnostic.het_breuschpagan(res2.resid,res2.model.exog)
#bp3=sm.stats.diagnostic.het_breuschpagan(glm3_res,glm3_res.model.exog)
###########White
#wh1=sm.stats.diagnostic.het_white(res1.resid,res1.model.exog)
#wh2=sm.stats.diagnostic.het_white(res2.resid,res2.model.exog)
#wh3=sm.stats.diagnostic.het_
#white(res3.resid,res3.model.exog)
##########Linearidade
ln1=sm.stats.diagnostic.linear_reset(res1, power=3, test_type='fitted', use_f=False, cov_type='nonrobust', cov_kwargs=None)
ln2=sm.stats.diagnostic.linear_reset(res2, power=3, test_type='fitted', use_f=False, cov_type='nonrobust', cov_kwargs=None)
ln3=sm.stats.diagnostic.linear_reset(res3, power=3, test_type='fitted', use_f=False, cov_type='nonrobust', cov_kwargs=None)



#####################Corrigindo a autocorrelação


x = sm.add_constant(x)
y1=dados['Taxa de Transmissão -B1']
y2=dados['Taxa de Transmissão -B2']
wls_model = sm.WLS(y1,x, weights=list(range(1,99)))
results = wls_model.fit()

wls_model2=sm.WLS(y2,x,weights=list(range(1,99)))
results2=wls_model2.fit()


###############Testes
###########Heterogeneidade

bp1=sm.stats.diagnostic.het_breuschpagan(results.resid,results.model.exog)
bp2=sm.stats.diagnostic.het_breuschpagan(results2.resid,results2.model.exog)

#############
bg1=sm.stats.diagnostic.acorr_breusch_godfrey(results)
bg1=sm.stats.diagnostic.acorr_breusch_godfrey(results2)
