
import boto3
import datetime
import json
import os
import time

'''
Create by sj kwon
Email kofdx7@gmail.com
'''
class ec2:
	def __init__(self,ec2_instance_id):
		self.ec2_client=boto3.client('ec2');
		self.ec2_instance_id=ec2_instance_id;
		
	def detach_ec2_from_asg(self):
        #need asg name
        response = client.detach_instances(
            InstanceIds=[
             'string',
            ],
            AutoScalingGroupName='string',
            ShouldDecrementDesiredCapacity=True
        )
		return ec2_status

	def attach_ec2_from_asg(self):
        #need asg name        
        response = client.attach_instances(
            InstanceIds=[
            'string',
            ],
            AutoScalingGroupName='string'
        )

	def schedule_ec2(self):
		ec2_status=self.get_ec2_status();
		cron_pattern=self.get_start_pattern(ec2_status) if ec2_status=="stopping" or ec2_status=="available" else self.get_stop_pattern(ec2_status);
		return cron_pattern
		
	def stop_ec2(self):
		response = self.ec2_client.stop_instances(
            InstanceIds=[
                'string',
            ]
		)
		print("#  SUCCESS ec2 STOP")
		
	def start_ec2(self):
		response = self.ec2_client.start_instances(
            InstanceIds=[
                'string',
            ]
		)
		print("#  SUCCESS ec2 START")	

	def get_start_pattern(self,ec2_status):

		cron_pattern="cron(0 0 ? * 2-6 *)"	
		return ("START",cron_pattern)


	def get_stop_pattern(self,ec2_status):
		if ec2_status == "stopped":
			print("# START ec2 ...! ")
			self.start_ec2();
		#set your time for ec2 stop. 
		#default is 1 hours.
		_datetime=datetime.datetime.today()+datetime.timedelta(minutes=15)
		cron_pattern="cron(0 12 ? * 2-6 *)"
		return ("STOP",cron_pattern)


class EventBridge:
	
	def __init__(self,events_rule_name):
		self.eb_client = boto3.client('events');
		self.events_rule_name=events_rule_name;

	def put_rule(self,schedule):
		response = self.eb_client.put_rule(
			Name=self.events_rule_name,
			ScheduleExpression=schedule[1],
			State='ENABLED'
		)
		print("#  PUT RULE ec2 "+ schedule[0]+":" + self.events_rule_name + "[" + schedule[1] + "]")
		



			
def get_cron_pattern(_datetime):
	cron_pattern = "cron("  + _datetime.strftime("%M %H %d %m").strip() + " ? " + _datetime.strftime("%Y") + ")"
	return cron_pattern


def lambda_handler(event, context):
	# TODO implement


    # ec2 list .... with asg 
    # instanceIds 
    # asg = 
     
    # ec2 list ... InstanceIds=[ 'i-xxx','i-xxx],
    
    #1. ec2 start evnet  or ec2 stop event
    #2. detach ec2 from asg... or  attatch ec2 to asg...
    #3. stop ec2 ... or start ec2 ...
    #4. put rule next time ...

    

    

	ec2=ec2(os.getenv('ec2_instance_id'))
	eb=EventBridge("ec2-scheduler-event")

	schedule=ec2.schedule_ec2();
	eb.put_rule(schedule);
	
	return {
		'statusCode': 200,
		'body': json.dumps('End')
	}
