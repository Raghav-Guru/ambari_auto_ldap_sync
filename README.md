# ambari_auto_ldap_sync
This script can be used to automate the ldap usersync sync based on the group filter option

**Step 1:**
On ambari server (copy the python script to the file on ambari host)

    #git clone https://github.com/Raghav-Guru/ambari_auto_ldap_sync.git
    (or)
    #vi /var/tmp/ambari_auto_ldap_sync.py 

**Step 2:** 

    #python <path>/ambari_auto_ldap_sync/ambari_auto_ldap_sync.py -u <ambariAdmin> -p <ambariAdminPassword> -f '(<groupFilter>)'

eg: 

     #python ambari_auto_ldap_sync.py -u admin -p rguruvannagari -f '(|(cn=hr*))'
        Created group file /tmp/groups.20190108-022629.csv
        Groups synced :hr
        
    
        Completed LDAP Sync.
        Summary:
          memberships:
            removed = 0
            created = 0
          users:
            skipped = 0
            removed = 0
            updated = 0
            created = 0
          groups:
            updated = 0
            removed = 0
            created = 0
        
        Ambari Server 'sync-ldap' completed successfully.
        
        Using python  /usr/bin/python
        Syncing with LDAP...
        Syncing existing...
        
        Completed LDAP Sync.
        Summary:
          memberships:
            removed = 0
            created = 0
          users:
            skipped = 0
            removed = 0
            updated = 0
            created = 0
          groups:
            updated = 0
            removed = 0
            created = 0
    
        Ambari Server 'sync-ldap' completed successfully.
        
        Deleting the groups file : /tmp/groups

.20190108-022629.csv

**Note:** Schedule in crontab if required below example to sync all the users of the groups mentioned with the filter for every 12hours. 

    #crontab -e
    0 */12 * * * /var/tmp/ambari_auto_ldap_sync/ambari_auto_ldap_sync.py -u admin -p admin -f '(|(cn=hr*)(cn=hadoop-*))' > /tmp/ambari_ldap_auto_sync.log  2>&1
