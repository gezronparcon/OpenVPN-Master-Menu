# OpenVPN-Master-Menu
#!/bin/bash
clear                    	        
function create_user() {
echo -e "[Fill-up the field]"
read -p "Username : " Login
read -p "Password : " Pass
read -p "Expired (Days): " Date

IP=`dig +short myip.opendns.com @resolver1.opendns.com`
useradd -e `date -d "$Date days" +"%Y-%m-%d"` -s /bin/false -M $Login
exp="$(chage -l $Login | grep "Account expires" | awk -F": " '{print $2}')"
echo -e "$Pass\n$Pass\n"|passwd $Login &> /dev/null
echo -e ""
echo -e "======Account Information======"
echo -e "Username: $Login "
echo -e "Password: $Pass"
echo -e "-------------------------------"
echo -e "Expired Date: $exp"
echo -e "==============================="
echo -e "Mod By kikay001"
echo -e "Type (menu) to back menu option."
echo -e ""
	}
function create_ss() {

	nano /etc/shadowsocks.json
	echo -e "Successfully edit your Shadowsocks Clients Account"
	echo -e ""
	echo -e ""
	
	clear
	echo "Shadowsocks will restart to start the new added port." 
	echo "Connecting to..."
	sleep 0.5
	echo "Showdowsocks Restarting..."
	sleep 0.5
	
	/etc/init.d/shadowsocks restart
	echo -e "Type [menu] to back menu option."
	}
function restart_ss() {
	 /etc/init.d/shadowsocks restart
	echo -e "Successfully Restart your Shadowsocks Clients Account"
		
	echo -e "Type [menu] to back menu option."
	}
function Addlimit_ss() {
	echo -e "Bandwidth limit for the port currently added"
	read -p "Enter the Port: " port
	read -p "Enter the [ 10000000000 (10GB-10ZERO) OR 1000000000000 (1tb-12ZERO) ]limit: " limit
	sudo iptables -I OUTPUT -p tcp --sport $port -j DROP
	sudo iptables -I OUTPUT -p tcp --sport $port -m quota --quota $limit -j ACCEPT
	echo -e "Successfully added limit to the port: $port"
	
	echo -e "Type [menu] to back menu option."
	}
function limit_ss() {
	sudo iptables -nvL -t filter --line-numbers
	echo -e "Type [menu] to back menu option."
	}
function removeportlimit_ss() {
	sudo iptables -nvL -t filter --line-numbers
	read -p "Enter the Chain num: " chain
	sudo iptables -D OUTPUT $chain
	sudo iptables -D OUTPUT $chain
	echo -e "Sucessfully remove the chain num: $chain and remove the limit to the port." 
	echo -e "Type [menu] to back menu option."
	}
function change_user_pass() {
read -p "Enter Username Who Changed Password: " username
egrep "^$username" /etc/passwd >/dev/null
if [ $? -eq 0 ]; then
read -p "Enter a new Password for the user $username: " password

clear
echo "Connecting to..."
sleep 0.5
echo "Change Password..."
sleep 0.5
  egrep "^$username" /etc/passwd >/dev/null
  echo -e "$password\n$password" | passwd $username
  clear
  echo " "
  echo "---------------------------------------"
  echo -e "Password for user ${blue}$username${NC} It has been successfully replaced."
  echo -e "Password for new user ${blue}$username${NC} is ${red}$password${NC}"
  echo "--------------------------------------"
  echo " "

else
echo -e "Username ${red}$username${NC} not found on your VPS"
exit 0
fi
echo -e "Thank you! Please type "menu" to back."
	}

function lock_account() {
	
	echo -e "$uname account has been lock"
	usermod -L $uname
	echo -e "Thank you! Please type "menu" to back."
	}

function unlock_account() {
	
	echo -e "$uname account has been unlock"
	usermod -U $uname
	echo - "Thank you! Please type "menu" to back."
	}
	
