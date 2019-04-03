export GIT_SSL_NO_VERIFY=1
git remote set-url origin git@git.ucsd.edu:mobagher/interview.git
git pull
echo "Last Pull on $(date)" > logfile.txt
