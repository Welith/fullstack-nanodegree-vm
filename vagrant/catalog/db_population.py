from database_setup import Category, CategoryItem, User, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Create a dummy user (pass: secret)
user1 = User(username="borko", email="testers@test.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/'
             '18debd694829ed78203a5a36dd364160_400x400.png',
             password_hash='2bb80d537b1da3e38bd30361'
             'aa855686bde0eacd7162fef6a25fe97bf527a25b')
db.session.add(user1)
db.session.commit()

# Create a dummy user (pass: secret)
user2 = User(username="borko95", email="tester@testers.com",
             picture='https://pbs.twimg.com/profile_images/'
             '2671170543/18debd694829ed78203a5a36dd364160_400x400.png',
             password_hash='2bb80d537b1da3e38bd30361aa85'
             '5686bde0eacd7162fef6a25fe97bf527a25b')
db.session.add(user2)
db.session.commit()

# Items for basketball category
category1 = Category(name="Basketball")

db.session.add(category1)
db.session.commit()

BasketballItem1 = CategoryItem(title="Spalding Ball",
                               description="The perfect basketball ball."
                               "Meant to be used in any condition.",
                               price="$20", category_id=category1.id,
                               category=category1, user_id=user1.id,
                               picture='https://www.spalding.com/dw/image/'
                               'v2/ABAH_PRD/on/demandware.static/-/Sites-'
                               'masterCatalog_SPALDING/default/'
                               'dw98a8f396/images/hi-res/Spalding-Digital-'
                               'Assets_34779.png?sw=555&sh=689&sm=cut')

db.session.add(BasketballItem1)
db.session.commit()


BasketballItem2 = CategoryItem(title="Reebok shorts",
                               description="The perfect basketball shorts. "
                               "Meant to be used in any condition.",
                               price="$30", category_id=category1.id,
                               category=category1, user_id=user1.id,
                               picture='https://assets.reebok.com/images'
                               '/w_280,h_280,f_auto,q_auto:sensitive/'
                               '0a3772aea5cf424eae1aaa4801178247_9366/'
                               'reebok-crossfit-games-austin-ii-shorts.jpg')

db.session.add(BasketballItem2)
db.session.commit()

BasketballItem3 = CategoryItem(title="Reebok vest",
                               description="The perfect basketball vest."
                               "Meant to be used in any condition.",
                               price="$25", category_id=category1.id,
                               category=category1, user_id=user1.id,
                               picture='https://encrypted-tbn0.gstatic.com'
                               '/images?q=tbn:ANd9GcSulnPKCL7uJSpQ'
                               'yOkLqELcidYuH9SEo9gy-nNpUxpCGV5iU3km')

db.session.add(BasketballItem3)
db.session.commit()

BasketballItem4 = CategoryItem(title="Nike Air shoes",
                               description="The perfect basketball shoes."
                               "Meant to be used in any condition.",
                               price="$100", category_id=category1.id,
                               category=category1, user_id=user1.id,
                               picture='http://www.famousfootwear.com'
                               '/ProductImages/shoes_ia92320.jpg')

db.session.add(BasketballItem4)
db.session.commit()

BasketballItem5 = CategoryItem(title="Nike Air headband",
                               description="The perfect basketball headband."
                               "Meant to be used in any condition.",
                               price="$10", category_id=category1.id,
                               category=category1, user_id=user1.id,
                               picture='https://images.nike.com/is/image'
                               '/DotCom/PDP_HERO/NNN07_101_A/swoosh-headband'
                               '-Plwcr9.jpg')

db.session.add(BasketballItem5)
db.session.commit()

# Items for baseball category
category2 = Category(name="Baseball")

db.session.add(category2)
db.session.commit()

