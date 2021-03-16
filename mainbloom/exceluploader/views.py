import pandas as pandas
from django.shortcuts import render
import pandas as pd
# Create your views here.
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .core import fetch_bank_data_by_ifsc, bulk_insert_data, fetch_all_bank_details, fetch_all_bank_details_by_search


class Excel(APIView):

    def get(self, request):
        return render(request, 'upload.html', context={})

    def post(self, request):
        file = request.FILES.get('filename')
        data = pd.read_excel(file)
        bank_data = data.T.to_dict()
        all_bank_details = bank_data.values()
        all_ifsc_codes = [bank.get('IFSC') for bank in all_bank_details]

        bank_details = fetch_bank_data_by_ifsc(all_ifsc_codes)
        existing_ifsc_codes = [bank.ifsc for bank in bank_details]
        need_to_insert_ifc_codes = list(set(all_ifsc_codes) ^ set(existing_ifsc_codes))
        inserted_data = bulk_insert_data(all_bank_details, need_to_insert_ifc_codes)
        message = "Inserted {} rows successfully".format(len(inserted_data))
        return render(request, 'upload.html', context={'message': message})


class Home(APIView):

    def get(self, request):
        search = request.GET.get("search", "")
        search_value = search
        if search:
            all_bank_details = fetch_all_bank_details_by_search(search)
        else:
            all_bank_details = fetch_all_bank_details()
        page = request.GET.get('page', 1)

        paginator = Paginator(all_bank_details, 10)
        try:
            bank_details = paginator.page(page)
        except PageNotAnInteger:
            bank_details = paginator.page(1)
        except EmptyPage:
            bank_details = paginator.page(paginator.num_pages)

        return render(request, 'home.html', context={'data': bank_details, 'search_value': search_value})
