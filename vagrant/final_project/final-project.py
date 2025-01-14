from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

# Restaurant related actions

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    return render_template("restaurant-index.html", restaurants=restaurants)


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
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
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
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant.id))




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
