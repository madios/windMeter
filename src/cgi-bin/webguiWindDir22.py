#!/usr/bin/env python

import sqlite3
import sys
import cgi
import cgitb


# global variables
speriod=(15*60)-1
dbwind='/var/www/windspeed.db'
dbdir='/var/www/direction.db'
#dbname='/home/pi/python/plantProjectV2/templog.db'



# print the HTTP header
def printHTTPheader():
    print "Content-type: text/html\n\n"



# print the HTML head section
# arguments are the page title and the table for the chart
def printHTMLHead(title, table,chartId):
    print "<head>"
    print "    <title>"
    print title
    print "    </title>"
    
    print_graph_script(table,chartId)

    print "</head>"


# get data from the database
# if an interval is passed, 
# return a list of records from the database
def get_data(interval,dbname):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if interval == None:
    	curs.execute("SELECT * FROM temps")
    else:
    	curs.execute("SELECT * FROM temps WHERE timestamp>datetime('now','-%s hours')" % interval)
    	#curs.execute("SELECT * FROM temps WHERE timestamp>datetime('2013-09-19 21:30:02','-%s hours') AND timestamp<=datetime('2013-09-19 21:31:02')" % interval)

    rows=curs.fetchall()

    conn.close()

    return rows


# convert rows from database into a javascript table
def create_table(rows):
    chart_table=""

    for row in rows[:-1]:
        rowstr="['{0}', {1}],\n".format(str(row[0]),str(row[1]))
        chart_table+=rowstr

    row=rows[-1]
    rowstr="['{0}', {1}]\n".format(str(row[0]),str(row[1]))
    chart_table+=rowstr

    return chart_table


