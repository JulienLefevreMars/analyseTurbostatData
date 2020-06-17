This little project plots power consumption data obtained by different sources:
- the output of a turbostat command (.out file)
- the output of a Voltcraft wattmeter (.csv file converted from .BIN to .csv by using this online tool http://llbteam.free.fr/el4000/el4000.php)

**How to use it ?**

- Assumes turbostat has been run with a temporal sampling of 1 minute (60s)
sudo turbostat --interval 60 -out Test.out
- .out and .csv files should be in the same directory (e.g. Data)
- Run 
python script_analyse.py 'Data/'
for a ready-made example
or python script_analyse.py 'pathToFiles'

