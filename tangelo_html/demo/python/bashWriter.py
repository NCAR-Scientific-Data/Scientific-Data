from observable import Observable
from observer import Observer
 
class BashWriter(Observer):
    def update(self, *args, **kwargs):
        dest = args[0]
        task = args[1]
        index = args[2]
        message = args[3]
        filename = args[4] 

        if(dest == 'bashWriter'):   
            if(task == 'append'):
                f = open(filename, 'a')
                f.write(message)
                f.close()
            elif(task == 'insert'):
                f = open(filename, 'r')
                lines = f.readlines()
                lines.insert(index, message)
                f.close()
                f = open(filename, 'w')
                for line in lines:
                    f.write(line)
                f.close()                
            elif(task == 'delete'):
                f = open(filename, 'r+')
                lines = f.readlines()
                try:
                    del lines[index]
                    found = True
                except ValueError:
                    found = False
                f.close()
                if(found):
                    f = open(filename, 'w')
                    for line in lines:
                        f.write(line)
                    f.close()
            elif(args[1] == 'comment'):
                f = open(args[3], 'r+')
                lines = f.readlines()
                f.close()
        else:
        	pass

 
 
if __name__ == "__main__":
    observable = Observable()
 
    bashWriter = BashWriter()
    observable.register(bashWriter)
 
    #observable.update_observers('bashWriter',  'insert', 1, "free willy \n", 'bash/test.sh')
    observable.update_observers('foo', 'append', 0, "echo hello mars \n", 'bash/test.sh')
    observable.update_observers('bashWriter', 'delete', 1, "echo Hello World \n", 'bash/test.sh')