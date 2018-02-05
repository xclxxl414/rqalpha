python -m rqalpha.__main__  run -f ipynbs\testStrategy.ipynb -s 20170101 -e 20170131 -d ..\bundle\ --config rqalpha\config.yml -mc sys_analyser.plot True

python -m rqalpha.mod.rqalpha_mod_alphaStar_mgr.test registerandpublishstrategy --uname xcl --sname test --account 665 --adminDB "E:\evilAlpha\rqalpha\alphaStar_mgr.db" --admin-passwd "123"
rqalpha registerandpublishfactor --uname xcl --fname "testFactor" --admin-passwd 123 --adminDB alphaStar_mgr.db

python -m rqalpha.mod.rqalpha_mod_alphaStar_mgr.__init__ callafactor -s 20170101 -e 20170131 --fname testFactor --adminDB "E:\evilAlpha\rqalpha\alphaStar_mgr.db" --sourcePath .\ipynbs\ --fDataPath "../test"
python -m rqalpha.mod.rqalpha_mod_alphaStar_mgr.__init__ callfactors -s 20170101 -e 20180201 --adminDB "E:\evilAlpha\rqalpha\alphaStar_mgr.db" --sourcePath .\ipynbs\ --fDataPath "../test"

python -m rqalpha.mod.rqalpha_mod_alphaStar_mgr.__init__ callastrategy --adminDB "E:\evilAlpha\rqalpha\alphaStar_mgr.db" --config "rqalpha\config_taskmgr.yml" --sname "testStrategy" -e 20170131 --tgw-account 665 - -sourcePath .\ipynbs\

python -m rqalpha.mod.rqalpha_mod_alphaStar_mgr.__init__ callstrategys --adminDB "E:\evilAlpha\rqalpha\alphaStar_mgr.db" --config "rqalpha\config_taskmgr.yml" -e 20180201 --tgw-account 665 --sourcePath .\ipynbs\