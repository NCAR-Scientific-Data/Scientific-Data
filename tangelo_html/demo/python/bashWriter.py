from observable import Observable
from observer import Observer
 
class BashWriter(Observer):
    def update(self, *args, **kwargs):
        dest = args[0]
        if(dest == 'bashWriter'):   
            # Get Arguments
            task = args[1]
            if(task == 'insert' or task == 'delete'):
                index = args[2]
                message = args[3]
                comment = args[4]
                filename = args[5]
            elif(task == 'append'):
                message = args[2]
                comment = args[3]
                filename = args[4]
            elif(task == 'move'):
                index = args[2]
                filename = args[3]

            # Run Task
            if(task == 'append'):
                f = open(filename, 'a')
                f.write(message + " # " + comment + "\n")
                f.close()
            elif(task == 'insert'):
                f = open(filename, 'r')
                lines = f.readlines()
                lines.insert(index, message + " # " + comment + "\n")
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
            elif(task == 'move'):
                f = open(filename, 'r')
                lines = f.readlines()
                currentIndex = lines.index("# CURRENT STEP\n")
                lines[index], lines[currentIndex] = lines[currentIndex], lines[index]
                f.close()
                f = open(filename, 'w')
                for line in lines:
                    f.write(line)
                f.close()                
        else:
        	pass

 
 
if __name__ == "__main__":
    observable = Observable()
 
    bashWriter = BashWriter()
    observable.register(bashWriter)
 
    #observable.update_observers('bashWriter',  'insert', 1, "free willy \n", 'bash/test.sh')
    observable.update_observers('foo', 'append', 0, "echo hello mars", 'bash/test.sh')
    observable.update_observers('bashWriter', 'move', 2, 'bash/test.sh')