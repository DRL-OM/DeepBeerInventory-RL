import argparse
import os
import numpy as np 

def str2bool(v):
  return v.lower() in ('true', '1')

arg_lists = []
parser = argparse.ArgumentParser()

def add_argument_group(name):
  arg = parser.add_argument_group(name)
  arg_lists.append(arg)
  return arg

# crm
game_arg = add_argument_group('BeerGame')
game_arg.add_argument('--task', type=str, default='bg')
game_arg.add_argument('--fixedAction', type=str2bool, default='False', help='if you want to have actions in [0,actionMax] set it to True. with False it will set it [actionLow, actionUp]')
game_arg.add_argument('--observation_data', type=str2bool, default=False, help='if it is True, then it uses the data that is generated by based on few real world observation')
game_arg.add_argument('--data_id', type=int, default=22, help='the default item id for the basket dataset')
game_arg.add_argument('--TLow', type=int, default=100, help='duration of one GAME (lower bound)')
game_arg.add_argument('--TUp', type=int, default=100, help='duration of one GAME (upper bound)')
game_arg.add_argument('--demandDistribution', type=int, default=0, help='0=uniform, 1=normal distribution, 2=the sequence of 4,4,4,4,8,..., 3= basket data, 4= forecast data')
game_arg.add_argument('--scaled', type=str2bool, default=False, help='if true it uses the (if) existing scaled parameters')
game_arg.add_argument('--demandLow', type=int, default=0, help='the lower bound of random demand')
game_arg.add_argument('--demandUp', type=int, default=3, help='the upper bound of random demand')
game_arg.add_argument('--demandMu', type=float, default=10, help='the mu of the normal distribution for demand ')
game_arg.add_argument('--demandSigma', type=float, default=2, help='the sigma of the normal distribution for demand ')
game_arg.add_argument('--actionMax', type=int, default=2, help='it works when fixedAction is True')
game_arg.add_argument('--actionUp', type=int, default=2, help='bounds on my decision (upper bound), it works when fixedAction is True')
game_arg.add_argument('--actionLow', type=int, default=-2, help='bounds on my decision (lower bound), it works when fixedAction is True')
game_arg.add_argument('--action_step', type=int, default=1, help='The obtained action value by dnn is multiplied by this value')
game_arg.add_argument('--actionList', type=list, default=[],  help='The list of the available actions')
game_arg.add_argument('--actionListLen', type=int, default=0, help='the length of the action list')
game_arg.add_argument('--actionListOpt', type=int, default=0 , help='the action list which is used in optimal and sterman')
game_arg.add_argument('--actionListLenOpt', type=int, default=0, help='the length of the actionlistopt')
game_arg.add_argument('--agentTypes', type=list, default=['dnn','dnn','dnn','dnn'], help='the player types')
game_arg.add_argument('--agent_type1', type=str, default='dnn', help='the player types for agent 1, it can be dnn, Strm, bs, rnd')
game_arg.add_argument('--agent_type2', type=str, default='dnn', help='the player types for agent 2, it can be dnn, Strm, bs, rnd')
game_arg.add_argument('--agent_type3', type=str, default='dnn', help='the player types for agent 3, it can be dnn, Strm, bs, rnd')
game_arg.add_argument('--agent_type4', type=str, default='dnn', help='the player types for agent 4, it can be dnn, Strm, bs, rnd')
game_arg.add_argument('--NoAgent', type=int, default=1, help='number of agents, currently it should be in {1,2,3,4}')
game_arg.add_argument('--cp1', type=float, default=2.0, help='shortage cost of player 1')
game_arg.add_argument('--cp2', type=float, default=0.0, help='shortage cost of player 2')
game_arg.add_argument('--cp3', type=float, default=0.0, help='shortage cost of player 3')
game_arg.add_argument('--cp4', type=float, default=0.0, help='shortage cost of player 4')
game_arg.add_argument('--ch1', type=float, default=2.0, help='holding cost of player 1')
game_arg.add_argument('--ch2', type=float, default=2.0, help='holding cost of player 2')
game_arg.add_argument('--ch3', type=float, default=2.0, help='holding cost of player 3')
game_arg.add_argument('--ch4', type=float, default=2.0, help='holding cost of player 4')
game_arg.add_argument('--alpha_b1', type=float, default=-0.5, help='alpha of Sterman formula parameter for player 1')
game_arg.add_argument('--alpha_b2', type=float, default=-0.5, help='alpha of Sterman formula parameter for player 2')
game_arg.add_argument('--alpha_b3', type=float, default=-0.5, help='alpha of Sterman formula parameter for player 3')
game_arg.add_argument('--alpha_b4', type=float, default=-0.5, help='alpha of Sterman formula parameter for player 4')
game_arg.add_argument('--betta_b1', type=float, default=-0.2, help='beta of Sterman formula parameter for player 1')
game_arg.add_argument('--betta_b2', type=float, default=-0.2, help='beta of Sterman formula parameter for player 2')
game_arg.add_argument('--betta_b3', type=float, default=-0.2, help='beta of Sterman formula parameter for player 3')
game_arg.add_argument('--betta_b4', type=float, default=-0.2, help='beta of Sterman formula parameter for player 4')
game_arg.add_argument('--eta', type=list, default=[0,4,4,4], help='the total cost regulazer')
game_arg.add_argument('--distCoeff', type=int, default=20, help='the total cost regulazer')
game_arg.add_argument('--brainTypes', type=int, default=3, help='if it is "0", it uses the current "agentType", otherwise sets agent types according to the function setAgentType() in this file.')
game_arg.add_argument('--ifUseTotalReward', type=str2bool, default='False', help='if you want to have the total rewards in the experience replay, set it to true.')
game_arg.add_argument('--ifUsedistTotReward', type=str2bool, default='True', help='If use correction to the rewards in the experience replay for all iterations of current game')
game_arg.add_argument('--ifUseASAO', type=str2bool, default='True', help='if use AS and AO, i.e., received shipment and received orders in the input of DNN')
game_arg.add_argument('--ifUseActionInD', type=str2bool, default='False', help='if use action in the input of DNN')
game_arg.add_argument('--stateDim', type=int, default=5, help='Number of elements in the state desciptor - Depends on ifUseASAO')
game_arg.add_argument('--iftl', type=str2bool, default=False, help='if apply transfer learning')
game_arg.add_argument('--ifTransferFromSmallerActionSpace', type=str2bool, default=False, help='if want to transfer knowledge from a network with different action space size.')
game_arg.add_argument('--baseActionSize', type=int, default=5, help='if ifTransferFromSmallerActionSpace is true, this determines the size of action space of saved network')
game_arg.add_argument('--tlBaseBrain', type=int, default=3, help='the brainTypes of the base network for re-training with transfer-learning')
game_arg.add_argument('--MultiAgent', type=str2bool, default=False, help='if run multi-agent RL model, not fully operational')
game_arg.add_argument('--MultiAgentRun', type=list, default=[True, True, True, True], help='In the multi-RL setting, it determines which agent should get training.')
game_arg.add_argument('--if_use_AS_t_plus_1', type=str2bool, default='False', help='if use AS[t+1], not AS[t] in the input of DNN')
game_arg.add_argument('--preload_config', type=str2bool, default=False, help='If true it calls the set_config function from sensitivity_run.py .')
game_arg.add_argument('--ifSinglePathExist', type=str2bool, default=False, help='If true it uses the predefined path in pre_model_dir and does not merge it with demandDistribution.')
game_arg.add_argument('--ifPlaySavedData', type=str2bool, default=False, help='If true it uses the saved actions which are read from file.')