BaseballItem1 = CategoryItem(title="Spalding Bat",
                             description="The perfect baseball bat."
                             "Meant to be used in any condition.",
                             price="$150", category_id=category2.id,
                             category=category2, user_id=user1.id,
                             picture='https://www.flaghouse.com/'
                             'productImages/image.axd/i.15815/w.600/'
                             'h.600/xm.0/Rawlings+reg%3B+Big+Stick+'
                             'Little+League+Baseball+Bat_.jpg')

db.session.add(BaseballItem1)
db.session.commit()

BaseballItem2 = CategoryItem(title="Adidas Cap",
                             description="The perfect baseball cap."
                             "Meant to be used in any condition.",
                             price="$50", category_id=category2.id,
                             category=category2, user_id=user1.id,
                             picture='https://rukminim1.flixcart.com/'
                             'image/400/400/jfoac280/cap/m/k/y/'
                             'm-baseball-cap-25214-adidas-original'
                             '-imaf42zdrsk5yybz.jpeg?q=90')

db.session.add(BaseballItem2)
db.session.commit()

BaseballItem3 = CategoryItem(title="Adidas Spiked Shoes",
                             description="The perfect baseball shoes."
                             "Meant to be used in any condition.",
                             price="$200", category_id=category2.id,
                             category=category2, user_id=user1.id,
                             picture='https://images-na.ssl-images-'
                             'amazon.com/images/I/81w37BANPiL._'
                             'UX395_.jpg')

db.session.add(BaseballItem3)
db.session.commit()

BaseballItem4 = CategoryItem(title="Adidas Training Kit",
                             description="The perfect baseball training kit."
                             "Meant to be used in any condition.",
                             price="$500", category_id=category2.id,
                             category=category2, user_id=user1.id,
                             picture='https://images-na.ssl-images-'
                             'amazon.com/images/I/81CxQtfR2-L._SY355_.jpg')

db.session.add(BaseballItem4)
db.session.commit()

# Items for footbal category
category3 = Category(name="Football")

db.session.add(category3)
db.session.commit()

FootballItem1 = CategoryItem(title="Adidas Ball",
                             description="The perfect football ball."
                             "Meant to be used in any condition.",
                             price="$150", category_id=category3.id,
                             category=category3, user_id=user2.id,
                             picture='https://images-na.ssl-images-'
                             'amazon.com/images/I/81piGHzhrdL._SY355_.jpg')

db.session.add(FootballItem1)
db.session.commit()

FootballItem2 = CategoryItem(title="Adidas Kit",
                             description="The perfect football training kit."
                             "Meant to be used in any condition.",
                             price="$300", category_id=category3.id,
                             category=category3, user_id=user2.id,
                             picture='https://www.kitking.co.uk/upload/'
                             'categories/210.jpg')

db.session.add(FootballItem2)
db.session.commit()

FootballItem3 = CategoryItem(title="Adidas trainers",
                             description="The perfect football trainers."
                             "Meant to be used in any condition.",
                             price="$100", category_id=category3.id,
                             category=category3, user_id=user2.id,
                             picture='https://images-na.ssl-images-'
                             'amazon.com/images/I/81AcjAWzCbL._UY395_.jpg')

db.session.add(FootballItem3)
db.session.commit()

FootballItem4 = CategoryItem(title="Nike shirt",
                             description="The perfect football shirt."
                             "Meant to be used in any condition.",
                             price="$50", category_id=category3.id,
                             category=category3, user_id=user2.id,
                             picture='https://www.admdirect.co.uk/'
                             'content/images/thumbs/0074885_nike-'
                             'tiempo-premier-jersey-short-sleeve_480.jpeg')
db.session.add(FootballItem4)
db.session.commit()


# Items for footbal category
category4 = Category(name="Boxing")

db.session.add(category4)
db.session.commit()


BoxingItem1 = CategoryItem(title="Adidas Gloves",
                           description="The perfect boxing gloves."
                           "Meant to be used in any condition.",
                           price="$150", category_id=category4.id,
                           category=category4, user_id=user2.id,
                           picture='https://images-na.ssl-images-'
                           'amazon.com/images/I/81NAheBaO4L._SY450_.jpg')

