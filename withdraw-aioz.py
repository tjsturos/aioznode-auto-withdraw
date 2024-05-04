import json
import subprocess
from datetime import datetime
import time

def run_withdrawal(aioznode_dir, address, show_output=False):
    def log_balance(balance_amount_atto, balance_amount_aioz):
        # Log the date and balance to a file in aioznode_dir directory
        log_filename = aioznode_dir + "withdraw_log.txt"
        with open(log_filename, "a") as log_file:
            log_file.write(f"{datetime.now().isoformat()} Balance: {balance_amount_atto} attoaioz ({balance_amount_aioz} AIOZ)\n")

    def withdraw(aioznode_dir, balance_amount, address):
        # Prepare the withdraw command
        withdraw_command = [aioznode_dir + "aioznode", "reward", "withdraw", "--address", address, "--amount", balance_amount + "attoaioz", "--priv-key-file", "privkey.json"]

        # Run the withdraw command and capture the output
        withdraw_output = subprocess.run(withdraw_command, capture_output=True, text=True)

        # Check if the withdraw command was successful
        if "txid" in withdraw_output.stdout:
            if show_output:
                print("Withdrawal successful. Transaction ID:", json.loads(withdraw_output.stdout)["txid"])
            return True
        else:
            if show_output:
                error_message = withdraw_output.stderr.strip().split("\n")[0]
                print("Withdrawal failed. Error:", error_message)
            return False

    # Run the command to fetch the reward balance
    output = subprocess.check_output([aioznode_dir + "aioznode", "reward", "balance"])
    data = json.loads(output)

    # Extract the balance amount in attoaioz
    balance_amount_atto = int(data["balance"][0]["amount"])

    # Convert balance to AIOZ
    balance_amount_aioz = balance_amount_atto / 10**18

    log_balance(balance_amount_atto, balance_amount_aioz)

   
   

    # Convert 1 AIOZ to attoAIOZ
    one_aioz = 1000000000000000000

    # Check if the balance is greater than or equal to 1 AIOZ
    if balance_amount_atto >= one_aioz:
        while True:
            # Try to withdraw
            if withdraw(aioznode_dir, str(balance_amount_atto), address):
                break  # Exit the loop if withdrawal is successful
            else:
                # Check if the error is rate limit exceeded
                if "rate limit exceeded" in error_message:
                    # Parse the wait time from the error message
                    wait_time = int(error_message.split("after ")[1].split(" minutes")[0]) + 1
                    print(f"Rate limit exceeded. Retrying in {wait_time} minutes.")
                    time.sleep(wait_time * 60)  # Wait for wait_time minutes before retrying
                else:
                    break  # Exit the loop if the error is not rate limit exceeded
    else:
        if show_output:
            print("Balance is less than 1 AIOZ, cannot withdraw.")

# Set the directory of the aioznode binary
aioznode_dir = "/path/to/your/aioznode/directory/"
address = "address"
# Run the withdrawal function
run_withdrawal(aioznode_dir, address)