#################### parameters of the leadtimes ########################
leadtimes_arg = add_argument_group('leadtimes')
leadtimes_arg.add_argument('--leadRecItemLow', type=list, default=[2,2,2,4], help='the min lead time for receiving items')
leadtimes_arg.add_argument('--leadRecItemUp', type=list, default=[2,2,2,4], help='the max lead time for receiving items')
leadtimes_arg.add_argument('--leadRecOrderLow', type=int, default=[2,2,2,0], help='the min lead time for receiving orders')
leadtimes_arg.add_argument('--leadRecOrderUp', type=int, default=[2,2,2,0], help='the max lead time for receiving orders')
leadtimes_arg.add_argument('--ILInit', type=list, default=[0,0,0,0], help='')
leadtimes_arg.add_argument('--AOInit', type=list, default=[0,0,0,0], help='')
leadtimes_arg.add_argument('--ASInit', type=list, default=[0,0,0,0], help='the initial shipment of each agent')
leadtimes_arg.add_argument('--leadRecItem1', type=int, default=2, help='the min lead time for receiving items')
leadtimes_arg.add_argument('--leadRecItem2', type=int, default=2, help='the min lead time for receiving items')
leadtimes_arg.add_argument('--leadRecItem3', type=int, default=2, help='the min lead time for receiving items')
leadtimes_arg.add_argument('--leadRecItem4', type=int, default=2, help='the min lead time for receiving items')
leadtimes_arg.add_argument('--leadRecOrder1', type=int, default=2, help='the min lead time for receiving order')
leadtimes_arg.add_argument('--leadRecOrder2', type=int, default=2, help='the min lead time for receiving order')
leadtimes_arg.add_argument('--leadRecOrder3', type=int, default=2, help='the min lead time for receiving order')
leadtimes_arg.add_argument('--leadRecOrder4', type=int, default=2, help='the min lead time for receiving order')
leadtimes_arg.add_argument('--ILInit1', type=int, default=0, help='the initial inventory level of the agent')
leadtimes_arg.add_argument('--ILInit2', type=int, default=0, help='the initial inventory level of the agent')
leadtimes_arg.add_argument('--ILInit3', type=int, default=0, help='the initial inventory level of the agent')
leadtimes_arg.add_argument('--ILInit4', type=int, default=0, help='the initial inventory level of the agent')
leadtimes_arg.add_argument('--AOInit1', type=int, default=0, help='the initial arriving order of the agent')
leadtimes_arg.add_argument('--AOInit2', type=int, default=0, help='the initial arriving order of the agent')
leadtimes_arg.add_argument('--AOInit3', type=int, default=0, help='the initial arriving order of the agent')
leadtimes_arg.add_argument('--AOInit4', type=int, default=0, help='the initial arriving order of the agent')
leadtimes_arg.add_argument('--ASInit1', type=int, default=0, help='the initial arriving shipment of the agent')
leadtimes_arg.add_argument('--ASInit2', type=int, default=0, help='the initial arriving shipment of the agent')
leadtimes_arg.add_argument('--ASInit3', type=int, default=0, help='the initial arriving shipment of the agent')
leadtimes_arg.add_argument('--ASInit4', type=int, default=0, help='the initial arriving shipment of the agent')


