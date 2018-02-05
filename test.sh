rqalpha registerandpublishstrategy --uname xcl --sname test --account 665 --adminDB "E:\evilAlpha\rqalpha\alphaStar_mgr.db" --admin-passwd "123"
rqalpha registerandpublishfactor --uname xcl --fname "testFactor" --admin-passwd 123 --adminDB alphaStar_mgr.db

rqalpha callafactor -i 20170101 -e 20170131 --fname testFactor --adminDB "E:\evilAlpha\rqalpha\alphaStar_mgr.db" --sourcePath .\ipynbs\ --fDataPath "../test"
rqalpha callfactors -i 20170101 -e 20180201 --adminDB "E:\evilAlpha\rqalpha\alphaStar_mgr.db" --sourcePath .\ipynbs\ --fDataPath "../test"

rqalpha callastrategy --adminDB "E:\evilAlpha\rqalpha\alphaStar_mgr.db" --config "rqalpha\config_taskmgr.yml" --sname "testStrategy" -e 20170131 --sourcePath .\ipynbs\
rqalpha callstrategys --adminDB "E:\evilAlpha\rqalpha\alphaStar_mgr.db" --config "rqalpha\config_taskmgr.yml" -e 20180201 --sourcePath .\ipynbs\

rqalpha dailyprocess -i 20170101 -e 20180202 --adminDB ..\rqalpha\alphaStar_mgr.db --sourcePath .\ipynbs\ --config rqalpha\config_taskmgr.yml