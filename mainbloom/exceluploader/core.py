from django.db.models import Q

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


def fetch_all_bank_details():
    return BankDetails.objects.all()


def fetch_all_bank_details_by_search(search):
    search = search.upper()
    return BankDetails.objects.filter(Q(bank_name__icontains=search) | Q(ifsc__icontains=search) |
                                      Q(branch__icontains=search) | Q(address__icontains=search) |
                                      Q(district__icontains=search) | Q(state__icontains=search) |
                                      Q(city__icontains=search) | Q(phone__icontains=search))

