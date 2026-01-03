import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from graphql import GraphQLError
from graphene.types import Decimal as GrapheneDecimal
from django.utils import timezone
from . models import Customer, Product, Order


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email', 'phone', 'created_at')


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock')


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ('id', 'customer', 'products', 'total_amount', 'order_date')

class CustomerInput(graphene.InputObjectType):
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int()


class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()


class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        try:
            validate_email(input.email)
            if Customer.objects.filter(email=input.email).exists():
                return CreateCustomer(
                    customer=None,
                    message='Email already exists'
            )
            
            customer = Customer.objects.create(
                name=input.name,
                email=input.email,
                phone=input.phone or ''
            )

            return CreateCustomer(
                customer=customer, 
                message='Customer created successfully'
            )
        
        except ValidationError:
            return CreateCustomer(
                customer=None, 
                message='Invalid email format'
            )
        

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        created = []
        errors = []

        with transaction.atomic():
            for c in input:
                try:
                    validate_email(c.email)
                    if Customer.objects.filter(email=c.email).exists():
                        errors.append(f'{c.email}: Email already exists')
                        continue
                    customer = Customer.objects.create(name=c.name, email=c.email, phone=c.phone or '')
                    created.append(customer)
                except ValidationError:
                    errors.append(f'{c.email}: Invalid email')
        
        return BulkCreateCustomers(customers=created, errors=errors)
    

class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, input):
        if input.price <= 0.00:
            raise GraphQLError('Price must be positive')

        if input.stock is not None and input.stock < 0:
            raise GraphQLError('Stock cannot be negative')
        
        product = Product.objects.create(
            name=input.name, 
            price=input.price,
            stock=input.stock or 0
        )
        return CreateProduct(product=product)
    

class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, input):
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist():
            raise GraphQLError('Invalid customer ID')
        
        products = Product.objects.filter(pk__in=input.product_ids)
        if not products.exists():
            raise GraphQLError('No valid products selected')
        
        order = Order.objects.create(
            customer=customer,
            order_date=input.order_date or timezone.now()
        )
        order.products.set(products)

        # To calculate the sum of all products.
        order.total_amount = sum(p.price for p in products)
        order.save()

        return CreateOrder(order=order)


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return 'Hello, GraphQL!'
    

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()