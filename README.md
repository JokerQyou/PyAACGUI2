PyAACGUI2
========

A GUI glue program for converting high quality music using Nero AAC Codec. 
As three of its dependencies are Unix/Linux programs, it is probably 
not possible to use on Windows platform, though the graphic interface 
itself is non-platform-related. 

And for Windows users, the `Foobar 2000 ` seems to be good enough, it has a 
converter that supports Nero AAC Encoder. What's cool, it uses multiple 
subprocesses in conversion, so it works much faster than this program. 

##Requirements##

* `Python 2 `
* `wxPython `
* Unix `mediainfo ` program
* Unix `mplayer ` program
* Nero AAC programs for Linux (includes these executables: `neroAacDec `, 
`neroAacEnc ` and `neroAacTag ` )

###Notice!###

I cannot redistribute any part of Nero AAC Codecs according to the license 
agreement provided by Nero AG. So it is important that you have these 
programs installed correctly. Here's a brief introduction. 

For Nero AAC programs, go to the official site of Nero AG, search for `AAC 
Encoder `, download the compressed file from its introduction page (you'll 
have to agree that license agreement first). Decompress the package and the 
contents are as follows:

```
NeroAACCodec-1.5.1/
    |-linux/
    |   |-neroAacDec
    |   |-neroAacEnc
    |   |-neroAacTag
    |-win32/
    |   |-neroAacDec.exe
    |   |-neroAacEnc.exe
    |   |-neroAacTag.exe
    |-changelog.txt
    |-license.txt
    |-NeroAAC_tut.pdf
    |-readme.txt
```

Now copy these three files inside the `linux ` folder to anywhere you want, 
and add the path of the folder containing them to your `.bashrc ` file. 

E.G. I put these three files inside `/home/joker/ETC/tools/ `, so I added 
the following line to the end of my `.bashrc ` file (`~/.bashrc `):

`export PATH=${PATH}:/home/joker/ETC/tools `

###Experimental###

You could now set location of needed Nero programs in the config file rather 
than setting them in your `.bashrc ` file. If you don't want to change the 
global `PATH ` variable, you can try this experimental feature by setting 
the `enc ` and `tag ` option values in config file.

* `enc ` Set the location (currently absolute path recommended) of Nero AAC 
Encoder.
* `tag ` Set the location of Nero MPEG-4 Tagger.

##Usage##

Run the bash script `PyAACGUI2 ` (you might need to run `chmod +x PyAACGUI2 ` 
first). 

This is a GUI program, so don't even think about passing file paths to it 
through command line, it just doesn't work that way. 

##Configuration##

Only certain options are available in the `Preference ` dialog.

All available configurations are stored in the `config.ini ` file. Available 
options are as follows. Notice: Boolean values must be changed to int type 
before being stored in config file (1 == True; 0 == False).

* `locale ` Set UI locale.
* `debug ` Set debug switch.
* `tempdir ` Set temporary file directory.
* `bitrate ` Set the bitrate (in bps) that passed to Nero AAC encoder.
* `delorigin ` Delete original files after conversion.

Default values are as follows:

* `locale=en_US` (Set in `i.py `)
* `debug=True` (Set in `i.py `)
* `tempdir=` (Use result of python code `tempfile.gettempdir() `)
* `bitrate=512000` (Set in `i.py `)
* `delorigin=False` (Set in `i.py `)

###Notice!###

Setting `tempdir ` option to `/dev/shm ` might slightly speed up conversion. 

##License##

This program uses BSD license, see the `BSD.license ` file for details. 
The license content is also available in the `Help ` > `About ` section of 
this program.

##Author##

[Joker Qyou](http://mynook.info/)

##Extra##

If you need a program to split audio CD image to separated tracks, 
I personally recommend the Bash script `cue2tracks `. 

###wxStart Guide###

This project is based on `wxStart ` template, 
and here is a brief guideline for the developers.

Directory structure:
```
PyAACGUI2
    |-README                This README file
    |-BSD.license           License file
    |-PyAACGUI2             Application entrance for user
    |-main.py               The application entrance in Python
    |-app.py                The customized App class
    |-mainframe.py          The customized main frame class
    |-pref.py               Preference frame class
    |-i.py                  Contains basic information about this program
    |-q.py                  Shortcut of commonly-used functions
    |-config.ini            Configuration file
    |-core/                 Core module
    |    |-__init__.py      Empty file to make this folder a module
    |    |-mediainfo.py     Media info query tool
    |    |-converter.py     Background thread class
    |
    |-layout/               Contains XRC layout files
    |    |-main.xrc         Default main frame layout file
    |    |-preference.xrc   Preference dialog layout file
    |
    |-resources/            Place any other files in it, such as images
    |    |-icon_big.png     The default icon used in `about` dialog
    |    |                  You should change this file to your own icon.
    |    |-tools/           Contains icons used for tool bar.
    |-locale/               Contains locale files
    |    |-zh_CN            Contains locale file for Chinese(Simplified) 
    |        |              Note that this is only a example, you should
    |        |              create your own locale using the same structure.
    |        |-LC_MESSAGES  This folder contains the actual locale file (*.mo)
    |                       Place compiled locale file PyAACGUI2.mo here, 
    |                       and this program will support Chinese(Simplified).

```
