# Description

Zscaler Internet Access audit report creates and downloads an audit log report in csv format  for the specified time. 
By default from last 24 hours since the script was executed

# Installation ( Virtual Environment)
```
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
```

# usage
```
python zs_audit_report -h
```
```
python zs_audit_report -5 -a APIKEY -u USER -p PASSWORD  -c CLOUD -rlog IP:PROTOCOL:PORT
python zs_audit_report -24 -a APIKEY -u USER -p PASSWORD  -c CLOUD -rlog IP:PROTOCOL:PORT

```
# Docker instructions
```
docker build -t audit .  
docker run -it audit bash
python app -h
```
# Credits
```
Sergio Pereira 
Zscaler Professional Services
```
