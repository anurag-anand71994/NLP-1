# Convert .tsv file to dataturks json format. 
import json
import logging
import sys
import csv 



def process_line(line, start):
    sentence,word,pos,tag=line
    
    if tag!='O':
        d={}
        d['text']=word
        d['start']=start
        d['end']=start+len(word)-1
    else:
        d = None
    move =len(word)+1
    return d,word, tag, move

def tsv_to_json_format(input_path,output_path,unknown_label):
    try:
        f = get_csv( input_path )
        fp=open(output_path, 'w') # output file
        data_dict={}
        annotations =[]
        label_dict={}
        s=''
        start=0
        for line in f:
            if 'Sentence' not in line[0]:
                d, word, tag, move = process_line(line, start)
                start += move
                s+=word+" "
                if d != None:
                    try:
                        label_dict[tag].append(d)
                    except:
                        label_dict[tag]=[]
                        label_dict[tag].append(d)

            else:
                ##file away object for last sentence

                data_dict['content']=s
                label_list=[]
                for ents in list(label_dict.keys()):
                    for i in range(len(label_dict[ents])):
                        if(label_dict[ents][i]['text']!=''):
                            l=[ents,label_dict[ents][i]]
                            for j in range(i+1,len(label_dict[ents])): 
                                if(label_dict[ents][i]['text']==label_dict[ents][j]['text']):  
                                    di={}
                                    di['start']=label_dict[ents][j]['start']
                                    di['end']=label_dict[ents][j]['end']
                                    di['text']=label_dict[ents][i]['text']
                                    l.append(di)
                                    label_dict[ents][j]['text']=''
                            label_list.append(l)                          
                            
                for entities in label_list:
                    label={}
                    label['label']=[entities[0]]
                    label['points']=entities[1:]
                    annotations.append(label)
                data_dict['annotation']=annotations
                annotations=[]
                json.dump(data_dict, fp)
                fp.write('\n')
                data_dict={}


                ##start processing next sentence
                start=0
                label_dict={}
                s=''
                d, word, tag, move = process_line(line, start)
                start += move
                s+=word+" "
                if d != None:
                    try:
                        label_dict[tag].append(d)
                    except:
                        label_dict[tag]=[]
                        label_dict[tag].append(d)

        return data_dict
    except Exception as e:
        logging.exception("Unable to process file" + "\n" + "error = " + str(e))
        return None


def get_csv( filepath ):
    c = []      
    with open(filepath, newline='', encoding='utf8', errors='ignore') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(spamreader)
        for row in spamreader:
            c.append(row)
    return c

tsv_to_json_format( "data/ner_dataset.csv" ,'data/ner_corpus.json','abc')



