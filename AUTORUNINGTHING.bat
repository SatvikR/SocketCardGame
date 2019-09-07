gnome-terminal -e "python3 NotMyWork.py 127.0.0.1 12345"

echo Enter the number of clients you would like to have into the newly opened python file. Then enter the same number here.

read LOL

for i in {1.."$LOL"}
do
gnome-terminal -e "python3 ThisIsDefinetlyNotMyWork.py 127.0.0.1 12345"
done

