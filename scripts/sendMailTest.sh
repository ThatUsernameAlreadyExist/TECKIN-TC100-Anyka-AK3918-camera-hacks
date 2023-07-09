#!/bin/sh

. /mnt/scripts/update_timezone.sh

MAILDATE=$(date -R)

if [ ! -f /mnt/config/sendmail.conf ]
then
  echo "You must configure /mnt/config/sendmail.conf before using sendPictureMail or sendMailTest"
  exit 1
fi

. /mnt/config/sendmail.conf

if [ -f /tmp/sendPictureMail.lock ]; then
  rm /tmp/sendPictureMail.lock
fi

{

printf '%s\n' "From: ${FROM}
To: ${TO}
Subject: ${SUBJECT}
Date: ${MAILDATE}
Mime-Version: 1.0
Content-Type: text/plain; charset=\"US-ASCII\"
Content-Transfer-Encoding: 7bit
Content-Disposition: inline

${BODY}
"
} | busybox sendmail -v -H"exec /mnt/bin/openssl s_client -quiet -connect $SERVER:$PORT" -f"$FROM" -au"$AUTH" -ap"$PASS" $TO


