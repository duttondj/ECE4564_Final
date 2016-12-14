from flask import Flask, render_template
from flask_table import Table, Col
from GoogleCalendar import Events
import time
import copy
import json

''' ItemTable class used for the Flask Table extension'''
class ItemTable(Table):
    time = Col('Date')
    title = Col('Summary')

app = Flask(__name__)
 
@app.route('/')
def index():
    # Create new Events object and get next 5 events
    events = Events()
    event_list = events.getEvents(10)

    # Create table from events
    items = []
    for event in event_list:
        items.append({'time':event[0], 'title':event[1].encode("utf-8")})
    table = ItemTable(items)

    # Render the table using the template
    return render_template("index.html", table=table)

if __name__ == "__main__":
    app.run()