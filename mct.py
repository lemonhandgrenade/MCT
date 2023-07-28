import argparse, os, sys, json
import tkinter as tk
from tkinter import filedialog as fd
import tkinter.scrolledtext as tks
from tkinter import ttk
from googletrans import Translator

# Get Char Width Of Terminal
# Load Languages
languageDict = json.load(open("./lang.json"))
languages = list(languageDict)
languagesSplit = [l if i == len(languages)-1 else l + ", " for i, l in enumerate(languages)]
helpLanguages = [x for y in (languagesSplit[i:i+8] + ['\n  '] for i in range(0, len(languagesSplit), 8)) for x in y]
# Translation
methods = ["safe", "unsafe"]
translator = Translator()
output = {}

class CustomHelpFormatter(argparse.RawTextHelpFormatter):
	def _metavar_formatter(self, type, defaultMetavar):
		if type.metavar is not None:
			result = type.metavar
		elif type.choices is not None and len(type.choices) > 4:
			result = '{%s, %s .. %s}' % (type.choices[0], type.choices[1], max(type.choices))
		elif type.choices is not None:
			result = "{%s}" % ", ".join(type.choices)
		else:
			result = defaultMetavar

		def Format(tuple_size):
			return result if isinstance(result, tuple) else (result, ) * tuple_size
		return Format

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

parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter, usage='%(prog)s [options]')

parser.add_argument("-i", "--input", type=str, action=EnsureExtension(), help="path to the lang file\n  eg. ..\\en_us.json  Required\n ", required=True)
parser.add_argument("-l", "--language", choices=languages, type=str, help="language to be translated to (Default: french)\nAvailable Languages:\n  %s" % "".join(helpLanguages), default="french")
parser.add_argument("-m", "--method", choices=methods, type=str, help="translation mode\n  [Unsafe] translates all at once meaning more chance for bad translations but is hella fast\n  [Safe] is line by line so takes considerably longer but is more accurate\n ", default="safe")
parser.add_argument("-d", "--debug", action='count', help="displays last translated line in console\n ", default=0)

def ProgressBar(percent, debug, debugData=""):
	width = os.get_terminal_size()[0]-1
	progress = ("[%-20s] %d%% %s" % ('='*(int)(percent/5), percent, debugData if debug > 0 else "")).ljust(width).encode(encoding='ascii',errors='replace').decode()

	sys.stdout.write('\r')
	sys.stdout.write(progress[:width])
	sys.stdout.flush()

# Translate Keep Vars Safe
def Translate(words, lang):
	words.replace("%1$s", "__0__").replace("$s", "__1__")
	translation = translator.translate(words, dest=lang).text
	untransform = translation.replace("__0__", "%1$s").replace("__1__", "$s")
	return untransform

def Evaluate(file, lang, debug, isGUI, method = "safe"):

	def WriteFile(file,lang, data):
		with open("{}\\{}.json".format(os.path.dirname(file),languageDict[lang]["mc"]), "w") as langFile:
			jsonOutput = json.dumps(data, indent=4)
			langFile.write(jsonOutput)

	# User Input Lang File (UTF8 For Accented Chars)
	data = json.load(open(file, encoding='utf-8'))
	if method == "safe":
		i = 0
		for key in data:
			i += 1
			percent = round(((i/len(data))*100)-0.5)
		
			translation = Translate(data[key], languageDict[lang]["code"])
			newLine = {key: translation}
			output.update(newLine)
	
			ProgressBar(percent, debug, "{}=>{}".format(data[key].replace("\n", "\\n"), translation.replace("\n", "\\n")))
	
		WriteFile(file, lang, output)

	elif method == "unsafe":
		keys = list(data)
		values = list(data.values())

		batchString = "\n\n".join(values)
		translation = Translate(batchString, languageDict[lang]["code"])
		untransformed = translation.split("\n\n")

		if len(keys) != len(untransformed):
			return print("Error occured within unsafe translation")

		for i, key in enumerate(keys):
			newLine = {key: untransformed[i]}
			output.update(newLine)
			percent = round(((i+1)/len(keys)*100)-0.5)
			ProgressBar(percent, debug, "{}=>{}".format(key.replace("\n", "\\n"), untransformed[i].replace("\n", "\\n")))

		WriteFile(file, lang, output)



if not len(sys.argv) > 1:	# Run Without Args
	window = tk.Tk()
	window.title("MCT")
	window.minsize(450,650)
	window.geometry("1x1")
	window.columnconfigure(0, weight=1, pad=0)
	window.columnconfigure(1, weight=8, pad=0)
	window.rowconfigure(2,pad=0,weight=1)

	def Getlang():
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
			Evaluate(filename.name, clicked.get(), True, True, "safe" if isUnsafe.get() == 0 else "unsafe")

	selection = tk.Button(window, text='Select Lang File', command=Getlang, borderwidth=3).grid(column=0, columnspan=2, row=0, padx=(5,5), pady=(5,0), sticky="WSE")

	tk.Label(window, text="Translate To Language:").grid(column=0, row=1, padx=(5,5), pady=(5,5),sticky="WN")
	clicked = tk.StringVar()
	clicked.set("afrikaans")
	ttk.Combobox(window, textvariable=clicked, values=languages).grid(column=1, row=1, padx=(5,5), pady=(5,5),sticky="WNE")
	
	textDisp = tks.ScrolledText(window, borderwidth=3, height=16, state="disabled")
	textDisp.config(bg="#10141c", fg="#bfbdb6")
	textDisp.grid(column=0, columnspan=2, row=2, padx=(5,5), pady=(5,5),sticky="WNSE")
	
	isUnsafe = tk.IntVar()
	tk.Checkbutton(window, text='Unsafe Mode', variable=isUnsafe, onvalue=1, offvalue=0).grid(column=0, row=3, padx=(5,5), pady=0, sticky="WN")

	tk.Button(window, text='Convert', command=convert, borderwidth=3).grid(column=0, columnspan=2, row=4, padx=(5,5), pady=(5,5), sticky="ENSW")

	window.mainloop()
else:
	args = parser.parse_args()
	Evaluate(args.input, args.language, args.debug, False, args.method)