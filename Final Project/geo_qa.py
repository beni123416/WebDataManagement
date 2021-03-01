#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import rdflib
import requests 
import lxml.html
from rdflib import Literal, XSD

prefix = "https://en.wikipedia.org"
url="https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
              
def create(url):
    print("start")
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    g = rdflib.Graph()
    
    countries_links=doc.xpath("//table[position()=2]//table[position()=1]/tbody/tr//span[@class='flagicon']/following-sibling::a[position()=1]//@href")

    for i in range(len(countries_links)):
        country_info(prefix+countries_links[i], g)
    
    g.serialize("ontology.nt", format="nt")
    print("done!")
    return 
    
def country_info(url, g):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    
    population_relation = rdflib.URIRef('http://example.org/population')
    area_relation = rdflib.URIRef('http://example.org/area')
    government_relation = rdflib.URIRef('http://example.org/government')
    capital_relation = rdflib.URIRef('http://example.org/capital')
    type_relation = rdflib.URIRef('http://example.org/type')
    president_relation = rdflib.URIRef('http://example.org/president')
    prime_minister_relation = rdflib.URIRef('http://example.org/prime_minister')

    country=url.split("/wiki/")[-1]
    capital=doc.xpath("//table[@class='infobox geography vcard']//tr[.//*[text()='Capital']]/td//a/@title")
    if(len(capital)>0):
        capital=capital[0].split(",")[0]
        if(capital=="City-state"):
            capital=country   
        elif(country=="switzerland"):
            capital=doc.xpath("//table[@class='infobox geography vcard']//tr[.//*[text()='Capital']]/td/a/@title")[0]
        capital=rdflib.URIRef("http://example.org/"+capital.replace(" ","_").replace("-","_").lower())
    else:
        if(country=="gibraltar"):
            capital=doc.xpath("//table[@class='infobox geography vcard']//tr[.//*[text()='Capital']]/td/text()")[0]
            capital=rdflib.URIRef("http://example.org/"+capital.replace(" ","_").replace("-","_").lower())
        elif(country=="channel_islands"):
            capital=doc.xpath("//table[@class='infobox vcard']//tr[.//*[text()='Capital and largest settlement']]/td/text()")[0]
            capital=rdflib.URIRef("http://example.org/"+capital.replace(" ","_").replace("-","_").lower())
        else:
            capital=rdflib.URIRef("http://example.org/None")

    country=rdflib.URIRef("http://example.org/"+country.replace(" ","_").lower())
    g.add((country, capital_relation, capital))
    g.add((country, type_relation, rdflib.URIRef('http://example.org/country')))

    if("channel_islands" in country):
        population=doc.xpath("//table[@class='infobox vcard']//tr[.//*[text()='Population']]/td/text()")[0]  
    else:
        population=doc.xpath("//table[@class='infobox geography vcard']//tr[.//*[text()='Population']]/following-sibling::tr[position()=1]/td/text()")[0]  
    population=population.split("(")[0].lstrip().rstrip()
    population=rdflib.URIRef("http://example.org/"+population)
    g.add((country, population_relation, population))

    if("channel_islands" in country):
        area=doc.xpath("//table[@class='infobox vcard']//tr[.//*[contains(text(),'Area')]]/td/text()")[0]  
    else:
        area = doc.xpath("//table[@class='infobox geography vcard']//tr[.//*[contains(text(),'Area')]]/following-sibling::tr[position()=1]/td/text()")[0]
    area=area.split("(")[-1].split(" ")[0].split("&")[0].split("km")[0].split("\xa0")[0]
    area=rdflib.URIRef("http://example.org/"+area + "_km2")
    g.add((country, area_relation, area))

    
    governments=doc.xpath("//table[@class='infobox geography vcard']//tr[.//*[text()='Government']]/td//text()")
    gov=""
    count=0
    flag=0
    for t in governments:
        if(flag==0):
            if t=="\n":
                count+=1
                if count>1:
                    break
                else:
                    continue
            elif ("[" in t) and ("]" in t):
                t=""
            elif "(" in t:
                flag=1;
                continue
        elif(flag==1):
            if ")" in t:
                flag=0
            continue
        gov= gov+t.lower()
    if gov!="":
        if gov[-1]==" ":
            gov=gov[:-1]
        if gov[0]==" ":
            gov=gov[1:]
    gov=gov.replace(" ","_").replace("-","_").replace(",","").replace("de_jure:","")
    govern=rdflib.URIRef("http://example.org/"+str(gov))
    g.add((country, government_relation, govern))  
    
    prime_minister_link=doc.xpath("//table[@class='infobox geography vcard']//tr[.//*[text()='Prime Minister']]/td//a[contains(@href,'/wiki/')]/@href")
    if len(prime_minister_link)>0:
        person_info(prefix+prime_minister_link[0],country,"prime_minister",g)
    else:
        prime_minister=rdflib.URIRef("http://example.org/None")
        g.add((country, prime_minister_relation, prime_minister)) 
    
    president_link=doc.xpath("//table[@class='infobox geography vcard']//tr[.//*[text()='President']]/td//a[contains(@href,'/wiki/')]/@href")
    if len(president_link)>0:
        person_info(prefix+president_link[0],country,"president",g)
    else:
        president=rdflib.URIRef("http://example.org/None")
        g.add((country, president_relation, president)) 
        
