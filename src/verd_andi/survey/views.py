from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView
from django.utils import timezone
import datetime
from .models import Survey, User, Item, ItemObserver, Characteristic, Observation, ObservedCharacteristic, ItemCommentary
from .forms import ObservationForm, ItemCommentaryForm
from django.contrib.auth.views import redirect_to_login

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


		surveys = Survey.objects.all() # could use filter in the future for current surveys.

		context = {
			"user_name" : str(request.user),
			"user_id" : str(request.user.id),
			"items" : items,
			"surveys" : surveys,
		}

		return render(request, "survey/survey_dash.html", context)
	else:
		return redirect(settings.REDIRECT_TO_LOGIN)


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
		if form.is_valid():  #POST request
			# create observation, insert user-observer, obs-time, item, survey?
			obs_time = datetime.datetime.now()
			observer = request.user.pk
			item = idx
			# fields included in form.
			shop_type = form.cleaned_data['shop_type']
			shop_identifier = form.cleaned_data['shop_identifier']
			#flag = form.cleaned_data['flag']
			discount = form.cleaned_data['discount']
			value = form.cleaned_data['value']
			observed_quantity = form.cleaned_data['observed_quantity']
			obs_comment = form.cleaned_data['obs_comment']
			theitem = Item.objects.filter(pk=item)[0]
			theuser = User.objects.filter(pk=observer)[0]
			print(theitem)
			surv = getattr(theitem, 'survey')
			#survey = Survey.objects.filter(pk=surv.pk)
			observation = Observation.objects.create(
				observer=theuser, 
				obs_time=obs_time, 
				item=theitem, 
				shop_type=shop_type,
				shop_identifier=shop_identifier,
				flag="O",
				discount=discount,
				value=value,
				observed_quantity=observed_quantity,
				obs_comment=obs_comment,
				survey = surv
				)
			observation.save()
			print(obs_time, observer, item, shop_type, shop_identifier, discount, value, observed_quantity, obs_comment)
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
			#return redirect("/survey/udash")
			#return redirect("survey.views.survey-userdash")
			return HttpResponseRedirect(reverse('survey:survey-userdash'))
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


def search(request, pk):
	if request.user.is_authenticated():

		items = Item.objects.filter(survey=pk)

		context = {
			"user_name" : str(request.user),
			"user_id" : str(request.user.id),
			"items" : items,
		}


		return render(request, "survey/survey_search.html", context)

	else:
		return redirect(settings.LOGIN_REDIRECT_URL)




def ItemCommentaryView(request, idx):
	if request.user.is_superuser:
		commentary = ItemCommentary.objects.get_or_create(pk=idx)[0]
		print(str(commentary))

		data = {
			'seasonality': commentary.seasonality, 
			'representativity':commentary.representativity,
			'comment':commentary.comment,
			'vat':commentary.vat
			}

		form = ItemCommentaryForm(request.POST or None, initial=data)
		if form.is_valid():  #POST request
			#shop_type = form.cleaned_data['shop_type']
			seasonality = form.cleaned_data['seasonality']
			representativity = form.cleaned_data['representativity']
			comment = form.cleaned_data['comment']
			vat = form.cleaned_data['vat']

			commentary.seasonality = seasonality
			commentary.representativity = representativity
			commentary.comment = comment
			commentary.vat = vat

			commentary.save()
			print("form was good")
			return HttpResponseRedirect(reverse('survey:survey-userdash'))

		context = {
			"form" : form,
		}

		return render(request, "survey/itemcommentary_update_form.html", context)

		#return HttpResponse("Hey, you superuser you")
	else:  # not superuser
		return HttpResponse("YOU ARE NOT AUTHORIZED!")


def ObservationUpdate(request, idx):
	if request.user.is_authenticated():
		observation = Observation.objects.get(pk=idx)
		if (request.user.id == observation.observer.id or request.user.is_superuser):
			# continue to do thing.
			item_id = observation.item.code
			item = Item.objects.filter(pk=item_id)
			# get item, get characteristics of item ..
			chars = Characteristic.objects.filter(item=item_id)
			observations = Observation.objects.filter(item=item_id)
			
			spec_chars = chars.filter(specify=True)
			specified_chars = list( sc.name for sc in spec_chars)
			specified_chars_pk = list( sc.pk for sc in spec_chars)

			data = {
			'obs_time': observation.obs_time, 
			'shop_type':observation.shop_type,
			'shop_identifier':observation.shop_identifier,
			'flag':observation.flag,
			'discount':observation.discount,
			'value':observation.value,
			'observed_quantity':observation.observed_quantity,
			'obs_comment':observation.obs_comment
			}
			# adding specified chars to form
			ochars = []
			for idp, schar_pk in enumerate(specified_chars_pk):
				schar = ObservedCharacteristic.objects.get(characteristic=schar_pk, observation=observation.pk)
				data[specified_chars[idp]]=schar.value
				ochars.append(schar)

			form = ObservationForm(request.POST or None, extra=specified_chars, initial=data)
			context = {
			"form" : form,
			"user_name" : str(request.user),
			"user_id" : str(request.user.id),
			"item" : item,
			"characteristics" : chars,
			"observations" : observations,
			}

			for sc in ochars:
				print(sc.pk)
				print(sc.value)
				print(sc.characteristic.name)

			if form.is_valid():  #POST request
				shop_type = form.cleaned_data['shop_type']
				shop_identifier = form.cleaned_data['shop_identifier']
				#flag = form.cleaned_data['flag']
				discount = form.cleaned_data['discount']
				value = form.cleaned_data['value']
				observed_quantity = form.cleaned_data['observed_quantity']
				obs_comment = form.cleaned_data['obs_comment']
				# updating the observation
				observation.shop_type = shop_type
				observation.shop_identifier = shop_identifier
				observation.discount = discount
				observation.value = value
				observation.observed_quantity = observed_quantity
				observation.obs_comment = obs_comment
				observation.save()
				# updating observed characteristics
				for (question, answer) in form.extra_answers():
					print(question) # label
					print(answer) # value
					# create observerd characteristic
					print(specified_chars.index(question))
					char_pk = specified_chars_pk[specified_chars.index(question)]
					# char = Characteristic.objects.filter(pk=char_pk)[0]
					print(observation.pk)
					for sc in ochars:
						if (sc.characteristic.name == question):
							sc.value = answer
							sc.save()
					# adding observed_characteristic, currently relies on order in QueryObject spec_chars bieng same as order inlists derived from it, which I think holds.
					#observed_characteristic = ObservedCharacteristic.objects.create(observation=observation,characteristic=spec_chars[specified_chars.index(question)],value=answer) #
					#observed_characteristic.save()

			return render(request, "survey/item_observation.html", context)
		else:
			return HttpResponse("you don't have permission to edit this observation")

	else:
		return redirect(settings.LOGIN_REDIRECT_URL)


# ================================================================================


class ItemCommentaryUpdate(UpdateView):
	model = ItemCommentary
	fields = ['vat','comment','seasonality','representivity']
	template_name_suffix = '_update_form'


	def user_passes_test(self, request, pk):
		if request.user.is_superuser:
			#Model.objects.get_or_create()
			#self.object = ItemCommentary.objects.get_or_create(pk)
			return True
		return False

	def dispatch(self, request, *args, **kwargs):
		#print args
		#print kwargs['pk']
		if not self.user_passes_test(request, kwargs['pk']):
			return redirect_to_login(request.get_full_path())
		return super(ItemCommentaryUpdate, self).dispatch(request, *args, **kwargs)


