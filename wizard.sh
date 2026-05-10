#!/bin/bash

echo "TRIP Resurgence Network Registration Wizard"

read -r -p "Base Name: " base
read -r -p "Person: " person
read -r -p "E-Mail: " email
read -r -p "WWW: " www
read -r -p "PGP Fingerprint: " fingerprint
read -r -p "Organization Name: " orgname
read -r -p "ITAD: " itad
read -r -p "Prefix: " prefix

cat <<EOF > data/person/$base-TRIPNET
person:             $person
e-mail:             $email
www:                $www
nic-hdl:            $base-TRIPNET
org:                ORG-$base
pgp-fingerprint:    $fingerprint
mnt-by:             $base-MNT
source:             TRIPNET
EOF

cat <<EOF > data/mntner/$base-MNT
mntner:             $base-MNT
admin-c:            $base-TRIPNET
tech-c:             $base-TRIPNET
mnt-by:             $base-MNT
source:             TRIPNET
auth:               pgp-fingerprint $fingerprint
EOF

cat <<EOF > data/organisation/ORG-$base
organisation:       ORG-$base
org-name:           $orgname
admin-c:            $base-TRIPNET
tech-c:             $base-TRIPNET
mnt-by:             $base-MNT
source:             TRIPNET
EOF

cat <<EOF > data/itad/ITAD$itad
itad:               ITAD$itad
itad-name:          $orgname
admin-c:            $base-TRIPNET
tech-c:             $base-TRIPNET
mnt-by:             $base-MNT
org:                ORG-$base
source:             IANA
EOF

cat <<EOF > data/e164num/$itad
e164num:            ${prefix}0000 - ${prefix}9999
prefix:             $prefix
netname:            $base-NETWORK
admin-c:            $base-TRIPNET
tech-c:             $base-TRIPNET
mnt-by:             $base-MNT
status:             ASSIGNED
source:             TRIPNET
EOF

cat <<EOF > data/route/$itad
route:              $itad
origin:             ITAD$itad
length:             8
mnt-by:             $base-MNT
source:             TRIPNET
EOF