db.session.add(BoxingItem1)
db.session.commit()

BoxingItem2 = CategoryItem(title="Adidas shorts",
                           description="The perfect boxing shorts."
                           "Meant to be used in any condition.",
                           price="$200", category_id=category4.id,
                           category=category4, user_id=user2.id,
                           picture='https://images-na.ssl-images-'
                           'amazon.com/images/I/81ntjyFJSNL._SY355_.jpg')

db.session.add(FootballItem2)
db.session.commit()

BoxingItem3 = CategoryItem(title="Everlas Shoes",
                           description="The perfect boxing shoes."
                           "Meant to be used in any condition.",
                           price="$100", category_id=category4.id,
                           category=category4, user_id=user2.id,
                           picture='https://www.titleboxing.com/media/'
                           'catalog/product/cache/569e53797540ada5649'
                           'c3f8ae774fdb7/t/b/tbs18-bk_1_2.jpg')

db.session.add(BoxingItem3)
db.session.commit()


# Items for footbal category
category5 = Category(name="Fitness")

db.session.add(category5)
db.session.commit()

FitnessItem1 = CategoryItem(title="Adidas Gloves",
                            description="The perfect fitness gloves."
                            "Meant to be used in any condition.",
                            price="$150", category_id=category5.id,
                            category=category5, user_id=user2.id,
                            picture='https://images-na.ssl-images-'
                            'amazon.com/images/I/81HCNZV14mL._SY355_.jpg')

db.session.add(FitnessItem1)
db.session.commit()

FitnessItem2 = CategoryItem(title="Adidas Kit",
                            description="The perfect fitness training kit."
                            "Meant to be used in any condition.",
                            price="$400", category_id=category5.id,
                            category=category5, user_id=user2.id,
                            picture='https://rukminim1.flixcart.com/'
                            'image/832/832/resistance-tube/n/m/2/na-'
                            'adidas-36zero-trainer-original-imaea45h4t'
                            '467g3r.jpeg?q=70')

db.session.add(FitnessItem2)
db.session.commit()

FitnessItem3 = CategoryItem(title="Adidas Shoes",
                            description="The perfect fitness shoes."
                            "Meant to be used in any condition.",
                            price="$200", category_id=category5.id,
                            category=category5, user_id=user2.id,
                            picture='https://s7d2.scene7.com/is'
                            '/image/academy/20107496?$m-pdp-product-image$')

db.session.add(FitnessItem3)
db.session.commit()


# Items for footbal category
category6 = Category(name="Hiking")

db.session.add(category6)
db.session.commit()

HikingItem1 = CategoryItem(title="Adidas Backpack",
                           description="The perfect hicking backpack."
                           "Meant to be used in any condition.",
                           price="$300", category_id=category6.id,
                           category=category6, user_id=user2.id,
                           picture='https://images-na.ssl-images'
                           '-amazon.com/images/I/71wANzAKe3L._SY355_.jpg')

db.session.add(HikingItem1)
db.session.commit()

HikingItem2 = CategoryItem(title="Adidas Bottle",
                           description="The perfect hicking water bottle."
                           "Meant to be used in any condition.",
                           price="$50", category_id=category6.id,
                           category=category6, user_id=user2.id,
                           picture='https://i.ebayimg.com/images/'
                           'g/EIgAAOSwrLZbaspL/s-l640.jpg')

db.session.add(HikingItem2)
db.session.commit()

HikingItem3 = CategoryItem(title="Adidas Hiking Kit",
                           description="The perfect hiking kit."
                           "Meant to be used in any condition.",
                           price="$600", category_id=category6.id,
                           category=category6, user_id=user2.id,
                           picture='http://cdn.shopify.com/s/files'
                           '/1/0038/8890/6340/products/product-image-'
                           '876672147_1200x1200.jpg?v=1548382883')

db.session.add(HikingItem3)
db.session.commit()


print("added catalog items!")
