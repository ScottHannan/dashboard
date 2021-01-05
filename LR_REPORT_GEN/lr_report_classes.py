## CLASSES FOR THE COMPARISON GEN ##
## Each Loadrunner report is represented by an LR_Report ##
## Each transaction is represented by.... a Transaction ## 

class LR_Report:
  
  def __init__(self, s3_data):
    self.lr_name = s3_data[0][2]
    self.lr_moneymakers = []
    self.lr_transactions = []
    
    for transaction in s3_data:
      self.lr_transactions.append(Transaction(transaction))
    
    ## find the moneymakers
    for transaction in self.lr_transactions:
      if "_Total" in transaction.transaction_name:
        self.lr_moneymakers.append(transaction)
    self.lr_money_maker_count = len(self.lr_moneymakers)

class Transaction:

  def __init__(self, scenario_data): 
    self.transaction_name = scenario_data[0]
    self.nintieth_percentile = scenario_data[1]
    self.partition_0 = scenario_data[2]