function generate_trial() {
#IP=`dig +short myip.opendns.com @resolver1.opendns.com`
uname=trial`</dev/urandom tr -dc X-Z0-9 | head -c4`
hari="1"
pass=`</dev/urandom tr -dc a-f0-9 | head -c9`

useradd -e `date -d "$hari days" +"%Y-%m-%d"` -s /bin/false -M $uname
echo -e "$pass\n$pass\n"|passwd $uname &> /dev/null
echo -e ""
echo -e "====Trial account info.===="
echo -e "Username: $uname"
echo -e "Password: $pass\n"
echo -e "==========================="
echo -e ""
echo -e "Type (menu) to back."
echo -e ""
}
function renew_user() {
	
	echo "New expiration date for $uname: $expdate...";
	usermod -e $expdate $uname
	echo "Thank you! Please type "menu" to back."
}
function check_ssh_user(){

data=( `ps aux | grep -i dropbear | awk '{print $2}'`);

echo "-----------------------";
echo "Checking Dropbear login";
echo "-----------------------";

for PID in "${data[@]}"
do
	#echo "check $PID";
	NUM=`cat /var/log/auth.log | grep -i dropbear | grep -i "Password auth succeeded" | grep "dropbear\[$PID\]" | wc -l`;
	USER=`cat /var/log/auth.log | grep -i dropbear | grep -i "Password auth succeeded" | grep "dropbear\[$PID\]" | awk '{print $10}'`;
	IP=`cat /var/log/auth.log | grep -i dropbear | grep -i "Password auth succeeded" | grep "dropbear\[$PID\]" | awk '{print $12}'`;
	if [ $NUM -eq 1 ]; then
		echo "$PID - $USER - $IP";
	fi
done

echo "";

data=( `ps aux | grep "\[priv\]" | sort -k 72 | awk '{print $2}'`);

echo "----------------------";
echo "Checking OpenSSH login";
echo "----------------------";

for PID in "${data[@]}"
do
        #echo "check $PID";
	NUM=`cat /var/log/auth.log | grep -i sshd | grep -i "Accepted password for" | grep "sshd\[$PID\]" | wc -l`;
	USER=`cat /var/log/auth.log | grep -i sshd | grep -i "Accepted password for" | grep "sshd\[$PID\]" | awk '{print $9}'`;
	IP=`cat /var/log/auth.log | grep -i sshd | grep -i "Accepted password for" | grep "sshd\[$PID\]" | awk '{print $11}'`;
        if [ $NUM -eq 1 ]; then
                echo "$PID - $USER - $IP";
        fi
done

echo "";

echo "------------------------------------------------"
echo " Multi Login = Kill "
echo " Usurname : Kill number PID "
echo "------------------------------------------------"

echo "";
echo -e "Type [menu] to back MENU OPTION."
echo "Mod by kikay001";

}
function delete_user(){
	userdel $uname
	
	echo "$uname Successfully Deleted"
	echo "Thank you! Please type "menu" to back."
}

function expired_users(){

	echo -e "Username Expired list:"
	cat /etc/shadow | cut -d: -f1,8 | sed /:$/d > /tmp/expirelist.txt
	totalaccounts=`cat /tmp/expirelist.txt | wc -l`
	for((i=1; i<=$totalaccounts; i++ )); do
		tuserval=`head -n $i /tmp/expirelist.txt | tail -n 1`
		username=`echo $tuserval | cut -f1 -d:`
		userexp=`echo $tuserval | cut -f2 -d:`
		userexpireinseconds=$(( $userexp * 86400 ))
		todaystime=`date +%s`
		if [ $userexpireinseconds -lt $todaystime ] ; then
			echo $username
		fi
	done
	rm /tmp/expirelist.txt
	
	echo ""
	echo "Thank you! Please type "menu" to back."
}

