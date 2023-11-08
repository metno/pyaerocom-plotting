# pyaerocom-plotting
command line tool that uses pyaerocom to create plots

## Installation
Standard user installation is done via pip:

```bash
python -m pip install 'git+https://github.com/metno/pyaerocom-plotting.git'
```

For a different branch than main
```bash
python -m pip install 'git+https://github.com/metno/pyaerocom-plotting.git@<branch name>'
```

for development:
```bash
pip install --no-deps -e <source directory>
```


## Help

### pyaerocom_plot

pyaerocom_plot [-h] [-m MODELS [MODELS ...]] [-p PLOTTYPE [PLOTTYPE ...]] [-l] [-s STARTYEAR] [-e [ENDYEAR]]  
                      &emsp;[-v VARIABLES [VARIABLES ...]] [-o OUTDIR]

create plots with Met Norway's pyaerocom package

options:  
  -h, --help  
  &emsp;show this help message and exit  
  -m MODELS [MODELS ...], --models MODELS [MODELS ...]  
  &emsp;models(s) to read  
  -p PLOTTYPE [PLOTTYPE ...], --plottype PLOTTYPE [PLOTTYPE ...]  
  &emsp;plot type(s) to plot
  -l, --list  
  &emsp;list supported plot types  
  -s STARTYEAR, --startyear STARTYEAR  
  &emsp;startyear to read  
  -e [ENDYEAR], --endyear [ENDYEAR]  
  &emsp;endyear to read; defaults to startyear.  
  -v VARIABLES [VARIABLES ...], --variables VARIABLES [VARIABLES ...]  
  &emsp;variable(s) to read  
  -o OUTDIR, --outdir OUTDIR  
  &emsp;output directory for the plot files; defaults to .


**Example usages:**  
&emsp;__- basic usage:__  
	  The following line plots the **pixelmap** for the model **ECMWF_CAMS_REAN** for the year **2019** for the 
variable **od550aer**  
	  `pyaerocom_plot -p pixelmap -m ECMWF_CAMS_REAN -s 2019 -v od550aer`


        

### pyaerocom_plot_json

pyaerocom_plot_json [-h] [-f FILE] [-p PLOTTYPE [PLOTTYPE ...]] [-l] [-o OUTDIR]

create plots based on json files created with Met Norway's pyaerocom/aeroval package

options:
  -h, --help              
  &emsp;show this help message and exit  
  -f FILE, --file FILE  
  &emsp;file to read
  -p PLOTTYPE [PLOTTYPE ...], --plottype PLOTTYPE [PLOTTYPE ...]  
  &emsp;plot type(s) to plot  
  -l, --list             
  &emsp;list supported plot types  
  -o OUTDIR, --outdir OUTDIR  
  &emsp;output directory for the plot files; defaults to .

&emsp;**Example usages:**  
&emsp;**- basic usage:**  
	  The following line plots the time series plot (model mean) for the file **./hm/ts/ALL-Aeronet-od550aer-Column.json**  
	  `pyaerocom_plot_json -o /tmp -p overall_ts -f ./hm/ts/ALL-Aeronet-od550aer-Column.json`