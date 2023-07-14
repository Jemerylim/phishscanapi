import csv
csv_file_path = 'web/statics/datasets/malicious_phish.csv'
#csv_file_path = '/Users/jeremy/Documents/GitHub/phishscanapi/web/statics/datasets/malicious_phish.csv'
malicious_urls=[]

class BlackListTrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class BlackListTrie:
    def __init__(self):
        self.root = BlackListTrieNode()

    def insert(self, url):
        if url.startswith("http://"):
            url = url[7:]
        elif url.startswith("https://"):
            url = url[8:]

        # Reverse and split the URL components
        components = url.split(".")
        components.reverse()

        # Traverse the trie and insert the URL components
        node = trie.root
        for component in components:
            component = component.lower()
            if component not in node.children:
                node.children[component] = BlackListTrieNode()
            node = node.children[component]
        node.is_end_of_word = True

        return True

    def search(self, url):
        # Reverse and split the URL
        components = url.split(".")
        components.reverse()

        # Perform the search
        node = trie.root
        for component in components:
            component = component.lower()
            if component not in node.children:
                return False
            node = node.children[component]
        else:
            if node.is_end_of_word:
                return True
            else:
                return False
    
def create_trie():
    trie = BlackListTrie()
    with open(csv_file_path, 'r') as file:
        # Create a CSV reader
        csv_reader = csv.reader(file)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Access data in each row
            # Example: Assuming the CSV has two columns 'Name' and 'Age'
            if(row[1] != 'benign'):
                malicious_urls.append(row[0])

            # Do something with the data
       # print(malicious_urls)


    for url in malicious_urls:
        if url.startswith("http://"):
            url = url[7:]
        elif url.startswith("https://"):
            url = url[8:]

        components = url.split(".")
        components.reverse()

        node = trie.root
        for component in components:
            component = component.lower()
            if component not in node.children:
                node.children[component] = BlackListTrieNode()
            node = node.children[component]
        node.is_end_of_word = True

    return trie

# Create the trie
trie = create_trie()
if trie is not None:
    print("Trie is created.")
else:
    print("Trie is not created.")
