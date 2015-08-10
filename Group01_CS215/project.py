import csv
import os
import re
from copy import deepcopy

country_array = []
attribute_array_main = []
e = 2.718
cn = dict()
cc = dict()
p = dict()

key_words = ["land_area","investment_FDI_investments_foreign_","export_exports_trade","electricity_energy_power","co2_carbon","petroleum_diesel_fuel","inflation_hike_cpi","internet_surfing_web_www","gdp_income_gross","expectancy_mortality_infant_newborn_deaths","population_people_inhabitants_citizens_citizen"]
threshold = 0.01
entries = set()

class Attribute:	
	def __init__(self,keywords,desc,code,units):
		self.code = code
		self.keywords = []
		self.keywords = keywords
		self.desc = desc
		self.units = units
		self.values = []
		self.years = []
		self.expect = 0
		self.var = 0
		self.w0 = 0
		self.w1 = 0
	
class Country:
	def __init__(self,code,name):
		self.attribute_array = []
		self.code=code
		self.name_array = []
		self.name_array.append(name)

	def addCountry(self,name):
		self.name_array.append(name)

	def addAttribute(self):
		for i in range(len(attribute_array_main)):
			self.attribute_array.append(deepcopy(attribute_array_main[i]))

	def regression(self):
		for j in self.attribute_array:
			for i in range(len(j.values)):
				j.years.append(1900 + (2010-1900)*i/len(j.values) )
			num=0; den=0;
			for i in range(len(j.values)):
				num=num + (float(j.values[i])-float(j.expect))*( float(j.years[i])-1955)
				den=den + ( float(j.years[i])-1955)*( float(j.years[i])-1955) 
				j.var = j.var + (float(j.values[i])-float(j.expect))*(float(j.values[i])-float(j.expect))
			if(len(j.values) != 0):
				j.var = j.var / len(j.values)
			if(den !=0):
				j.w1 = float(num/den)
				j.w0 = float(j.expect) - float(j.w1)*1955
		
class Sentence:
	def __init__(self,code,words,values,country_name):
		self.words = words
		self.code = code
		self.year = 0
		self.values = []
		self.values = deepcopy(values)
		self.country_name = []
		self.country_name = country_name

	def Score(self,Country,value,Attribute):
		if(len(Country.attribute_array[p[Attribute.code]].values)!=0):
			wordings = self.words.split(' ')
			for w in wordings:
				for key in Attribute.keywords:
					w = re.sub(r'[^a-zA-Z]',r'',w)
					if(key.lower()==w.lower()):
						acc_expect = 0
						if ( self.year == None or self.year==0):
							if( float(value) > float(Country.attribute_array[p[Attribute.code]].values[0]) and float(value) < float(Country.attribute_array[p[Attribute.code]].values[len(Country.attribute_array[p[Attribute.code]].values)-1]) ) : return 90
							elif ( float(value) < float(Country.attribute_array[p[Attribute.code]].values[0]) ): acc_expect = float(Country.attribute_array[p[Attribute.code]].values[0])
							elif ( float(value) > float(Country.attribute_array[p[Attribute.code]].values[len(Country.attribute_array[p[Attribute.code]].values)-1]) ): acc_expect = float(Country.attribute_array[p[Attribute.code]].values[len(Country.attribute_array[p[Attribute.code]].values)-1])
						else :
							acc_expect = float(Country.attribute_array[p[Attribute.code]].w0) + float(Country.attribute_array[p[Attribute.code]].w1) * float(self.year)
						if(Country.attribute_array[p[Attribute.code]].var!=0):
							ret = (pow(float(e),-1*pow(float(acc_expect)-float(value),2)/(2*float(Country.attribute_array[p[Attribute.code]].var)))*100/(pow(2*3.14*float(Country.attribute_array[p[Attribute.code]].var),0.5)) )
						else:
							if (acc_expect==float(value)): ret = 100
							else : ret = 0
						return ret

	def doAll(self):
		out = open("output.csv","ab")
		for c in self.country_name:
			while ((c not in cn.keys() ) and ( c!="")):
				c=c[:len(c)-1]
			if c!="":
				cntry=country_array[cn[c]]
				for v in self.values:
					if v!="":
						if( 1500 < float(v) and float(v) <  2200 ): self.year = v
						for a in cntry.attribute_array:
							score = self.Score(cntry,v,a)
							try:
								if(float(score)>threshold and float(score)<float(100) ):
									key2 = (self.code,c,a.code,v)
									if key2 not in entries:
										out.write(str(self.code)+","+str(c)+","+str(a.code)+","+str(v)+","+str(score)+"\n")
										entries.add(key2)
							except : pass

def main():
	with open('countries_id_map.txt','r') as country_cin:
		country_cin=csv.reader(country_cin, delimiter='\t')
		count=0	
		for row in country_cin:
			if(count>0):
				if (country_array[count-1].code) == row[0]:
					country_array[count-1].name_array.append(row[1])
					cn[row[1]]=count-1
				else:
					ct=Country(row[0], row[1])
					country_array.append(ct)
					cn[row[1]]=count
					cc[row[0]]=count
					count=count+1
			else:
				ct=Country(row[0], row[1])
				country_array.append(ct)
				cn[row[1]]=count
				cc[row[0]]=count
				count=count+1
	
	with open('selected_indicators','r') as attrib_cin:
		attrib_cin=csv.reader(attrib_cin, delimiter='\t')
		count=0
		for row in attrib_cin:
			key=(key_words[count]).split('_')
			if len(row)==3:	ext=""
			else: ext=row[3]
			ct=Attribute(key, row[1], row[2], ext)
			attribute_array_main.append(ct)
			p[row[2]]=count
			count=count+1
	
	for i in country_array:
		i.addAttribute()

	country_array[0].attribute_array[2].expect=10

	with open('kb-facts-train_SI.tsv','r') as fact_cin:
		fact_cin=csv.reader(fact_cin, delimiter='\t')
		count=0;exp=0;prevc="";prevp="";
		for row in fact_cin:
			if count==0: 
				exp=exp+float(row[1])
				count=count+1
				prevc=row[0]
				prevp=row[2]
			else :
				if ( prevc==row[0] and prevp==row[2] ):
					exp=exp+float(row[1])
					count=count+1
				else :
					Expect=(exp/count)
					country_array[cc[prevc]].attribute_array[p[prevp]].expect=Expect
					prevp=row[2]; prevc=row[0];
					exp=float(row[1])
					count=1
			country_array[cc[row[0]]].attribute_array[p[row[2]]].values.append(row[1])
		Expect=(exp/count)
		country_array[cc[prevc]].attribute_array[p[prevp]].expect=Expect

	for i in country_array:
		i.regression()
			
	os.system("rm -f output.csv")
				
	with open('sentences.tsv','r') as sent_cin:
		sent_cin=csv.reader(sent_cin, delimiter='\t')
		count=0
		for row in sent_cin:
			a= Sentence(row[0].strip(),row[1],map(str.strip,row[2].split(',')),map(str.strip,row[3].split(',')))
			a.doAll()

main()