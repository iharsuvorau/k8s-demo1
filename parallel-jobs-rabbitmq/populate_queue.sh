#!/usr/bin/env bash

/usr/bin/amqp-declare-queue --url=$BROKER_URL -q job1 -d

for f in apple banana cherry date fig grape lemon melon
do
  /usr/bin/amqp-publish --url=$BROKER_URL -r job1 -p -b $f
done