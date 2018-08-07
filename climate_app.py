#dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#-----------------------------------------

#create engine object based on URL
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

#reflect database
Base = automap_base()
#reflect the database's tables
Base.prepare(engine, reflect=True)


#create mapped class for database
Measurement = Base.classes.measurement
Station = Base.classes.station

#create session from Python to the database
session = Session(bind=engine)



#-----------------------------------------
#setting up Flask
app = Flask(__name__)

#-----------------------------------------
#Flask Routes
#-------------
@app.route("/")
def index():
 
    return'<h2 align=center>Climate API for Honolulu, Hawaii</h2>\
            <p align=center><u>Available Routes:</u></p>\
            <p align=center>/api/v1.0/precipitation</p>\
            <p align=center>/api/v1.0/stations</p>\
            <p align=center>/api/v1.0/tobs</p>\
            <p align=center>/api/v1.0/start/end</p>'



@app.route("/api/v1.0/precipitation")
def precipitation():
    
    #start and end date of data collected for last year (2017)
    start = '2017-01-01'
    end = '2017-12-31'

    #query the measurement table for the temperature of a day in 2017
    prcp_query = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    #create dictionary
    prcp_dic = {}
    for key, value in prcp_query:
        prcp_dic[key] = value
        
    return jsonify(prcp_dic)
    

    
@app.route("/api/v1.0/stations")
def stations():
    
    #query stations in stations table
    stations = session.query(Station.station).all()
    
    #create list of stations queried in stations table
    list_stations = [x for x, in stations]
    
    #return json list of stations
    return jsonify(list_stations)



@app.route('/api/v1.0/tobs')
def temp_obs():
    
    #start and end date of data collected for last year (2017)
    start = '2017-01-01'
    end = '2017-12-31'

    #query the measurement table for the temperature of a day in 2017
    tobs_query = session.query(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    #create list of temperature measurements from in 2017
    tobs_list = [temp for temp, in tobs_query]
        
    return jsonify(tobs_list)





@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def date_range_temp(start, end=None):
    
    if end == None: 
        
        #query minimum, average, maximum temperature from start date to most recent measurement
        describe_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).first()  
        
    else: 
        
        #query minimum, average, maximum temperature from start date to most recent measurement
        describe_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).first()
    
    #unpack minimum, average, maximum temperature from tuple result from query
    t_min, t_avg, t_max = describe_temp

    #create dictionary with temperature description as keys and the temperature values as values
    start_describe = {'min_temp':t_min, 'avg_temp':t_avg, 'max_temp':t_max}
    
    return jsonify([start_describe])


    

if __name__ == '__main__':
    app.run(debug=True)