import string
import random
from flask import session as login_session
from database_setup import Base, Category, CategoryItem, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, asc, desc, text
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']

app = Flask(__name__)

engine = create_engine('sqlite:///catalogItems.db')
Base.metadata.bind = engine

''' Helpfull user methods used for user login '''


def createUser(login_session):
    newUser = User(username=login_session['username'],
                   email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s') % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 50)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID does not match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Tokens do not match!"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("User is already logged in"), 200)
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

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.ascii_lowercase) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Catalog related actions

@app.route('/', defaults={"page": 1})
@app.route('/<int:page>')
@app.route('/categories/', defaults={"page": 1})
@app.route('/categories/<int:page>')
def showCategories(page):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    page = page
    per_page = 6
    categories = session.query(Category).all()
    category_items = session.query(
        CategoryItem).order_by(text("id DESC")).all()
    latest_category_item = session.query(
        CategoryItem).order_by(text("id DESC")).first()
    return render_template("category-index.html", categories=categories, category_items=category_items,
                           latest_category_item=latest_category_item)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu-index.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/edit', methods=["POST", "GET"])
def editRestaurant(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "POST":
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        restaurant.name = request.form['name']
        session.commit()
        flash('Restaurant Edited')
        return redirect(url_for('showRestaurants'))


@app.route('/restaurants/<int:restaurant_id>/delete', methods=["POST", "GET"])
def deleteRestaurant(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "POST":
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        print(restaurant.name)
        session.delete(restaurant)
        session.commit()
        flash('Restaurant Deleted')
        return redirect(url_for('showRestaurants'))


@app.route('/restaurants/add', methods=["POST", "GET"])
def addRestaurant():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "POST":
        newRestaurant = Restaurant(name=request.form['new-name'])
        session.add(newRestaurant)
        session.commit()
        flash('Restaurant added')
        return redirect(url_for('showRestaurants'))


# Menu Item related actions
@app.route('/restaurants/<int:restaurant_id>/item/<int:item_id>/edit', methods=["POST", "GET"])
def editItem(restaurant_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "POST":
        item = session.query(
            MenuItem).filter_by(id=item_id).one()
        item.name = request.form['name']
        session.commit()
        flash('Item Edited')
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant.id))


@app.route('/restaurants/<int:restaurant_id>/item/<int:item_id>/delete', methods=["POST", "GET"])
def deleteItem(restaurant_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "POST":
        item = session.query(
            MenuItem).filter_by(id=item_id).one()
        session.delete(item)
        session.commit()
        flash('Item Deleted')
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant.id))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
