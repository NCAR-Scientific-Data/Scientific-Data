from observable import Observable
from observer import Observer
 
class BashWriter(Observer):
    def update(self, *args, **kwargs): 
        if(args[0]) == 'bashWriter'):   
            if(args[0] == 'add'):
                f = open(args[2], 'a')
                f.write(args[1])
                f.close()
            elif(args[0] == 'delete'):
                f = open(args[2], 'r+')
                lines = f.readlines()
                try:
                    lines.remove(args[1])
                    found = True
                except ValueError:
                    found = False
                f.close()
                if(found):
                    f = open(args[2], 'w')
                    for line in lines:
                        f.write(line)
                    f.close()
        else:
        	pass

 
 
if __name__ == "__main__":
    observable = Observable()
 
    bashWriter = BashWriter()
    observable.register(bashWriter)
 
    observable.update_observers('bashWriter',  'add', "echo Hello World \n", 'bash/test.sh')
    observable.update_observers('add', "echo hello mars \n", 'bash/test.sh')
    observable.update_observers('delete', "echo Hello World \n", 'bash/test.sh')