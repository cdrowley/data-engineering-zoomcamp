# Command Line Cheat Sheet

The command line is a text-based interface for interacting with a computer's operating system, and it allows users to enter commands and execute them by pressing the enter key. A terminal is a program that provides a command-line interface.

Unix shell is a command-line interface based on Unix-like systems, such as Linux, macOS, and BSD. It provides a powerful and flexible environment for managing files, running programs, and automating tasks.

In contrast, Windows uses a different command-line interface, known as the Windows command prompt, which has a different set of commands and utilities. However, Windows 10 also includes a Linux subsystem that allows users to run Linux commands natively in the Windows command prompt.

-------

| Command | Description                                   | Example                 |
| ------- | --------------------------------------------- | ----------------------- |
| `cd`    | Change directory                              | `cd documents/`         |
| `ls`    | List files in directory                       | `ls -al`                |
| `mkdir` | Create a new directory                        | `mkdir test`            |
| `rmdir` | Remove an empty directory                     | `rmdir test`            |
| `touch` | Create a new file                             | `touch file.txt`        |
| `rm`    | Remove a file or directory                    | `rm file.txt`           |
| `mv`    | Move or rename a file or directory            | `mv file.txt newdir/`   |
| `cp`    | Copy a file or directory                      | `cp file.txt file2.txt` |
| `echo`  | Display a message                             | `echo Hello, world!`    |
| `cat`   | Display contents of a file                    | `cat file.txt`          |
| `less`  | Display contents of a file one page at a time | `less file.txt`         |
| `head`  | Display the first few lines of a file         | `head file.txt`         |
| `tail`  | Display the last few lines of a file          | `tail file.txt`         |
| `grep`  | Search for a pattern in a file                | `grep "hello" file.txt` |
| `find`  | Find files or directories                     | `find / -name file.txt` |
| `sort`  | Sort lines of text                            | `sort file.txt`         |
| `uniq`  | Filter out repeated lines of text             | `uniq file.txt`         |
| `wc`    | Count lines, words, and characters in a file  | `wc file.txt`           |

------

## Flags

Flags modify a command's behavior to enable/disable features, change output format, or perform other tasks and are usually optional. Flags are denoted by a hyphen and a single or combined letter(s).

Think of them as optional arguments you may pass to a function `print('Hello', 'world!', sep=' ', end='\n')`

For example:

- `ls -a` lists all files, including hidden files
- `ls -l` lists files in long format
- `ls -al` lists all files in long format

## Input and Output Redirection

Input and output redirection are techniques used to control the flow of data between commands and files.

#### Output Redirection

`>` is used to direct the output of a command to a file. For example, to write to a file:

- `echo "Hello, world\!" > file.txt` **careful as this will overwrite the file if it exists**

`>>` is used to append output to a file instead of overwriting it. For example, adding a string to the end of a file:

- `echo "Goodbye, world" >> file.txt`

`<` is used to direct the input of a command from a file. For example, to sort the contents of a file:

- `sort < file.txt` **this only prints to the terminal**

Input and output redirection can be used together to pass data between commands and files. For example, to sort the contents of a file and write the output to a new file:

- `sort < file.txt > sorted.txt`

## Pipes

Pipes (`|`) are used to connect the output of one command to the input of another command. This allows you to chain multiple commands together to perform more complex tasks.

For example, create dummy data, sort it, and then print the first 3 lines:

- `echo -e "apple\nbanana\norange\ngrape" | sort | head -n 3`

Another example, to find the PID of the Chrome browser process (and use awk to print the second column):

- `ps -ef | grep chrome | awk '{print $2}'`

## More Commands

| Command | Description                               | Example                                             |
| ------- | ----------------------------------------- | --------------------------------------------------- |
| `man`   | Display manual page for a command         | `man ls`                                            |
| `awk`   | Manipulate and process text files         | `awk '{print $2}' myfile.txt`                       |
| `sed`   | Stream editor for modifying a text stream | `sed 's/pattern/replacement/g' myfile.txt`          |
| `curl`  | Transfer data from or to a server         | `curl http://example.com`                           |
| `wget`  | Download files from the web               | `wget http://example.com/myfile.txt`                |
| `tar`   | Compress or extract files                 | `tar -czvf archive.tar.gz myfile.txt`               |
| `untar` | Extract files                             | `tar -xvf archive.tar.gz`                           |
| `ssh`   | Connect to a remote server                | `ssh user@hostname`                                 |
| `scp`   | Copy files to or from a remote server     | `scp myfile.txt user@hostname:/path/to/destination` |
| `chmod` | Change file permissions                   | `chmod 755 myfile.txt`                              |
| `chown` | Change file ownership                     | `chown user:group myfile.txt`                       |
| `ps`    | Display running processes                 | `ps -ef`                                            |
| `kill`  | Terminate a process                       | `kill pid`                                          |
