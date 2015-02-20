from pywmata import Wmata
from x84.bbs import echo, getterminal, getsession, LineEditor
from common import waitprompt
import json, sys

api = Wmata("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

def listLines():
	term = getterminal()
	echo(term.clear)
	lines = api.lines()
	n = len (lines)
	for i in range (0,n):
		echo (str(i+1) + ": " + getColor(lines[i]['LineCode'],lines[i]['DisplayName']) + " ")

        echo(term.bold_cyan("\r\nPlease select a line, 'Q' to quit: "))
	le = LineEditor(2)
	le.colors['highlight'] = term.magenta
	inp = le.read()
	echo (inp)
	if inp is not None and inp.isnumeric():
		inp = int(inp)
		color = lines[inp-1]["LineCode"]
		listStations(color)

def listStations(color):
	term = getterminal()
	echo(term.clear)
	stations = api.stations(color)
	n = len (stations)
	col = len(stations)/3
	for i in range (0,col):
		echo (term.move(i+1,0) + str(i+1) + ": " + getColor(color,stations[i]["Name"]) + "\r\n")	
        for i in range (col,n-col):
                echo (term.move(i-(col-1),25) + str(i+1) + ": " + getColor(color,stations[i]["Name"]) + "\r\n")
        for i in range (n-col,len (stations)):
                echo (term.move(i-((n-col)-1),50) + str(i+1) + ": " + getColor(color,stations[i]["Name"]) + "\r\n")


        echo(term.bold_cyan("\r\nPlease select a station: "))
	le = LineEditor(2)
	le.colors['highlight'] = term.cyan
	inp = le.read()
	if inp is not None and inp.isnumeric():
                inp = int(inp)
                station = stations[inp-1]["Code"]
                listTimes(station)
	elif inp.upper() == u'Q':
		main()
	else:
                echo(term.red("Please select a station"))
		waitprompt(term)
                listStations(color)

def listTimes(station):
	term = getterminal()
	echo(term.clear)
	times = api.rail_predictions(station)
        n = len (times)
        if n  == 0:
                echo(term.red_reverse("No sign data is available"))
                waitprompt(term)
                main()

	else:
		name = str(times[0]["LocationName"])
		echo(term.bold_magenta_reverse("STATIONS TIMES FOR " + name.upper()))
		echo(term.bold_yellow("\r\nLN CAR DESTINATION MIN\r\n"))
		n = len (times) 
		if n is not None:
			for i in range (0,n):
				echo (getColor(times[i]["Line"],times[i]["Line"]) + term.move_x(4) + str(times[i]["Car"]) + term.move_x(7) + str(times[i]["Destination"]).upper() + term.move_x(19) + str(times[i]["Min"]) + "\r\n")
				waitprompt(term)
				main()

def getColor(line,txt):
	term = getterminal()
	if line == "RD": 
		line = term.bold_red(txt)
	elif line == "GR":
		line = term.green(txt)
        elif line == "BL":
                line = term.cyan(txt)
        elif line == "SV":
                line = term.white(txt)
        elif line == "YL":
                line = term.bold_yellow(txt)
        elif line == "OR":
                line = term.yellow(txt)
	else:
		line = term.white(txt)
	return line

def main():
	listLines()
