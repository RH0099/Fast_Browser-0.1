#system update 

pkg update -y && apt upgrade -y


pkg install python3
pkg instoll python3-pip
pkg instoll git -y 
pkg instoll aria2
pkg instoll rclone 
pkg instoll curl

# Clone CloudHunterX
git clone https://github.com/cloudhunterx/engine.git
cd engine

# Install Python deps
pip install -r requirements.txt

# Configure rclone (optional)
rclone config
