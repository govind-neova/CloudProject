log_response=log_client.create_log_group(
            logGroupName='VpcFlowLogGroup'
        )

log_response=log_client.describe_log_groups()

for name in log_response["logGroups"]["logGroupName"]
   
   if name == "VpcFlowLogGroup"
   print (name)

log_client.put_retention_policy(
            logGroupName=log_group_name,
            retentionInDays=30
         )

print ( name )

