#-*- coding: utf-8 -*- 
#(for potential non-ASCII encoding)#Tool for the Automatic Analysis of COhesion

from __future__ import division
import Tkinter as tk
import tkFont
import tkFileDialog
import Tkconstants
import os
import re
import sys 
import glob
import math
import re
import platform
import shutil
import subprocess

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

###THIS IS NEW IN V2.0.1 ###
from threading import Thread
import Queue


#This creates a que in which the core TAACO program can communicate with the GUI
dataQueue = Queue.Queue()

#This creates the message for the progress box (and puts it in the dataQueue)
progress = "...Waiting for Data to Process"
dataQueue.put(progress)

#Def1 is the core TAALES program; args is information passed to TAALES
def start_thread(def1, arg1, arg2, arg3): 
	t = Thread(target=def1, args=(arg1, arg2, arg3))
	t.start()

#This allows for a packaged gui to find the resource files.
def resource_path(relative):
	if hasattr(sys, "_MEIPASS"):
		return os.path.join(sys._MEIPASS, relative)
	return os.path.join(relative)

if platform.system() == "Darwin":
	system = "M"
	title_size = 16
	font_size = 14
	geom_size = "425x575"
	color = "#FFFF99"
elif platform.system() == "Windows":
	system = "W"
	title_size = 12
	font_size = 12
	geom_size = "475x575"
	color = "#FFFF99"
elif platform.system() == "Linux":
	system = "L"
	title_size = 12
	font_size = 12
	geom_size = "525x600"
	color = "#FFFF99"

def start_watcher(def2, count, folder):
	t2 = Thread(target=def2, args =(count,folder))
	t2.start()

def watcher(count, folder):
	import glob
	import time
	counter = 1

	while count>len(glob.glob(folder+"*")):
		#print "Count ", count
		#counter = 1
		if len(glob.glob(folder+"*")) == 0:
			if counter == 1:
				output = "Starting Stanford CoreNLP..."
				counter+=1
			elif counter == 2:
				output = "Starting Stanford CoreNLP."
				counter+=1
			elif counter == 3:
				output = "Starting Stanford CoreNLP.."
				counter+=1
				counter = 1
		else:
			output = "CoreNLP has tagged " + str(len(glob.glob(folder+"*"))) + " of " + str(count) + " paragraphs."
		dataQueue.put(output)
		root.update_idletasks()
		
		time.sleep(.3) #seconds it waits before checking again  

