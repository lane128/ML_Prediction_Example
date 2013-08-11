#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import division
import sys,json
from jubatus.classifier import client
from jubatus.classifier import types
import time

def get_most_likely(estm):
    ans = None
    prob = None
    result = {}
    result[0] = ''
    result[1] = 0
    for res in estm:
        if prob == None or res.score > prob :
            ans = res.label
            prob = res.score
            result[0] = ans
            result[1] = prob
    return result

def parse_args():
    from optparse import OptionParser, OptionValueError
    p = OptionParser()
    p.add_option('-s', '--server_ip', action='store',
                 dest='server_ip', type='string', default='192.168.170.129')
    p.add_option('-p', '--server_port', action='store',
                 dest='server_port', type='int', default='9199')
    p.add_option('-n', '--name', action='store',
                 dest='name', type='string', default='tutorial')
    return p.parse_args()

if __name__ == '__main__':
	options,remainder=parse_args()
  	classifier=client.classifier(options.server_ip,options.server_port)
   	pname=options.name

   	print classifier.get_config(pname)
    	print classifier.get_status(pname)

       	for line in open('adult.data'):
    		age,workclass,fnlwgt,education,education_num,marital_status,occupation,relationship,race,sex,capital_gain,capital_loss,hours_per_week,native_country,income=line[:-1].split(',')
    		datum=types.datum([('workclass',workclass),('sex',sex),('occupation',occupation),('education',education),('marital_status',marital_status),('native_country',native_country),('race',race),('relationship',relationship)],[('age',float(age)),('hours_per_week',float(hours_per_week)),('education_num',float(education_num))])
    		classifier.train(pname,[(income,datum)])
    		pass

    	print classifier.get_status(pname)

	print classifier.save(pname, "tutorial")

	print classifier.load(pname, "tutorial")

	print classifier.get_config(pname)

	total_num=0.00
	ok_num=0.00
	start_time=time.clock()
	for line in open('adult.test'):
		total_num=total_num+1
    		age,workclass,fnlwgt,education,education_num,marital_status,occupation,relationship,race,sex,capital_gain,capital_loss,hours_per_week,native_country,income=line[:-2].split(',')
    		datum=types.datum([('workclass',workclass),('sex',sex),('occupation',occupation),('education',education),('marital_status',marital_status),('native_country',native_country),('race',race),('relationship',relationship)],[('age',float(age)),('hours_per_week',float(hours_per_week)),('education_num',float(education_num))])
    		ans=classifier.classify(pname,[(datum)])
    		if ans!=None:
    			estm=get_most_likely(ans[0])
    			if(income==estm[0]):
    				ok_num=ok_num+1
    				result='Ok'
    			else:
    				result='No'
    			pass
    			print line
    			print result+',[actual:'+income+'],[predict:'+estm[0]+'],'+str(estm[1])
		pass

	k=ok_num/total_num
	end_time=time.clock()
	print end_time- start_time
	print ok_num,total_num,k
	print 'SuccessPercent:['+str(k)+']'
	
