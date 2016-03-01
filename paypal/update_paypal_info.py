from paypal.pro.helpers import PayPalWPP
from paypal.pro.exceptions import PayPalFailure
from paypal.pro.models import PayPalNVP
from users.models import UsersProfile

wpp = PayPalWPP()

user_email = "benfatola@cloudcustomsolutions.com"
params = {'expdate': '012024', 'cvv2': u'123', 'acct': u'4032031179702831', 'creditcardtype': 'Visa'}

usr_obj = UsersProfile.objects.get(email=user_email)
paypal_obj = PayPalNVP.objects.filter(user=usr_obj).latest('updated_at')

params['profileid'] = paypal_obj.profileid

nvp_obj = wpp.updateRecurringPaymentsProfile(params)


