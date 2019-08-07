from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=["POST", "GET"])
def newMenuItem(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "POST":
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash('Menu Item ADded')
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    elif request.method == "GET":
        return render_template('newMenuItem.html', restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/edit/<int:menu_id>/', methods=["POST", "GET"])
def editMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    currItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        currItem.name = request.form['name']
        session.commit()
        flash('Menu Item Edited')
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    elif request.method == "GET":
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, curr_item = currItem)

    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>', methods=["POST", "GET"])
def deleteMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    currItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        session.delete(currItem)
        session.commit()
        flash('Menu Item deleted')
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    elif request.method == "GET":
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, curr_item = currItem)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)