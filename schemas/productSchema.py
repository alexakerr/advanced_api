from marshmallow import fields, validate
from schemas import ma


# For Creating a new Product
class ProductSchema(ma.Schema):
    id = fields.Integer(required=False) # id is autogenerated
    name = fields.String(required=True, validate=validate.Length(min=5, max=20)) # Product Name must be between 5 and 20 characters
    price = fields.Float(required=True, validate=validate.Range(min=0)) # Product Price must be >= 0

    class Meta:
        fields = ("id", "name", "price")

# For adding products to Order
class ProductIdSchema(ma.Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=False)
    price = fields.String(required=False)


# Create an instance of the ProductSchema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True) # For handling multiple products