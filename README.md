# Expedite

Simple encrypted file transfer service

## Introduction

Expedite is a simple encrypted file transfer service that allows for people to 
share synchronously assets among each other without having to rely on third 
party file sharing services (and constantly worrying about how their data might
be used) or feeling the need of having publicly visible IP addresses (and
constantly worrying about script kiddies attacking your computer).

Expedite Server can be deployed on a virtual private server having an IP 
address that is discoverable by the Expedite Client users to broker file 
contents. The transfers facilitated using WebSockets are end-to-end encrypted 
with the use of 128-bit Advanced Encryption Standard and the server is 
restricted to logging only unidentifiable activities to the volatile memory.

Expedite is currently in BETA phase and if you like to direction the project is
heading towards, kindly consider helping me out by starring the project 
repository, filing issue tickets for software errors or feature requests, 
contributing to the codebase of the project or sponsoring me to help maintain 
the servers and to help me keep working on more FOSS projects like these.

## Offerings

You can either deploy your own Expedite Server to broker file contents from 
your group of Expedite Client users or you can use the following publicly
available servers setup by me instead. Picking the server that is closer to 
your group of users can help with improving performance and reliability of the
transfer. Please open up a pull request if you wish to list your server here.

- Atlanta, GA - `ws://expedite-atla.apexaltruism.net:6969`
- Mumbai, MH - `ws://expedite-mumb.apexaltruism.net:6969`

## Illustration

### Client - Bridge - Info

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/bridge-info-stat.png)

### Client - Bridge - Delivering - Static

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/bridge-send-stat.png)

### Client - Bridge - Collecting - Static

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/bridge-recv-stat.png)

### Client - Bridge - Delivering - Progress

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/bridge-send-prog.gif)

### Client - Bridge - Collecting - Progress

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/bridge-recv-prog.gif)

### Client - Prompt - Help

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/prompt-help-stat.png)

### Client - Prompt - Delivering - Help

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/prompt-send-help.png)

### Client - Prompt - Collecting - Help

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/prompt-recv-help.png)

### Client - Prompt - Delivering - Static

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/prompt-send-stat.png)

### Client - Prompt - Collecting - Static

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/prompt-recv-stat.png)

### Client - Prompt - Delivering - Progress

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/prompt-send-prog.gif)

### Client - Prompt - Collecting - Progress

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/prompt-recv-prog.gif)

### Server - Broker

