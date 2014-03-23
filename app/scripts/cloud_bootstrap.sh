#!/bin/bash

NODE_NAME=''
RUN_LIST=''
AWS_ACCESS_KEY=''
AWS_SECRET_KEY=''
INSTANCE_TYPE=''
AMI=''

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

        --access-key)
            AWS_ACCESS_KEY="$2"
            shift 2
        ;;

        --secret-key)
            AWS_SECRET_KEY="$2"
            shift 2
        ;;

        --instance-type)
            INSTANCE_TYPE="$2"
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

#check parameters are not empty
[ -z "$NODE_NAME" ] && {
  error "Node Name is not set. Use option --node-name."
  exit 1
}

[ -z "$RUN_LIST" ] && {
  error "Run List is not set. Use option --run-list."
  exit 1
}

[ -z "$AWS_ACCESS_KEY" ] && {
  error "Aws Access Key is not set. Use option --access-key."
  exit 1
}

[ -z "$AWS_SECRET_KEY" ] && {
  error "Aws Secret Key is not set. Use option --secret-key."
  exit 1
}

[ -z "$INSTANCE_TYPE" ] && {
  error "Instance type is not set. Use option --instance-type."
  exit 1
}

info "Parameters Correctly received"

info "Starting Cloud Instance creation followed by chef-bootstrap"

for COUNT in 1 2; do
    knife ec2 server create --node-name $NODE_NAME -A $AWS_ACCESS_KEY -K $AWS_SECRET_KEY -r $RUN_LIST -f $INSTANCE_TYPE -I $AMI || {
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