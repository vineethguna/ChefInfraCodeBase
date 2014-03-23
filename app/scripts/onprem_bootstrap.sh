#!/bin/bash

NODE_NAME=''
RUN_LIST=''
IP_ADDRESS=''
USERNAME=''
PASSWORD=''

while [ $# -gt 0 ]
do
    case "$1" in
        --node-name)
            NODE_NAME="$2"
            shift 2
        ;;

        --run-list)
            RUN_LIST="$2"
            shift 2
        ;;

        --ip-address)
            IP_ADDRESS="$2"
            shift 2
        ;;

        --username)
            USERNAME="$2"
            shift 2
        ;;

        --password)
            PASSWORD="$2"
            shift 2
        ;;
    esac
done

#sub routines for logging
error() {
  TIMESTAMP="`date "+%F %T"`"
  echo "$TIMESTAMP ERROR  $@" >&2
}

warn() {
  TIMESTAMP="`date "+%F %T"`"
  echo "$TIMESTAMP WARN $@" >&2
}

info() {
  TIMESTAMP="`date "+%F %T"`"
  echo "$TIMESTAMP INFO $@"
}

#check node_name and run_list are not empty
[ -z "$NODE_NAME" ] && {
  error "Node Name is not set. Use option --node-name."
  exit 1
}

[ -z "$RUN_LIST" ] && {
  error "Run List is not set. Use option --run-list."
  exit 1
}

[ -z "$IP_ADDRESS" ] && {
  error "IP address is not set. Use option --ip-address."
  exit 1
}

[ -z "$USERNAME" ] && {
  error "Username is not set. Use option --username."
  exit 1
}

[ -z "$PASSWORD" ] && {
  error "Password is not set. Use option --password."
  exit 1
}

info "Parameters Correctly received"

info "Starting Chef Bootstrap"

#knife command to bootstrap the node
for COUNT in 1 2; do
    knife bootstrap $IP_ADDRESS --node-name $NODE_NAME -r $RUN_LIST -x $USERNAME -P $PASSWORD --sudo || {
        error 'Failed to execute bootstrap script'
        if [ $COUNT -lt 2 ]; then
            info "Trying to run chef-client one more time."
            sleep 60
            continue
        else
            exit 1
        fi
    }
    break
done