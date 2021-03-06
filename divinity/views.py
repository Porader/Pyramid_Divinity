from pyramid.view import view_config
from pyramid.response import Response
from models import User, Session, Base, engine, Item, Recipe, Category

from pyramid.security import (
remember,
forget,
)

from pyramid.httpexceptions import (
HTTPFound,
HTTPNotFound,
)

@view_config(route_name='home', renderer='templates/home.jinja2')
def my_view(request):
    DBSession = Session(bind=engine)
    categories = DBSession.query(Category)
    user = None
    if request.authenticated_userid!=None:
    	user = DBSession.query(User).filter(User.name == request.authenticated_userid).first()
    return {'categories': categories,
            'username': request.authenticated_userid,
	    'user':user
            }

@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    if 'POST' == request.method:
        login = request.params['login']
        password = request.params['password']
        DBSession = Session(bind=engine)
        user = DBSession.query(User).filter(login==User.name).first()
        if user!=None and user.password == password:
             headers = remember(request, login)			
             return HTTPFound(location = '/', headers = headers)
        else:
             return {'message': "Incorrect login or password",
                     'username': request.authenticated_userid
                    }
    else: return{'username': request.authenticated_userid}

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = '/', headers = headers)

@view_config(route_name='registration', renderer='templates/registration.jinja2')
def registration_view(request):
    if 'POST' == request.method:
        user_name = request.params['login']
        user_password = request.params['password']
	user_password_copy = request.params['password_copy']
	user_fullname = request.params['fullname']
	new_user = None
        DBSession = Session(bind=engine)
	if DBSession.query(User).filter_by(name=user_name).first()==None:
		if user_password!=None and user_password!="" and user_name!=None and user_name!="":
        		if user_password == user_password_copy:
				new_user = User(name=user_name, password=user_password, fullname=user_fullname, info="")
				DBSession.add(new_user)
				DBSession.commit()
	    		else:
            			return {'message': "Passwords do not match",
					'username': request.authenticated_userid}
		else:
			return {'message': "Passwords or login is none",
				'username': request.authenticated_userid}
	else:
		return {'message': "User already exists",
			'username': request.authenticated_userid}
	if new_user!=None:
            headers = remember(request, user_name) 
            return HTTPFound(location = '/', headers = headers)
	else:
            return {'message': "new_user is none",
                    'username': request.authenticated_userid
                    }
    else: return{'username': request.authenticated_userid}

@view_config(route_name='addItem', renderer='templates/addItem.jinja2', permission = 'add')
def addItem_view(request):
	DBSession = Session(bind=engine)
	user = None
    	if request.authenticated_userid!=None:
    		user = DBSession.query(User).filter(User.name == request.authenticated_userid).first()
	if 'POST' == request.method:
		item_info = None
		if request.params['item_category']!="":
			if 'item_info' in request.params:
				item_info = request.params['item_info']
			if 'item_name' in request.params and request.params['item_name']!="" and 'item_image' in request.params:
				if DBSession.query(Item).filter_by(name=request.params['item_name']).first()==None:
					item_name = request.params['item_name']
					item_category = request.params['item_category']
					new_item_category_id = DBSession.query(Category).filter_by(id=item_category).first().id
					new_item = Item(image="", name=item_name, info = item_info, category_id=new_item_category_id)
					DBSession.add(new_item)
					DBSession.commit()
					new_item.image=str(new_item.id)+".jpg"
					DBSession.commit()
					with open("divinity/static/image/"+new_item.image,'wb') as f: 
						f.write(request.params["item_image"].value)
					return {'message': "added",
						'username': request.authenticated_userid,
						'categories' : DBSession.query(Category),
						'user':user}
				else:
					return {'message': "Name already exists",
						'username': request.authenticated_userid,
						'categories' : DBSession.query(Category),
						'user':user
					       }
			else:
				return {'message': "nofull",
					'username': request.authenticated_userid,
					'categories' : DBSession.query(Category),
					'user':user
				       }
		else:
			return {'message': "nofull",
				'username': request.authenticated_userid,
				'categories' : DBSession.query(Category),
				'user':user
				}
	else: return{'username': request.authenticated_userid,
		     'categories' : DBSession.query(Category),
		     'user':user }

