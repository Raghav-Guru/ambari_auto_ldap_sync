import ConfigParser
import os
from datetime import datetime
import StringIO
import subprocess
import argparse

parse_args=argparse.ArgumentParser()
parse_args.add_argument("-f","--filter",required=False,help="Group filter to get the list of groups to sync \n eg: '(|(cn=hdp_*)(cn=hr*))'")
parse_args.add_argument("-u","--admin_user",required=True,help="Ambari admin user")
parse_args.add_argument("-p","--admin_password",required=True,help="Ambari admin password")
args=vars(parse_args.parse_args())

ambari_properties_file='[global]\n' + open('/etc/ambari-server/conf/ambari.properties','r').read()
fp = StringIO.StringIO(ambari_properties_file)
config = ConfigParser.RawConfigParser()
config.readfp(fp)


###get LDAP properties###

ldap_filter=args["filter"]
ldap_base=config.get('global','authentication.ldap.baseDn')
ldap_group_name_attr=config.get('global','authentication.ldap.groupNamingAttr')
ldap_group_objectClass=config.get('global','authentication.ldap.groupObjectClass')
ldap_bind_dn=config.get('global','authentication.ldap.managerDn')
ldap_primary_url='ldap://'+config.get('global','authentication.ldap.primaryUrl')
ldap_passwd_file=open(config.get('global','authentication.ldap.managerPassword'),'r').read()



if ldap_filter is not None:
    ldap_search = "ldapsearch -LLL -H {0} -D {1} -b \'{2}\' -w \'{3}\' \'(&(objectClass={4}) {5})\' cn | grep ^cn | sed \'s/cn: //g\'| paste -s -d ',' ".format(
        ldap_primary_url, ldap_bind_dn, ldap_base, ldap_passwd_file, ldap_group_objectClass,ldap_filter)

else:
    ldap_search= "ldapsearch -LLL -H {0} -D {1} -b \'{2}\' -w \'{3}\' \'objectClass={4}\' cn | grep ^cn | sed \'s/cn: //g\'| paste -s -d ',' ".format(ldap_primary_url, ldap_bind_dn, ldap_base, ldap_passwd_file, ldap_group_objectClass)


def clean_up(file):
    os.remove(file)

###Function to create group file ###

def get_file_name():
    return "/tmp/groups."+str(datetime.now().strftime("%Y%m%d-%H%M%S"))+".csv"


###Function to sync groups from file and all the member users###

def sync_groups_from_file():

    group_file=get_file_name()

    with open(group_file,'w') as groups:
        print "Created group file {0}".format(group_file)
        execute_ldap_serach=subprocess.Popen(ldap_search,shell=True, stdout=groups, stderr=subprocess.PIPE)
        execute_ldap_serach.communicate()

    group_list=open(group_file,'r').read()
    sync_user=args["admin_user"]
    sync_password=args["admin_password"]

    sync_groups='ambari-server sync-ldap --ldap-sync-admin-name={0} --ldap-sync-admin-password={1} --groups={2}'.format(sync_user,sync_password,group_file)
    execute_sync_groups=subprocess.Popen(sync_groups,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err=execute_sync_groups.communicate()

    print "Groups being synced :{0}\n".format(group_list)

    print out


    sync_existing='ambari-server sync-ldap --ldap-sync-admin-name={0} --ldap-sync-admin-password={1} --existing'.format(sync_user,sync_password)
    execute_sync_existing=subprocess.Popen(sync_existing,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err=execute_sync_existing.communicate()

    print out


    print "Deleting the groups file : {0}".format(group_file)
    clean_up(group_file)


sync_groups_from_file()