####################	DQN setting		####################	
DQN_arg = add_argument_group('DQN')
DQN_arg.add_argument('--maxEpisodesTrain', type=int, default=60100, help='number of GAMES to be trained')
DQN_arg.add_argument('--NoHiLayer', type=int, default=3, help='number of hidden layers')
DQN_arg.add_argument('--NoFixedLayer', type=int, default=1, help='number of hidden layers')
DQN_arg.add_argument('--node1', type=int, default=180, help='the number of nodes in the first hidden layer')
DQN_arg.add_argument('--node2', type=int, default=130, help='the number of nodes in the second hidden layer')
DQN_arg.add_argument('--node3', type=int, default=61, help='the number of nodes in the third hidden layer')
DQN_arg.add_argument('--nodes', type=list, default=[], help='')

DQN_arg.add_argument('--seed', type=int, default=4, help='the seed for DNN stuff')
DQN_arg.add_argument('--batchSize', type=int, default=64, help='the batch size which is used to obtain')
DQN_arg.add_argument('--minReplayMem', type=int, default=50000, help='the minimum of experience reply size to start dnn')
DQN_arg.add_argument('--maxReplayMem', type=int, default=1000000, help='the maximum size of the replay memory')
DQN_arg.add_argument('--alpha', type=float, default=.97, help='learning rate for total reward distribution ')
DQN_arg.add_argument('--gamma', type=float, default=.99, help='discount factor for Q-learning')
DQN_arg.add_argument('--saveInterval', type=int, default=10000, help='every xx training iteration, saves the games network')
DQN_arg.add_argument('--epsilonBeg', type=float, default=0.9, help='')
DQN_arg.add_argument('--epsilonEnd', type=float, default=0.1, help='')
				