class MyApp:
	def __init__(self, parent):
		
		#Creates font styles
		helv14= tkFont.Font(family= "Helvetica Neue", size=font_size)
		times14= tkFont.Font(family= "Lucida Grande", size=font_size)
		helv16= tkFont.Font(family= "Helvetica Neue", size = title_size, weight = "bold", slant = "italic")
		#This defines the GUI parent
		
		self.myParent = parent
		
		
		#This creates the header text
		self.spacer1= tk.Label(parent, text= "Tool for the Automatic Analysis of Lexical Sophistication", font = helv16, background = color)
		self.spacer1.pack()
		
		#This creates a frame for the meat of the GUI
		self.thestuff= tk.Frame(parent, background =color)
		self.thestuff.pack()
		
		self.myContainer1= tk.Frame(self.thestuff, background = color)
		self.myContainer1.pack(side = tk.RIGHT, expand= tk.TRUE)

		self.labelframe2 = tk.LabelFrame(self.myContainer1, text= "Instructions", background = color)
		self.labelframe2.pack(expand=tk.TRUE)
		
		#This creates the list of instructions.
		self.instruct = tk.Button(self.myContainer1, text = "Instructions", justify = tk.LEFT)
		self.instruct.pack()
		self.instruct.bind("<Button-1>", self.instruct_mess)

		self.checkboxframe = tk.LabelFrame(self.myContainer1, text= "Options", background = color, width = "45")
		self.checkboxframe.pack(expand=tk.TRUE)
		
		self.type_frame = tk.LabelFrame(self.checkboxframe, text= "Lemma tokens to analyze for overlap and TTR", background = color, width = "45")
		self.type_frame.pack(expand=tk.TRUE)

		self.overlap_frame = tk.LabelFrame(self.checkboxframe, text= "Overlap options", background = color, width = "45")
		self.overlap_frame.pack(expand=tk.TRUE)

		self.other_frame = tk.LabelFrame(self.checkboxframe, text= "Other indices", background = color, width = "45")
		self.other_frame.pack(expand=tk.TRUE)

		self.diag_frame = tk.LabelFrame(self.myContainer1, text= "Diagnostic output options", background = color, width = "45")
		self.diag_frame.pack(expand=tk.TRUE)
				
		self.all_frame = tk.LabelFrame(self.checkboxframe, background = color, width = "45")
		self.all_frame.pack(expand=tk.TRUE)
		
		self.cb1_var = tk.IntVar()			
		self.cb1 = tk.Checkbutton(self.type_frame, text="All", variable=self.cb1_var,background = color)
		self.cb1.grid(row=1,column=1, sticky = "W")		
		self.cb1.deselect()

		self.cb2_var = tk.IntVar()			
		self.cb2 = tk.Checkbutton(self.type_frame, text="Content", variable=self.cb2_var,background = color)
		self.cb2.grid(row=1,column=2, sticky = "W")		
		self.cb2.select()

		self.cb3_var = tk.IntVar()			
		self.cb3 = tk.Checkbutton(self.type_frame, text="Function", variable=self.cb3_var,background = color)
		self.cb3.grid(row=1,column=3, sticky = "W")		
		self.cb3.deselect()		

		self.cb4_var = tk.IntVar()			
		self.cb4 = tk.Checkbutton(self.type_frame, text="Noun", variable=self.cb4_var,background = color)
		self.cb4.grid(row=1,column=4, sticky = "W")		
		self.cb4.deselect()

		self.cb5_var = tk.IntVar()			
		self.cb5 = tk.Checkbutton(self.type_frame, text="Pronoun", variable=self.cb5_var,background = color)
		self.cb5.grid(row=1,column=5, sticky = "W")		
		self.cb5.deselect()

		self.cb6_var = tk.IntVar()			
		self.cb6 = tk.Checkbutton(self.type_frame, text="Argument", variable=self.cb6_var,background = color)
		self.cb6.grid(row=2,column=1, sticky = "W")		
		self.cb6.select()
		
		self.cb7_var = tk.IntVar()			
		self.cb7 = tk.Checkbutton(self.type_frame, text="Verb", variable=self.cb7_var,background = color)
		self.cb7.grid(row=2,column=2, sticky = "W")		
		self.cb7.select()

		self.cb8_var = tk.IntVar()			
		self.cb8 = tk.Checkbutton(self.type_frame, text="ADJ", variable=self.cb8_var,background = color)
		self.cb8.grid(row=2,column=3, sticky = "W")		
		self.cb8.deselect()

		self.cb9_var = tk.IntVar()			
		self.cb9 = tk.Checkbutton(self.type_frame, text="ADV", variable=self.cb9_var,background = color)
		self.cb9.grid(row=2,column=4, sticky = "W")		
		self.cb9.deselect()

		self.cb10_var = tk.IntVar()			
		self.cb10 = tk.Checkbutton(self.overlap_frame, text="Sentence", variable=self.cb10_var,background = color)
		self.cb10.grid(row=1,column=1, sticky = "W")		
		self.cb10.select()

		self.cb11_var = tk.IntVar()			
		self.cb11 = tk.Checkbutton(self.overlap_frame, text="Paragraph", variable=self.cb11_var,background = color)
		self.cb11.grid(row=1,column=2, sticky = "W")		
		self.cb11.deselect()

		self.cb12_var = tk.IntVar()			
		self.cb12 = tk.Checkbutton(self.overlap_frame, text="Adjacent", variable=self.cb12_var,background = color)
		self.cb12.grid(row=1,column=3, sticky = "W")		
		self.cb12.select()

		self.cb13_var = tk.IntVar()			
		self.cb13 = tk.Checkbutton(self.overlap_frame, text="Adjacent 2", variable=self.cb13_var,background = color)
		self.cb13.grid(row=1,column=4, sticky = "W")		
		self.cb13.deselect()

		self.cb14_var = tk.IntVar()			
		self.cb14 = tk.Checkbutton(self.other_frame, text="TTR", variable=self.cb14_var,background = color)
		self.cb14.grid(row=1,column=1, sticky = "W")		
		self.cb14.deselect()

		self.cb15_var = tk.IntVar()			
		self.cb15 = tk.Checkbutton(self.other_frame, text="Connectives", variable=self.cb15_var,background = color)
		self.cb15.grid(row=1,column=2, sticky = "W")		
		self.cb15.select()

		self.cb16_var = tk.IntVar()			
		self.cb16 = tk.Checkbutton(self.other_frame, text="Givenness", variable=self.cb16_var,background = color)
		self.cb16.grid(row=1,column=3, sticky = "W")		
		self.cb16.deselect()

		#the next three will be in V2.0
		#self.cb17_var = tk.IntVar()			
		#self.cb17 = tk.Checkbutton(self.other_frame, text="LSA", variable=self.cb17_var,background = color, state=tk.DISABLED)
		#self.cb17.grid(row=2,column=1, sticky = "W")		
		#self.cb17.deselect()

		#self.cb18_var = tk.IntVar()			
		#self.cb18 = tk.Checkbutton(self.other_frame, text="LDA", variable=self.cb18_var,background = color, state=tk.DISABLED)
		#self.cb18.grid(row=2,column=2, sticky = "W")		
		#self.cb18.deselect()

		#self.cb19_var = tk.IntVar()			
		#self.cb19 = tk.Checkbutton(self.other_frame, text="word2vec", variable=self.cb19_var,background = color, state=tk.DISABLED)
		#self.cb19.grid(row=2,column=3, sticky = "W")		
		#self.cb19.deselect()

		self.cb20_var = tk.IntVar()			
		self.cb20 = tk.Checkbutton(self.other_frame, text="Syn overlap", variable=self.cb20_var,background = color)
		self.cb20.grid(row=1,column=4, sticky = "W")		
		self.cb20.deselect()

		self.cb21_var = tk.IntVar()			
		self.cb21 = tk.Checkbutton(self.type_frame, text="N-grams", variable=self.cb21_var,background = color)
		self.cb21.grid(row=2,column=5, sticky = "W")		
		self.cb21.deselect()

		self.cb22_var = tk.IntVar()
		self.cb22 = tk.Checkbutton(self.diag_frame, text="Output tagged files", variable=self.cb22_var,background = color)
		self.cb22.grid(row=1,column=2, sticky = "W")	
		self.cb22.select()

		self.cb23_var = tk.IntVar()
		self.cb23 = tk.Checkbutton(self.diag_frame, text="Output diagnostic file", variable=self.cb23_var,background = color)
		self.cb23.grid(row=1,column=1, sticky = "W")	
		self.cb23.select()



		self.var_list = ["null", self.cb1_var, self.cb2_var,self.cb3_var,self.cb4_var,self.cb5_var,self.cb6_var,self.cb7_var,self.cb8_var,self.cb9_var,self.cb10_var,self.cb11_var,self.cb12_var,self.cb13_var,self.cb14_var,self.cb15_var,self.cb16_var,"null","null","null",self.cb20_var,self.cb21_var,self.cb22_var,self.cb23_var]
		
		self.box_list = [self.cb1, self.cb2,self.cb3,self.cb4,self.cb5,self.cb6,self.cb7,self.cb8,self.cb9,self.cb10,self.cb11,self.cb12,self.cb13,self.cb14,self.cb15,self.cb16,self.cb20,self.cb21]



		self.cb_all = tk.Button(self.all_frame, text = "Select All",justify = tk.LEFT)
		self.cb_all.grid(row=1, column = 1, sticky = "W")
		self.cb_all.bind("<Button-1>", self.cb_all_Click)

		self.cb_none = tk.Button(self.all_frame, text = "Select None")
		self.cb_none.grid(row=1, column = 3)
		self.cb_none.bind("<Button-1>", self.cb_none_Click)

		self.button_spacer = tk.Label(self.all_frame, text= "            ", background = color)
		self.button_spacer.grid(row=1, column = 2)

		
		#Creates Label Frame for Data Input area
		self.secondframe= tk.LabelFrame(self.myContainer1, text= "Data Input", background = color)
		self.secondframe.pack(expand=tk.TRUE) 
		
		#This Places the first button under the instructions.
		self.button1 = tk.Button(self.secondframe)
		self.button1.configure(text= "Select Input Folder")
		self.button1.pack()
		
		#This tells the button what to do when clicked.	 Currently, only a left-click
		#makes the button do anything (e.g. <Button-1>). The second argument is a "def"
		#That is defined later in the program.
		self.button1.bind("<Button-1>", self.button1Click)
		
		#Creates default dirname so if statement in Process Texts can check to see
		#if a directory name has been chosen
		self.dirname = ""
		
		#This creates a label for the first program input (Input Directory)
		self.inputdirlabel =tk.LabelFrame(self.secondframe, height = "1", width= "45", padx = "4", text = "Your selected input folder:", background = color)
		self.inputdirlabel.pack()
		
		#Creates label that informs user which directory has been chosen
		directoryprompt = "(No Folder Chosen)"
		self.inputdirchosen = tk.Label(self.inputdirlabel, height= "1", width= "44", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text = directoryprompt)
		self.inputdirchosen.pack()
		
		#This creates the Output Directory button.
		self.button2 = tk.Button(self.secondframe)
		self.button2["text"]= "Select Output Filename"
		#This tells the button what to do if clicked.
		self.button2.bind("<Button-1>", self.button2Click)
		self.button2.pack()
		self.outdirname = ""
				
		#Creates a label for the second program input (Output Directory)
		self.outputdirlabel = tk.LabelFrame(self.secondframe, height = "1", width= "45", padx = "4", text = "Your selected output filename:", background = color)
		self.outputdirlabel.pack()
				
		#Creates a label that informs sure which directory has been chosen
		outdirectoryprompt = "(No Output Filename Chosen)"
		self.outputdirchosen = tk.Label(self.outputdirlabel, height= "1", width= "44", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text = outdirectoryprompt)
		self.outputdirchosen.pack()
		
		self.BottomSpace= tk.LabelFrame(self.myContainer1, text = "Run Program", background = color)
		self.BottomSpace.pack()

		self.button3= tk.Button(self.BottomSpace)
		self.button3["text"] = "Process Texts"
		self.button3.bind("<Button-1>", self.runprogram)
		self.button3.pack()

		self.progresslabelframe = tk.LabelFrame(self.BottomSpace, text= "Program Status", background = color)
		self.progresslabelframe.pack(expand= tk.TRUE)
		
		self.progress= tk.Label(self.progresslabelframe, height= "1", width= "45", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text=progress)
		self.progress.pack()
		
		self.poll(self.progress)
	
	def cb_all_Click(self, event):
		for items in self.box_list:
			items.select()
	
	def cb_none_Click(self, event):
		for items in self.box_list:
			items.deselect()
			
	def instruct_mess(self, event):
		import tkMessageBox
		tkMessageBox.showinfo("Instructions", "1. Select desired indices\n2. Choose the input folder (where your files are).\n3. Name your output file \n4. Press the 'Process Texts' button.")

	def entry1Return(self,event):
		input= self.entry1.get()
		self.input2 = input + ".csv"
		self.filechosenchosen.config(text = self.input2)
		self.filechosenchosen.update_idletasks()
	
	#Following is an example of how we can update the information from users...
	def button1Click(self, event):
		#import Tkinter, 
		import tkFileDialog
		self.dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
		self.displayinputtext = '.../'+self.dirname.split('/')[-1]
		self.inputdirchosen.config(text = self.displayinputtext)
		
	def button2Click(self, event):
		#self.outdirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
		self.outdirname = tkFileDialog.asksaveasfilename(parent=root, defaultextension = ".csv", initialfile = "results",title='Choose Output Filename')
		print self.outdirname
		if self.outdirname == "":
			self.displayoutputtext = "(No Output Filename Chosen)"
		else: self.displayoutputtext = '.../' + self.outdirname.split('/')[-1]
		self.outputdirchosen.config(text = self.displayoutputtext)
		
	def runprogram(self, event):
		self.poll(self.progress)
		start_thread(main, self.dirname, self.outdirname, self.var_list)

	def poll(self, function):
		
		self.myParent.after(10, self.poll, function)
		try:
			function.config(text = dataQueue.get(block=False))
			
		except Queue.Empty:
			pass

