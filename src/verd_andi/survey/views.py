from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from django.conf import settings

from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.utils import timezone
import datetime
from .models import Survey, User, Item, ItemObserver, Characteristic, Observation, ObservedCharacteristic
from .forms import ObservationForm

# Create your views here.
def index(request):
        return HttpResponse("Hello, world. You're at the survey index.")


class SurveyListView(ListView):
	model = Survey

	def get_context_data(self, **kwargs):
		context = super(SurveyListView, self).get_context_data(**kwargs)
		context['now'] = timezone.now()
		return context

class SurveyDetailView(DetailView):
	model = Survey

	def get_context_data(self, **kwargs):
		context = super(SurveyDetailView, self).get_context_data(**kwargs)
		context['now'] = timezone.now()
		print(str(context))
		return context


def survey_dash(request, id):
	if request.user.is_authenticated():



		context = {
			"user_name" : str(request.user),
			"user_id" : str(request.user.id),
		}

		return render(request, "survey/survey_dash.html", context)
	else:
		return redirect(settings.LOGIN_REDIRECT_URL)


def user_dash(request):
	if request.user.is_authenticated():

		focus_items = ItemObserver.objects.filter(user=request.user.id)
		items = set()  # creating a queryset of items, that have been slected for the user to observe.
		for i in focus_items.select_related('item'):
			items.add(i.item) 


		context = {
			"user_name" : str(request.user),
			"user_id" : str(request.user.id),
			"items" : items,
		}

		return render(request, "survey/survey_dash.html", context)
	else:
		return redirect(settings.LOGIN_REDIRECT_URL)


def item_observation(request, idx):
	if request.user.is_authenticated():
		item = Item.objects.filter(pk=idx)
		#print(item)
		# get item, get characteristics of item ..
		chars = Characteristic.objects.filter(item=idx)
		#print(chars)
		observations = Observation.objects.filter(item=idx)

		#form = ObservationForm(request.POST or None)
		#if request.method == 'POST':
		spec_chars = chars.filter(specify=True)
		#print(spec_chars[0].pk)
		#print(spec_chars[0].name)
		specified_chars = list( sc.name for sc in spec_chars)
		specified_chars_pk = list( sc.pk for sc in spec_chars)
		form = ObservationForm(request.POST or None, extra=specified_chars)
		if form.is_valid():
			# create observation, insert user-observer, obs-time, item, survey?
			obs_time = datetime.datetime.now()
			observer = request.user.pk
			item = idx
			# fields included in form.
			shop_type = form.cleaned_data['shop_type']
			shop_identifier = form.cleaned_data['shop_identifier']
			flag = form.cleaned_data['flag']
			discount = form.cleaned_data['discount']
			value = form.cleaned_data['value']
			brand = form.cleaned_data['brand']
			observed_quantity = form.cleaned_data['observed_quantity']
			obs_comment = form.cleaned_data['obs_comment']
			theitem = Item.objects.filter(pk=item)[0]
			theuser = User.objects.filter(pk=observer)[0]
			print(theitem)
			survey = getattr(theitem, 'survey')
			#survey = Survey.objects.filter(pk=surv.pk)
			observation = Observation.objects.create(
				observer=theuser, 
				obs_time=obs_time, 
				item=theitem, 
				shop_type=shop_type,
				shop_identifier=shop_identifier,
				flag=flag,
				discount=discount,
				value=value,
				brand=brand,
				observed_quantity=observed_quantity,
				obs_comment=obs_comment,
				survey = survey
				)
			observation.save()
			print(obs_time, observer, item, shop_type, shop_identifier, flag, discount, value, brand, observed_quantity, obs_comment)
			for (question, answer) in form.extra_answers():
				print(question) # label
				print(answer) # value
				# create observerd characteristic
				print(specified_chars.index(question))
				char_pk = specified_chars_pk[specified_chars.index(question)]
				# char = Characteristic.objects.filter(pk=char_pk)[0]
				print(observation.pk)
				# adding observed_characteristic, currently relies on order in QueryObject spec_chars bieng same as order inlists derived from it, which I think holds.
				observed_characteristic = ObservedCharacteristic.objects.create(observation=observation,characteristic=spec_chars[specified_chars.index(question)],value=answer) #
				observed_characteristic.save()
				#save_answer(request, question, answer)
			#return redirect(settings.LOGIN_REDIRECT_URL)
			return redirect("/survey/udash")
			#return redirect('')
			# for (question, answer) in form.extra_answers():
		 #    	save_answer(request, question, answer)
			# 	return redirect("create_user_success")
			

		context = {
			"form" : form,
			"user_name" : str(request.user),
			"user_id" : str(request.user.id),
			"item" : item,
			"characteristics" : chars,
			"observations" : observations,
		}

		return render(request, "survey/item_observation.html", context)
	else:
		return redirect(settings.LOGIN_REDIRECT_URL)

# def survey(request):
# 	if request.user.is_authenticated():

# 		org_qs = Org.objects.filter(members=request.user.id).order_by('name')

# 		context = {

# 			"user_name": str(request.user),
# 			"user_id": str(request.user.id),
# 			"orgs": org_qs,
# 		}
	
# 		return render(request, "user_dash.html", context)
# 	else:
# 		return redirect(settings.LOGIN_REDIRECT_URL)