# print the javascript to generate the chart
# pass the table generated from the database info
def print_graph_script(table,chartId):

    # google chart snippet
    chart_code1="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([['Time', 'windspeed [m/s]'],%s]);
        var options = {title: 'Windspeed'};
        var chartID = 'chart_div1'
        var chart = new google.visualization.LineChart(document.getElementById(chartID));
       chart.draw(data, options);
      }
    </script>"""

    # google chart snippet
    chart_code2="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([['Time', 'wind Direction'],%s]);
        var options = {title: 'Wind Direction'};
        var chartID = 'chart_div2'
        var chart = new google.visualization.LineChart(document.getElementById(chartID));
       chart.draw(data, options);
      }
    </script>"""

    # google chart snippet
    chart_code3="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([['Time', 'Temperature'],%s]);
        var options = {title: 'Wind Speed'};
        var chartID = 'chart_div3'
        var chart = new google.visualization.LineChart(document.getElementById(chartID));
       chart.draw(data, options);
      }
    </script>"""

    if chartId == 1:
    	print chart_code1 % (table)
    if chartId == 2:
        print chart_code2 % (table)
    if chartId == 3:
        print chart_code3 % (table)



# print the div that contains the graph
def show_graph(chartId):
#    print "<h2>Temperature Chart</h2>"
    charId =  '<div id=' + chartId + ' style="width: 900px; height: 500px;"></div>'
#    print '<div id="chart_div" style="width: 900px; height: 500px;"></div>'
    print charId

# connect to the db and show some stats
# argument option is the number of hours
def show_stats(option):

    conn=sqlite3.connect(dbwind)
    curs=conn.cursor()

    if option is None:
        option = str(24)

    curs.execute("SELECT timestamp,max(temp) FROM temps WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
#    curs.execute("SELECT timestamp,max(temp) FROM temps WHERE timestamp>datetime('2013-09-19 21:30:02','-%s hour') AND timestamp<=datetime('2013-09-19 21:31:02')" % option)
    rowmax=curs.fetchone()
    rowstrmax="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmax[0]),str(rowmax[1]))

    curs.execute("SELECT timestamp,min(temp) FROM temps WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
#    curs.execute("SELECT timestamp,min(temp) FROM temps WHERE timestamp>datetime('2013-09-19 21:30:02','-%s hour') AND timestamp<=datetime('2013-09-19 21:31:02')" % option)
    rowmin=curs.fetchone()
    rowstrmin="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmin[0]),str(rowmin[1]))

    curs.execute("SELECT avg(temp) FROM temps WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
#    curs.execute("SELECT avg(temp) FROM temps WHERE timestamp>datetime('2013-09-19 21:30:02','-%s hour') AND timestamp<=datetime('2013-09-19 21:31:02')" % option)
    rowavg=curs.fetchone()


    print "<hr>"


    print "<h2>Minumum temperature&nbsp</h2>"
    print rowstrmin
    print "<h2>Maximum temperature</h2>"
    print rowstrmax
    print "<h2>Average temperature</h2>"
    print "%.3f" % rowavg+"C"

    print "<hr>"

    print "<h2>In the last hour:</h2>"
    print "<table>"
    print "<tr><td><strong>Date/Time</strong></td><td><strong>Temperature</strong></td></tr>"

    rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('new','-1 hour') AND timestamp<=datetime('new')")
#    rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('2013-09-19 21:30:02','-1 hour') AND timestamp<=datetime('2013-09-19 21:31:02')")
    for row in rows:
        rowstr="<tr><td>{0}&emsp;&emsp;</td><td>{1}C</td></tr>".format(str(row[0]),str(row[1]))
        print rowstr
    print "</table>"
    print "<META HTTP-EQUIV='refresh' CONTENT='5'>"
    print "<hr>"

    conn.close()




def print_time_selector(option):


    if option is not None:
        peter = 2
        print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        print option
        if option == "1":
            print """<form action="/cgi-bin/webguiWindDir2.py" method="POST">
                    Show the temperature logs for  
                    <select name="timeinterval">"""
        if option == "2":
            print """<form action="/cgi-bin/webguiWindDir22.py" method="POST">
                    Show the temperature logs for  
                    <select name="timeinterval">"""
        if option == "3":
            print """<form action="/cgi-bin/webguiWindDir2.py" method="POST">
                    Show the temperature logs for  
                    <select name="timeinterval">"""

    else:
        print """<form action="/cgi-bin/webguiWindDir2.py" method="POST">
                Show the temperature logs for  
                <select name="timeinterval">"""

    if option is not None:

        if option == "1":
            print "<option value=\"1\" selected=\"selected\">the last 1 hours</option>"
        else:
            print "<option value=\"1\">the last 1 hours</option>"

        if option == "2":
            print "<option value=\"2\" selected=\"selected\">the last 2 hours</option>"
        else:
            print "<option value=\"2\">the last 2 hours</option>"

        if option == "3":
            print "<option value=\"3\" selected=\"selected\">the last 3 hours</option>"
        else:
            print "<option value=\"3\">the last 3 hours</option>"

    else:
        print """<option value="6">the last 1 hours</option>
            <option value="2">the last 2 hours</option>
            <option value="3" selected="selected">the last 3 hours</option>"""

    print """        </select>
        <input type="submit" value="Display">
    </form>"""


# check that the option is valid
# and not an SQL injection
def validate_input(option_str):
    # check that the option string represents a number
    if option_str.isalnum():
        # check that the option is within a specific range
        if int(option_str) > 0 and int(option_str) <= 24:
            return option_str
        else:
            return None
    else: 
        return None


#return the option passed to the script
def get_option():
    form=cgi.FieldStorage()
    if "timeinterval" in form:
        option = form["timeinterval"].value
        return validate_input (option)
    else:
        return None




# main function
# This is where the program starts 
def main():
    cgitb.enable()
    # get options that may have been passed to this script
    option=get_option()
    #option=3
    if option is None:
        option = str(0.1)

    # get data from the database
    recordsWind=get_data(option,dbwind)
    recordsDir=get_data(option,dbdir)

    # print the HTTP header
    printHTTPheader()

    if len(recordsWind) != 0:
        # convert the data into a table
        tableWind=create_table(recordsWind)
        tableDir=create_table(recordsDir)
    else:
        print "No data found"
        return

    # start printing the page
    print "<html>"
    # print the head section including the table
    # used by the javascript for the chart
    printHTMLHead("Raspberry Pi Temperature Logger", tableWind,1)
    printHTMLHead("Raspberry Pi Temperature Logger", tableDir,2)

    # print the page body
    print "<body>"
    print "<h1>Raspberry Pi Temperature Logger</h1>"
    print "<hr>"
    print_time_selector(option)
    show_graph("chart_div1")
    show_graph("chart_div2")
    show_stats(option)
    print "</body>"
    print "</html>"

    sys.stdout.flush()

if __name__=="__main__":
    main()




