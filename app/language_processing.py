from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from io import StringIO, BytesIO
import urllib.request
from urllib import request
import glob
import pandas as pd
import numpy as np
from google.colab import files
from collections import defaultdict
import re
from datetime import datetime
import os, config

class language_processing:
    def pdf_to_txt(fp):
      sentence=[]
      rsrcmgr = PDFResourceManager()
      retstr = StringIO()
      codec = 'utf-8'
      laparams = LAParams()
      device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
      # fp= open(name, 'rb')
      interpreter = PDFPageInterpreter(rsrcmgr, device)
      password = ""
      maxpages = 0
      caching = True
      pagenos = set()
      for page in PDFPage.get_pages(fp,
                                    pagenos,
                                    maxpages=maxpages,
                                    password=password,
                                    caching=caching,
                                    check_extractable=True):
          interpreter.process_page(page)
      fp.close()
      device.close()
      str = retstr.getvalue()
      str=str.replace('\n',' ')
      retstr.close()
      sentence=str.split('.')
      return  sentence


    def decect_DLP(tempary_sentence,DLP_Dictionary):
      page=0
      Report_number="DLP"
      test=0
      for i in tempary_sentence:
        if 'DLP'in i :
          DLP_list=i.split(' ')
          for j in range(len(DLP_list)-1,-1,-1):
            if 'mGy' in DLP_list[j]:
              test=1
              DLP=DLP_list[j-1]
              DLP_Dictionary[str(Report_number)].append(DLP)
              break
          if test==0:
            new_list=i.split('DLP')[1]
            report_number = re.compile('\d+')
            number=report_number.findall(new_list)[0]
            DLP_Dictionary[str(Report_number)].append(number)
            test=1
            break


      if test==0:
        DLP_Dictionary[str(Report_number)].append('DLP_NONE')

      return

    def decect_date(tempary_sentence,DLP_Dictionary):
      page=0
      Report_number='Date'
      Moth_dict={'01':'JAN','02':"FEB",'03':'MAR','04':"APR",'05':'MAY','06':'JUN','07':'JUL','08':'AUG','09':"SEP",'10':"OCT",'11':'NOV',"12":'DEC'}
      final_date='Date_NONE'
      for i in tempary_sentence:
        if 'Date Serviced' in i:
          i=i.split('Date Serviced')[1]
          date_reg_exp = re.compile('\d{2}[/]\d{2}[/]\d{4}')
          data=date_reg_exp.findall(i)[0]
          data=data.split('/')
          day=data[0]
          mon=Moth_dict[data[1]]
          year=data[2]
          final_date=day+'-'+mon+'-'+year
          DLP_Dictionary[str(Report_number)].append(final_date)
        if 'performed on' in i:
          date_reg_exp2 = re.compile('\d{2}[-][A-Z]{3}[-]\d{4}')
          final_date=date_reg_exp2.findall(i)[0]
          DLP_Dictionary[str(Report_number)].append(final_date)


      if final_date=='Date_NONE':
        DLP_Dictionary[str(Report_number)].append(final_date)

      return


    def Decect_Unique_Number(tempary_sentence,DLP_Dictionary):
      Doctor_name='Reprot_Number_NONE'
      Report_number='Unique Episode Number'
      for i in tempary_sentence:
        if 'General Report' in i :
          report_number = re.compile('\d+')
          number=report_number.findall(i)[0]
          DLP_Dictionary[str(Report_number)].append(number)
        if 'Acc	No:' in i :
          split=i.split('Ward:')[1]
          report_number = re.compile('\d+')
          number=report_number.findall(split)[0]
          DLP_Dictionary[str(Report_number)].append(number)
        if 'Exam	Date:' in i:
          report_number = re.compile('\d+')
          number=report_number.findall(i)[0]
          DLP_Dictionary[str(Report_number)].append(number)
      if Doctor_name=='Report_Number_NONE':
        DLP_Dictionary[str(Report_number)].append(number)




    def Decect_location(tempary_sentence,DLP_Dictionary):
      location='location_NONE'
      Report_number='Facility'
      for i in tempary_sentence:
        if 'Hospital' in i :
          splits=i.split(',')
          for location in splits:
            if 'Hospital' in location:
              DLP_Dictionary[str(Report_number)].append(location)
              return
        if 'Site:' in i:
          splits=i.split('Site:')[1]
          location=splits.split(')')[0]
          DLP_Dictionary[str(Report_number)].append(location)
          return
      if location=='location_NONE':
        DLP_Dictionary[str(Report_number)].append(location)
        return




    def Decect_Coreporting_Doctor(tempary_sentence,DLP_Dictionary):
      Doctor_name='Doctor_NONE'
      Report_number='Co-reporting Doctor'
      for i in tempary_sentence:

        if 'Co-read' in i :
          splits_1=i.split('Co-read')[1]
          try:
            if 'by' in splits_1:
              splits=splits_1.split('by')[1]
            else:
              splits=splits_1.split('By')[1]
          except:
            splits=splits_1
          Doctor_name=splits.split('    ')[0]
          p=re.compile('[\t]+')
          new_string=re.sub(p,'$',Doctor_name)
          Doctor_name=new_string.split('$')[0]
          Doctor_name=Doctor_name.strip(':')
          DLP_Dictionary[str(Report_number)].append(Doctor_name)
        if 'Coread' in i:
          splits_1=i.split('Coread')[1]
          try:
            if 'by' in splits_1:
              splits=splits_1.split('by')[1]
            else:
              splits=splits_1.split('By')[1]
          except:
            splits=splits_1
          Doctor_name=splits.split('    ')[0]
          p=re.compile('[\t]+')
          new_string=re.sub(p,'$',Doctor_name)
          Doctor_name=new_string.split('$')[0]
          Doctor_name=Doctor_name.strip(':')
          DLP_Dictionary[str(Report_number)].append(Doctor_name)
        if 'coread' in i:
          splits_1=i.split('coread')[1]
          try:
            if 'by' in splits_1:
              splits=splits_1.split('by')[1]
            else:
              splits=splits_1.split('By')[1]
          except:
            splits=splits_1
          Doctor_name=splits.split('    ')[0]
          p=re.compile('[\t]+')
          new_string=re.sub(p,'$',Doctor_name)
          Doctor_name=new_string.split('$')[0]
          Doctor_name=Doctor_name.strip(':')
          DLP_Dictionary[str(Report_number)].append(Doctor_name)
      if Doctor_name=='Doctor_NONE':
        DLP_Dictionary[str(Report_number)].append(Doctor_name)


    def Decect_cardiac_findings(tempary_sentence,DLP_Dictionary):
      findings='cardiac_findings_NONE'
      Report_number1='Non_cardiac_findings'
      for i in tempary_sentence:

        if 'Non-Cardiac Findings' in i or 'Non cardiac findings' in i or  'no additional cardiac findings' in i:
          findings=1
          DLP_Dictionary[str(Report_number1)].append(findings)
          return
        if 'normal' in i and 'cardiac' in i: 
            findings=1
            DLP_Dictionary[str(Report_number1)].append(findings)
            return
        if 'normal' in i and 'Cardiac' in i: 
            findings=1
            DLP_Dictionary[str(Report_number1)].append(findings)
            return
      if findings=='cardiac_findings_NONE':
        DLP_Dictionary[str(Report_number1)].append(findings)
        return




    def Decect_coronary_cardiac_findings(tempary_sentence,DLP_Dictionary):
      findings='coronary_cardiac_findings_NONE'
      Report_number1='Non_coronary_cardiac_findings'
      for i in tempary_sentence:
        if 'non coronary cardiac findings' in i:
          findings=1
          DLP_Dictionary[str(Report_number1)].append(findings)
          return
        if ('coronary' in i) and ('normal' in i): 
          findings=1
          DLP_Dictionary[str(Report_number1)].append(findings)
          return
        if ('no evidence' in i) and ('coronary' in i) :
          findings=1
          DLP_Dictionary[str(Report_number1)].append(findings)
          return
      if findings=='coronary_cardiac_findings_NONE':
        DLP_Dictionary[str(Report_number1)].append(findings)
        return



"""if __name__ == '__main__':


  #read the report
  Conclustion_Dictionary=defaultdict(list)
  report = os.path.join(config.DATA_DIR, '25.pdf')
  tempary_sentence=pdf_to_txt(report)
  decect_DLP(tempary_sentence,Conclustion_Dictionary)
  decect_date(tempary_sentence,Conclustion_Dictionary)
  Decect_Unique_Number(tempary_sentence,Conclustion_Dictionary)
  Decect_location(tempary_sentence,Conclustion_Dictionary)
  Decect_Coreporting_Doctor(tempary_sentence,Conclustion_Dictionary)
  Conclustion_Dictionary['Correlated'].append("None")
  print(Conclustion_Dictionary)"""








