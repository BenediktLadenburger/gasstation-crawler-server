# !/bin/bash
#
BRed='\033[1;31m'         # Red
BGreen='\033[1;32m'       # Green
BBlue='\033[1;34m'        # Blue
BPurple='\033[1;35m'      # Purple
BWhite='\033[1;37m'       # White
Color_Off='\033[0m'       # Text Reset
NC='\033[0m' # No Color

_info="${BBlue}==>${NC}"
_info2="${BBlue}====>${NC}"
_cmd="${BGreen}==>${NC}"
_cmd2="${BGreen}====>${NC}"


printf "${_info}${BWhite} checking virtual environment\n${NC}"
VENV_DIR=${2:-./venv/}
if [ -d "${VENV_DIR}" ]; then
    printf "${_info2} Python virtual environment ${VENV_DIR} already exists.\n"
else
    printf "${_cmd2} ${BWhite}Creating virtual environment ${NC}${VENV_DIR}\n"
    python -m venv ${VENV_DIR}
fi

printf "${_cmd2} activating virtual environment ${NC}${VENV_DIR}bin/activate\n"
source "${VENV_DIR}/bin/activate"


printf "\n\n${_cmd2} ${BWhite}executing ${NC}pip install \n"
printf "\n${BGreen}============ "
printf "${BWhite}$pip requirements.txt ${BGreen}"
printf "============${NC} \n"
while IFS= read -r LINE; do
    pip install "$LINE"
done < "./requirements.txt"
printf "${BGreen}=====================================${NC}"
printf "${BGreen}=====================================${NC} \n"


printf "\n\n${_info}${BWhite} loading environment variables\n${NC}"
printf "${_cmd2}${BWhite} exporting ${NC}.env values\n"
while IFS= read -r LINE; do
    export "$LINE"
done < ".env"
printf "${_cmd2}${BWhite} executing ${NC}py.load_env()\n"
python ./src/helpers/load_env.py

printf "\n\n${_cmd} ${BWhite}initializing database${NC} ${DATABASE_PATH}\n"
python ./src/helpers/init_db.py

printf "\n\n${BGreen}==> ${BWhite}stopping screens${NC}\n"
./src/helpers/kill_screens.sh

printf "\n${_cmd} ${BWhite}starting${NC} api-server \n"
printf "${_cmd2} ${BWhite}creating screen${NC} 'crawler-api'"
screen -S crawler-api -d -m -- sh -c "python ./src/flask-api/main.py"
# python ./src/flask-api/main.py

printf "\n${_cmd2} server starting "
for ((i=1; i<=15; i++)); do
    printf "${BGreen}...${NC}"
    sleep 0.05
done

printf "\n\n${BGreen}========== GET -- /health_check  ==========${NC}\n"
curl -i  -X GET http://${API_IP_ADDRESS}:${API_PORT}/health_check
printf "\n${BGreen}=========================================== ${NC}\n"


printf "\n${_cmd} ${BWhite}starting crawler${NC}"
printf "\n${_cmd2} ${BWhite}creating screen${NC} 'crawler'"
# screen -S crawler -d -m -- sh -c 'python ./src/crawler/main.py'
python './src/crawler/main.py'


printf "\n\n${_info} ${BPurple}Done!${NC}"
printf "\n${_info2} ${BWhite}You may check on your processes here:\n${NC}"
screen -ls
