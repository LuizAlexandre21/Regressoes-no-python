import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


####################Funções
########## Sequencia de floats
def seq(start, stop, step=1):
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([start + step*i for i in range(n+1)])
    elif n == 1:
        return("{:.2f}".format([start]))
    else:
        return([])
###########Derivação
def deriv(y,t,N,beta,gamma):
    S,I,R=y
    dSdt=-beta*S*I/N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt
##########Beta-Met-1
def beta_1(In,I,S,T,N):
    betas=-np.log(1-In/I)/((T*S)/N)
    return(betas)

##########Beta-Met-2
def beta_2(In,I,S,T,N):
    betas=(1/T)*np.log(1-In*((1/I)+(1/S)))
    return(betas)
##########Beta-Poisson-1
def beta_poisson(In,S,I,N):
    betas=np.log(In)-np.log((S*I)/N)
    return(betas)

###################Importando os dados
local="/home/alexandre/Documentos/Artigo/COVID-19/SIR/saida.csv"
data=pd.read_csv(local)
Capitais=['Rio Branco/AC','Maceió/AL','Macapá/AP','Manaus/AM','Salvador/BA','Fortaleza/CE','Vitória/ES','Goiânia/GO','São Luís/MA','Cuiabá/MT','Campo Grande/MS','Belo Horizonte/MG','Belém/PA','João Pessoa/PB','Curitiba/PR','Recife/PE','Teresina/PI','Rio de Janeiro/RJ','Natal/RN','Porto Alegre/RS','Porto Velho/RO','Boa Vista/RR','Florianópolis/SC','São Paulo/SP','Aracaju/SE','Palmas/TO','Brasília/DF','Guarulhos/SP','Campinas/SP','São Gonçalo/RJ','Duque de Caxias/RJ','São Bernardo do Campo/SP','Nova Iguaçu/RJ','São José dos Campos/SP','Santo André/SP','Ribeirão Preto/SP','Jaboatão dos Guararapes/PE','Osasco/SP','Uberlândia/MG','Contagem/MG','Feira de Santana/BA','Joinville/SC','Aparecida de Goiânia/GO','Londrina/PR','Juiz de Fora/MG','Ananindeua/PA','Serra/ES','Niterói/RJ','Belford Roxo/RJ','Caxias do Sul/RS','Campos dos Goytacazes/RJ','Mauá/SP','São João de Meriti/RJ','São José do Rio Preto/SP','Mogi das Cruzes/SP','Betim/MG','Santos/SP','Diadema/SP','Maringá/PR','Jundiaí/SP','Campina Grande/PB','Montes Claros/MG','Piracicaba/SP','Carapicuíba/SP','Olinda/PE','Anápolis/GO','Cariacica/ES','Bauru/SP','Itaquaquecetuba/SP','São Vicente/SP','Caucaia/CE','Caruaru/PE','Blumenau/SC','Franca/SP','Ponta Grossa/PR','Petrolina/PE','Canoas/RS','Pelotas/RS','Vitória da Conquista/BA','Ribeirão das Neves/MG','Uberaba/MG','Paulista/PE','Cascavel/PR','Praia Grande/SP','São José dos Pinhais/PR','Guarujá/SP','Taubaté/SP','Petrópolis/RJ','Limeira/SP','Santarém/PA','Camaçari/BA','Suzano/SP','Mossoró/RN','Taboão da Serra/SP','Várzea Grande/MT','Sumaré/SP','Santa Maria/RS','Gravataí/RS']
Populações=[407319,1018948,503327,2182763,2872347,2669342,362097,1516113,1101884,612547,895982,2512070,1492745,809015,1993105,1645727,864845,6718903,884122,1483771,529544,399213,500973,12252023,657013,299127,3015268,1379182,1204073,1084839,919596,838936,821128,721944,718773,703293,702298,698418,691305,679378,663855,614872,590466,578179,569733,568873,530598,517510,513584,510906,510906,507548,472912,472406,460671,445842,439340,433311,423884,423666,418962,409731,409341,404142,400927,392482,386923,381285,376818,370821,365798,361400,361118,357199,353187,351736,349145,346616,342405,341597,334858,333783,331774,328454,325073,323340,320459,314924,306191,306114,304589,299132,297637,297378,289664,284971,282441,282123,281519]

################Calculando as taxas de transmissão

##############Beta 1
Beta_1=[]
Beta_2=[]
Beta_p=[]
k=0
for i in Capitais:
    capital=data[data["city"]==i]['newCases']
    cum_capital=np.cumsum(capital)
    cum_capital.reindex(range(0,len(cum_capital)))
    N=Populações[k]
    T0=range(0,len(capital))
    list_1=[]
    list_2=[]
    list_p=[]
    for j in range(0,len(capital)):
        if j!=0:
            I=cum_capital.iloc[j]
            IN=capital.iloc[j]
            T=j
            S=N-IN
            betas_1=beta_1(IN,I,S,T,N)
            betas_2=beta_2(IN,I,S,T,N)
            betas_p=beta_poisson(IN,S,I,N)
            list_1.append(betas_1)
            list_2.append(betas_2)
            list_p.append(betas_p)

    Beta_1.append(list_1)
    Beta_2.append(list_2)
    Beta_p.append(list_p)
    k=k+1
    print(i)

##################Media
media=[]
var=[]
for i in Beta_1:
    mean=np.mean(i)
    media.append(mean)
    vari=np.std(i)
    var.append(vari)

media1=[]
var=[]
for i in Beta_2:
    mean=np.mean(i)
    media1.append(np.abs(mean))

    
#################Criando graficos
k=0
capital=range(0,len(Capitais))
for i in Beta_1:
    plt.plot(i)
    a=capital[k]
    plt.title(Capitais[k])
    plt.savefig(str(a)+'.png')
    plt.clf()
    k=k+1
    
