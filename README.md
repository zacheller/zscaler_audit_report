# Description

Zscaler Internet Access audit report creates and downloads an audit log report in CSV format for the specified time frame (defaults to previous 24 hours).

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
