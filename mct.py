import argparse, os, sys, json
import tkinter as tk
from tkinter import filedialog as fd
import tkinter.scrolledtext as tkscrolled
from tkinter import ttk
import time
from googletrans import Translator

# Get Char Width Of Terminal
# Load Languages
languageDict = json.load(open("./lang.json"))
languages = list(languageDict)

# Translation
translator = Translator()
output = {}

# This Makes Sure That The Input File Is A JSON File And Exists

def EnsureExtension():
	class Run(argparse.Action):
		def __call__(self, parser, namespace, fname, option_string=None):
			if os.path.isfile(fname):
				ext = os.path.splitext(fname)[1][1:]
				if ext != "json":
					parser.error("Input file must be json")
				else:
					setattr(namespace, self.dest, fname)
			else:
				parser.error("File not found")
	return Run

parser = argparse.ArgumentParser(
	description="{} -i en_us.json -l french".format(os.path.basename(__file__)),
	formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument("-i", "--input", type=str, action=EnsureExtension(), help="Input file", required=True)
parser.add_argument("-l", "--language", choices=languages, type=str, help="Output language", default="french")
parser.add_argument("-d", "--debug", action='count', help="Displays debug per line", default=0)


# Translate Keep Vars Safe
def Translate(words, lang):
	words.replace("%1$s", "__0__").replace("$s", "__1__")
	translation = translator.translate(words, dest=lang).text
	untransform = translation.replace("__0__", "%1$s").replace("__1__", "$s")
	return untransform
	
def Evaluate(file, lang, debug, isGUI):
	# User Input Lang File (UTF8 For Accented Chars)
	data = json.load(open(file, encoding='utf-8'))
	sys.stdout.reconfigure(encoding='utf-8')
	i = 0
	for key in data:
		i += 1
		width = os.get_terminal_size()[0]-1
		percent = round(((i/len(data))*100)-0.5)
	
		translation = Translate(data[key], languageDict[lang]["code"])
		newLine = {key: translation}
		output.update(newLine)

		progress = ("[%-20s] %d%% %s" % ('='*(int)(percent/5), percent, "{}=>{}".format(data[key].replace("\n", "\\n"), translation.replace("\n", "\\n")) if debug > 0 else "")).ljust(width).encode(encoding='ascii',errors='replace').decode()
	
		sys.stdout.write('\r')
		sys.stdout.write(progress[:width])
		sys.stdout.flush()
	
	with open("{}\\{}.json".format(os.path.dirname(file),languageDict[lang]["mc"]), "w") as lang:
		jsonOutput = json.dumps(output, indent=4)
		lang.write(jsonOutput)


if not len(sys.argv) > 1:	# Run Without Args
	window = tk.Tk()
	window.title("MCT")
	window.minsize(450,650)
	window.geometry("1x1")
	window.columnconfigure(0, weight=1, pad=0)
	window.columnconfigure(1, weight=8, pad=0)
	window.rowconfigure(2,pad=0,weight=1)
	window.rowconfigure(3,pad=0)

	def getlang():
		filetypes = (('Json file', '*.json'), ('All Files', '*.*'))
		global filename
		filename = fd.askopenfile(
			title='Open a file',
			initialdir='./',
			filetypes=filetypes
		)
		if filename != None and os.path.isfile(filename.name):
				textShow = json.load(open(filename.name, 'r'))
				textDisp.config(state='normal')
				textDisp.delete('1.0', tk.END)
				textDisp.insert('1.0', json.dumps(textShow, indent=4))
				textDisp.config(state='disabled')

	def convert():
		if os.path.isfile(filename.name):
			Evaluate(filename.name, clicked.get(), True, True)

	selection = tk.Button(window, text='Select Lang File', command=getlang, borderwidth=3).grid(column=0, columnspan=2, row=0, padx=(5,5), pady=(5,0),sticky="WSE")

	tk.Label(window, text="Translate To Language:").grid(column=0, row=1, padx=(5,5), pady=(5,5),sticky="WN")
	clicked = tk.StringVar()
	clicked.set("afrikaans")
	ttk.Combobox(window, textvariable=clicked, values=languages).grid(column=1, row=1, padx=(5,5), pady=(5,5),sticky="WNE")
	
	textDisp = tkscrolled.ScrolledText(window, borderwidth=3, height=16, state="disabled")
	textDisp.config(bg="#10141c", fg="#bfbdb6")
	textDisp.grid(column=0, columnspan=2, row=2, padx=(5,5), pady=(5,5),sticky="WNSE")
	
	tk.Button(window, text='Convert', command=convert, borderwidth=3).grid(column=0, columnspan=2, row=3, padx=(5,5), pady=(5,5),sticky="ENSW")

	window.mainloop()
else:
	args = parser.parse_args()
	Evaluate(args.input, args.language, args.debug, False)