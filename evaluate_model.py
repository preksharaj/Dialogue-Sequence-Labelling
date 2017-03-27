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

	dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    #print(dialog_filenames)
    
	for dialog_filename in dialog_filenames:

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



# Main Fuction
def get_crf_info(dirname):
	labellist=[]
	trial= get_data(dirname)
	#print(trial)
	for utterances in trial:
		for utterance in utterances:
							#Iterate through each utterance in the file
			if utterance[0] != "":				#Check if dialog_tag is present or else insert UNKNOWN tag
				dialog_tag = utterance[0]
				#print dialog_tag
				labellist.append(dialog_tag)
			elif utterance[0]=="":
				dialog_tag = "UNKNOWN"
	return labellist
lisA=[]
lisA=get_crf_info(sys.argv[1])
#print(lisA)	
			
myNames=[]
with open(sys.argv[2], 'r') as f:
    myNames = f.readlines()
grades=[]
for i in range(len(myNames)):
	#print(myNames[i])
	if myNames[i]!='\n' and "Filename" not in myNames[i] :
    		grades.append(myNames[i].split("\n")[0])



bottom=len(lisA)
top=sum([1 for i,j in zip(lisA,grades) if i==j])
accuracy=round(100* float(top)/float(bottom),2)
print("Number of Correct Labels= "+top+"/"+bottom)

print("Accuracy= "+str(accuracy)+"%")




