import string
import random
from flask import session as login_session
from database_setup import Category, CategoryItem, User, db
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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./testDB.db'
db.init_app(app)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']

''' Helpfull user methods used for user login '''


def createUser(login_session):
    newUser = User(username=login_session['username'],
                   email=login_session['email'], picture=login_session['picture'])
    db.session.add(newUser)
    db.session.commit()
    user = User.query.filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = User.query.filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = User.query.filter_by(email=email).one()
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
    del login_session['username']
    del login_session['email']
    del login_session['facebook_id']
    del login_session['access_token']
    del login_session['user_id']
    del login_session['picture']
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


@app.route('/logout')
def logout():
    if 'facebook_id' in login_session.keys():
        fbdisconnect()
    if 'gplus_id' in login_session.keys():
        gdisconnect()
    flash('You have successfuly logged out!')
    return redirect(url_for('showLogin'))


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Catalog related actions

@app.route('/', defaults={"page": 1})
@app.route('/<int:page>')
@app.route('/categories/', defaults={"page": 1})
@app.route('/categories/page/<int:page>')
def showCategories(page):
    page = page
    per_page = 6
    categories = Category.query.all()
    category_items = CategoryItem.query.order_by(
        text("id DESC")).paginate(page, per_page, error_out=False)
    latest_category_item = CategoryItem.query.order_by(text("id DESC")).first()
    if 'username' not in login_session:
        flash("Please log in to be able to add,edit or delete items.")
        return render_template("category-index_not_logged.html", categories=categories, category_items=category_items,
                               latest_category_item=latest_category_item)
    return render_template("category-index_logged.html", categories=categories, category_items=category_items,
                           latest_category_item=latest_category_item)


@app.route('/categories/<int:category_id>/pages/<int:page>', defaults={"page": 1})
def categoryItems(category_id, page):
    page = page
    per_page = 6
    categories = Category.query.all()
    category = Category.query.filter_by(id=category_id).one()
    latest_category_item = CategoryItem.query.order_by(text("id DESC")).first()
    items = CategoryItem.query.filter_by(
        category_id=category.id).paginate(page, per_page, error_out=False)
    if 'username' not in login_session:
        return render_template('category-item-index_not_logged.html', category=category, items=items, categories=categories,
                               latest_category_item=latest_category_item)
    return render_template('category-item-index_logged.html', category=category, items=items, categories=categories,
                           latest_category_item=latest_category_item)


@app.route('/categories/<int:category_id>/items/<int:item_id>')
def itemIndex(category_id, item_id):
    categories = Category.query.all()
    category = Category.query.filter_by(id=category_id).one()
    latest_category_item = CategoryItem.query.order_by(text("id DESC")).first()
    item = CategoryItem.query.filter_by(id=item_id).one()
    if 'username' not in login_session:
        return render_template('item-index_not_logged.html', item=item, category=category, categories=categories,
                               latest_category_item=latest_category_item)
    return render_template('item-index_logged.html', item=item, category=category, categories=categories,
                           latest_category_item=latest_category_item)


@app.route('/categories/<int:category_id>/items/<int:item_id>/edit', methods=['POST', 'GET'])
def editItem(category_id, item_id):
    if request.method == "POST":
        item = CategoryItem.query.filter_by(id=item_id).one()
        item.name = request.form['title']
        item.description = request.form['description']
        item.price = request.form['price']
        item.category_id = request.form['category_id']
        db.session.commit()
        flash('Item Edited!')
        return redirect(url_for('categoryItems', category_id=category_id, item_id=item_id))

# API endpoints
@app.route('/api/v1/catalog.json')
def catalog_JSON():
    '''All items and categories from the catalog as a JSON'''
    catalog_items = CategoryItem.query.order_by(text('id ASC')).all()
    catalog_categories = Category.query.order_by(text('id ASC')).all()
    return jsonify(
        Categories=[
            category.serialize for category in catalog_categories], Items=[
            item.serialize for item in catalog_items])


@app.route('/api/v1/catalog_items/JSON')
def catalog_items_JSON():
    '''All items from the catalog as a JSON'''
    catalog_items = CategoryItem.query.order_by(text('id ASC')).all()
    return jsonify(catalog_items=[item.serialize for item in catalog_items])


@app.route('/api/v1/catalog_categories/JSON')
def catalog_categories_JSON():
    '''All categories from the catalog as a JSON'''
    catalog_categories = Category.query.order_by(text('id ASC')).all()
    return jsonify(catalog_categories=[categories.serialize for categories in catalog_categories])


@app.route('/api/v1/catalog_category/<int:category_id>/JSON')
def catalog_category_JSON(category_id):
    '''A specific category from the catalog as a JSON'''
    catalog_category = Category.query.filter_by(id=category_id).one()
    return jsonify(catalog_category=[catalog_category.serialize])


@app.route('/api/v1/catalog_item/<int:item_id>/JSON')
def catalog_item_JSON(item_id):
    '''A specific item from the catalog as a JSON'''
    catalog_item = CategoryItem.query.filter_by(id=item_id).one()
    return jsonify(catalog_item=[catalog_item.serialize])


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
