#!/usr/bin/env python
# coding: utf-8

# In[2]:


import rdflib
import requests 
import lxml.html
from rdflib import Literal, XSD

prefix = "https://en.wikipedia.org"

def ontology():
    res = requests.get("https://en.wikipedia.org/wiki/2019%E2%80%9320_Premier_League")
    doc = lxml.html.fromstring(res.content)
    g = rdflib.Graph()
    
    country = rdflib.URIRef('http://example.org/country')
    league = rdflib.URIRef('http://example.org/league')
    home_city = rdflib.URIRef('http://example.org/homeCity')
    located_in = rdflib.URIRef('http://example.org/locatedIn')
    l=doc.xpath("//table[@class='infobox']//caption//text()")
    league_link=doc.xpath("//table[@class='infobox']//caption/a/@href")[0]
    res_league = requests.get(prefix+league_link)
    doc_league = lxml.html.fromstring(res_league.content)
    premierLeague = rdflib.URIRef('http://example.org/'+ str(l[0].replace(" ","_")))
    league_country = doc_league.xpath("//table[@class='infobox']//tr[.//*[contains(text(),'Country') or contains(text(),'country')]]/td//text()")[0]
    
    
    league_c = rdflib.URIRef('http://example.org/'+league_country.rstrip().lstrip().replace(" ","_"))
    g.add((premierLeague, country, league_c))

    teams = doc.xpath("//table[position()=2]//tr/td[position()=1]/a/text()")
    cities = []
    teams_links = doc.xpath("//table[position()=2]//tr/td[position()=1]/a/@href")
    
    for i in range(2,len(teams)+2):
        city=doc.xpath("//table[position()=2]//tr[position()="+str(i)+"]/td[position()=2]//text()")[0]
        cities.append(city.rstrip())
    
    for i in range(2,len(teams)+2):
        city_URLs = doc.xpath("//table[position()=2]//tr/td[position()=2]/a[position()=1]/@href")
    
    d={}
    for item in city_URLs:
            res2 = requests.get(prefix+item)
            doc2 = lxml.html.fromstring(res2.content)
            c = doc2.xpath("//table[@class='infobox geography vcard']//tr[.//*[contains(text(),'Country') or contains(text(),'country')]]/td//text()")[-1]
            city= doc2.xpath("//table[@class='infobox geography vcard']//tr[position()=1]//text()")[0]
            d.update({city:c})   
    
    for i in range(len(teams)):
        team=rdflib.URIRef("http://example.org/"+teams[i].replace(" ","_"))
        city=rdflib.URIRef("http://example.org/"+cities[i].replace(" ","_"))
        c=rdflib.URIRef("http://example.org/"+d[cities[i]].replace(" ","_"))
        g.add((team, league, premierLeague))
        g.add((team, home_city, city))
        g.add((city,located_in,c))
        info_on_teams(prefix+teams_links[i],g,team)

    g.serialize("ontology.nt", format="nt")
    print("done!")

def info_on_teams(url, g,team):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    
    position = rdflib.URIRef('http://example.org/position')
    plays_for = rdflib.URIRef('http://example.org/playsFor')
   
    players=doc.xpath("//table[@border=0][position()=1]//tr//table//tr/td[position()=4]/descendant::a[position()=1]/text()")
    poss=doc.xpath("//table[@border=0][position()=1]//tr//table//tr/td[position()=3]/descendant::a[position()=1]/text()")
    players_links=doc.xpath("//table[@border=0][position()=1]//tr//table//tr/td[position()=4]/descendant::a[position()=1]/@href")
    
    for i in range(len(players)):
        player=rdflib.URIRef("http://example.org/"+players[i].replace(" ","_"))
        pos=rdflib.URIRef("http://example.org/"+poss[i].replace(" ","_"))
        g.add((player, position, pos))
        g.add((player, plays_for, team))
        info_on_player(prefix+players_links[i],g,player)

def info_on_player(url, g, player):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)

    birth_place = rdflib.URIRef('http://example.org/birthPlace')
    birth_date = rdflib.URIRef('http://example.org/birthDate')
    o_country = rdflib.URIRef('http://example.org/country')
    located_in = rdflib.URIRef('http://example.org/locatedIn')

    date=doc.xpath("//table//th[text()='Date of birth']//..//span[@class='bday']/text()")
    place=doc.xpath("//table//th[text()='Place of birth']//..//td[@class='birthplace']/a/text()")    
    country=doc.xpath("//table//th[text()='Place of birth']//..//td[@class='birthplace']/text()")
    if len(place)!=0:
        place=rdflib.URIRef("http://example.org/"+place[0].replace(" ","_"))
        g.add((player, birth_place, place))

        if len(country)!=0:
            c=country[-1].split(",")[-1].lstrip().replace(" ","_")
            if len(c)>2:
                country=rdflib.URIRef("http://example.org/"+c)
                g.add((place,located_in,country))
        
    date = Literal(date[0],datatype=XSD.date) 
    g.add((player, birth_date,date))
    

print("start...")  
ontology()


# In[ ]:




