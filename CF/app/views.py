from app import app
from flask import render_template
import requests
import json


def all_div2(contest_js):
	ans={};
	for curr in contest_js["result"]:
		if(curr["phase"] == "FINISHED"):
			if( curr["name"].find("Div. 2") != -1):
				ans[ curr["id"] ] = True;
				#print( curr["id"]);
	return ans;

def all_div1(contest_js):
	ans={};
	for curr in contest_js["result"]:
		if(curr["phase"] == "FINISHED"):
			if( curr["name"].find("Div. 1") != -1):
				ans[ curr["id"] ] = True;
				#print( curr["id"]);
	return ans;

def all_accepted(sub_js):
	ans={};
	for sub in (sub_js["result"]):
		if( (sub["problem"]["contestId"] , sub["problem"]["index"] ) in ans ):
			continue;
		if( sub["verdict"] == "OK"):
			ans[ (sub["problem"]["contestId"] , sub["problem"]["index"] )] = True;
	return ans;


def get_div2(contest , index):
	#div_1 contest have lower contest Id
	contest-=1;
	if( index=='A'):
		index = 'C';
	elif( index == 'B' ):
		index = 'D';
	elif(index =='C' ):
		index = 'E';
	else:
		index='Z';
	return (contest,index);

def  get_unsolved():#unsolved questions after Div_2_200 [A.D];
	contest_url="http://codeforces.com/api/contest.list?gym=false";
	contest_req = requests.get(contest_url);
	contest_js= contest_req .json();


	sub_url="http://codeforces.com/api/user.status?handle=rituraj&from=1&count=10000000";
	sub_req = requests.get(sub_url);
	sub_js= sub_req.json();

	div_2 = all_div2(contest_js);
	div_1 = all_div1(contest_js);
	accepted = all_accepted(sub_js);

	done = {}

	for asub in accepted:
		curr = asub;
		if( curr[0] in div_1):
			curr=get_div2( curr[0] , curr[1]);

		if( curr[0] in div_2):
			done[ curr ] = True;

	#print("Mapping done");

	tosolve="ABCD";

	solved =0 ;
	unsolved=0;

	ans=[];

	for con_id in div_2:
		for pro_id in tosolve:
			
			if( con_id < 342):#199 th ka ID 342 hai
				continue;

			if( (con_id,pro_id) in done):
				solved+=1;
			else:
				unsolved+=1;
				ans.append( (con_id,pro_id));

	#print( "Unsolved is %s \n and Solved is %s" % (unsolved,solved));
	return ans;


def get_problem( contest , id):
	ans = "http://codeforces.com/contest/{0}/problem/{1}".format(contest,id);
	return ans;

def get_todo():
	todo = get_unsolved();

	a=0;b=0;c=0;d=0;

	ans=[]

	for curr in todo:		
		if( curr[1] =='A'):
			a+=1;
		elif( curr[1] == 'B'):
			b+=1;
		elif( curr[1] =='C'):
			c+=1;
			ans.append( get_problem(curr[0] , curr[1]) );
		elif( curr[1] =='D'):
			d+=1;
	
	return ans;


@app.route('/')
def home():
    return "Hello, World!"

@app.route('/index')
def index():
	rem_prob = get_todo();
	rem_prob= sorted(rem_prob);
	return render_template("index.html", rem_probs = rem_prob );