DQN_arg.add_argument('--lr0', type=float, default=0.00025 , help='the learning rate')
DQN_arg.add_argument('--Minlr', type=float, default=1e-8, help='the minimum learning rate, if it drops below it, fix it there ')
DQN_arg.add_argument('--ifDecayAdam', type=str2bool, default=True, help='decays the learning rate of the adam optimizer')
DQN_arg.add_argument('--decayStep', type=int, default=10000, help='the decay step of the learning rate')
DQN_arg.add_argument('--decayRate', type=float, default=0.98, help='the rate to reduce the lr at every decayStep')

DQN_arg.add_argument('--display', type=int, default=1000, help='the number of iterations between two display of results.')
DQN_arg.add_argument('--momentum', type=float, default=0.9, help='the momentum value')
DQN_arg.add_argument('--dnnUpCnt', type=int, default=10000, help='the number of iterations that updates the dnn weights')
DQN_arg.add_argument('--multPerdInpt', type=int, default=10, help='Number of history records which we feed into DNN')


####################	Utilities			####################	
utility_arg = add_argument_group('Utilities')
utility_arg.add_argument('--address', type=str, default="", help='the address which is used to save the model files')
utility_arg.add_argument('--ifUsePreviousModel', type=str2bool, default='False', help='if there is a saved model, then False value of this parameter will overwrite.')
utility_arg.add_argument('--number_cpu_active', type=int, default=5, help='number of cpu cores')
utility_arg.add_argument('--gpu_memory_fraction', type=float, default=0.1, help='the fraction of gpu memory which we are gonna use')
# Dirs
utility_arg.add_argument('--load_path', type=str, default='', help='The directory to load the models')
utility_arg.add_argument('--log_dir', type=str, default=os.path.expanduser('./logs/'), help='')
utility_arg.add_argument('--pre_model_dir', type=str, default=os.path.expanduser('./pre_model'),help='')
utility_arg.add_argument('--action_dir', type=str, default=os.path.expanduser('./'),help='if ifPlaySavedData is true, it uses this path to load actions')
utility_arg.add_argument('--model_dir', type=str, default='./',help='')
utility_arg.add_argument('--TB', type=str2bool, default=False, help='set to True if use tensor board and save the required data for TB.')
utility_arg.add_argument('--INFO_print', type=str2bool, default=True, help='if true, it does not print anything all.')
utility_arg.add_argument('--tbLogInterval', type=int, default=80000, help='number of GAMES for testing')
		
####################	testing			####################	
test_arg = add_argument_group('testing')
test_arg.add_argument('--testRepeatMid', type=int, default=50, help='it is number of episodes which is going to be used for testing in the middle of training')
test_arg.add_argument('--testInterval', type=int, default=100, help='every xx games compute "test error"')
test_arg.add_argument('--ifSaveFigure', type=str2bool, default=True, help='if is it True, save the figures in each testing.')
test_arg.add_argument('--if_titled_figure', type=str2bool, default='True', help='if is it True, save the figures with details in the title.')
test_arg.add_argument('--saveFigInt', type=list, default=[59990,60000], help='')
test_arg.add_argument('--saveFigIntLow', type=int, default=59990, help='')
test_arg.add_argument('--saveFigIntUp', type=int, default=60000, help='')
test_arg.add_argument('--ifsaveHistInterval', type=str2bool, default=False, help='if every xx games save details of the episode')
test_arg.add_argument('--saveHistInterval', type=int, default=50000, help='every xx games save details of the play')
test_arg.add_argument('--Ttest', type=int, default=100, help='it defines the number of periods in the test cases')
test_arg.add_argument('--ifOptimalSolExist', type=str2bool, default=True, help='if the instance has optimal base stock policy, set it to True, otherwise it should be False.')
test_arg.add_argument('--f1', type=float, default=8, help='base stock policy decision of player 1')
test_arg.add_argument('--f2', type=float, default=8, help='base stock policy decision of player 2')
test_arg.add_argument('--f3', type=float, default=0, help='base stock policy decision of player 3')
test_arg.add_argument('--f4', type=float, default=0, help='base stock policy decision of player 4')
test_arg.add_argument('--f_init', type=list, default=[32,32,32,24], help='base stock policy decision for 4 time-steps on the C(4,8) demand distribution')
test_arg.add_argument('--use_initial_BS', type=str2bool, default=False, help='If use f_init set it to True')

