# Dialogue-Sequence-Labelling

The goal of this assignment is to get some experience with sequence labeling. Specifically, you
will be assigning dialogue acts to sequences of utterances in conversations from a corpus.
Using a machine learning technique, conditional random fields, which is designed for sequence labeling I have implemented sequence labelling
using the toolkit, CRFsuite.

The raw data for each utterance in the conversation consists of the speaker name, the tokens and
their part of speech tags. Given a labeled set of data, you will first create a baseline set of
features as specified below, and measure the accuracy of the CRFsuite model created using those
features. You will then experiment with additional features in an attempt to improve
performance. The best set of features you develop will be called the advanced feature set.


In all data, individual conversations are stored as individual CSV files. These CSV files have
four columns and each row represents a single utterance in the conversation. The order of the
utterances is the same order in which they were spoken. The columns are:
• act_tag - the dialogue act associated with this utterance. This is blank for the unlabeled data.
• speaker - the speaker of the utterance (A or B).
• pos - a whitespace-separated list where each item is a token, "/", and a part of speech tag (e.g.,
"What/WP are/VBP your/PRP$ favorite/JJ programs/NNS ?/."). When the utterance has no words
(e.g., the transcriber is describing some kind of noise), the pos column may be blank, consist
solely of "./.", have a pos but no token, or have an invented token such as MUMBLEx. You can
view the text column to see the original transcription.
• text - The transcript of the utterance with some cleanup but mostly unprocessed and untokenized.
This column may or may not be a useful source of features when the utterance solely consists of
some kind of noise.
