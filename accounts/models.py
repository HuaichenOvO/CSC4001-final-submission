from django.db import models
from django.contrib.auth.models import User


"""
0. Token    | Stores the temporal data of registration. The token attribute will be sent to the user's email 
              in the format of website_main_url/token. Once the user clicks the link, aotumatically the token's
              information will be used to create a USER instance in the django's latent table.
1. Client   | Stores the profile of the user (since the user table a default django database.
              CLIENT is as the extension of USER table, storing attributes that USER does not include.
              Hence, CLIENT and USER is one to one)
3. Post     | Stores a user's post (a post is an order that nobody acts as a sender)
2. Order    | Stores a user's post (an post comes from a post, plus user as a sender)
4. Address  | Stores the address of the school of a user
"""


class Token(models.Model):
    uname = models.CharField(max_length=100)
    email = models.EmailField()
    pwd_1 = models.CharField(max_length=100)
    token = models.CharField(max_length=100)


class Client(models.Model):

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=100, blank=True, default="Anonymous"+str(id))
    phone = models.CharField(max_length=200, null=True)
    coin_num = models.IntegerField(default=2)
    tasks_delivered = models.IntegerField(default=0)
    join_date = models.DateTimeField(auto_created=True, auto_now_add=True, null=True)
    photo = models.ImageField(null=True, blank=True, default="ohh.png")
    # models, forms, views, html, settings
    # orders = models.ManyToManyField(Order) # 如果一个用户对应的多个xx，可以使用manytomanyField

    def __str__(self):
        return self.nick_name

class Address(models.Model):
    AREA = (
        ('Harmonia','Harmonia'),
        ('Shaw','Shaw'),
        ('Muse','Muse'),
        ('Diligentia','Diligentia'),
        ('Startup','Startup'),
        ('Teaching','Teaching'),
        ('Others','Others'),
    )
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    area = models.CharField(max_length=200, null=True, choices=AREA) #choices相当于一个枚举
    building = models.CharField(max_length=50, null=True)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.area + " " + self.building + str(self.number)

class Order(models.Model):
    STATUS = (
        ('Pending','Pending'), 
        ('Sending','Sending'),
        ('Claiming','Claiming'),# arrived
        ('Canceled','Canceled'),
        ('Done','Done'),
    )
    buyer = models.ForeignKey(User, related_name="as_buyer", null=True, on_delete=models.SET_NULL)
    sender = models.ForeignKey(User, related_name="as_sender", null=True, on_delete=models.SET_NULL)
    coin_reward = models.IntegerField(null=True)
    take_addr = models.ForeignKey(Address, related_name="as_start_addr",  null=True,on_delete=models.SET_NULL)
    send_addr = models.ForeignKey(Address, related_name="as_target_addr", null=True, on_delete=models.SET_NULL)
    exp_min = models.IntegerField(default=30)
    note = models.TextField(max_length=4000, blank=True, default="None")
    status = models.CharField(max_length=200, default='Pending', choices=STATUS)
    food_info = models.ImageField(null=True, blank=True)


    def __str__(self):
        return self.buyer.client.nick_name + "'s order- " + str(self.id)

    def can_cancel(self) -> bool:
        if (self.status == "Pending"): return  True
        else: return False

    """
    determine if an order's status is Sending or Claiming
    """
    def is_picked(self) -> bool:
        if (self.status == "Sending" or self.status=="Claiming"): return  True
        else: return False

    """
    determine if an order's status is Claiming
    """
    def is_arrived(self) -> bool:
        if (self.status=="Claiming"): return  True
        else: return False


class Task(models.Model):
    buyer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    coin_reward = models.IntegerField(null=True)
    take_addr = models.ForeignKey(Address, related_name="tobe_start_addr",  null=True,on_delete=models.SET_NULL)
    send_addr = models.ForeignKey(Address, related_name="tobe_target_addr", null=True, on_delete=models.SET_NULL)
    exp_min = models.IntegerField(default=30)
    note = models.TextField(max_length=4000, null=True, blank=True, default="None")
    food_info = models.ImageField(null=True, blank=True)
    post_time = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.buyer.client.nick_name + "'s post- " + str(self.id)