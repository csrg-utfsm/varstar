import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit

def cut(c):
	flag = True
	data = []
	head = []
	patron = re.compile("\s+")
	for i in c:
		if flag == True:
			head.append(patron.split(i))
			flag = False
		else:
			data.append(patron.split(i))
	return np.array(data),head

def parser(data):
	c = []
	alpha = []
	gamma = []
	flag = 0
	flag1 = False
	for i in range(len(data)):
		flag1= re.findall("\# ######### LIGHT ",data[i])
		if flag1:
			data= data[i+1:]
			break
	for i in range(len(data)):
		head = re.findall("\A#\s+(.+)",data[i])
		new_line = re.findall("\A   (.+)",data[i]) 
		ra = re.findall("\#ra=\s+(.+)",data[i])
		dec = re.findall("\#dec=\s+(.+)",data[i])
		#ndataset = re.findall("\#dataset=(.+)",linea)
		if ra:
			ra_aux = ra
		if dec:
			dec_aux = dec
		if head:
			[c.append(j) for j in head]
		if new_line:
			[c.append(k) for k in new_line]
			alpha.append(ra_aux)
			gamma.append(dec_aux)
			try:
				next_line = re.findall("\A   (.+)",data[i+1])
				if not next_line:
					reg, col= cut(c)
					if flag == 0:
						df = pd.DataFrame(reg,columns=col)
						df["RA"] = np.array(alpha)
						df["DEC"] = np.array(gamma)
						c = []
						alpha = []
						gamma = []
						flag += 1                    
					else:
						df_aux = pd.DataFrame(reg,columns=col)
						df_aux["RA"] = np.array(alpha)
						df_aux["DEC"] = np.array(gamma)
						df = pd.concat([df,df_aux],ignore_index=True)
						c = []
						alpha = []
						gamma = []

			except:
				reg, col = cut(c)
				if flag == 0:
					df = pd.DataFrame(reg,columns=col)
					df["RA"] = np.array(alpha)
					df["DEC"] = np.array(gamma)
					c = []
					alpha = []
					gamma = []
					flag += 1   
				else:    
					df_aux = pd.DataFrame(reg,columns=col)
					df_aux["RA"] = np.array(alpha)
					df_aux["DEC"] = np.array(gamma)
					df = pd.concat([df,df_aux],ignore_index=True)

	col[0].remove('GRADE')
	df[col[0]] = df[col[0]].astype(float)

	return df


def outliers_iqr(ys):
	quartile_1, quartile_3 = np.percentile(ys, [25, 75])
	iqr = quartile_3 - quartile_1
	lower_bound = quartile_1 - (iqr*1.5)
	upper_bound = quartile_3 + (iqr*1.5)
	return np.where((ys > upper_bound) | (ys < lower_bound))

def high_photometric_errors(data):
	mer_mean = np.mean(data)
	mer_std = np.std(data)
	error_limit = mer_mean + 3*mer_std
	return np.where((data >= error_limit))


def lineal_fit(t,a,b):
	m = a+b*t
	return m

def parabolic_fit(t,a,b,c):
	m = a + b*t + c*t*t
	return m

def select_aperture(data):
	mean = []
	apertures = ["0","1","2","3","4"]
	for i in apertures:
		m = data["MER_"+i].mean()
		mean.append(m.values[0])
	values = mean.index(min(mean)) 
	return apertures[values]

# funcion que hace todo el preprocesamiento
def preprocessing(data,aperture):
	# 1 - se eliminan las mediciones con alto error fotometrico
	hpe_index = high_photometric_errors(data["MER_"+aperture].values)
	data = data.drop(data.index[hpe_index[0]])
	#2 - se eliminan datos atípicos
	outliers_index = outliers_iqr(data["MAG_"+aperture].values)
	data = data.drop(data.index[outliers_index[0]])
	# Se retornan los dias julianos y la magnitud de la apertura seleccionada
	return data["HJD"].values.ravel(),data["MAG_"+aperture].values.ravel()

# Por ahora fit puede ser lineal o parabolico
def get_statistics(t,y):
	# Desviacion estandar y
	dep = np.std(yy)
	#para fit lineal
	poptl, pcovl = curve_fit(lineal_fit, t, y)
	y_hatl = lineal_fit(t,*poptl)
	perrl = np.sqrt(np.diag(pcovl))
	defl = np.sqrt(np.sum((y_hatl- y)*(y_hatl- y))/len(y))
	q1 = poptl[1]/perrl[1]
	c1 = 1-(defl/dep)
	# Para fit parabolico
	poptp, pcovp = curve_fit(parabolic_fit, t, y)
	y_hatp = parabolic_fit(t,*poptp)
	perrp = np.sqrt(np.diag(pcovp))
	defp = np.sqrt(np.sum((y_hatp- y)*(y_hatp- y))/len(y))
	q2 = poptp[2]/perrp[2]
	c2 = 1-(defp/defl)
	stat = [q1,c1,q2,c2]
	return stat

def get_ra_dec(data):
	ra= data.iloc[0]["RA"].values[0]
	ra= ra.split(" ")
	dec= data.iloc[0]["DEC"].values[0]
	dec= dec.split(" ")
	return ra[0],dec[0]

archivo = open ("../crawler/id_data/000000-4411.0.txt","r")
text = archivo.readlines()
dataset = parser(text)
dataset.head()


archivo.close()