@view_config(route_name='addCategory', renderer='templates/addCategory.jinja2', permission = 'add')
def addCategory_view(request):
	DBSession = Session(bind=engine)
	user = None
    	if request.authenticated_userid!=None:
		user = DBSession.query(User).filter(User.name == request.authenticated_userid).first()
	if 'POST' == request.method:
        	Category_name = request.params['Category_name']
		if Category_name!="":
			if DBSession.query(Category).filter(Category.name==Category_name).first()==None:
				new_category = Category(name=Category_name)
				DBSession.add(new_category)
				DBSession.commit()
				return {'message': "added",
					'username': request.authenticated_userid,
					'user':user}
			else:
				return {'message': "Name already exists",
		                	'username': request.authenticated_userid,
		     			'user':user
		                	}
		else:
			return {'message': "nofull",
                    		'username': request.authenticated_userid,
		     		'user':user
                    		}
	else: return{'username': request.authenticated_userid,
		     'user':user}

@view_config(route_name='addRecipe', renderer='templates/addRecipe.jinja2', permission = 'add')
def addRecipe_view(request):
    	DBSession = Session(bind=engine)
	user = None
    	if request.authenticated_userid!=None:
		user = DBSession.query(User).filter(User.name == request.authenticated_userid).first()
	if 'POST' == request.method:
		if request.params['recipe_final']!="" and request.params['recipe_first']!="" and request.params['recipe_second']!="" and request.params['recipe_level']!="":
			recipe_final = request.params['recipe_final']
			recipe_first = request.params['recipe_first']
			recipe_second = request.params['recipe_second']
			recipe_level = request.params['recipe_level']
			new_recipe_final_id = DBSession.query(Item).filter_by(id=recipe_final).first().id
			new_recipe_first = DBSession.query(Item).filter_by(id=recipe_first).first()
			new_recipe_second = DBSession.query(Item).filter_by(id=recipe_second).first()
			new_recipe = Recipe(level=recipe_level, result_item_id =new_recipe_final_id)
			DBSession.add(new_recipe)
			DBSession.commit()
			new_recipe.first_item.append(new_recipe_first)
			new_recipe.second_item.append(new_recipe_second)
			DBSession.commit()
			return {'message': "added",
					'username': request.authenticated_userid,
					'items': DBSession.query(Item),
					'user':user}
		else:
			return {'message': "nofull",
                    		'username': request.authenticated_userid,
				'items': DBSession.query(Item),
		     		'user':user
                    		}
	else: return{'username': request.authenticated_userid,
		     'items': DBSession.query(Item),
		     'user':user}

@view_config(route_name='item', renderer='templates/item.jinja2')
def item_view(request):
    DBSession = Session(bind=engine)
    user = None
    if request.authenticated_userid!=None:
	user = DBSession.query(User).filter(User.name == request.authenticated_userid).first()
    item_id = request.matchdict['id']
    item = DBSession.query(Item).filter_by(id=item_id).first()
    try:
	item.recipe_use
	item.first_items
	item.second_items
    except Exception: i=0
    return {'username': request.authenticated_userid,
	    'item': item,
	    'user':user}

@view_config(route_name='recipe', renderer='templates/recipe.jinja2')
def recipe_view(request):
    DBSession = Session(bind=engine)
    user = None
    if request.authenticated_userid!=None:
	user = DBSession.query(User).filter(User.name == request.authenticated_userid).first()
    recipe_id = request.matchdict['id']
    recipe = DBSession.query(Recipe).filter_by(id=recipe_id).first()
    return {'username': request.authenticated_userid,
	    'recipe': recipe,
	    'user':user}
