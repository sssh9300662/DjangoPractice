# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from simple_salesforce import Salesforce


@csrf_exempt
def query_activation_form(request):
    return render(request, "query_activation_form.html")

@csrf_exempt
def query_activation(request):
    sf = Salesforce(username='michelle_kao@trend.com.tw.full',
                    password='forPLStest99',
                    security_token='TmFxKN2zOWl1RPjZrgaKLmOA',
                    sandbox=True)
    # ====== get request param ======================
    contract_name = request.POST['contract_name']
    # ===== get contract by name =====================
    query = "SELECT Id, Whitelist_Override_For__c, End_User__c FROM Contracts_Custom__c where Name='%s'" % (
        contract_name)
    contract = sf.query(query)['records'][0]
    contract_id = contract.get('Id')
    end_user = contract.get('End_User__c')
    # ==== get account data ========================
    account = sf.Account.get(end_user)
    # ==== get command data ======================
    command_query = "Select Name, Status__c, Action__c from CI_Command__c WHERE Contract__c='%s' order by CreatedDate desc" %(contract_id)
    commands = sf.query(command_query)['records']

    return render(request, "query_activation_result.html", {
        'contract_name': contract_name,
        'account': account.get('Name'),
        'commands': commands
    })


@csrf_exempt
def activate_form(request):
    return render(request, "activate_form.html")


@csrf_exempt
def activate(request):
    sf = Salesforce(username='michelle_kao@trend.com.tw.full',
                    password='forPLStest99',
                    security_token='TmFxKN2zOWl1RPjZrgaKLmOA',
                    sandbox=True)
    # ====== get request param ======================
    contract_name = request.POST['contract_name']
    handle_now = request.POST['handle_now']
    # ===== get contract by name =====================
    query = "SELECT Id, Whitelist_Override_For__c, End_User__c FROM Contracts_Custom__c where Name='%s'" % (
        contract_name)
    contract = sf.query(query)['records'][0]
    contract_id = contract.get('Id')
    override_white_list = contract.get('Whitelist_Override_For')
    end_user = contract.get('End_User__c')
    # ====== try to do a real action to trigger some things ====
    '''
    The followings are read-only or pickup value type fields, filed security level must be modified on salesforce if we want to update or create them through api
    Contract__c: readonly
    Command_Type__c: pickup value type
    Status__c: pickup value type
    Action__c: pickup value type
    '''
    # Change contract entitlement status to ''Pending Activation"
    contract_ent_status_result = sf.Contracts_Custom__c.update(
        contract_id, {'Entitlement_Status__c': 'Pending Activation'})
    # Add command
    command = {}
    status = 'Deferred'
    if handle_now:
        status = 'Ready'
    command['Contract__c'] = contract_id
    command['Account__c'] = end_user
    command['Command_Type__c'] = 'Contract'
    command['Action__c'] = 'Activate'
    command['Status__c'] = status
    command['Blacklist_Request__c'] = override_white_list

    command_submission_result = sf.CI_Command__c.create(command)

    return render(request, "activate_submit_result.html")
