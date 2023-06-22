read -r -p "Select distro (Arch / RedHat / Debian)? [A/R/D] " response
case $response in
        [aA]* ) sh build.Arch.sh; break;;
        [rR]* ) sh build.RHEL.sh; break;;
        [dD]* ) sh build.Debian12.sh; break;;
        * ) echo "Please answer A, R, or D.";;
    esac

sh install.sh
