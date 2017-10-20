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

from django.db.models import Q

from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseForbidden
from django.core.exceptions import PermissionDenied

# xml stuff
from xml.dom import minidom
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree

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

		user_observations = Observation.objects.filter(observer=request.user.id)

		#item_aggregated_observations = Observation.objects.filter(observer=request.user.id).order_by('item')

		observed_items = Observation.objects.filter(observer=request.user.id).order_by('item').values('item').distinct()

		print(str(observed_items))

		for item in observed_items:
			obs_group = Observation.objects.filter(observer=request.user.id, item=item['item'])
			print(str(obs_group))
			print(obs_group.count())

		context = {
			"user_name" : str(request.user),
			"user_id" : str(request.user.id),
			"items" : items,
			"surveys" : surveys,
			"observations": user_observations,
		}

		return render(request, "survey/survey_dash.html", context)
	else:
		return redirect(settings.REDIRECT_TO_LOGIN)


def item_observation(request, idx):
	if request.user.is_authenticated():
		item = Item.objects.filter(pk=idx)
		# get item, get characteristics of item ..
		chars = Characteristic.objects.filter(item=idx)
		observations = Observation.objects.filter(item=idx)

		#form = ObservationForm(request.POST or None)
		#if request.method == 'POST':
		spec_chars = chars.filter(specify=True)
		specified_chars = list( sc.name for sc in spec_chars)
		specified_chars_pk = list( sc.pk for sc in spec_chars)

		# min max stuff.
		max_quantity_char = chars.filter(name="Maximum quantity")
		min_quantity_char = chars.filter(name="Minimum quantity")


		form = ObservationForm(request.POST or None, extra=specified_chars, max_quantity=max_quantity_char[0].value if max_quantity_char else [], min_quantity=min_quantity_char[0].value if min_quantity_char else [])
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
			observed_price = form.cleaned_data['observed_price']
			observed_quantity = form.cleaned_data['observed_quantity']
			obs_comment = form.cleaned_data['obs_comment']
			theitem = Item.objects.filter(pk=item)[0]
			theuser = User.objects.filter(pk=observer)[0]
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
				observed_price=observed_price,
				observed_quantity=observed_quantity,
				obs_comment=obs_comment,
				survey = surv
				)
			observation.save()

			for (question, answer) in form.extra_answers():
				# create observerd characteristic
				char_pk = specified_chars_pk[specified_chars.index(question)]
				# adding observed_characteristic, currently relies on order in QueryObject spec_chars bieng same as order inlists derived from it, which I think holds.
				observed_characteristic = ObservedCharacteristic.objects.create(observation=observation,characteristic=spec_chars[specified_chars.index(question)],value=answer) #
				observed_characteristic.save()
				
			#return redirect(settings.LOGIN_REDIRECT_URL)
			#return redirect("/survey/udash")
			#return redirect("survey.views.survey-userdash")
			return HttpResponseRedirect(reverse('survey:survey-userdash'))
			

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

		user = User.objects.filter(pk=request.user.id)
		itemObs = ItemObserver.objects.filter(user=request.user.id)
		chosen_items = set()
		for i in itemObs.select_related('item'):
			#print(i.item.survey.pk)
			i.item.iobspk = i.pk
			if(int(i.item.survey.pk) == int(pk)):
				chosen_items.add(i.item)

		chosen_item_pks = itemObs.values('item')
		ch_i_pk = []
		for i in chosen_item_pks:
			ch_i_pk.append(i["item"])
		
		items = Item.objects.exclude(code__in=ch_i_pk) # taking away already chosen items.
		#items = Item.objects.all()
		items = items.filter(survey=pk)
		context = {
			"user_name" : str(request.user),
			"user_id": str(request.user.id),
			"items": items,
			"itemObservers": itemObs,
			"target_user_id": request.user.id,
			"chosen_items": chosen_items,
			"target_user": user[0],
		}
		
		return render(request, "survey/observer_items.html", context)

	else:
		return redirect(settings.LOGIN_REDIRECT_URL)