####################	reporting			####################	
reporting_arg = add_argument_group('reporting')
reporting_arg.add_argument('--Rsltdnn', type=list, default=[], help='the result of dnn play tests will be saved here')
reporting_arg.add_argument('--RsltRnd', type=list, default=[], help='the result of random play tests will be saved here')
reporting_arg.add_argument('--RsltStrm', type=list, default=[], help='the result of heuristic fomula play tests will be saved here')
reporting_arg.add_argument('--Rsltbs', type=list, default=[], help='the result of optimal play tests will be saved here')
reporting_arg.add_argument('--ifSaveHist', type=str2bool, default='False', help='if it is true, saves history, prediction, and the randBatch in each period, WARNING: just make it True in small runs, it saves huge amount of files.')

		
#buildActionList: actions for the beer game problem	
def buildActionList(config):
	aDiv = 1  # difference in the action list
	if config.fixedAction:
		actions = list(range(0,config.actionMax+1,aDiv)) # If you put the second argument =11, creates an actionlist from 0..xx
	else:
		actions = list(range(config.actionLow,config.actionUp+1,aDiv) )
	return actions	
	
# specify the dimension of the state of the game	
def getStateDim(config):
	if config.ifUseASAO:
		stateDim=5
	else:
		stateDim=3

	if config.ifUseActionInD:
		stateDim += 1

	return stateDim	

# agents 1=[dnn,dnn,dnn,dnn]; 2=[dnn,Strm,Strm,Strm]; 3=[dnn,bs,bs,bs]
def setAgentType(config):
	if config.brainTypes == 1:   # all agents are run by DNN- Also, load-model loads from brain-3+agentNum-
		# Also multi-agent with double target uses this brainTypes.
		config.agentTypes = ["srdqn", "srdqn","srdqn","srdqn"]
		config.to_prev_ai = [3,-1,-1,-1]
	elif config.brainTypes == 2: # one agent is run by DNN- Also, load-model loads from brain-3+agentNum-
		# Also multi-agent with double target uses this brainTypes.
		config.agentTypes = ["srdqn", "srdqn","srdqn","srdqn"]
		config.to_prev_ai = [3,-1,-1,-1]
	elif config.brainTypes == 3: 
		config.agentTypes = ["srdqn", "bs","bs","bs"]
	elif config.brainTypes == 4: 
		config.agentTypes = ["bs", "srdqn","bs","bs"]
	elif config.brainTypes == 5: 
		config.agentTypes = ["bs", "bs","srdqn","bs"]
	elif config.brainTypes == 6: 
		config.agentTypes = ["bs", "bs","bs","srdqn"]
	elif config.brainTypes == 7: 
		config.agentTypes = ["srdqn", "Strm","Strm","Strm"]
	elif config.brainTypes == 8: 
		config.agentTypes = ["Strm", "srdqn","Strm","Strm"]
	elif config.brainTypes == 9: 
		config.agentTypes = ["Strm", "Strm","srdqn","Strm"]
	elif config.brainTypes == 10: 
		config.agentTypes = ["Strm", "Strm","Strm","srdqn"]
	elif config.brainTypes == 11: 
		config.agentTypes = ["srdqn", "rnd","rnd","rnd"]
	elif config.brainTypes == 12: 
		config.agentTypes = ["rnd", "srdqn","rnd","rnd"]
	elif config.brainTypes == 13: 
		config.agentTypes = ["rnd", "rnd","srdqn","rnd"]
	elif config.brainTypes == 14: 
		config.agentTypes = ["rnd", "rnd","rnd","srdqn"]
	elif config.brainTypes == 15: 
		config.agentTypes = ["Strm", "bs","bs","bs"]		
	elif config.brainTypes == 16: 
		config.agentTypes = ["bs", "Strm","bs","bs"]		
	elif config.brainTypes == 17: 
		config.agentTypes = ["bs", "bs","Strm","bs"]		
	elif config.brainTypes == 18: 
		config.agentTypes = ["bs", "bs","bs","Strm"]
	elif config.brainTypes == 19: 
		config.agentTypes = ["rnd", "bs","bs","bs"]		
	elif config.brainTypes == 20: 
		config.agentTypes = ["bs", "rnd","bs","bs"]		
	elif config.brainTypes == 21: 
		config.agentTypes = ["bs", "bs","rnd","bs"]		
	elif config.brainTypes == 22: 
		config.agentTypes = ["bs", "bs","bs","rnd"]						
	elif config.brainTypes == 23: 
		config.agentTypes = ["Strm", "Strm","Strm","Strm"]
	elif config.brainTypes == 24: 
		config.agentTypes = ["rnd", "rnd","rnd","rnd"]		
	elif config.brainTypes == 25: 
		config.agentTypes = ["bs", "bs","bs","bs"]
	elif config.brainTypes == 26: 
		config.agentTypes = ["bs", "Strm","Strm","Strm"]
	elif config.brainTypes == 27: 
		config.agentTypes = ["Strm", "bs","Strm","Strm"]
	elif config.brainTypes == 28: 
		config.agentTypes = ["Strm", "Strm","bs","Strm"]
	elif config.brainTypes == 29: 
		config.agentTypes = ["Strm", "Strm","Strm","bs"]
	elif config.brainTypes == 30: 
		config.agentTypes = ["bs", "rnd","rnd","rnd"]
	elif config.brainTypes == 31: 
		config.agentTypes = ["rnd", "bs","rnd","rnd"]
	elif config.brainTypes == 32: 
		config.agentTypes = ["rnd", "rnd","bs","rnd"]
	elif config.brainTypes == 33: 
		config.agentTypes = ["rnd", "rnd","rnd","bs"]		
	else:
		config.agentTypes = ["bs", "bs","bs","bs"]

