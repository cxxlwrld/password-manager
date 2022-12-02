from cryptography.fernet import Fernet

class PasswordManager:

    def __int__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()


    def create_password_file(self, path, initial_values=None):
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
               self.add_password(key, value)

    def load_password_file(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def  add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":"  + encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict[site]



def main():
    password = {
        'email': "3567890",
        "facebook": "myfbpassword",
        "youtube": "cxxl123",
        "sololearn": "1123356789"
    }

    pm = PasswordManager()

    print("""What would you liketo do?
    (a) Create a new key
    (b) Load an existing key
    (c) Create a new password file
    (d) Load existing password file
    (e) Add a new password
    (f) Get a password
    (q) Quit
    
    """)
    done = False
    while not done:

        choice = input("enter your choice: ")
        if choice == "a":
            path = input("enter path: ")
            pm.create_key(path)
        elif choice == "b":
            path = input("enter path")
            pm.load_key(path)
        elif choice == "c":
            path = input("enter path")
            pm.create_password_file(path, password)
        elif choice == "d":
            path = input("enter path")
            pm.load_password_file(path)
        elif choice == "e":
            site = input("enter the site")
            password = input("enter the password")
            pm.add_password(site, password)
        elif choice == "f":
            site = input("what site's password do you wish to retrieve?")
            print(f"password for {site} is {pm.get_password(site)}")
        elif choice == "q":
            done = True
            print("quiting.......")
        else:
            print("Invalid choice")


if __name__  == "__main__":
    main()

