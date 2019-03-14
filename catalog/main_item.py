from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_structure import Base, CarBrandName, CarName, SUser
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///cars.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Car_Club"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
glg = session.query(CarBrandName).all()


# login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    glg = session.query(CarBrandName).all()
    clg = session.query(CarName).all()
    return render_template('login.html',
                           STATE=state, glg=glg, clg=clg)
    # return render_template('myhome.html', STATE=state
    # glg=glg,clg=clg)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials objects
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Hi!..Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    User1 = SUser(name=login_session['username'], email=login_session[
                   'email'])
    session.add(User1)
    session.commit()
    user = session.query(SUser).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(SUser).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(SUser).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
# Home


@app.route('/')
@app.route('/home')
def home():
    glg = session.query(CarBrandName).all()
    return render_template('myhome.html', glg=glg)

# Car Brand for admins


@app.route('/CarClub')
def CarClub():
    try:
        if login_session['username']:
            name = login_session['username']
            glg = session.query(CarBrandName).all()
            gil = session.query(CarBrandName).all()
            clg = session.query(CarName).all()
            return render_template('myhome.html', glg=glg,
                                   gil=gil, clg=clg, uname=name)
    except:
        return redirect(url_for('showLogin'))
# Showing cars details based on car brand


@app.route('/CarClub/<int:flfid>/AllBrands')
def showCars(flfid):
    ''' show all the car details in according to their car brands'''
    glg = session.query(CarBrandName).all()
    gil = session.query(CarBrandName).filter_by(id=flfid).one()
    clg = session.query(CarName).filter_by(carbrandnameid=flfid).all()
    try:
        if login_session['username']:
            return render_template('showCars.html', glg=glg,
                                   gil=gil, clg=clg,
                                   uname=login_session['username'])
    except:
        return render_template('showCars.html',
                               glg=glg, gil=gil, clg=clg)


# Add New Car Brands


@app.route('/CarClub/addCarBrand', methods=['POST', 'GET'])
def addCarBrand():
    ''' adding of new car brands'''
    if request.method == 'POST':
        brand = CarBrandName(name=request.form['name'],
                             user_id=login_session['user_id'])
        session.add(brand)
        session.commit()
        return redirect(url_for('CarClub'))
    else:
        return render_template('addCarBrand.html', glg=glg)


# Edit Car Brands which are already in existing