def fillnodes(config):
	if config.NoHiLayer == 2:
		config.nodes = [config.stateDim * config.multPerdInpt, config.node1,config.node2,config.actionListLen]
	elif config.NoHiLayer == 3:
		config.nodes = [config.stateDim * config.multPerdInpt, config.node1,config.node2,config.node3,config.actionListLen]


def setSavedDimentionPerBrain(config):
	if config.ifUsePreviousModel and not config.iftl:
		if config.demandDistribution == 0 and config.demandUp == 9 and config.demandLow == 0 and config.actionUp == 8:
			if config.brainTypes == 3:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61
			elif config.brainTypes == 4:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61
			elif config.brainTypes == 5:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 6:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 7:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 8:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 9:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 10:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 11:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 12:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 13:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 14:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
		
		elif config.demandDistribution == 1 and config.demandMu == 10 and config.demandSigma == 2 and config.actionUp == 5:
			if config.brainTypes == 3:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61
			elif config.brainTypes == 4:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61
			elif config.brainTypes == 5:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 6:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 7:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 8:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 9:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 10:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 11:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 12:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 13:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 14:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		

		elif config.demandDistribution == 2 and config.demandUp == 9 and config.demandLow == 0 and config.actionUp == 8:
			if config.brainTypes == 3:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61
			elif config.brainTypes == 4:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61
			elif config.brainTypes == 5:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 6:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 7:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 8:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 9:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 10:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 11:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 12:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 13:
				config.multPerdInpt = 5
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		
			elif config.brainTypes == 14:
				config.multPerdInpt = 10
				config.NoHiLayer = 3
				config.node1=180
				config.node2=130
				config.node3=61		

		elif config.demandDistribution != 3 and config.demandDistribution != 4:
			if config.brainTypes == 7:
				config.dnnUpCnt = 10000
				config.multPerdInpt = 5
				config.NoHiLayer = 2
				config.lr0 = 0.001
			elif config.brainTypes == 8:
				config.dnnUpCnt = 5000
				config.multPerdInpt = 5
				config.NoHiLayer = 2 # this should be 3
				config.lr0 = 0.00025
			elif config.brainTypes == 9:
				config.dnnUpCnt = 5000
				config.multPerdInpt = 3
				config.NoHiLayer = 2
				config.lr0 = 0.001
			elif config.brainTypes == 10:
				config.dnnUpCnt = 5000
				config.multPerdInpt = 3 # it should be 5 
				config.NoHiLayer = 2
				config.lr0 = 0.001

