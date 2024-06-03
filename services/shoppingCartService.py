from models.shoppingCart import ShoppingCart, CartItem
from database import db
from sqlalchemy.orm import Session

def add_cart_item(customer_id, product_id, quantity):
    with Session(db.engine) as session:
        shopping_cart = session.query(ShoppingCart).filter_by(customer_id=customer_id).first()
        if not shopping_cart:
            shopping_cart = ShoppingCart(customer_id=customer_id)
            session.add(shopping_cart)
            session.flush()  
        cart_item = session.query(CartItem).filter_by(shopping_cart_id=shopping_cart.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += int(quantity)
        else:
            cart_item = CartItem(product_id=product_id, quantity=int(quantity), shopping_cart_id=shopping_cart.id)
            session.add(cart_item)
        
        session.commit()
        
        session.refresh(shopping_cart)
        shopping_cart.items
        
    return shopping_cart

def delete_cart_item(customer_id, product_id):
    with Session(db.engine) as session:
        shopping_cart = session.query(ShoppingCart).filter_by(customer_id=customer_id).first()
        if shopping_cart:
            cart_item = session.query(CartItem).filter_by(shopping_cart_id=shopping_cart.id, product_id=product_id).first()
            if cart_item:
                session.delete(cart_item)
                session.commit()
                session.refresh(shopping_cart) 

def update_item_quantity(customer_id, product_id, quantity):
    with Session(db.engine) as session:
        shopping_cart = session.query(ShoppingCart).filter_by(customer_id=customer_id).first()
        if shopping_cart:
            cart_item = session.query(CartItem).filter_by(shopping_cart_id=shopping_cart.id, product_id=product_id).first()
            if cart_item:
                cart_item.quantity = int(quantity)
                session.commit()
                session.refresh(shopping_cart) 

def get_shopping_cart(customer_id):
    with Session(db.engine) as session:
        shopping_cart = session.query(ShoppingCart).filter_by(customer_id=customer_id).first()
        if shopping_cart:
            session.refresh(shopping_cart) 
        return shopping_cart

def empty_shopping_cart(customer_id):
    with Session(db.engine) as session:
        shopping_cart = session.query(ShoppingCart).filter_by(customer_id=customer_id).first()
        if shopping_cart:
            session.query(CartItem).filter_by(shopping_cart_id=shopping_cart.id).delete()
            session.commit()
            session.refresh(shopping_cart)