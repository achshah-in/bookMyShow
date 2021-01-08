#All imports
from flask import Flask
from flask_cors import CORS
from flask import request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import threading

#All classes
class user:
    '''
    Used to define user for login
    :param username: Username of user
    :type arg: str
    :param password: Password of user
    :type arg: str
    '''
    def __init__(self, username, password):
        self.username = username
        self.password = password

class city:
    '''
    Used to define a city
    :param name: Name of city
    :type arg: str
    :param allTheatres: Lists all the theatres in the city
    :type arg: list
    '''
    def __init__(self, name, allTheatres):
        self.name = name
        self.allTheatres = allTheatres

class theatre:
    '''
    Used to define a theatre
    :param name: Name of theatre
    :type arg: str
    :param city: City to which theatre belongs
    :type arg: str
    :param slots: Slots booked in the theatre
    :type arg: map
    :param capacity: Capacity of the theatre
    :type arg: int
    '''
    def __init__(self, name, city, slots, capacity):
        self.name = name
        self.city = city
        self.slots = slots
        self.capacity = capacity

class event:
    '''
    Used to define an event
    :param name: Name of the event
    :type arg: str
    :param city: City to which event belongs
    :type arg: str
    :param theatre: Theatre where the event is happening
    :type arg: str
    :param timeSlot: Capacity of the theatre
    :type arg: int
    '''
    def __init__(self, name, city, theatre, timeSlot, sitsFilled):
        self.name = name
        self.city = city
        self.theatre = theatre
        self.timeSlot = timeSlot
        self.sitsFilled = sitsFilled

class movie(event):
    '''
    Used to define an event
    :param name: Name of the event
    :type arg: str
    :param city: City to which event belongs
    :type arg: str
    :param theatre: Theatre where the event is happening
    :type arg: str
    :param timeSlot: Capacity of the theatre
    :type arg: int
    '''
    def __init__(self, name, city, theatre, timeSlot, sitsFilled):
        event.__init__(self, name, city, theatre, timeSlot, sitsFilled)

#All global variables
auth = HTTPBasicAuth()
userMap = {'admin':user('admin',generate_password_hash('admin')),'user1':user('user1',generate_password_hash('abc')),'user2':user('user2',generate_password_hash('xyz'))}
cityMap = {'Mumbai':city('Mumbai',[]),'Delhi':city('Delhi',[]),'Chennai':city('Chennai',[])}
lock = threading.Lock()
app = Flask(__name__)
CORS(app)

#All APIs
@auth.verify_password
def verify_password(username, password):
    '''This function is used to authenticate login'''
    if username in userMap and \
            check_password_hash(userMap.get(username).password, password):
        return username

@app.route('/registerUser',methods=['POST'])
@auth.login_required
def registerUser():
    '''The function is used to register User'''
    try:
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        if username is None or password is None:
            return {"data":"Please enter username/password"}
        if username in userMap:
            return {"data":"User is already registered"}
        userMap[username] = user(username,generate_password_hash(password))
        return {"data":"User registered successfully"}
    except:
        logging.error('An error occured while registering user')
        return {"data":"An error occured while registering user"}

@app.route('/registerTheatre',methods=['POST'])
@auth.login_required
def registerTheatre():
    '''This function is used to register theatre in specified city'''
    try:
        user = request.get_json().get('user')
        if user != 'admin':
            return {"data":"You are not authorized to registerTheatre"}
        retDict = {}
        cityParam = request.get_json().get('city')
        theatreParam = request.get_json().get('theatre')
        if user is None or cityParam is None or theatreParam is None:
            return {"data":"Please enter a valid request"}
        capacityParam = 500
        if request.get_json().get('capacity') is not None:
            capacityParam = request.get_json().get('capacity')
        if cityParam not in cityMap:
            return {"data":"Application not available in the mentioned city"}
        else:
            for theatreVar in cityMap[cityParam].allTheatres:
                if theatreVar.name == theatreParam:
                    return {"data":"Theatre already registered in the mentioned city"}
            theatreObject = theatre(theatreParam,cityParam,{},capacityParam)
            cityObject = cityMap[cityParam]
            theatreList = cityObject.allTheatres
            theatreList.append(theatreObject)
            cityObject.allTheatres = theatreList
        return {"data":"Theatre registered successfully"}
    except:
        logging.error('An error occured while registering Theatre')
        return {"data":"An error occured while registering Theatre"}