def set_optimal(config):
	if config.demandDistribution == 0:
		if config.cp1==2 and config.ch1==2 and config.ch2==2 and config.ch3==2 and config.ch4==2 :
			config.f1 = 8.
			config.f2 = 8.
			config.f3 = 0.
			config.f4 = 0.

def get_config():
	config, unparsed = parser.parse_known_args()
	config = update_config(config)

	return config, unparsed

def fill_leadtime_initial_values(config):
	config.leadRecItemLow = [config.leadRecItem1, config.leadRecItem2, config.leadRecItem3, config.leadRecItem4]
	config.leadRecItemUp = [config.leadRecItem1, config.leadRecItem2, config.leadRecItem3, config.leadRecItem4]
	config.leadRecOrderLow = [config.leadRecOrder1, config.leadRecOrder2, config.leadRecOrder3, config.leadRecOrder4]
	config.leadRecOrderUp = [config.leadRecOrder1, config.leadRecOrder2, config.leadRecOrder3, config.leadRecOrder4]
	config.ILInit = [config.ILInit1, config.ILInit2, config.ILInit3, config.ILInit4]
	config.AOInit = [config.AOInit1, config.AOInit2, config.AOInit3, config.AOInit4]
	config.ASInit = [config.ASInit1, config.ASInit2, config.ASInit3, config.ASInit4]

def get_auxuliary_leadtime_initial_values(config):
	config.leadRecOrderUp_aux = [config.leadRecOrder1, config.leadRecOrder2, config.leadRecOrder3, config.leadRecOrder4]
	config.leadRecItemUp_aux = [config.leadRecItem1, config.leadRecItem2, config.leadRecItem3, config.leadRecItem4]

def fix_lead_time_manufacturer(config):
	if config.leadRecOrder4 > 0:
		config.leadRecItem4 += config.leadRecOrder4
		config.leadRecOrder4 = 0 

def set_sterman_parameters(config):
	config.alpha_b =[config.alpha_b1,config.alpha_b2,config.alpha_b3,config.alpha_b4]
	config.betta_b =[config.betta_b1,config.betta_b2,config.betta_b3,config.betta_b4]	


def update_config(config):
	config.actionList = buildActionList(config)		# The list of the available actions
	config.actionListLen = len(config.actionList)		# the length of the action list
		
	# set_optimal(config)
	config.f = [config.f1, config.f2, config.f3, config.f4] # [6.4, 2.88, 2.08, 0.8]

	config.actionListLen=len(config.actionList)
	if config.demandDistribution == 0:
		config.actionListOpt=list(range(0,int(max(config.actionUp*30+1, 3*sum(config.f))),1))
	else:
		config.actionListOpt=list(range(0,int(max(config.actionUp*30+1, 7*sum(config.f))),1))
	config.actionListLenOpt=len(config.actionListOpt)
	config.agentTypes=['dnn','dnn','dnn','dnn']
	config.saveFigInt = [config.saveFigIntLow, config.saveFigIntUp]
	
	if config.brainTypes == 0:
		config.NoAgent=min(config.NoAgent,len(config.agentTypes))
		config.agentTypes=[config.agent_type1,config.agent_type2,config.agent_type3,config.agent_type4]
	else:
		config.NoAgent=4
		setAgentType(config)					# set the agent brain types according to ifFourDNNtrain, ...

	config.c_h =[config.ch1, config.ch2, config.ch3, config.ch4]
	config.c_p =[config.cp1, config.cp2, config.cp3, config.cp4]

	config.stateDim= getStateDim(config) # Number of elements in the state description - Depends on ifUseASAO		
	np.random.seed(seed = config.seed)
	setSavedDimentionPerBrain(config) # set the parameters of pre_trained model. 
	fillnodes(config)			# create the structure of network nodes 	
	get_auxuliary_leadtime_initial_values(config)
	fix_lead_time_manufacturer(config)
	fill_leadtime_initial_values(config)
	set_sterman_parameters(config)

	return config