function not_expired_users(){
	echo -e "Username Not-Expired list:"
    cat /etc/shadow | cut -d: -f1,8 | sed /:$/d > /tmp/expirelist.txt
    totalaccounts=`cat /tmp/expirelist.txt | wc -l`
    for((i=1; i<=$totalaccounts; i++ )); do
        tuserval=`head -n $i /tmp/expirelist.txt | tail -n 1`
        username=`echo $tuserval | cut -f1 -d:`
        userexp=`echo $tuserval | cut -f2 -d:`
        userexpireinseconds=$(( $userexp * 86400 ))
        todaystime=`date +%s`
        if [ $userexpireinseconds -gt $todaystime ] ; then
            echo $username
        fi
    done
    	echo ""
	echo "Thank you! Please type "menu" to back."
	rm /tmp/expirelist.txt
		
}
function Auto_reboot(){
#!/bin/bash
if [ ! -e /usr/local/bin/reboot_otomatis ]; then
echo '#!/bin/bash' > /usr/local/bin/reboot_otomatis 
echo 'date=$(date +"%m-%d-%Y")' >> /usr/local/bin/reboot_otomatis 
echo 'time=$(date +"%T")' >> /usr/local/bin/reboot_otomatis 
echo 'echo "The server was successfully rebooted on $date at $time." >> /root/log-reboot.txt' >> /usr/local/bin/reboot_otomatis 
echo '/sbin/shutdown -r now' >> /usr/local/bin/reboot_otomatis 
chmod +x /usr/local/bin/reboot_otomatis
fi

echo "-------------------------------------------"
echo "Automatic Reboot System Menu"
echo "-------------------------------------------"
echo "1. Set Auto-Reboot 1 hour once"
echo "2. Set Auto-Reboot 6 hours once"
echo "3. Set Auto-Reboot 12 hours once"
echo "4. Set Auto-Reboot Once a Day"
echo "5. Set Auto-Reboot once a week"
echo "6. Set Auto-Reboot once a month"
echo "7. Turn Off Auto-Reboot"
echo "8. View log reboot"
echo "9. Clear log reboot"
echo "-------------------------------------------"
read -p "Write your Choices (numbers):" x

if test $x -eq 1; then
echo "10 * * * * root /usr/local/bin/reboot_otomatis" > /etc/cron.d/reboot_otomatis
echo "Auto-Reboot has been successfully set once an hour."
elif test $x -eq 2; then
echo "10 */6 * * * root /usr/local/bin/reboot_otomatis" > /etc/cron.d/reboot_otomatis
echo "Auto-Reboot has been successfully set 6 hours."
elif test $x -eq 3; then
echo "10 */12 * * * root /usr/local/bin/reboot_otomatis" > /etc/cron.d/reboot_otomatis
echo "Auto-Reboot has been successfully set up 12 hours."
elif test $x -eq 4; then
echo "10 0 * * * root /usr/local/bin/reboot_otomatis" > /etc/cron.d/reboot_otomatis
echo "Auto-Reboot has been successfully set once every day."
elif test $x -eq 5; then
echo "10 0 */7 * * root /usr/local/bin/reboot_otomatis" > /etc/cron.d/reboot_otomatis
echo "Auto-Reboot has been successfully set once a week."
elif test $x -eq 6; then
echo "10 0 1 * * root /usr/local/bin/reboot_otomatis" > /etc/cron.d/reboot_otomatis
echo "Auto-Reboot has been successfully set once a month."
elif test $x -eq 7; then
rm -f /etc/cron.d/reboot_otomatis
echo "Auto-Reboot has been switched off."
elif test $x -eq 8; then
if [ ! -e /root/log-reboot.txt ]; then
	echo "No reboot activity found yet"
	else 
	echo 'LOG REBOOT'
	echo "-------"
	cat /root/log-reboot.txt
fi
elif test $x -eq 9; then
echo "" > /root/log-reboot.txt
echo "Auto Reboot Log was deleted!"
else
echo "Options Not Available In Menu."
exit
fi

echo -e "Type menu to back Menu Option. Thank you!."
}
function used_data(){
	echo -e ""
	echo -e "Total Data Usage:"

	myip=`ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0' | head -n1`
	myint=`ifconfig | grep -B1 "inet addr:$myip" | head -n1 | awk '{print $1}'`
	ifconfig $myint | grep "RX bytes" | sed -e 's/ *RX [a-z:0-9]*/Received: /g' | sed -e 's/TX [a-z:0-9]*/\nTransfered: /g'
	
	echo ""
	echo "Thank you! Please type "menu" to back."
}