def person_info(url,country, role, g):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    president_relation = rdflib.URIRef('http://example.org/president')
    prime_minister_relation = rdflib.URIRef('http://example.org/prime_minister')
    type_relation = rdflib.URIRef('http://example.org/type')
    person=url.split("/wiki/")[-1].replace("-","_")
    person=rdflib.URIRef("http://example.org/" + person.lower())
    birth_date = rdflib.URIRef('http://example.org/birthDate')

    date=doc.xpath("//table[@class='infobox vcard']//tr[.//*[text()='Born']]/td//span[@class='bday']/text()")  
    if len(date)>0:
        date = Literal(date[0],datatype=XSD.date) 
        g.add((person, birth_date,date))
    if(role=="president"):
        g.add((person, type_relation, rdflib.URIRef('http://example.org/president_of')))
        g.add((country, president_relation, person))    
    elif role=="prime_minister":
        g.add((person, type_relation, rdflib.URIRef('http://example.org/prime_minister_of')))
        g.add((country, prime_minister_relation, person))    
    
def question(q,file):
    g=rdflib.Graph()
    g.parse(file, format="nt")
    q=q.lower()
    subject=q.split(" of ")
    if len(subject)==2:
        subject=subject[1].lstrip().rstrip().replace(" ","_").replace("?","")
    elif len(subject)>2:
        subject=(subject[1]+" of "+ subject[2]).lstrip().rstrip().replace(" ","_").replace("?","")
    if "who is" in q:
        if "president of" in q:
            query="select ?p                 where{<http://example.org/"+subject+"> <http://example.org/president> ?p . }"
        elif "prime minister of" in q:
            query="select ?p                 where{<http://example.org/"+subject+"> <http://example.org/prime_minister> ?p . }"        
        else:
            subject=q.split(" is")[1].lstrip().rstrip().replace(" ","_").replace("?","")
            query="select ?t                where{<http://example.org/"+subject+"> <http://example.org/type> ?t . }"
            role=str(list(g.query(query))[0])
            if "president" in role:
                print("President of ", end="")
                query="select ?c                     where{?c <http://example.org/president> <http://example.org/"+subject+"> . }" 
            else:
                print("Prime minister of ", end="")
                query="select ?c                     where{?c <http://example.org/prime_minister> <http://example.org/"+subject+"> . }" 
    
    elif "what is the" in q:
        if "population" in q:
            query="select ?p                     where{<http://example.org/"+subject+"> <http://example.org/population> ?p . }"         
        elif "area" in q:
            query="select ?a                     where{<http://example.org/"+subject+"> <http://example.org/area> ?a . }" 
        elif "government" in q:
             query="select ?g                     where{<http://example.org/"+subject+"> <http://example.org/government> ?g . }"        
        else:
             query="select ?c                     where{<http://example.org/"+subject+"> <http://example.org/capital> ?c . }"    
    
    else:
        subject=subject.replace("_born","")
        if "president" in q:
            query="select ?d                     where{  <http://example.org/"+subject+"> <http://example.org/president> ?p .                               ?p <http://example.org/birthDate> ?d . }"
        else:
            query="select ?d                     where{  <http://example.org/"+subject+"> <http://example.org/prime_minister> ?p .                               ?p <http://example.org/birthDate> ?d . }"   
        result=list(g.query(query))
        for i in range(len(result)):
            print(str(result[i]).replace("(rdflib.term.Literal('","").replace("', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#date')),)",""), end="")
            if i<len(result)-1:
                print(", ", end="")
        return 
    
    result=list(g.query(query))
    for i in range(len(result)):
        print(str(result[i]).replace("(rdflib.term.URIRef('http://example.org/","").replace("'),)","").replace("_"," "), end="")
        if i<len(result)-1:
            print(", ", end="")
            
    return 
    
if __name__ == "__main__":
    args = sys.argv
    if len(args)<3:
        print("invalid number of args!")
    else:    
        if (args[1]=="question"):
            ontology='ontology.nt'
            question(args[2],ontology)
        elif (args[1]== "create" and args[2]=="ontology.nt"):
            create(url)
        else:
            print("invalid command!") 

