from django.db.models import Q, QuerySet
from bulk_update.helper import bulk_update

from .models import BankDetails


def fetch_bank_data_by_ifsc(ifsc_codes):
    return list(BankDetails.objects.filter(ifsc__in=ifsc_codes))


def bulk_insert_data(all_bank_details, need_to_insert_ifc_codes):
    instances = list()
    append_to_instances = instances.append
    for each_bank in all_bank_details:
        if each_bank.get('IFSC') in need_to_insert_ifc_codes:
            ifsc = each_bank.get('IFSC')
            bank_name = each_bank.get('BANK NAME') or each_bank.get('BANK')
            branch = each_bank.get('OFFICE') or each_bank.get('BRANCH')
            address = each_bank.get('ADDRESS')
            district = each_bank.get('DISTRICT') or each_bank.get('CITY1')
            city = each_bank.get('CITY') or each_bank.get('CITY2')
            state = each_bank.get('STATE')
            phone = each_bank.get('PHONE')
            bank_obj = BankDetails(ifsc=ifsc, bank_name=bank_name, branch=branch, address=address,
                                   district=district, city=city, state=state, phone=phone)
            append_to_instances(bank_obj)
    bank_details = BankDetails.objects.bulk_create(instances)
    return bank_details


def list_of_dict_to_dict(list_obj, dict_key):
    new_dict_obj = dict()
    if not list_obj:
        return list_obj
    for list_item in list_obj:
        try:
            key = getattr(list_item, dict_key) if isinstance(list_obj, QuerySet) else list_item.get(dict_key)
            if key:
                new_dict_obj[key] = list_item
        except (ValueError, Exception) as e:
            print(e)
    return new_dict_obj


def bulk_update_data(all_bank_details, bank_details):
    all_bank_details = list_of_dict_to_dict(all_bank_details, "IFSC")
    for each_bank in bank_details:
        bank = all_bank_details.get(each_bank.ifsc)
        if bank:
            each_bank.bank_name = bank.get('BANK NAME') or bank.get('BANK')
            each_bank.branch = bank.get('OFFICE') or bank.get('BRANCH')
            each_bank.address = bank.get('ADDRESS')
            each_bank.district = bank.get('DISTRICT') or bank.get('CITY1')
            each_bank.city = bank.get('CITY') or bank.get('CITY2')
            each_bank.state = bank.get('STATE')
            each_bank.phone = bank.get('PHONE')
    bulk_update(bank_details, update_fields=['bank_name', 'branch', 'address', 'district', 'city', 'state', 'phone'])
    return len(bank_details)


def fetch_all_bank_details():
    return BankDetails.objects.all().order_by('ifsc')


def fetch_all_bank_details_by_search(search):
    search = search.upper()
    return BankDetails.objects.filter(Q(bank_name__icontains=search) | Q(ifsc__icontains=search) |
                                      Q(branch__icontains=search) | Q(address__icontains=search) |
                                      Q(district__icontains=search) | Q(state__icontains=search) |
                                      Q(city__icontains=search) | Q(phone__icontains=search)).order_by('ifsc')

