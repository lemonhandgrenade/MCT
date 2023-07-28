# MCT
A python tool to automatically translate lang files into other languages

# Usage

(The lang file generated will be exported to the same directory as the input file with the inputted language code)  

## Supported Languages

Currently 58 languages are supported to translate to.  

<details><summary>Open to see supported languages</summary>

 - Afrikaans
 - Albanian
 - Arabic
 - Azerbaijani
 - Basque
 - Belarusian
 - Bulgarian
 - Catalan
 - Chinese Simplified
 - Chinese Traditional
 - Croatian
 - Czech
 - Danish
 - Dutch
 - English
 - Esperanto
 - Estonian
 - Filipino
 - Finnish
 - French
 - Galician
 - Georgian
 - German
 - Greek
 - Hebrew
 - Hindi
 - Hungarian
 - Icelandic
 - Indonesian
 - Irish
 - Italian
 - Japanese
 - Kannada
 - Korean
 - Latin
 - Latvian
 - Lithuanian
 - Macedonian
 - Malay
 - Maltese
 - Norwegian
 - Persian
 - Polish
 - Portuguese
 - Romanian
 - Russian
 - Serbian
 - Slovak
 - Slovenian
 - Spanish
 - Swedish
 - Tamil
 - Thai
 - Turkish
 - Ukrainian
 - Vietnamese
 - Welsh
 - Yiddish

</details>

## CLI

If running from the command line there are a few arguments you can use.  
Example:  
```
foo> python mct.py -i en_us.json -l french
```

### Arguments

`-h, --help`: Shows the help dialogue with all optional arguments.  
`-i <file>, --input <file>`: Path to the language file pre written. eg: ...\assets\minecraft\lang\en_us.json  
`-l <language>, --language <language>`: The desired language to translate to. See [Supported Languages](#supported-languages) for the list of current languages.  
`-m <method>, --method <method>`: The method that should be used when translating. "safe", "unsafe"  
Safe translates line by line and is far more accurate than unsafe however takes a lot longer.  
Unsafe batch translates the entire value range at once. However, in doing so translations can be very inaccurate but overall extermely fast.  
`-d, --debug`: Outputs the current line being translated beside the progress bar whilst translating.  

## GUI

When mct.py is run without any arguments it'll prompt a GUI to appear which has buttons for, selecting the lang file, selecting the language and converting. 

![gui](https://github.com/lemonhandgrenade/MCT/assets/36611142/68b83dc6-0b01-45d6-b94f-49a2b20c9cca)

# Installation

With a terminal open in the working directory run the command `pip install -r requirements.txt`  
Then you can use mct.py either in the [CLI](#cli) or using the [GUI](#gui)  