@app.route('/addMovie',methods=['POST'])
@auth.login_required
def addMovie():
    '''This function is used to add movie to a specified theatre'''
    try:
        user = request.get_json().get('user')
        if user != 'admin':
            return {"data":"You are not authorized to registerTheatre"}
        cityParam = request.get_json().get('city')
        movieParam = request.get_json().get('movie')
        slotParam = request.get_json().get('slot')
        if user is None or cityParam is None or movieParam is None or slotParam is None:
            return {"data":"Please enter a valid request"}
        if slotParam!='9AM' and slotParam!='12PM' and slotParam!='3PM' and slotParam!='6PM' and slotParam!='9PM':
            return {"data":"Please enter a valid time slot"}
        if cityParam not in cityMap and cityParam != 'all':
            return {"data":"Application not available in the mentioned city"}
        if cityParam == 'all':
            for city in cityMap:
                for theatre in city.allTheatres:
                    if slotParam not in theatre.slots:
                        slotList = theatre.slots
                        movieObject = movie(movieParam,city,theatre,slotParam,0)
                        slotList[slotParam] = movieObject
        else:
            theatreParam = request.get_json().get('theatre')
            theatreObject = None
            for theatreVar in cityMap[cityParam].allTheatres:
                if theatreVar.name == theatreParam:
                    theatreObject = theatreVar
                    break
            if theatreObject is None:
                return {"data":"Theatre is not registered"}
            if slotParam not in theatreObject.slots:
                slotList = theatreObject.slots
                movieObject = movie(movieParam,cityParam,theatreParam,slotParam,0)
                slotList[slotParam] = movieObject
            else:
                return {"data":"Movie already registered for this time slot"}
        return {"data":"Movie added successfully"}
    except:
        logging.error('An error occured while adding Movie')
        return {"data":"An error occured while adding Movie"}

@app.route('/getCities',methods=['GET'])
def getCities():
    '''This function is used to get all the cities where the application runs'''
    try:
        result = {}
        cityArr = []
        for city in cityMap:
            cityArr.append(cityMap[city].name)
        result["data"] = cityArr
        return result
    except:
        logging.error('An error occured while fetching cities')
        return {"data":"An error occured while fetching cities"}

@app.route('/getTheatres',methods=['GET'])
def getTheatres():
    '''This function is used to get all the cities where the application runs'''
    try:
        result = {}
        movieParam = request.args.get('movie')
        cityParam = request.args.get('city')
        if cityParam is None or movieParam is None:
            return {"data":"Please enter a valid request"}
        if cityParam not in cityMap:
            return {"data":"Application not available in the mentioned city"}
        theatreList = []
        for theatre in cityMap[cityParam].allTheatres:
            for slot in theatre.slots:
                if theatre.slots[slot].name == movieParam:
                    theatreList.append(theatre.name)
                    break
        result['data'] = theatreList
        return result
    except:
        logging.error('An error occured while fetching theatreList')
        return {"data":"An error occured while fetching theatreList"}

@app.route('/availableShows',methods=['GET'])
def getAvailableShows():
    '''This function is used to check available shows'''
    try:
        result = {}
        theatreParam = request.args.get('theatre')
        movieParam = request.args.get('movie')
        cityParam = request.args.get('city')
        if cityParam is None or movieParam is None or theatreParam is None:
            return {"data":"Please enter a valid request"}
        slotList = []
        for theatre in cityMap[cityParam].allTheatres:
            if theatre.name == theatreParam:
                for slot in theatre.slots:
                    if theatre.slots[slot].name == movieParam:
                        slotList.append(slot)
        result['data'] = slotList
        return result
    except:
        logging.error('An error occured while fetching availableShows')
        return {"data":"An error occured while fetching availableShows"}

@app.route('/seatMap',methods=['GET'])
def getSeatMap():
    '''This function is used to check seat Map'''
    try:
        result = {}
        theatreParam = request.args.get('theatre')
        movieParam = request.args.get('movie')
        cityParam = request.args.get('city')
        showParam = request.args.get('show')
        if cityParam is None or movieParam is None or theatreParam is None:
            return {"data":"Please enter a valid request"}
        totalSeats = 'N/A'
        avaiableSeats = 'N/A'
        for theatre in cityMap[cityParam].allTheatres:
            if theatre.name == theatreParam:
                for slot in theatre.slots:
                    if theatre.slots[slot].name == movieParam:
                        totalSeats = theatre.capacity
                        avaiableSeats = totalSeats-theatre.slots[slot].sitsFilled
                        return {"data":{"TotalSeats":totalSeats,"AvailableSeats":avaiableSeats}}

        return {"data":"Please enter a request with valid data"}
    except:
        logging.error('An error occured while fetching seatMap')
        return {"data":"An error occured while fetching seatMap"}

@app.route('/bookTicket',methods=['POST'])
@auth.login_required
def bookTicket():
    '''This function is used to book ticket'''
    with lock:
        try:
            result = {}
            theatreParam = request.get_json().get('theatre')
            movieParam = request.get_json().get('movie')
            cityParam = request.get_json().get('city')
            showParam = request.get_json().get('show')
            if cityParam is None or movieParam is None or theatreParam is None or showParam is None:
                return {"data":"Please enter a valid request"}
            for theatre in cityMap[cityParam].allTheatres:
                if theatre.name == theatreParam:
                    for slot in theatre.slots:
                        if theatre.slots[slot].name == movieParam:
                            totalSeats = theatre.capacity
                            avaiableSeats = totalSeats-theatre.slots[slot].sitsFilled
                            if avaiableSeats == 0:
                                return {"data":"All seats have been booked"}
                            else:
                                theatre.slots[slot].sitsFilled = theatre.slots[slot].sitsFilled+1
                                return {"data":"Your ticket has been successfully booked"}

            return {"data":"Please enter a request with valid data"}
        except:
            logging.error('An error occured while booking ticket')
            return {"data":"An error occured while booking ticket"}

#The main method
if __name__== '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
