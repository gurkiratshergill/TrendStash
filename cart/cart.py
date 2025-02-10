from store.models import Product
class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {} 

        self.cart = cart
    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id not in self.cart:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        
        self.session['cart'] = self.cart  
        self.session.modified = True  

    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        return products
    def get_quantities(self):
        quantities = self.cart
        return quantities