def ItemCommentaryView(request, idx):
	if request.user.is_superuser:
		commentary = ItemCommentary.objects.get_or_create(pk=idx)[0]
		print(str(commentary))
		item = Item.objects.get(code=idx)

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
			"item" : item,
		}

		return render(request, "survey/itemcommentary_update_form.html", context)

		#return HttpResponse("Hey, you superuser you")
	else:  # not superuser
		raise PermissionDenied


def ObservationUpdate(request, idx):
	if request.user.is_authenticated():
		observation = Observation.objects.get(pk=idx)
		if (request.user.id == observation.observer.id or request.user.is_superuser):
			# user is qualified to update observation
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
			'observed_price':observation.observed_price,
			'observed_quantity':observation.observed_quantity,
			'obs_comment':observation.obs_comment
			}
			# adding specified chars to form
			ochars = []
			for idp, schar_pk in enumerate(specified_chars_pk):
				schar = ObservedCharacteristic.objects.get(characteristic=schar_pk, observation=observation.pk)
				data[specified_chars[idp]]=schar.value
				ochars.append(schar) # for use later in case of POST request.

			max_quantity_char = chars.filter(name="Maximum quantity")
			min_quantity_char = chars.filter(name="Minimum quantity")


			form = ObservationForm(request.POST or None, extra=specified_chars, initial=data, max_quantity=max_quantity_char[0].value if max_quantity_char else [], min_quantity=min_quantity_char[0].value if min_quantity_char else [])

			context = {
			"form" : form,
			"user_name" : str(request.user),
			"user_id" : str(request.user.id),
			"item" : item,
			"characteristics" : chars,
			"observations" : observations,
			}

			if form.is_valid():  #POST request
				shop_type = form.cleaned_data['shop_type']
				shop_identifier = form.cleaned_data['shop_identifier']
				#flag = form.cleaned_data['flag']
				discount = form.cleaned_data['discount']
				observed_price = form.cleaned_data['observed_price']
				observed_quantity = form.cleaned_data['observed_quantity']
				obs_comment = form.cleaned_data['obs_comment']
				# updating the observation
				observation.shop_type = shop_type
				observation.shop_identifier = shop_identifier
				observation.discount = discount
				observation.observed_price = observed_price
				observation.observed_quantity = observed_quantity
				observation.obs_comment = obs_comment
				observation.save()
				# updating observed characteristics
				for (question, answer) in form.extra_answers():
					for sc in ochars:
						if (sc.characteristic.name == question):
							sc.value = answer
							sc.save()


			return render(request, "survey/item_observation.html", context)
		else:
			raise PermissionDenied

	else:
		return redirect(settings.LOGIN_REDIRECT_URL)

class ObservationDelete(DeleteView):
	model = Observation
	success_url = reverse_lazy('survey:survey-userdash')

	def get_object(self, queryset=None):
		""" Hook to ensure object is owned by request.user. """
		obj = super(ObservationDelete, self).get_object()
		if not ((obj.observer == self.request.user) or self.request.user.is_superuser):
		    #raise Http404
		    raise PermissionDenied
		return obj


def ObserversManagement(request):
	if request.user.is_superuser:
		observers = User.objects.all()
		#items = Item.objects.filter(survey=1)
		#itemObs = ItemObserver.objects.all()

		context = {
			"user_name" : str(request.user),
			"user_id" : str(request.user.id),
			"observers" : observers,
		}

		return render(request, "survey/observers_management.html", context)
	else:
		raise PermissionDenied


