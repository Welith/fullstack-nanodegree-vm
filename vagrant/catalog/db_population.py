from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, CategoryItem, User


engine = create_engine('sqlite:///catalogItems.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create a dummy user (pass: secret)
user1 = User(username="borko", email="testers@test.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png',
             password_hash='2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b')
session.add(user1)
session.commit()

# Create a dummy user (pass: secret)
user2 = User(username="borko95", email="tester@testers.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png',
             password_hash='2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b')
session.add(user2)
session.commit()

# Items for basketball category
category1 = Category(name="Basketball")

session.add(category1)
session.commit()

BasketballItem1 = CategoryItem(title="Spalding Ball", description="The perfect basketball ball. Meant to be used in any condition.",
                               price="$20", category_id=category1.id, category=category1, user_id=user1.id,
                               picture='https://www.spalding.com/dw/image/v2/ABAH_PRD/on/demandware.static/-/Sites-masterCatalog_SPALDING/default/dw98a8f396/images/hi-res/Spalding-Digital-Assets_34779.png?sw=555&sh=689&sm=cut')

session.add(BasketballItem1)
session.commit()


BasketballItem2 = CategoryItem(title="Reebok shorts", description="The perfect basketball shorts. Meant to be used in any condition.",
                               price="$30", category_id=category1.id, category=category1, user_id=user1.id,
                               picture='https://assets.reebok.com/images/w_280,h_280,f_auto,q_auto:sensitive/0a3772aea5cf424eae1aaa4801178247_9366/reebok-crossfit-games-austin-ii-shorts.jpg')

session.add(BasketballItem2)
session.commit()

BasketballItem3 = CategoryItem(title="Reebok vest", description="The perfect basketball vest. Meant to be used in any condition.",
                               price="$25", category_id=category1.id, category=category1, user_id=user1.id,
                               picture='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSulnPKCL7uJSpQyOkLqELcidYuH9SEo9gy-nNpUxpCGV5iU3km')

session.add(BasketballItem3)
session.commit()

BasketballItem4 = CategoryItem(title="Nike Air shoes", description="The perfect basketball shoes. Meant to be used in any condition.",
                               price="$100", category_id=category1.id, category=category1, user_id=user1.id,
                               picture='http://www.famousfootwear.com/ProductImages/shoes_ia92320.jpg')

session.add(BasketballItem4)
session.commit()

BasketballItem5 = CategoryItem(title="Nike Air headband", description="The perfect basketball headband. Meant to be used in any condition.",
                               price="$10", category_id=category1.id, category=category1, user_id=user1.id,
                               picture='https://images.nike.com/is/image/DotCom/PDP_HERO/NNN07_101_A/swoosh-headband-Plwcr9.jpg')

session.add(BasketballItem5)
session.commit()

# Items for baseball category
category2 = Category(name="Baseball")

session.add(category2)
session.commit()

BaseballItem1 = CategoryItem(title="Spalding Bat", description="The perfect baseball bat. Meant to be used in any condition.",
                             price="$150", category_id=category2.id, category=category2, user_id=user1.id,
                             picture='https://www.flaghouse.com/productImages/image.axd/i.15815/w.600/h.600/xm.0/Rawlings+reg%3B+Big+Stick+Little+League+Baseball+Bat_.jpg')

session.add(BaseballItem1)
session.commit()

BaseballItem2 = CategoryItem(title="Adidas Cap", description="The perfect baseball cap. Meant to be used in any condition.",
                             price="$50", category_id=category2.id, category=category2, user_id=user1.id,
                             picture='https://rukminim1.flixcart.com/image/400/400/jfoac280/cap/m/k/y/m-baseball-cap-25214-adidas-original-imaf42zdrsk5yybz.jpeg?q=90')

session.add(BaseballItem2)
session.commit()

BaseballItem3 = CategoryItem(title="Adidas Spiked Shoes", description="The perfect baseball shoes. Meant to be used in any condition.",
                             price="$200", category_id=category2.id, category=category2, user_id=user1.id,
                             picture='https://images-na.ssl-images-amazon.com/images/I/81w37BANPiL._UX395_.jpg')

session.add(BaseballItem3)
session.commit()

BaseballItem4 = CategoryItem(title="Adidas Training Kit", description="The perfect baseball training kit. Meant to be used in any condition.",
                             price="$500", category_id=category2.id, category=category2, user_id=user1.id,
                             picture='https://images-na.ssl-images-amazon.com/images/I/81CxQtfR2-L._SY355_.jpg')

session.add(BaseballItem4)
session.commit()

# Items for footbal category
category3 = Category(name="Football")

session.add(category3)
session.commit()

FootballItem1 = CategoryItem(title="Adidas Ball", description="The perfect football ball. Meant to be used in any condition.",
                             price="$150", category_id=category3.id, category=category3, user_id=user2.id,
                             picture='https://images-na.ssl-images-amazon.com/images/I/81piGHzhrdL._SY355_.jpg')

session.add(FootballItem1)
session.commit()

FootballItem2 = CategoryItem(title="Adidas Kit", description="The perfect football training kit. Meant to be used in any condition.",
                             price="$300", category_id=category3.id, category=category3, user_id=user2.id,
                             picture='https://www.kitking.co.uk/upload/categories/210.jpg')

session.add(FootballItem2)
session.commit()

FootballItem3 = CategoryItem(title="Adidas trainers", description="The perfect football trainers. Meant to be used in any condition.",
                             price="$100", category_id=category3.id, category=category3, user_id=user2.id,
                             picture='https://images-na.ssl-images-amazon.com/images/I/81AcjAWzCbL._UY395_.jpg')

session.add(FootballItem3)
session.commit()

FootballItem4 = CategoryItem(title="Nike shirt", description="The perfect football shirt. Meant to be used in any condition.",
                             price="$50", category_id=category3.id, category=category3, user_id=user2.id,
                             picture='https://www.admdirect.co.uk/content/images/thumbs/0074885_nike-tiempo-premier-jersey-short-sleeve_480.jpeg')
session.add(FootballItem4)
session.commit()


# Items for footbal category
category4 = Category(name="Boxing")

session.add(category4)
session.commit()


BoxingItem1 = CategoryItem(title="Adidas Gloves", description="The perfect boxing gloves. Meant to be used in any condition.",
                           price="$150", category_id=category4.id, category=category4, user_id=user2.id,
                           picture='https://images-na.ssl-images-amazon.com/images/I/81NAheBaO4L._SY450_.jpg')

session.add(BoxingItem1)
session.commit()

BoxingItem2 = CategoryItem(title="Adidas shorts", description="The perfect boxing shorts. Meant to be used in any condition.",
                           price="$200", category_id=category4.id, category=category4, user_id=user2.id,
                           picture='https://images-na.ssl-images-amazon.com/images/I/81ntjyFJSNL._SY355_.jpg')

session.add(FootballItem2)
session.commit()

BoxingItem3 = CategoryItem(title="Everlas Shoes", description="The perfect boxing shoes. Meant to be used in any condition.",
                           price="$100", category_id=category4.id, category=category4, user_id=user2.id,
                           picture='https://www.titleboxing.com/media/catalog/product/cache/569e53797540ada5649c3f8ae774fdb7/t/b/tbs18-bk_1_2.jpg')

session.add(BoxingItem3)
session.commit()


# Items for footbal category
category5 = Category(name="Fitness")

session.add(category5)
session.commit()

FitnessItem1 = CategoryItem(title="Adidas Gloves", description="The perfect fitness gloves. Meant to be used in any condition.",
                            price="$150", category_id=category5.id, category=category5, user_id=user2.id,
                            picture='https://images-na.ssl-images-amazon.com/images/I/81HCNZV14mL._SY355_.jpg')

session.add(FitnessItem1)
session.commit()

FitnessItem2 = CategoryItem(title="Adidas Kit", description="The perfect fitness training kit. Meant to be used in any condition.",
                            price="$400", category_id=category5.id, category=category5, user_id=user2.id,
                            picture='https://rukminim1.flixcart.com/image/832/832/resistance-tube/n/m/2/na-adidas-36zero-trainer-original-imaea45h4t467g3r.jpeg?q=70')

session.add(FitnessItem2)
session.commit()

FitnessItem3 = CategoryItem(title="Adidas Shoes", description="The perfect fitness shoes. Meant to be used in any condition.",
                            price="$200", category_id=category5.id, category=category5, user_id=user2.id,
                            picture='https://s7d2.scene7.com/is/image/academy/20107496?$m-pdp-product-image$')

session.add(FitnessItem3)
session.commit()


# Items for footbal category
category6 = Category(name="Hiking")

session.add(category6)
session.commit()

HikingItem1 = CategoryItem(title="Adidas Backpack", description="The perfect hicking backpack. Meant to be used in any condition.",
                            price="$300", category_id=category6.id, category=category6, user_id=user2.id,
                            picture='https://images-na.ssl-images-amazon.com/images/I/71wANzAKe3L._SY355_.jpg')

session.add(HikingItem1)
session.commit()

HikingItem2 = CategoryItem(title="Adidas Bottle", description="The perfect hicking water bottle. Meant to be used in any condition.",
                            price="$50", category_id=category6.id, category=category6, user_id=user2.id,
                            picture='https://i.ebayimg.com/images/g/EIgAAOSwrLZbaspL/s-l640.jpg')

session.add(HikingItem2)
session.commit()

HikingItem3 = CategoryItem(title="Adidas Hiking Kit", description="The perfect hiking kit. Meant to be used in any condition.",
                            price="$600", category_id=category6.id, category=category6, user_id=user2.id,
                            picture='http://cdn.shopify.com/s/files/1/0038/8890/6340/products/product-image-876672147_1200x1200.jpg?v=1548382883')

session.add(HikingItem3)
session.commit()


print("added catalog items!")
