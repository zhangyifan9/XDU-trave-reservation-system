from django import forms

class LoginForm(forms.Form):
    id = forms.CharField(label="id", max_length=20)
    password = forms.CharField(label="password", max_length=20)
    position = forms.CharField(label="position", max_length=20)

class RegisterForm(forms.Form):
    custID = forms.CharField(label="custID", max_length=20)
    custPassword = forms.CharField(label="custPassword", max_length=20)
    custName = forms.CharField(label="custName", max_length=50)
    age = forms.IntegerField(label="age")
    sex = forms.CharField(label="sex", max_length=5)
    balance = forms.IntegerField(label="balance")


class FLIGHTSForm(forms.Form):
    flightNum = forms.CharField(label="flightNum", max_length=50)
    price = forms.IntegerField(label="price")
    numSeats = forms.IntegerField(label="numSeats")
    numAvail = forms.IntegerField(label="numAvail")
    FromCity = forms.CharField(label="FromCity", max_length=50)
    ArivCity = forms.CharField(label="ArivCity", max_length=50)


class HOTELSForm(forms.Form):
    location = forms.CharField(label="location", max_length=50)
    price = forms.IntegerField(label="price")
    numRooms = forms.IntegerField(label="numRooms")
    numAvail = forms.IntegerField(label="numAvail")


class BUSForm(forms.Form):
    location = forms.CharField(label="location", max_length=50)
    price = forms.IntegerField(label="price")
    numBus = forms.IntegerField(label="numRooms")
    numAvail = forms.IntegerField(label="numAvail")


class RESERVATIONSForm(forms.Form):
    custName = forms.CharField(label="custName", max_length=50)
    resvType = forms.IntegerField(label="resvType")
    resvKey = forms.CharField(label="resvKey", max_length=50)
    resvInfo = forms.CharField(max_length=50)

class AdministratorForm(forms.Form):
    adminID = forms.CharField(label="adminID", max_length=20)
    adminPassword = forms.CharField(label="adminPassword",max_length=20)
    Balance = forms.IntegerField(label="Balance")


class CUSTOMERSForm(forms.Form):
    custName = forms.CharField(label="custName", max_length=50)
    custID = forms.CharField(label="custID", max_length=20)
    custPassword = forms.CharField(label="custPassword", max_length=20)
    age = forms.IntegerField(label="age")
    sex = forms.CharField(label="sex", max_length=5)
    balance = forms.IntegerField(label="balance")


class CHECKForm(forms.Form):
    FromCity = forms.CharField(label="FromCity", max_length=50)
    ArivCity = forms.CharField(label="ArivCity", max_length=50)