clear
sleep 0.5
echo "Connecting..."
sleep 0.5
screenfetch
echo "[--------------------Hainvenge--------------------]"
echo "[----------Welcome to kikay001 Autoscript --------]"
echo "[---------------Contact: 09126852632 -------------]"
echo "[Menu]"
PS3='Please enter number your choice [1-23]: '
options=("Shadowsock How to?"	
	 "Add/edit Shadowsocks account" 
	 "View the shadowsocks limit per port"
	 "Add limit on Shadowsocks port"
	 "Remove limit on Shadowsocks port"
	 "Restart Shadowsocks configuration" 
	 "Add OVPN account"
	 "Generate_trial for OVPN"
	 "User List for OVPN" 
	 "Change password for OVPN" 
	 "lock account for OVPN" 
	 "unlock account for OVPN" 
	 "Check ssh user list for OVPN" 
	 "Renew User for OVPN" 
	 "Delete User for OVPN" 
	 "Ram Status for OVPN" 
	 "Speedtest" 
	 "Refresh Squid" 
	 "Users Not Expired for OVPN"  
	 "Expired Users for OVPN" 
	 "Auto reboot"
	 "Used Data By Users" 
	 "Quit")
select opt in "${options[@]}"
do
    case $opt in
        
	 "Shadowsock How to?")
clear
echo -e ""
echo -e ""
echo -e ""
echo -e ""
echo "Connecting to..."
sleep 0.5
echo "Shadowsocks GUIDElines..."
sleep 0.5
echo -e "SHADOWSOCKS ACCOUNT HOW TO?"
echo -e ""
                echo -e "Do not delete any text just edit password"

echo -e ""
echo -e "ITO ANG MGA IBIBIGAY MO SA CLIENT MO."
echo -e "[IP]                   [PASS]            [PORT]         [ENCRYPTION MODE]"
echo -e "[139.XX.XX.XX]  [EDITMOTOPASWORD]     [9000-9015]     [AES-256-CFB,ORIGIN,PLAIN]"
echo -e ""
echo -e "1) WAG MO NA GALAWIN YANG MGA NAKIKITA MO SA JSON FOLDER "PASSWORD" LANG ANG EDIT MO WALA NG IBA."
echo -e ""
echo -e "2) PAG KATAPOS MO EDIT ANG PASSWORD CHECK MO YUNG KATAPAT NA PORT YUNG ANG KASAMANYA."
echo -e ""
echo -e "3) THEN GAWIN MO YUNG COMMAND "1" PARA MA-SAVE ANG GINAWA MO."
echo -e ""
echo -e "4) PARA MAKITA MO YUNG ILALIM PRESS MO LANG ARROW KEY TO MOVE UP-DOWN-LEFT-RIGHT"
echo -e ""
echo -e "5) YANG KULAY YELLOW GREEN ANG ARROW MO PARA MAKA PAG TYPE KA AT MA EDIT MO YUNG MGA TEXT."
echo -e ""
echo -e "6) PRESS DELETE TO REMOVE TEXT TAPAT MO YUNG ARROW KEY DOON SA TEXT NA EDIT MO."
echo -e ""
echo -e "7) PALITAN MO LANG YUNG PASSWORD QUOTED "editmoitopassword" dont remove the QUOTE."
echo -e ""
echo -e "8) PAG KA EXIT TYPE KA ULIT menu THEN PRESS 4 TO RESTART AND SHADOWSOCKS ACCOUNT WILL START CORRECTLY."
echo -e ""
echo -e "9) SA EXPIRATION MANUAL MO LISTA SA EXCEL OR NOTEPAD HINDI TO AUTOMATIC NA MERON EXPIRATION."
echo -e ""
echo -e "10)PAG EXPIRED NA ACCOUNT NG SHADOWSOCK CHANGE PASSWORD MO LANG."

