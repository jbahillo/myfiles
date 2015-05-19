#!/bin/bash
OLDIFS=$IFS     # conserva el separador de campo
IFS=$'\n'     # nuevo separador de campo, el caracter fin de línea
#He definido esta variable ya que en otros sistemas, puede estar almacenado en otras ubicaciones como /var/vmail
MAILDIR="/var/spool/mail"
for e in $(cat /etc/passwd)
do
    USUARIO=$(echo $e | cut -d\: -f1)
    USERID=$(echo $e| cut -d\: -f3)
    if [ "$USERID" -gt "500" ]; then
        if [ -d "/home/$USUARIO" ]; then
            HOMESIZE=$(du -s /home/$USUARIO | awk '{print $1}')
        else
            HOMESIZE=0
        fi
        if [ -a "$MAILDIR/$USUARIO" ]; then
            MAILSIZE=$(du -s $MAILDIR/$USUARIO | awk '{print $1}')
        else
            MAILSIZE=0
        fi
        TOTALSIZE=$(expr $HOMESIZE + $MAILSIZE)
        #Por tamaño de la maquina virtual he reducido el "aviso" a 1G
        if [ $TOTALSIZE -gt "1000000" ]; then
           echo  "$USUARIO  ocupa $TOTALSIZE"
           #No me ha quedado claro en el enunciado si lo que había que almacenar era el usuario, el UID, o su correo. He optamos por almacenar el nombre del usuario
           if [ -a "/root/Rusuario" ];then
               if  grep $USUARIO /root/Rusuario> /dev/null ; then
                   echo "El usuario ya está introducido"
               else
                   echo $USUARIO >> /root/Rusuario
               fi
           else
               echo $USUARIO >> /root/Rusuario
           fi
        fi
    fi
done
IFS=$OLDIFS
