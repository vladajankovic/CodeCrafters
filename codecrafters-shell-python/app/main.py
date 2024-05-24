import sys
import os
import subprocess


def main():

    builtin_cmds = ["echo", "type", "exit"] 

    sys.stdout.write("$ ")
    sys.stdout.flush()

    # Wait for user input
    command = input()

    while command != "":
        if len(command.split()) > 1:
            command, args = command.split(maxsplit=1)
        else:
            args = ""

        if command == "exit":
            break

        elif command == "echo":
            print(args)

        elif command == "type":
            if args in builtin_cmds:
                print(f"{args} is a shell builtin")
            else:
                found = False
                paths = os.environ["PATH"].split(":")
                for _path in paths:
                    if os.path.exists(_path+'/'+args):
                        print(f"{args} is {_path+'/'+args}")
                        found = True
                        break
                if not found:
                    print(f"{args}: not found")

        else:
            if os.path.exists(command):
                subprocess.run([command, args]) 
            else:
                print(f"{command}: command not found")
            
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()


if __name__ == "__main__":
    main()