@app.route('/CarClub/<int:flfid>/edit', methods=['POST', 'GET'])
def editCarBrand(flfid):
    '''edit the car brands to change their names'''
    editCar = session.query(CarBrandName).filter_by(id=flfid).one()
    creator = getUserInfo(editCar.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Car Brand."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('CarClub'))
    if request.method == "POST":
        if request.form['name']:
            editCar.name = request.form['name']
        session.add(editCar)
        session.commit()
        flash("Car Brand Edited Successfully")
        return redirect(url_for('CarClub'))
    else:
        # glg is global variable we can use them in entire application
        return render_template('editCarBrand.html',
                               flf=editCar, glg=glg)

# Delete Car Brand which is existing


@app.route('/CarClub/<int:flfid>/delete', methods=['POST', 'GET'])
def deleteCarBrand(flfid):
    '''delete the car brands from the existing data'''
    flf = session.query(CarBrandName).filter_by(id=flfid).one()
    creator = getUserInfo(flf.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this Car Brand."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('CarClub'))
    if request.method == "POST":
        session.delete(flf)
        session.commit()
        flash("Car Brand Deleted Successfully")
        return redirect(url_for('CarClub'))
    else:
        return render_template('deleteCarBrand.html', flf=flf,
                               glg=glg)

# Add New Car Details


@app.route('/CarClub/addBrand/addCarDetails/<string:flfname>/add',
           methods=['GET', 'POST'])
def addCarDetails(flfname):
    '''adding of new car details to their particular car brands'''
    gil = session.query(CarBrandName).filter_by(name=flfname).one()
    # See if the logged in user is not the owner of car
    creator = getUserInfo(gil.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new car details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showCars', flfid=gil.id))
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        color = request.form['color']
        engines = request.form['engines']
        price = request.form['price']
        gearboxes = request.form['gearboxes']
        seeting = request.form['seeting']
        steering = request.form['steering']
        cardetails = CarName(name=name, year=year,
                             color=color, engines=engines,
                             price=price,
                             gearboxes=gearboxes,
                             seeting=seeting,
                             steering=steering,
                             date=datetime.datetime.now(),
                             carbrandnameid=gil.id,
                             suser_id=login_session['user_id'])
        session.add(cardetails)
        session.commit()
        return redirect(url_for('showCars', flfid=gil.id))
    else:
        return render_template('addCarDetails.html',
                               flfname=gil.name, glg=glg)

# Edit Car details to the existing one


@app.route('/CarClub/<int:flfid>/<string:mumename>/edit',
           methods=['GET', 'POST'])
def editCarDetails(flfid, mumename):
    '''edit the car details which is already in exist'''
    flf = session.query(CarBrandName).filter_by(id=flfid).one()
    cardetails = session.query(CarName).filter_by(name=mumename).one()
    # See if the logged in user is not the owner of car
    creator = getUserInfo(flf.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this car name"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showCars', flfid=flf.id))
    # POST methods
    if request.method == 'POST':
        cardetails.name = request.form['name']
        cardetails.year = request.form['year']
        cardetails.color = request.form['color']
        cardetails.engines = request.form['engines']
        cardetails.price = request.form['price']
        cardetails.gearboxes = request.form['gearboxes']
        cardetails.seeting = request.form['seeting']
        cardetails.steering = request.form['steering']
        cardetails.date = datetime.datetime.now()
        session.add(cardetails)
        session.commit()
        flash("Car Details Edited Successfully")
        return redirect(url_for('showCars', flfid=flfid))
    else:
        return render_template('editCarDetails.html',
                               flfid=flfid, cardetails=cardetails,
                               glg=glg)

# Delte Car Details from the existing one


@app.route('/CarClub/<int:flfid>/<string:mumename>/delete',
           methods=['GET', 'POST'])
def deleteCarDetails(flfid, mumename):
    '''dalete the car details that are in exist'''
    flf = session.query(CarBrandName).filter_by(id=flfid).one()
    cardetails = session.query(CarName).filter_by(name=mumename).one()
    # See if the logged in user is not the owner of car
    creator = getUserInfo(flf.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this car details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showCars', flfid=flf.id))
    if request.method == "POST":
        session.delete(cardetails)
        session.commit()
        flash("Deleted Car Successfully")
        return redirect(url_for('showCars', flfid=flfid))
    else:
        return render_template('deleteCarDetails.html',
                               flfid=flfid, cardetails=cardetails,
                               glg=glg)

# Logout from current user


@app.route('/logout')
def logout():
    '''logging-out from the current user'''
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type': 'application/x-www-form-urlencoded'}
                  )[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps(
            'Successfully disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON


@app.route('/CarClub/JSON')
def allCarsJSON():
    '''DISPLAY ALL THE DETAILS OF DIFFERENT CAR BRANDS'''
    carcategory = session.query(CarBrandName).all()
    category_dict = [c.serialize for c in carcategory]
    for c in range(len(category_dict)):
        cars = [i.serialize for i in session.query(CarName).filter_by(
                                carbrandnameid=category_dict[c]["id"]).all()]
        if cars:
            category_dict[c]["car"] = cars
    return jsonify(CarBrandName=category_dict)



@app.route('/carClub/carCategory/JSON')
def categoriesJSON():
    '''all the car brands are displayed'''
    cars = session.query(CarBrandName).all()
    return jsonify(carCategory=[c.serialize for c in cars])



@app.route('/carClub/cars/JSON')
def itemsJSON():
    '''all the cars of different car brands are displayed with their values'''
    items = session.query(CarName).all()
    return jsonify(cars=[i.serialize for i in items])



@app.route('/carClub/<path:car_name>/cars/JSON')
def categoryItemsJSON(car_name):
    ''' all the car details of one particular car brand are displayed with values'''
    carCategory = session.query(CarBrandName).filter_by(name=car_name).one()
    cars = session.query(CarName).filter_by(carbrandname=carCategory).all()
    return jsonify(carEdtion=[i.serialize for i in cars])



@app.route('/carClub/<path:car_name>/<path:edition_name>/JSON')
def ItemJSON(car_name, edition_name):
    ''' car details of particular car brand are displayed'''
    carCategory = session.query(CarBrandName).filter_by(name=car_name).one()
    carEdition = session.query(CarName).filter_by(
           name=edition_name, carbrandname=carCategory).one()
    return jsonify(carEdition=[carEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=2222)