def ObserverItems(request, idx):
	if request.user.is_superuser:
		user = User.objects.filter(pk=idx)
		itemObs = ItemObserver.objects.filter(user=idx)
		chosen_items = set()
		for i in itemObs.select_related('item'):
			i.item.iobspk = i.pk
			chosen_items.add(i.item)

		chosen_item_pks = itemObs.values('item')
		ch_i_pk = []
		for i in chosen_item_pks:
			ch_i_pk.append(i["item"])

		current_survey = Survey.objects.get(current=True)
		
		items = Item.objects.exclude(code__in=ch_i_pk) # taking away already chosen items.
		#items = Item.objects.all()
		items = items.filter(survey=current_survey)
		context = {
			"user_name" : str(request.user),
			"user_id": str(request.user.id),
			"items": items,
			"itemObservers": itemObs,
			"target_user_id": idx,
			"chosen_items": chosen_items,
			"target_user": user[0],
		}
		
		return render(request, "survey/observer_items.html", context)
	else:
		raise PermissionDenied


def SurveyXML(request, pk):
	if request.user.is_superuser:
		survey = Survey.objects.get(pk=pk)


		root=Element('CrossSectionalData')
		tree=ElementTree(root)
		#xmlns=Element('xmlns')
		# root.append(xmlns)
		# xmlns.text("http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message")

		root.set('xmlns','http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message')
		root.set('xmlns:cgs',"urn:sdmx:org.sdmx.infomodel.keyfamily.KeyFamily=ESTAT:PPP_CGS:cross")
		root.set('xmlns:cross',"http://www.SDMX.org/resources/SDMXML/schemas/v2_0/cross")
		root.set('xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance")
		root.set('xsi:schemaLocation',"http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message SDMXMessage.xsd urn:sdmx:org.sdmx.infomodel.keyfamily.KeyFamily=ESTAT:PPP_CGS:cross ESTAT_PPP_CGS_COUNTRY_Cross.xsd http://www.SDMX.org/resources/SDMXML/schemas/v2_0/cross SDMXCrossSectionalData.xsd")

		header = Element('Header')
		root.append(header)
		header_ID = Element('ID')


		header.append(header_ID)
		#header_ID.text = 'PPP_SRVIC_3'
		header_ID.text = survey.dataflowID
		

		header_Test = Element('Test')
		header_Test.text = 'false'
		header.append(header_Test)

		header_Truncated = Element('Truncated')
		header_Truncated.text = 'false' 
		header.append(header_Truncated)

		header_Name = Element('Name')
		header_Name.text = 'PPP Dataset'
		header.append(header_Name)

		header_Prepared = Element('Prepared') # date , timedate.now typathing  @dynam
		#header_Prepared.text = '2014-06-16T15:00:16+00:00'
		dt = datetime.datetime.now()
		header_Prepared.text = dt.strftime('%Y-%m-%dT%H:%m:%S+00:00')
		header.append(header_Prepared)

		header_Sender = Element('Sender')
		header_Sender.set('id','statice')
		header.append(header_Sender)

		header_Sender_Name = Element('Name')
		header_Sender_Name.text = 'Statistics Iceland'
		header_Sender.append(header_Sender_Name)

		header_Sender_Contact = Element('Contact')

		header_Sender_Contact_Name = Element('Name')
		header_Sender_Contact_Name.text = "Snorri Gunnarsson"
		header_Sender_Contact_Department = Element('Department')
		header_Sender_Contact_Department.text = "Price Statistics"
		header_Sender_Contact_Role = Element('Role')
		header_Sender_Contact_Role.text = "xx"
		header_Sender_Contact_Telephone = Element('Telephone')
		header_Sender_Contact_Telephone.text = "xx"
		header_Sender_Contact_Fax = Element('Fax')
		header_Sender_Contact_Fax.text = "xx"
		header_Sender_Contact_Email = Element('Email')
		header_Sender_Contact_Email.text = "Snorri.Gunnarsson@hagstofa.is"

		header_Sender_Contact.append(header_Sender_Contact_Name)
		header_Sender_Contact.append(header_Sender_Contact_Department)
		header_Sender_Contact.append(header_Sender_Contact_Role)
		header_Sender_Contact.append(header_Sender_Contact_Telephone)
		header_Sender_Contact.append(header_Sender_Contact_Fax)
		header_Sender_Contact.append(header_Sender_Contact_Email)

		header_Sender.append(header_Sender_Contact)

		header_Receiver = Element('Receiver')
		header_Receiver.set('id','EUROSTAT')
		header_Receiver_Name = Element('Name')
		header_Receiver_Name.text = 'EUROSTAT'
		header_Receiver.append(header_Receiver_Name)

		header.append(header_Receiver)

		header_DataSetID = Element('DataSetID')
		#header_DataSetID.text = "PPP_SRVIC_3-2014-06-16T15:00:16"  # time stuff @dynam dt.strftime('%Y-%m-%dT%H:%m:%S
		header_DataSetID.text = survey.dataflowID + "-" + dt.strftime('%Y-%m-%dT%H:%m:%S')
		header_DataSetAction = Element('DataSetAction')
		header_DataSetAction.text = 'Append'
		header_Extracted = Element('Extracted')
		#header_Extracted.text = '2014-06-16T15:00:16+00:00'
		header_Extracted.text = dt.strftime('%Y-%m-%dT%H:%m:%S+00:00')
		header_ReportingBegin = Element('ReportingBegin')
		#header_ReportingBegin.text = '2014-01-01'
		header_ReportingBegin.text = str(survey.year) + '-01-01' # perhaps change to erliest obs_time ?
		latest_obs = Observation.objects.filter(survey=pk).order_by('-id')
		if not latest_obs:
			reporting_end_str = dt.strftime('%Y-%m-%d')
		else:
			obs_latest =latest_obs[0]		
			reporting_end_str = obs_latest.obs_time.strftime('%Y-%m-%d')
		header_ReportingEnd = Element('ReportingEnd')
		#header_ReportingEnd.text = '2014-12-31'
		header_ReportingEnd.text = reporting_end_str

		header.append(header_DataSetID)
		header.append(header_DataSetAction)
		header.append(header_Extracted)
		header.append(header_ReportingBegin)
		header.append(header_ReportingEnd)

		# end header

		cgs_dataset = Element('cgs:DataSet')
		cgs_group = Element('cgs:Group')

		cgs_dataset.append(cgs_group)


		#cgs_group.set('REFERENCE_YEAR','2014')   # @dynam year from survey
		cgs_group.set('REFERENCE_YEAR', str(dt.year))
		#cgs_group.set('PPP_SURVEY','SRVIC')      # @dynam survey code
		cgs_group.set('PPP_SURVEY', survey.code)
		cgs_group.set('REPORTING_COUNTRY','IS')  
		cgs_group.set('CURRENCY','ISK')

		root.append(cgs_dataset)

		item_rows = Item.objects.filter(survey=pk).values_list()
		for i_row in item_rows:
			#print("hey dude")
			commentarys = ItemCommentary.objects.filter(item=i_row).values_list()
			#print(len(commentarys))
			if (len(commentarys) > 0):
				commentary = commentarys[0]
				commentary_seasonality = "true" if commentary[1] else "false"
				commentary_representativity = "true" if commentary[2] else "false"
				commentary_comment = commentary[3]
				commentary_vat = commentary[4]
				#print commentary, commentary_seasonality, commentary_representativity, commentary_comment, commentary_vat
			else:
				commentary_vat = commentary_comment = commentary_representativity = commentary_seasonality = False
			
			#print commentary, commentary_seasonality, commentary_representativity, commentary_comment
			# cgs_section stuff
			cgs_section = Element('cgs:Section')
			cgs_section.set("ECP_ITEM",i_row[0])
			if(commentary_vat):
				cgs_section.set("VAT", str(round(commentary_vat, 2)) if commentary_vat else "0.24")                   # almost static
			if (commentary_representativity):
				cgs_section.set("REPRESENTATIVITY", commentary_representativity if commentary_representativity else "true")         # default to true  ---- later to be derived from new model ItemCommentary
			if (commentary_seasonality):
				cgs_section.set("SEASONALITY", commentary_seasonality if commentary_seasonality else "false")          # default to false -----^
			cgs_section.set("ITEM_COMMENT", commentary_comment if commentary_comment else "")               # default to ""  ----------^
			cgs_section.set("FINALIZED","true")              # true

			#cgs_group.append(cgs_section)


			observations = Observation.objects.filter(item=i_row[0]).values_list()
			if( len(observations) <= 0):
				cgs_group.append(cgs_section)

			if(len(observations) > 0):
				cgs_section.set("VAT", str(round(commentary_vat, 2)) if commentary_vat else "0.24")
				cgs_section.set("REPRESENTATIVITY", commentary_representativity if commentary_representativity else "true")
				cgs_section.set("SEASONALITY", commentary_seasonality if commentary_seasonality else "false")
				cgs_group.append(cgs_section)
				observation_number = 1

				for obs_i in observations:
					cgs_observed_price = Element('cgs:OBSERVED_PRICE')
					cgs_observed_price.set('OBSERVATION_NUMBER',str(observation_number))
					cgs_observed_price.set('OBS_TIME', str(obs_i[2].strftime('%Y-%-m')))
					cgs_observed_price.set('SHOP_TYPE', str(obs_i[3]))
					cgs_observed_price.set('SHOP_IDENTIFIER', unicode(obs_i[4]))
					cgs_observed_price.set('OBS_COMMENT', unicode(obs_i[11]))
					cgs_observed_price.set('FLAG', str(obs_i[5]))
					cgs_observed_price.set('DISCOUNT', unicode(obs_i[6]))
					cgs_observed_price.set('value', str(round(obs_i[7], 1)))

					cgs_section.append(cgs_observed_price)

					cgs_observed_quantity = Element('cgs:OBSERVED_QUANTITY')
					cgs_observed_quantity.set('OBSERVATION_NUMBER', str(observation_number))
					cgs_observed_quantity.set('value', str(round(obs_i[8],1)))

					cgs_section.append(cgs_observed_quantity)
					observation_number += 1
			
					observedcharacteristics = ObservedCharacteristic.objects.filter(observation=str(obs_i[0])).values_list()
					char_arr = []
					for obs_char in observedcharacteristics:
						obs_char_id = obs_char[0]
						char_id = obs_char[2]
						obs_id = obs_char[1]
						obs_char_value = obs_char[3]
						# execute_string3 = 'SELECT * FROM  survey_characteristic WHERE id=' + '"' + str(char_id) + '"'
						# c.execute(execute_string3)
						# characteristic_i = c.fetchall()
						characteristic_i = Characteristic.objects.filter(pk=str(char_id)).values_list()
						#print(characteristic_i)
						char_name = characteristic_i[0][1]
						# get char Name 
						"""
						<cgs:OBSERVED_PRICE OBSERVATION_NUMBER="4" OBS_TIME="2014-5" 
						SHOP_TYPE="8" SHOP_IDENTIFIER="Rafholt" OBS_COMMENT="" FLAG="O" 
						DISCOUNT="N" value="25500.0" CHARACTERISTICS="Price of materials=8000|
						Travel costs=3500|Number of hours worked=2" CHARS_SEPARATOR="|" />
						"""
						# set observed price CHARACTERISTICS, CHARS_SEPARATOR='|'
						char_arr.append(str(char_name)+"="+unicode(obs_char_value))

					if (len(char_arr) > 0):
						char_string='|'.join(char_arr)
						cgs_observed_price.set("CHARACTERISTICS",char_string)
						cgs_observed_price.set("CHARS_SEPARATOR","|")
						

		#xml_string = etree.tostring(root)
		xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n' + etree.tostring(root)

		return HttpResponse(xml_string, content_type="text/plain")
	else:
		raise PermissionDenied