def main(indir, outdir, var_list):			
	import tkMessageBox
	options = []
	for items in var_list:
		if items == "null":
			options.append(0)
		elif items.get() == 1:
			options.append(1)
		else: options.append(0)
	
	#check to see if overlap boxes have been checked:
	overlap_box = sum(options[1:8])
	segment_box = sum([options[10],options[11]])
	adjacent_box = sum([options[12],options[13]])
	ttr_box = overlap_box + options[21]
	all_boxes = sum(options[:21])
	
	#interface validation:
	
	if indir is "":
		tkMessageBox.showinfo("Supply Information", "Choose an input directory!")
	
	elif outdir is "":
		tkMessageBox.showinfo("Choose Output Filename", "Choose an output filename!")
	
	elif all_boxes == 0:
		tkMessageBox.showinfo("Choose Indices", "Make an index selection!")
	
	elif overlap_box != 0 and options[14] == 0 and segment_box == 0:
		tkMessageBox.showinfo("Make an Overlap Choice", "Choose Sentence, Paragraph, and/or TTR!")
	
	elif overlap_box != 0 and options[14] == 0 and adjacent_box == 0:
		tkMessageBox.showinfo("Make an Overlap Choice", "Choose 'Adjacent' and/or 'Adjacent 2'!")
	
	elif segment_box != 0 and overlap_box == 0:
		tkMessageBox.showinfo("Make an Overlap Choice", "Choose which lemma tokens to analyze!")
	
	elif adjacent_box != 0 and overlap_box == 0:
		tkMessageBox.showinfo("Make an Overlap Choice", "Choose which lemma tokens to analyze!")
	
	elif options[14] == 1 and ttr_box == 0:
		tkMessageBox.showinfo("Make a TTR Choice", "Choose which lemma tokens to analyze!")
	
		
	else:
	#if indir is not "" and outdir is not "":
		#V. 1.5 was previously called version 2.0.20
				
		dataQueue.put("Starting TAACO...")

		#thus begins the text analysis portion of the program
		import glob
		import math
		
		def call_stan_corenlp(class_path, file_list, output_folder, memory, nthreads): #for CoreNLP 3.5.1 (most recent compatible version)
			#mac osx call:
			if system == "M" or system == "L":
				call_parser = "java -cp "+ class_path +"*: -Xmx" + memory + "g edu.stanford.nlp.pipeline.StanfordCoreNLP -threads "+ nthreads + " -annotators tokenize,ssplit,pos,lemma -filelist " + file_list + " -outputDirectory "+ output_folder
			#windows call:
			elif system == "W":
				call_parser = "java -cp "+ class_path +"*; -Xmx" + memory + "g edu.stanford.nlp.pipeline.StanfordCoreNLP -threads "+ nthreads + " -annotators tokenize,ssplit,pos,lemma -filelist " + file_list + " -outputDirectory "+ output_folder

			count = len(file(file_list, "rU").readlines())
			folder = output_folder
			print "starting checker"
			start_watcher(watcher, count, folder)
			
			subprocess.call(call_parser, shell=True) #This watches the output folder until all files have been parsed

		def dicter(spread_name):
			spreadsheet = file(resource_path(spread_name), "rU").read().split("\n")
			dict = {}
			for line in spreadsheet:
				if line == "":
					continue
				if line[0] == "#":
					continue
				vars = line.split("\t")
				if len(vars)<2:
					continue
				dict[vars[0]] = vars[1:]
			
			return dict
		
		def indexer(header_list, index_list, name, index):
			header_list.append(name)
			index_list.append(index)
		
		#This function deals with denominator issues that can kill the program:
		def safe_divide(numerator, denominator):
			if denominator == 0:
				index = 0
			else: index = numerator/denominator
			return index

		#This is for single givenness... if a word only occurs once in a text, the counter increases by one
		def single_givenness_counter(text):
			counter = 0
			for item in text:
				if text.count(item) == 1:
					counter+= 1
			return counter

		#This is for repeated givenness... if a word occurs more than once in a text, the counter increases by one
		def repeated_givenness_counter(text):
			counter = 0
			for item in text:
				if text.count(item) > 1:
					counter+= 1
			return counter

		def n_grammer(text, length, list = None):
			counter = 0
			ngram_text = []
			for word in text:
				ngram = text[counter:(counter+length)]
				if len(ngram)> (length-1):
					ngram_text.append(" ".join(str(x) for x in ngram))		
				counter+=1
			if list is not None:
				for item in ngram_text:
					#print item
					list.append(item)
			else:
				return ngram_text
		
		
		#revised version (6/19/17):
		def overlap_counter(header_list, index_list, name_suffix, list, seg_1, seg_2):# this completes all overlap functions:
			#print list
			## need to add check to ensure that list is a list of lists
			
			#first we have counters:
			
			n_segments = len(list) #number of sentences or paragraphs
			
			#this next section deals with texts that only have one segment
			if n_segments < 2:
				if seg_1 == 1:
					pre_header_list = ["adjacent_overlap_" + name_suffix, "adjacent_overlap_" + name_suffix + "_div_seg", "adjacent_overlap_binary_" + name_suffix]
					for header in pre_header_list: header_list.append(header)
					pre_index_list = [0,0,0]
					for pre_index in pre_index_list: index_list.append(pre_index)
				
				if seg_2 == 1:
					pre_header_list = [ "adjacent_overlap_2_"+name_suffix,  "adjacent_overlap_2_" + name_suffix + "_div_seg",  "adjacent_overlap_binary_2_"+ name_suffix]
					for header in pre_header_list: header_list.append(header)					
					pre_index_list = [0,0,0]
					for pre_index in pre_index_list: index_list.append(pre_index)

			
			#this is the "normal" procedure
			else:	
								
				single_overlap_denominator = 0
				double_overlap_denominator = 0
				
				overlap_counter_1 = 0
				overlap_counter_2 = 0
				binary_count_1 = 0
				binary_count_2 = 0
						
				for number in range (n_segments-1):
					#print number, "of", n_segments-1
					next_item_overlap = []#list so that overlap can be recovered for post-hoc
					next_two_item_overlap = []#list so that overlap can be recovered for post-hoc
				

					if number < n_segments -3 or number == n_segments -3: #Make sure we didn't go too far
						for items in set(list[number]):
							single_overlap_denominator +=1
							double_overlap_denominator +=1
							if items in list[number + 1]:
								next_item_overlap.append(items)
	
							if items in list[number + 1] or items in list[number + 2]:
								next_two_item_overlap.append(items)

					else: #Make sure we didn't go too far
						for items in set(list[number]):
							single_overlap_denominator +=1
							if items in list[number + 1]:
								next_item_overlap.append(items)
								
							
					overlap_counter_1 += len(next_item_overlap)
					overlap_counter_2 += len(next_two_item_overlap)
					print next_two_item_overlap
					if len(next_item_overlap) > 0: binary_count_1 += 1
					if len(next_two_item_overlap) > 0: binary_count_2 += 1
												
				if seg_1 == 1:
					overlap_1_nwords = safe_divide(overlap_counter_1, single_overlap_denominator)			
					overlap_1_nseg = safe_divide(overlap_counter_1, n_segments - 1)
					binary_1_nsent = safe_divide(binary_count_1, n_segments - 1)
					
					pre_header_list = ["adjacent_overlap_" + name_suffix, "adjacent_overlap_" + name_suffix + "_div_seg", "adjacent_overlap_binary_" + name_suffix]
					for header in pre_header_list: header_list.append(header)
					pre_index_list = [overlap_1_nwords, overlap_1_nseg,binary_1_nsent]
					for pre_index in pre_index_list: index_list.append(pre_index)
				
				if seg_2 == 1:
					overlap_2_nwords = safe_divide(overlap_counter_2, double_overlap_denominator)
					overlap_2_nseg = safe_divide(overlap_counter_2, n_segments - 2)
					binary_2_nsent = safe_divide(binary_count_2, n_segments - 2)
					
					pre_header_list = [ "adjacent_overlap_2_"+name_suffix,  "adjacent_overlap_2_" + name_suffix + "_div_seg",  "adjacent_overlap_binary_2_"+ name_suffix]
					for header in pre_header_list: header_list.append(header)					
					pre_index_list = [overlap_2_nwords,overlap_2_nseg,binary_2_nsent]
					for pre_index in pre_index_list: index_list.append(pre_index)
			
		#Revised 6-21-17
		def wordnet_dict_build(target_list, syn_dict):
			counter = len(target_list) #this is the number of paragraphs/sentences in the text
			
			#print "syn_counter", counter
			
			#holder structure:
			target_syn_dict = {}
			
			#creates a version of the text where each word is a list of synonyms:
			for i in range(counter): #iterates as many times as there are sentences/paragraphs in text
				
				if len(target_list[i]) < 1:
					target_syn_dict[i] = []
				else:
					syn_list1=[]
					for item in target_list[i]: #for word in sentence/paragraph
						#print "item: ", item
						if item in syn_dict:
							syns = syn_dict[item]
						else: syns = [item]
						syn_list1.append(syns)
		
					target_syn_dict[i]=syn_list1
			
			return target_syn_dict

		#Revised 6-21-17
		def syn_overlap(header_list, index_list, name_suffix, list, syn_dict):
			counter = len(list)		
			if counter < 2:
				syn_counter_norm = 0
			else:
				syn_counter=0
				for i in range(counter-1):
					for items in set(list[i]):
						for item in syn_dict[i+1]:
							if items in item:
								syn_counter +=1
				syn_counter_norm = safe_divide(syn_counter, counter-1) #note these are divided by segments
			header_list.append("syn_overlap_" + name_suffix)
			index_list.append(syn_counter_norm)
		
		#created 6-21-17 replaces regex_count
		def multi_list_counter(header_list, index_list, word_list, target_list, nwords):
			#print target_list
			for lines in word_list:
				if lines[0] == "#":
					continue
				line = lines.split("\t")	
				header_list.append(line[0])
				counter = 0
				for words in line[1:]:
					if words == "":
						continue
					#print words
					word = " " + words + " " # adds space to beginning and end to avoid over-counting (i.e., "forward" should not be a match for the conjunction "for")
					for sentences in target_list: #iterates through sentences to ensure that sentence boundaries are not crossed
						sentence = " " + " ".join(sentences)+ " " #turns list of words into a string, adds a space to the beginning and end
						#print sentence
						counter+= sentence.count(word) #counts list instances in each sentence
						#print words, sentence, sentence.count(words)
				index_list.append(safe_divide(counter,nwords)) #appends normed index to index_list
			
			
		### END DEFINED FUNCTIONS###
		
		variable_list = file(resource_path("Connectives_DICT_T3.txt"), 'rU').read().split("\n")
		wn_noun_dict = dicter(resource_path("wn_noun_2.txt"))
		wn_verb_dict = dicter(resource_path("wn_verb_2.txt"))
		
		punctuation = "' . , ? ! ) ( % / - _ -LRB- -RRB- SYM : ;".split(" ")
		punctuation.append('"')

		#filenames - takes from user-designated folder

		inputfile = indir + "/*.txt"
		filenames = glob.glob(inputfile)
		
		outf=file(outdir, "w")
		
		
		if options[22] == 1 or options[23] == 1:
			directory = outdir[:-4] + "_diagnostic/" #this is for diagnostic file
			if not os.path.exists(directory):
				os.makedirs(directory)
		
			for the_file in os.listdir(directory): #this cleans out the old diagnostic file (if applicable)
				file_path = os.path.join(directory, the_file)
				os.unlink(file_path)
		
		if options[23] == 1:
			basic_diag_file_name = directory + "_diagnostic_file.csv"
			basic_diag_file = file(basic_diag_file_name, "w")
			
		if not os.path.exists(resource_path("para_files/")):
			os.makedirs(resource_path("para_files/"))
			
		for the_file in os.listdir(resource_path("para_files/")): #this cleans out the old diagnostic file (if applicable)
			file_path = os.path.join(resource_path("para_files/"), the_file)
			os.unlink(file_path)
					
		#Iterates through target files:

		simple_filename_list = [] #this is for later file retrieval
		pre_file_counter = 0
		n_pre_files = len(filenames)
		
		for filename in filenames:
			if system == "M" or system == "L":
				simple_filename = filename.split("/")[-1]
			
			elif system == "W":
				simple_filename = filename.split("\\")[-1]
			
			simple_filename_list.append(simple_filename)
			
			pre_file_counter +=1
			
			dataQueue.put("TAACO is pre-processing " + str(pre_file_counter) + " of " + str(n_pre_files) + " files")
			root.update_idletasks()
			
			#simple read text, makes a single string:
			text= file(filename, 'rU').read()
			if len(text.split()) <=1:
				continue
	
			#creates paragraph separated version of text (which is a list of paragraphs):
			#print simple_filename
			para_text = text
			while "\t" in para_text:
				para_text = para_text.replace("\t", " ")
			#print "check1"			
			while "  " in para_text:
				para_text = para_text.replace("  ", " ")
			#print "check2"
			while "\t\t" in para_text:
				para_text.replace("\t\t","\t")
			#print "check3"			
			while "\n \n" in para_text:
				para_text = para_text.replace("\n \n", "\n")		
			#print "check4"
			while "\n\n" in para_text:
				para_text = para_text.replace("\n\n", "\n")


			
			if para_text[0] == "\n":
				para_text = para_text[1:]
			if para_text[-1] == "\n":
				para_text = para_text[:-1]
			para_text = para_text.split("\n")
			n_par = len(para_text)
			#print simple_filename, "\n", para_text
			len_last_para = len(para_text[-1].split(" "))
			
			#The following creates a file for each paragraph in the text. This is necessary
			#because the Stanford tokenizer is not sensitive to paragraph boundaries
			

			
			para_counter = 0	
			for item in para_text:
				out_filename = resource_path("para_files/") + simple_filename[:-4] + "_p" + str(para_counter) + ".txt"
				para_file = file(out_filename, "w")
				para_file.write(para_text[para_counter])
				para_file.flush()
				para_file.close()
				para_counter += 1
			
		para_folder = resource_path("para_files/")
		list_of_files = glob.glob(para_folder + "*.txt")

		file_list_file = file(para_folder + "_filelist.txt", "w")

		file_list = (para_folder + "_filelist.txt")
		##print "file list ", file_list
		for line in list_of_files:
			line = line + "\n"	
			file_list_file.write(line)
		file_list_file.flush()
		file_list_file.close()
		
		#For Stanford Tagger Operations:
		###First, we clean up all of the folders to make sure we only process the data we want:###
		if not os.path.exists(resource_path("parsed_files/")):
			os.makedirs(resource_path("parsed_files/"))
	
		folder_list = [resource_path('parsed_files/')]

		for folder in folder_list:
			for the_file in os.listdir(folder):
				file_path = os.path.join(folder, the_file)
				os.unlink(file_path)

		current_directory = resource_path("./")
		#print "current_directory :", current_directory
		stan_file_list = file_list
		stan_output_folder = resource_path("parsed_files/")
		memory = "3"
		nthreads = "2"
		
		call_stan_corenlp(current_directory, stan_file_list, stan_output_folder, memory, nthreads)

		#Now that the texts have been separated into paragraphs, tokenized, and POS tagged,
		#we start the actual text analysis
		
		parsed_file_folder = resource_path("parsed_files/")
		parsed_file_list = glob.glob(parsed_file_folder + "*.xml")

		para_file_dict = {} #this will consist of original final names (key) and lists of paragraph filenames (values)
		for items in simple_filename_list:
			para_file_dict[items] = []
			for p_files in parsed_file_list:
				#print "p_file:", p_files
				if system == "M" or system == "L":
					simple_p_file = p_files.split("/")[-1]
				if system == "W":
					simple_p_file = p_files.split("\\")[-1]
				
				simple_p_file = "_".join(simple_p_file.split("_")[:-1]) + ".txt"
				if items == simple_p_file:
					para_file_dict[items].append(p_files)
		
		### THESE ARE PERTINENT FOR ALL IMPORTANT INDICES ####
		noun_tags = ["NN", "NNS", "NNP", "NNPS"] #consider whether to identify gerunds
		proper_n = ["NNP", "NNPS"]
		no_proper = ["NN", "NNS"]
		pronouns = ["PRP", "PRP$"]
		adjectives = ["JJ", "JJR", "JJS"]
		verbs = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
		adverbs = ["RB", "RBR", "RBS"]
		content = ["NN", "NNS", "NNP", "NNPS","JJ", "JJR", "JJS","VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD","RB", "RBR", "RBS"]
		###
		
		###Givenness pronouns:
		givenness_prp = "he she her him his they them their himself herself themselves his their it its".split(" ")
		###
		
		file_number = 0	#this is so that the header list works correctly
		n_files = len(simple_filename_list)
		
		for items in simple_filename_list:
			output_filename = items
			
			if options[22] == 1:
				diagname = directory + output_filename[:-4] + "_diagnostic.txt"
				diag_file = file(diagname, "w")
				diag_file.write("word\tlemma\tPOS\tCW\FW\tother categories\n")
			
			header_list = ["Filename"]
			index_list = []
			
			diag_header_list = ["Filename"]
			diag_index_list = []
			
			filename1 = ("TAACO is processing " + str(file_number+1) + " of " + str(n_files) + " files") #these lines update the GUI
			dataQueue.put(filename1)
			root.update_idletasks()
			
			diagnostic_text = []
			givenness_prp_text = []
			raw_text = [] #all words, not lemmatized
			lemma_text = [] #all words, lemmatized
			content_text=[] #content words, lemmatized
			function_text=[] #function words, lemmatized
			noun_text=[] #nouns
			verb_text=[] #verbs 
			adj_text=[] #adjectives
			adv_text=[] #adverbs
			prp_text=[] #pronouns
			argument_text=[] #nouns + pronouns		

			para_raw_list=[]
			para_lemma_list=[]
			para_content_list=[]
			para_function_list=[]
			para_pos_noun_list=[] #nouns
			para_pos_verb_list=[] #verbs 
			para_pos_adj_list=[] #adjectives
			para_pos_adv_list=[] #adverbs
			para_pos_prp_list=[] #pronouns
			para_pos_argument_list=[] #nouns + pronouns		

			sent_raw_list=[]
			sent_lemma_list=[]
			sent_content_list=[]
			sent_function_list=[]
			sent_pos_noun_list=[] #nouns
			sent_pos_verb_list=[] #verbs 
			sent_pos_adj_list=[] #adjectives
			sent_pos_adv_list=[] #adverbs
			sent_pos_prp_list=[] #pronouns
			sent_pos_argument_list=[] #nouns + pronouns		

			text_items = {} #this will be the top-level organizer for the text?
			#print "dict:", para_file_dict
			for item in para_file_dict[items]: #iterates through paragraph files
				#print "item", item
				tree = ET.ElementTree(file=item) #this opens the file using an xml parser
				
				raw_list_para=[]
				lemma_list_para=[]
				content_list_para=[]
				function_list_para=[]
				pos_noun_list_para=[] #nouns
				pos_verb_list_para=[] #verbs 
				pos_adj_list_para=[] #adjectives
				pos_adv_list_para=[] #adverbs
				pos_prp_list_para=[] #pronouns
				pos_argument_list_para=[] #nouns + pronouns		

				for sentences in tree.iter("sentence"): #this iterates through sentences
					raw_list_sent=[]
					lemma_list_sent=[]
					content_list_sent=[]
					function_list_sent=[]
					pos_noun_list_sent=[] #nouns
					pos_verb_list_sent=[] #verbs 
					pos_adj_list_sent=[] #adjectives
					pos_adv_list_sent=[] #adverbs
					pos_prp_list_sent=[] #pronouns
					pos_argument_list_sent=[] #nouns + pronouns		
					
					for tokens in sentences.iter("token"): #this iterates through the tokens
						if tokens[4].text in punctuation:
							continue
						diagnostic_token = []
						diagnostic_token.append(tokens[0].text.lower()) #raw word
						diagnostic_token.append(tokens[1].text.lower())	#lemma word
						diagnostic_token.append(tokens[4].text)	#POS Tag
						
						#raw words
						raw_text.append(tokens[0].text.lower())
						raw_list_para.append(tokens[0].text.lower())
						raw_list_sent.append(tokens[0].text.lower())
						
						#lemmas
						lemma_text.append(tokens[1].text.lower())
						lemma_list_para.append(tokens[1].text.lower())
						lemma_list_sent.append(tokens[1].text.lower())
						
						if tokens[1].text.lower() in givenness_prp:
							givenness_prp_text.append(tokens[1].text.lower())
						
						if tokens[4].text in content:
							diagnostic_token.append("CW")
							content_text.append(tokens[1].text.lower())
							content_list_para.append(tokens[1].text.lower())
							content_list_sent.append(tokens[1].text.lower())
						
						if tokens[4].text not in content:
							diagnostic_token.append("FW")
							function_text.append(tokens[1].text.lower())
							function_list_para.append(tokens[1].text.lower())
							function_list_sent.append(tokens[1].text.lower())
						
						if tokens[4].text in noun_tags:
							diagnostic_token.append("NOUN")
							noun_text.append(tokens[1].text.lower())
							pos_noun_list_para.append(tokens[1].text.lower())
							pos_noun_list_sent.append(tokens[1].text.lower())
						
						if tokens[4].text in verbs:
							diagnostic_token.append("VERB")
							verb_text.append(tokens[1].text.lower())
							pos_verb_list_para.append(tokens[1].text.lower())
							pos_verb_list_sent.append(tokens[1].text.lower())
						
						if tokens[4].text in adjectives:
							diagnostic_token.append("ADJ")
							adj_text.append(tokens[1].text.lower())
							pos_adj_list_para.append(tokens[1].text.lower())
							pos_adj_list_sent.append(tokens[1].text.lower())
						
						if tokens[4].text in adverbs:
							diagnostic_token.append("ADV")
							adv_text.append(tokens[1].text.lower())
							pos_adv_list_para.append(tokens[1].text.lower())
							pos_adv_list_sent.append(tokens[1].text.lower())
						
						if tokens[4].text in pronouns:
							diagnostic_token.append("PRONOUN")
							prp_text.append(tokens[1].text.lower())
							pos_prp_list_para.append(tokens[1].text.lower())
							pos_prp_list_sent.append(tokens[1].text.lower())
						
						if tokens[4].text in pronouns or tokens[4].text in noun_tags:
							diagnostic_token.append("ARGUMENT")
							argument_text.append(tokens[1].text.lower())
							pos_argument_list_para.append(tokens[1].text.lower())
							pos_argument_list_sent.append(tokens[1].text.lower())
						
						diagnostic_text.append(diagnostic_token)
						
					#add sentence lists to full sentence list
					diagnostic_text.append(["\nsentence break\n"]) #adds sentence indicator for diagnostic text
					sent_raw_list.append(raw_list_sent)
					sent_lemma_list.append(lemma_list_sent)
					sent_content_list.append(content_list_sent)
					sent_function_list.append(function_list_sent)
					sent_pos_noun_list.append(pos_noun_list_sent)
					sent_pos_verb_list.append(pos_verb_list_sent)
					sent_pos_adj_list.append(pos_adj_list_sent)
					sent_pos_adv_list.append(pos_adv_list_sent)
					sent_pos_prp_list.append(pos_prp_list_sent)
					sent_pos_argument_list.append(pos_argument_list_sent)
								
				#adds paragraph lists to full paragraph lists
				diagnostic_text.append(["\nparagraph break\n"]) #adds paragraph indicator for diagnostic text
				para_raw_list.append(raw_list_para)
				para_lemma_list.append(lemma_list_para)
				para_content_list.append(content_list_para)
				para_function_list.append(function_list_para)
				para_pos_noun_list.append(pos_noun_list_para)
				para_pos_verb_list.append(pos_verb_list_para)
				para_pos_adj_list.append(pos_adj_list_para)
				para_pos_adv_list.append(pos_adv_list_para)
				para_pos_prp_list.append(pos_prp_list_para)
				para_pos_argument_list.append(pos_argument_list_para)
			
			#basic indices (including simple ttr):	
			
			#For TAACO 2.0: add alternative ttr calculations (e.g., MATTR)
			nsentences = len (sent_lemma_list)
			nparagraphs = len(para_lemma_list)
		
						
			#raw words
			nwords = len(raw_text)
			nprps = len(prp_text)
			nnouns = len(noun_text)

			if options[23] == 1:
					indexer(diag_header_list, diag_index_list, "nwords", nwords)
					indexer(diag_header_list, diag_index_list, "nsentences", nsentences)
					indexer(diag_header_list, diag_index_list, "nparagraphs", nparagraphs)
								
			if options[14] == 1:
				#all words (lemmatized)						
				if options[1] == 1:
					nlemmas = len(lemma_text)
					nlemma_types = len(set(lemma_text))
					indexer(header_list, index_list, "lemma_ttr", safe_divide(nlemma_types,nlemmas))
					if options[23] == 1:
						indexer(diag_header_list, diag_index_list, "nlemmas", nlemmas)
						indexer(diag_header_list, diag_index_list, "nlemma_types", nlemma_types)
			
				#content_words; note, these are ALL LEMMATIZED!!!			
				if options[2] == 1:	
					ncontent_words= len(content_text)
					ncontent_types= len(set(content_text))
					indexer(header_list, index_list, "content_ttr", safe_divide(ncontent_types, ncontent_words))
					
					if options[23] == 1:
						indexer(diag_header_list, diag_index_list, "ncontent_words", ncontent_words)
						indexer(diag_header_list, diag_index_list, "ncontent_types", ncontent_types)
			
				#function words; note, these are ALL LEMMATIZED!!!
			
				if options[3] == 1:			
					nfunction_words= len(function_text)
					nfunction_types= len(set(function_text))

					indexer(header_list, index_list, "function_ttr", safe_divide(nfunction_types, nfunction_words))
					if options[23] == 1:
						indexer(diag_header_list, diag_index_list, "nfunction_words", nfunction_words)
						indexer(diag_header_list, diag_index_list, "nfunction_types", nfunction_types)

				if options[4] == 1:					
					nnouns_types = len(set(noun_text))
					indexer(header_list, index_list, "noun_ttr", safe_divide(nnouns_types, nnouns))

					if options[23] == 1:
						indexer(diag_header_list, diag_index_list, "n_nouns", nnouns)
						indexer(diag_header_list, diag_index_list, "n_noun_types", nnouns_types)

				if options[7] == 1:					
					nverbs = len(verb_text)
					nverbs_types = len(set(verb_text))
					indexer(header_list, index_list, "verb_ttr", safe_divide(nverbs_types, nverbs))

					if options[23] == 1:
						indexer(diag_header_list, diag_index_list, "n_verbs", nverbs)
						indexer(diag_header_list, diag_index_list, "n_verb_types", nverbs_types)

				if options[8] == 1:					
					nadjs = len(adj_text)
					nadjs_types = len(set(adj_text))
					indexer(header_list, index_list, "adj_ttr", safe_divide(nadjs_types, nadjs))

					if options[23] == 1:
						indexer(diag_header_list, diag_index_list, "n_adjs", nadjs)
						indexer(diag_header_list, diag_index_list, "n_adj_types", nadjs_types)

				if options[9] == 1:					
					nadvs = len(adv_text)
					nadvs_types = len(set(adv_text))
					indexer(header_list, index_list, "adv_ttr", safe_divide(nadvs_types, nadvs))

					if options[23] == 1:
						indexer(diag_header_list, diag_index_list, "n_advs", nadvs)
						indexer(diag_header_list, diag_index_list, "n_adv_types", nadvs_types)

				
				if options[5] == 1:					
					nprps_types = len(set(prp_text))
					indexer(header_list, index_list, "prp_ttr", safe_divide(nprps_types, nprps))

					if options[23] == 1:
						indexer(diag_header_list, diag_index_list, "n_prps", nprps)
						indexer(diag_header_list, diag_index_list, "n_prp_types", nprps_types)

				if options[6] == 1:					
					narguments = len(argument_text)
					narguments_types = len(set(argument_text))
					indexer(header_list, index_list, "argument_ttr", safe_divide(narguments_types, narguments))

					if options[23] == 1:
						indexer(diag_header_list, diag_index_list, "n_arguments", narguments)
						indexer(diag_header_list, diag_index_list, "n_argument_types", narguments_types)


				### N-GRAM INDICES####
				if options[21] ==1:
					bigram_lemma_text = n_grammer(lemma_text, 2)
					n_bigram_lemmas = len(bigram_lemma_text)
					n_bigram_lemma_types = len(set(bigram_lemma_text))
					trigram_lemma_text = n_grammer(lemma_text, 3)
					n_trigram_lemmas = len(trigram_lemma_text)
					n_trigram_lemma_types = len(set(trigram_lemma_text))			

					indexer(header_list, index_list, "bigram_lemma_ttr", safe_divide(n_bigram_lemma_types,n_bigram_lemmas))
					indexer(header_list, index_list, "trigram_lemma_ttr", safe_divide(n_trigram_lemma_types,n_trigram_lemmas))
					
					if options[23] == 1:
						indexer(diag_header_list, diag_index_list, "n_bigram_lemmas", n_bigram_lemmas)
						indexer(diag_header_list, diag_index_list, "n_bigram_lemma_types", n_bigram_lemma_types)
						indexer(diag_header_list, diag_index_list, "n_trigram_lemmas", n_trigram_lemmas)
						indexer(diag_header_list, diag_index_list, "n_trigram_lemma_types", n_trigram_lemma_types)
			### END N-GRAM INDICES###
			

			###Begin SENTENCE OVERLAP SECTION###
			
			#Overlap- Counts here are organized by list. For each list there are six counts and two ways to calculate most indices (/nwords or /sent_counter). Comments are given for the first set, all other sets are identical				
			#revised 6/20/17
			if options[10] ==1:
				if options[1]==1:
					overlap_counter(header_list, index_list, "all_sent", sent_lemma_list, options[12],options[13]) #all words, lemmatized
				if options[2]==1:
					overlap_counter(header_list, index_list, "cw_sent", sent_content_list, options[12],options[13]) #Content Words, Lemmatized
				if options[3]==1:
					overlap_counter(header_list, index_list, "fw_sent", sent_function_list, options[12],options[13]) #Function Words, Lemmatized
				if options[4]==1:
					overlap_counter(header_list, index_list, "noun_sent", sent_pos_noun_list, options[12],options[13]) #POS NOUN, Lemmatized
				if options[7]==1:
					overlap_counter(header_list, index_list, "verb_sent", sent_pos_verb_list, options[12],options[13]) #POS Verb, Lemmatized
				if options[8]==1:
					overlap_counter(header_list, index_list, "adj_sent", sent_pos_adj_list, options[12],options[13]) #POS Adj, Lemmatized
				if options[9]==1:
					overlap_counter(header_list, index_list, "adv_sent", sent_pos_adv_list, options[12],options[13]) #POS Adv, Lemmatized
				if options[5]==1:
					overlap_counter(header_list, index_list, "pronoun_sent", sent_pos_prp_list, options[12],options[13]) #POS PRP, Lemmatized
				if options[6]==1:
					overlap_counter(header_list, index_list, "argument_sent", sent_pos_argument_list, options[12],options[13]) #POS ARGUMENT (PRP + NOUN)


		###BEGIN PARAGRAPH OVERLAP SECTION###
			if options[11] ==1:

				if options[1]==1:
					overlap_counter(header_list, index_list, "all_para", para_lemma_list, options[12],options[13]) #all words, lemmatized
				if options[2]==1:
					overlap_counter(header_list, index_list, "cw_para", para_content_list, options[12],options[13]) #Content Words, Lemmatized
				if options[3]==1:
					overlap_counter(header_list, index_list, "fw_para", para_function_list, options[12],options[13]) #Function Words, Lemmatized
				if options[4]==1:
					overlap_counter(header_list, index_list, "noun_para", para_pos_noun_list, options[12],options[13]) #POS NOUN, Lemmatized
				if options[7]==1:
					overlap_counter(header_list, index_list, "verb_para", para_pos_verb_list, options[12],options[13]) #POS Verb, Lemmatized
				if options[8]==1:
					overlap_counter(header_list, index_list, "adj_para", para_pos_adj_list, options[12],options[13]) #POS Adj, Lemmatized
				if options[9]==1:
					overlap_counter(header_list, index_list, "adv_para", para_pos_adv_list, options[12],options[13]) #POS Adv, Lemmatized
				if options[5]==1:
					overlap_counter(header_list, index_list, "pronoun_para", para_pos_prp_list, options[12],options[13]) #POS PRP, Lemmatized
				if options[6]==1:
					overlap_counter(header_list, index_list, "argument_para", para_pos_argument_list, options[12],options[13]) #POS ARGUMENT (PRP + NOUN)

			###END PARAGRAPH OVERLAP SECTION###

			###BEGIN WORDNET OVERLAP SECTION###
			if options[20] ==1:
				#Syn Sentence Dictionaries
				noun_sent_syn_lemma_dict=wordnet_dict_build(sent_pos_noun_list, wn_noun_dict)
				verb_sent_syn_lemma_dict= wordnet_dict_build(sent_pos_verb_list, wn_verb_dict)

				#Syn Paragraph Dictionaries
				noun_para_syn_lemma_dict=wordnet_dict_build(para_pos_noun_list, wn_noun_dict)
				verb_para_syn_lemma_dict= wordnet_dict_build(para_pos_verb_list, wn_verb_dict)

				#Syn Sentence Overlap Indices
				noun_sent_syn_lemma_overlap = syn_overlap(header_list, index_list, "sent_noun", sent_pos_noun_list,noun_sent_syn_lemma_dict)
				verb_sent_syn_lemma_overlap = syn_overlap(header_list, index_list, "sent_verb", sent_pos_verb_list,verb_sent_syn_lemma_dict)

				#Syn Paragraph Overlap Indices
				noun_para_syn_lemma_overlap = syn_overlap(header_list, index_list, "para_noun", para_pos_noun_list, noun_para_syn_lemma_dict)
				verb_para_syn_lemma_overlap = syn_overlap(header_list, index_list, "para_verb", para_pos_verb_list, verb_para_syn_lemma_dict)

		###END WORDNET OVERLAP SECTION####silence		


		### DICTIONARY LIST SECTION - GOES BACK TO FIRST DEFINED FUNCTION###
			if options[15] ==1:
				multi_list_counter(header_list, index_list, variable_list, sent_raw_list, nwords)

		###END DICTIONARY LIST SECTION###	

		###Pronoun/Noun Ratio###
			if options[16] == 1:
				indexer(header_list, index_list, "pronoun_density", safe_divide(len(givenness_prp_text), nwords))
				indexer(header_list, index_list, "pronoun_noun_ratio", safe_divide(len(givenness_prp_text), nnouns))
			
			### GIVENNESS See DEFINED FUNCTIONS for givenness counters###
				indexer(header_list, index_list, "repeated_content_lemmas", safe_divide(repeated_givenness_counter(content_text), nwords))
				indexer(header_list, index_list, "repeated_content_and_pronoun_lemmas", safe_divide((repeated_givenness_counter(content_text) + repeated_givenness_counter(givenness_prp_text)),nwords))

		###END GIVENNESS###

			
			#this prints the diagnostic file
			if options[22] == 1:
				for list_items in diagnostic_text:
					print_items = "\t".join(list_items) + "\n"
					diag_file.write(print_items)
				diag_file.flush()
				diag_file.close()
				#end diagnostic file
			
			if options[23] == 1:
				if file_number == 0:
					diag_header_string = ",".join(diag_header_list)
					basic_diag_file.write ('{0}\n'
					.format(diag_header_string))
				
				diag_index_string_list = []
				
				for items in diag_index_list:
					diag_index_string_list.append(str(items))
				diag_string = ",".join(diag_index_string_list)
	
				basic_diag_file.write ('{0},{1}\n'
				.format(output_filename,diag_string))

			
			index_string_list=[] 
			if file_number == 0:
				#print "header string should print"
				header_string = ",".join(header_list)
				outf.write ('{0}\n'
				.format(header_string))
			
			file_number+=1
			
			for items in index_list:
				index_string_list.append(str(items))
			string = ",".join(index_string_list)
	
			outf.write ('{0},{1}\n'
			.format(output_filename,string))
					
		outf.flush()
		outf.close()
		
		if options[23] == 1:
			basic_diag_file.flush()
			basic_diag_file.close()
		
		#Closing Message to let user know that the program did something: (may need to be more sophisticated)	
		
		nfiles = len(filenames)
		finishmessage = ("Processed " + str(nfiles) + " Files")
		dataQueue.put(finishmessage)
		if system == "M":
			tkMessageBox.showinfo("Finished!", "TAACO has converted your files to numbers.\n\n Now the real work begins!")
			
class Catcher:
    def __init__(self, func, subst, widget):
        self.func = func
        self.subst = subst
        self.widget = widget

    def __call__(self, *args):
        try:
            if self.subst:
                args = apply(self.subst, args)
            return apply(self.func, args)
        except SystemExit, msg:
            raise SystemExit, msg
        except:
            import traceback
            import tkMessageBox
            ermessage = traceback.format_exc(1)
            ermessage = re.sub(r'.*(?=Error)', "", ermessage, flags=re.DOTALL)
            ermessage = "There was a problem processing your files:\n\n"+ermessage
            tkMessageBox.showerror("Error Message", ermessage)
            
root = tk.Tk()
root.wm_title("TAACO 1.5.2")
root.configure(background = '#FFFF99')
#sets starting size: NOTE: it doesn't appear as though Tkinter will let you make the 
#starting size smaller than the space needed for widgets.
root.geometry(geom_size)
tk.CallWrapper = Catcher
myapp = MyApp(root)
root.mainloop()