![](https://raw.githubusercontent.com/gridhead/expedite/main/data/brok-stat.png)

## Installation

### For development

1.  Ensure that the required tools and dependencies are installed.
    ```
    $ sudo dnf install python3 python3-virtualenv python3-pip git poetry
    ```
2.  Fork the repository and clone the project to your local storage.
    ```
    $ git clone git@github.com:$(whoami)/expedite.git
    ```
3.  Make the project cloning location the present working directory.
    ```
    $ cd expedite
    ```
4.  Create a virtual environment for installing project dependencies.
    ```
    $ virtualenv venv
    ```
5.  Activate the newly created virtual environment before proceeding.
    ```
    $ source venv/bin/activate
    ```
6.  Install the project codebase alongside the dependencies.
    ```
    (venv) $ poetry install
    ```

### For consumption

#### From PyPI

1.  Ensure that the required tools and dependencies are installed.
    ```
    $ sudo dnf install python3 python3-virtualenv python3-pip
    ```
2.  Create a virtual environment for installing project dependencies.
    ```
    $ virtualenv venv
    ```
3.  Activate the newly created virtual environment before proceeding.
    ```
    $ source venv/bin/activate
    ```
4.  Install the project codebase from Python Package Index.
    ```
    (venv) $ pip3 install expedite
    ```

#### From GitHub

1.  Visit the **GitHub Actions** page of the project repository.
    ```
    https://github.com/gridhead/expedite/actions
    ```
2.  To get automated builds for **GNU/Linux distributions**, visit the following page.
    ```
    https://github.com/gridhead/expedite/actions/workflows/gnul.yml
    ```
3.  To get automated builds for **Microsoft Windows**, visit the following page.
    ```
    https://github.com/gridhead/expedite/actions/workflows/mswn.yml
    ```
4.  Please request for the builds if they are unavailable in the recent workflow runs.
    ```
    https://github.com/gridhead/expedite/issues
    ```

## Execution

### Server

1.  Ensure that the previously created virtual environment is activated.
    ```
    $ source venv/bin/activate
    ```
2.  Execute the following command to view the help topics of the project.
    ```
    (venv) $ ed-server --help
    ```
    ```
    Usage: ed-server [OPTIONS]

    Options:
      -a, --addr TEXT           Set the interface for the service endpoint
                                [default: 127.0.0.1]
      -p, --port INTEGER RANGE  Set the port value for the service endpoint
                                [default: 8080; 64<=x<=65535]
      --version                 Show the version and exit.
      --help                    Show this message and exit.
    ```
3.  Start the broker service using the following command.
    ```
    (venv) $ ed-server --addr 0.0.0.0 --p 9090
    ```
    1. The broker service will run on IPv4 addressing (i.e. `0.0.0.0`) and on a specific port (i.e. `9090`).
    3. The broker service can be stopped by sending a keyboard interrupt (i.e. `Ctrl` + `C`) when done.
4.  Note the IP address or the hostname for use by client connections.
    ```
    ip a
    ```

### Client

1.  Ensure that the previously created virtual environment is activated.
    ```
    $ source venv/bin/activate
    ```
2.  Execute the following command to view the help topics of the project.
    ```
    (venv) $ ed-server --help
    ```
    ```
    Usage: ed-client [OPTIONS] COMMAND [ARGS]...

    Options:
      -h, --host TEXT           Set the address for the service endpoint
                                [required]
      -t, --time INTEGER RANGE  Set the expiry period for participants  [default:
                                15; 5<=x<=30]
      -e, --endo TEXT           Set the identity of the opposing client
      --version                 Show the version and exit.
      --help                    Show this message and exit.

    Commands:
      recv  Collect file through an encrypted transfer
      send  Deliver file through an encrypted transfer
    ```

#### Delivering

1.  Execute the following command to view the help topics of the `SEND` subcommand.
    ```
    (venv) $ ed-client send --help
    ```
    ```
    Usage: ed-client send [OPTIONS]

      Deliver file through an encrypted transfer

    Options:
      -p, --pswd TEXT           Set the password for delivering encryption
                                [default: 123972B4]
      -f, --file PATH           Set the filepath for delivering to network
                                [required]
      -s, --size INTEGER RANGE  Set the unit size for file chunking (in B)
                                [default: 262144; 1024<=x<=524288]
      --help                    Show this message and exit.
    ```
2.  If the delivering client is joining the network **before** the collecting client, execute the following command.
    ```
    (venv) $ ed-client --host ws://localhost:9090 --time 30 send --file /path/to/file.extn --pswd expedite --size 131072
    ```
    ```
    [2024-07-06 11:52:10] Expedite Client v0.1.0a2
    [2024-07-06 11:52:10] Addr. ws://localhost:9090
    [2024-07-06 11:52:10] Pass. expedite
    [2024-07-06 11:52:10] Plan. DELIVERING
    [2024-07-06 11:52:10] Wait. 30 seconds
    [2024-07-06 11:52:10] Please share your acquired identity to begin interaction.
    [2024-07-06 11:52:10] Attempting to connect to the network.
    [2024-07-06 11:52:10] Successfully connected to the network.
    [2024-07-06 11:52:10] You are now identified as 01276D06 in the network.
    ```
    1. The delivering client is attempting to connect to the broker service deployed at `ws://localhost:9090`.
    2. The delivering client has an inactivity timeout for `30 seconds` beyond which it will automatically disconnect.
    3. The delivering client has acquired the identity `01276D06` which can be used by the collecting client for discovery.
    4. The delivering client is attempting to share the file named `file.extn` from the location `/path/to/file.extn`.
    5. The delivering client is using the password `expedite` to encrypt the file contents with 128-bit AES encryption.
    6. The delivering client is going to process chunks of size `131072 byte` or `128KiB` at a time for delivering.
    7. The user of the delivering client must share their identity `01276D06` and password to start delivering process.
    8. The delivering client will disconnect from the network if the collecting client opens the program in the wrong mode.
3.  If the delivering client is joining the network **after** the collecting client, execute the following command.
    ```
    (venv) $ ed-client --host ws://localhost:9090 --time 30 --endo DEADCAFE send --file /path/to/file.extn --pswd expedite --size 131072
    ```
    ```
    [2024-07-06 12:02:09] Expedite Client v0.1.0a2
    [2024-07-06 12:02:09] Addr. ws://localhost:9090
    [2024-07-06 12:02:09] Pass. expedite
    [2024-07-06 12:02:09] Plan. DELIVERING
    [2024-07-06 12:02:09] Wait. 30 seconds
    [2024-07-06 12:02:09] Please wait for DEADCAFE to begin interaction.
    [2024-07-06 12:02:09] Attempting to connect to the network.
    [2024-07-06 12:02:09] Successfully connected to the network.
    [2024-07-06 12:02:09] You are now identified as BA40BB0F in the network.
    ```
    1. The delivering client is attempting to connect to the broker service deployed at `ws://localhost:9090`.
    2. The delivering client has an inactivity timeout for `30 seconds` beyond which it will automatically disconnect.
    3. The delivering client has acquired the identity `BA40BB0F` which can be used by the collecting client for discovery.
    4. The delivering client is attempting to share the file named `file.extn` from the location `/path/to/file.extn`.
    5. The delivering client is using the password `expedite` to encrypt the file contents with 128-bit AES encryption.
    6. The delivering client is going to process chunks of size `131072 byte` or `128KiB` at a time for delivering.
    7. The user of the delivering client expects the collecting client with the identity `DEADCAFE` to start interaction.
    8. The delivering client will disconnect from the network if the collecting client opens the program in the wrong mode.
4.  If the average latency from the delivering client to the broker service is **below 100ms**, consider **increasing the chunking size** to **improve the stability** of the delivering process.
5.  If the average latency from the delivering client to the broker service is **above 100ms**, consider **decreasing the chunking size** to **improve the performance** of the delivering process.
6.  Let the delivering process complete or if needed, abort an ongoing delivering process by sending a keyboard interrupt (i.e. `Ctrl` + `C`).

#### Collecting

1.  Execute the following command to view the help topics of the `RECV` subcommand.
    ```
    Usage: ed-client recv [OPTIONS]

      Collect file through an encrypted transfer

    Options:
      -p, --pswd TEXT  Set the password for collecting encryption  [required]
      --help           Show this message and exit.
    ```
2.  If the collecting client is joining the network **before** the delivering client, execute the following command.
    ```
    (venv) $ ed-client --host ws://localhost:8080 --time 30 recv --pswd expedite
    ```
    ```
    [2024-07-06 12:57:43] Expedite Client v0.1.0a2
    [2024-07-06 12:57:43] Addr. ws://localhost:8080
    [2024-07-06 12:57:43] Pass. expedite
    [2024-07-06 12:57:43] Plan. COLLECTING
    [2024-07-06 12:57:43] Wait. 30 seconds
    [2024-07-06 12:57:43] Please share your acquired identity to begin interaction.
    [2024-07-06 12:57:43] Attempting to connect to the network.
    [2024-07-06 12:57:43] Successfully connected to the network.
    [2024-07-06 12:57:43] You are now identified as 13755346 in the network.
    ```
    1. The collecting client is attempting to connect to the broker service deployed at `ws://localhost:9090`.
    2. The collecting client has an inactivity timeout for `30 seconds` beyond which it will automatically disconnect.
    3. The collecting client has acquired the identity `13755346` which can be used by the delivering client for discovery.
    4. The collecting client is using the password `expedite` to decrypt the file contents with 128-bit AES encryption.
    5. The user of the collecting client must share their identity `13755346` and password to start collecting process.
    6. The collecting client will disconnect from the network if the delivering client opens the program in the wrong mode.
3.  If the collecting client is joining the network **after** the delivering client, execute the following command.
    ```
    (venv) $ ed-client --host ws://localhost:8080 --time 30 --endo DEADCAFE recv --pswd expedite
    ```
    ```
    [2024-07-06 12:55:30] Expedite Client v0.1.0a2
    [2024-07-06 12:55:30] Addr. ws://localhost:8080
    [2024-07-06 12:55:30] Pass. expedite
    [2024-07-06 12:55:30] Plan. COLLECTING
    [2024-07-06 12:55:30] Wait. 30 seconds
    [2024-07-06 12:55:30] Please wait for DEADCAFE to begin interaction.
    [2024-07-06 12:55:30] Attempting to connect to the network.
    [2024-07-06 12:55:30] Successfully connected to the network.
    [2024-07-06 12:55:30] You are now identified as 13AA7DB2 in the network.
    ```
    1. The collecting client is attempting to connect to the broker service deployed at `ws://localhost:9090`.
    2. The collecting client has an inactivity timeout for `30 seconds` beyond which it will automatically disconnect.
    3. The collecting client has acquired the identity `13AA7DB2` which can be used by the delivering client for discovery.
    4. The collecting client is using the password `expedite` to decrypt the file contents with 128-bit AES encryption.
    5. The user of the collecting client must share their identity `13AA7DB2` and password to start collecting process.
    6. The collecting client will disconnect from the network if the delivering client opens the program in the wrong mode.
4.  Let the collecting process complete or if needed, abort an ongoing collecting process by sending a keyboard interrupt (i.e. `Ctrl` + `C`).
