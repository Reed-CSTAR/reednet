#!/bin/sh

function die() {
	echo "$@"
	exit 1
}

[ -z "$1" ] && die "FQDN required as first argument."

openssl req \
	-x509 -newkey rsa -noenc -keyout "$1".key -days 45 -out "$1".cert \
	-subj "/C=US/ST=Oregon/O=The Reed Institute" \
	-addext "subjectAltName=DNS:$1"
