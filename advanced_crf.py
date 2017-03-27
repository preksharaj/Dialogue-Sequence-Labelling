from collections import namedtuple
import csv
import sys
import glob
import os
import collections
import re
import pycrfsuite


def get_utterances_from_file(dialog_csv_file):
    """Returns a list of DialogUtterances from an open file."""
    reader = csv.DictReader(dialog_csv_file)
    return [_dict_to_dialog_utterance(du_dict) for du_dict in reader]

def get_utterances_from_filename(dialog_csv_filename):
    """Returns a list of DialogUtterances from an unopened filename."""
    with open(dialog_csv_filename, "r") as dialog_csv_file:
        return get_utterances_from_file(dialog_csv_file)


def get_data(data_dir):
	flag=0
	if data_dir==sys.argv[2]:
		flag=1

	dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    #print(dialog_filenames)
    
	for dialog_filename in dialog_filenames:
		if flag==1:
            		file_list[dialog_filename]=len(open(dialog_filename).readlines())
			#file_list.append(dialog_filename.split("/")[-1])

		yield get_utterances_from_filename(dialog_filename)

DialogUtterance = namedtuple("DialogUtterance", ("act_tag", "speaker", "pos", "text"))

PosTag = namedtuple("PosTag", ("token", "pos"))

def _dict_to_dialog_utterance(du_dict):
    """Private method for converting a dict to a DialogUtterance."""

    # Remove anything with 
    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            du_dict[k] = None

    # Extract tokens and POS tags
    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    return DialogUtterance(**du_dict)


def get_crf_info(dirname):
	labellist=[]
	featurelist=[]	
	flag = 0
	if dirname==sys.argv[2]:
		flag = 1
	trial= get_data(dirname)
	for utterances in trial:
		
		
		line_no =1
		speaker_list=[]
		last=utterances[0][1]
		for utterance in utterances:
			
			initiallist=[]				
			if utterance[0] != "":				#Check if dialog_tag is present or else insert UNKNOWN tag
				dialog_tag = utterance[0]
				labellist.append(dialog_tag)
			elif utterance[0]=="":
				dialog_tag = "UNKNOWN"
			speaker = utterance[1]	
			
			if speaker != last:
				initiallist.append('1')#Check if speaker change
			
			else:
				initiallist.append('0')
			last=speaker
					

			if(line_no == 1):
				initiallist.append('1')#Check if it is the first line of the csv file
			else:
				initiallist.append('0')		
			
			token_pos_list = utterance[2]
			token_list=[]
			pos_list=[]
			if token_pos_list:	
          						
				for token_pos in token_pos_list: #token list
					token = token_pos[0]
					if token!="":
						initiallist.append("TOKEN_"+token)
						token_list.append(token)
				for token_pos in token_pos_list:#pos list
					pos = token_pos[1]
					if pos !="":
						initiallist.append("POS_"+pos)
						pos_list.append(pos)
				token_bigrams = zip(token_list,token_list[1:])#Bigrams of TOKENS	
				for i in token_bigrams:
					bigram ="/".join(i)
					initiallist.append("TOKEN_"+bigram)

				pos_bigrams = zip(pos_list,pos_list[1:])#Bigrams of POS tags
				for i in pos_bigrams:
					bigram ="/".join(i)
					initiallist.append("POS_"+bigram)
				
					
				if("?" in token_list):  #whether the utterance is a question
					initiallist.append('1')	

			line_no+=1
			
			featurelist.append(initiallist)

	
	return (featurelist,labellist) 

file_list = collections.OrderedDict()

inputfo= sys.argv[1]
X,Y= get_crf_info(inputfo)
trainer = pycrfsuite.Trainer(verbose=False)
trainer.append(X,Y)
trainer.set_params({
    'c1': 1.0,   # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 100,  # stop earlier
})

trainer.train('conll2002-esp.crfsuite')
testfo=sys.argv[2]
Xtest,Ytest= get_crf_info(testfo)
tagger = pycrfsuite.Tagger()
tagger.open('conll2002-esp.crfsuite')
trap=[]
trap=tagger.tag(Xtest)
filewrite=open(sys.argv[3],"w")
for i in file_list:
	filewrite.write("Filename=\""+i.split('/')[-1]+"\"\n")
	for j in range(0, file_list[i]-1):
		filewrite.write(trap.pop(0)+"\n")
	filewrite.write("\n")



	