echo -e ""
echo -e "*************shadowsocksjson folder COMMAND**************"
echo -e  "MOVE ARROW KEY TO EDIT TEXT'S [UP-DOWN-LEFT-RIGHT]"
echo -e "Command 1 to exit [ctrl+x] then press "Y" end hit enter"
echo -e ""
echo -e "To Start Edit, Add, create Password of port in shadowsocks choose number 3. Add SS account at menu option." 
echo -e ""
echo -e "*How to use shadowsocks account?"
echo -e "-Input the following info [IP-PASS-PORT-ENCRYPTION METHOD] to the SSCAP APP for PC, POSTERN APK for android, waterdrop for IOS"
echo -e "*Is this shadowsocks need promo to connect?"
echo -e "-NO!.. "
echo -e "*How to connect ?"
echo -e "Use CDC trick-Off/on modem or data-restarting phone or modem-airplain modem off/on"
echo -e "Kung meron kang atleast 2-3 SIM card use it alternately"
echo -e "Pahirapan na kasi sa pag connect." 
echo -e "PS. Alway use GLOBE OR TM SIM 4G only network! do not Recommend to 3G user."
echo -e ""
echo -e "Youtube TUT for sscap for pc link. https://youtu.be/p0pKxA520Hg credit to. AkosiShukimayi"
echo -e "Youtube TUT for postern android link. https://youtu.be/zsSWsZ9UwQg credit to. Ragside "
echo -e "Youtube TUT for waterdrop  IOS link. https://youtu.be/zSLb3qKetts credit to. VPN Philippines"
echo -e ""


echo "Thank you! Please type "menu" to back."
	    break
            ;;
	"Add/edit Shadowsocks account")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
            create_ss
	    break
            ;;
	"View the shadowsocks limit per port")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
	    limit_ss
	    break
	     ;;
	"Add limit on Shadowsocks port")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5	
	    Addlimit_ss
	    break
            ;;
	"Remove limit on Shadowsocks port")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
	    removeportlimit_ss
	    break
            ;;
	"Restart Shadowsocks configuration")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
	    restart_ss
	    break
            ;;
	"Add OVPN account")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
            create_user
	    break
            ;;
        "Generate_trial for OVPN")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
	      generate_trial
	      break
	      ;;   
    	"User List for OVPN")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
            /root/status
            break
	    ;;	
	"Change password for OVPN")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
             /root/status
	    change_user_pass
	    break
            ;;
	"lock account for OVPN")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
	    /root/status
	    read -p "What username you want Lock ?: " uname
	    lock_account
	    break
            ;;
	"unlock account for OVPN")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
	    /root/status
	    read -p "What username you want unLock ?: " uname
            unlock_account
	    break
            ;;
        "Renew User for OVPN")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
            read -p "Enter username to renew: " uname
            read -p "Enter expiry date (YYYY-MM-DD): " expdate
            renew_user
            break
            ;;
        "Delete User for OVPN")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
	    /root/status
            read -p "Enter username to be removed: " uname
            delete_user
            break
            ;;		
		
	"Check ssh user list for OVPN")
		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
           check_ssh_user
            break
            ;;	
	"Ram Status for OVPN")
			clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
		    free -h | grep -v + > /tmp/ramcache
            cat /tmp/ramcache | grep -v "Swap"
            break
            ;;	
	"Speedtest")
			clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
			./speedtest --share
			break
			;;
	"Refresh Squid")
			clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
			./refresh
			break
			;;
	"Users Not Expired for OVPN")
			clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
			not_expired_users
			break
			;;
	 "Expired Users for OVPN")
	 		clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
			expired_users
			break
			;;
	"Auto reboot")
			clear
			sleep 0.5
			echo "connecting..."
			sleep 0.5
			Auto_reboot
			break
			;;
	"Used Data By Users")
			used_data
			break
			;;
		"Quit")
            break
            ;;
	 *) echo invalid option;;
    esac
done
