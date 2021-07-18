# ansible_mongo
playbook ansible para instalação do mongo db
Maiores detalhes em: 
(https://hsoaress.wordpress.com/2019/11/02/instalando-mongodb-com-ansible/ )

## Requisitos minimos para reproducao dessa role
1 disco de 10GB para dados
1 discos de 10GB para indice

## Ambiente em que foi testado
Oracle Linux Server 7.6
1GB memória

## Pendente
Para melhorar a performance, devemos separar o diretório de dados, do diretório de indice.

Por esse motivo, foi criado o diretório /mongo_index, porém a movimentação está manual, não consta ainda no playbook.


Os passos para movimentação são:

1. Parar o banco de dados
2. Criar mesma estrutura de diretórios de banco de dados em /mongo_index
3. Entrar dentro de cada diretório de banco de dados em /mongo_data/banco_de_dados e mover a pasta de index para /mongo_index/banco_de_dados/
4. Criar link simbolico de /mongo_index/banco_de_dados/ para /mongo_data/banco_de_dados/
5. Iniciar o banco de dados novamente

Exemplo dos passos citados acima:

1- 
```command
[root@imagemol7 ~]# service mongod stop
Redirecting to /bin/systemctl stop mongod.service
```

2-
```command
[root@imagemol7 ~]# cd /mongo_data/
[root@imagemol7 mongo_data]# ls -ltr
total 108
-rw-------. 1 mongod mongod    21 Nov  3 14:23 WiredTiger.lock
-rw-------. 1 mongod mongod    47 Nov  3 14:23 WiredTiger
drwx------. 2 mongod mongod  4096 Nov  3 14:23 journal
-rw-------. 1 mongod mongod   114 Nov  3 14:23 storage.bson
drwx------. 4 mongod mongod    37 Nov  3 14:23 admin
drwx------. 4 mongod mongod    37 Nov  3 14:23 local
drwx------. 4 mongod mongod    37 Nov  3 14:23 config
drwx------. 2 mongod mongod    48 Nov  3 14:32 diagnostic.data
-rw-------. 1 mongod mongod  4096 Nov  3 14:32 WiredTigerLAS.wt
-rw-------. 1 mongod mongod 20480 Nov  3 14:32 sizeStorer.wt
-rw-------. 1 mongod mongod 20480 Nov  3 14:32 _mdb_catalog.wt
-rw-------. 1 mongod mongod 45056 Nov  3 14:32 WiredTiger.wt
-rw-------. 1 mongod mongod  1186 Nov  3 14:32 WiredTiger.turtle
-rw-------. 1 mongod mongod     0 Nov  3 14:32 mongod.lock
[root@imagemol7 mongo_data]# 
[root@imagemol7 mongo_data]# 
[root@imagemol7 mongo_data]# mkdir -p /mongo_index/{admin,local,config}
[root@imagemol7 mongo_data]# ls -ltr /mongo_index/
total 0
drwxr-xr-x. 2 root root 6 Nov  3 14:33 admin
drwxr-xr-x. 2 root root 6 Nov  3 14:33 local
drwxr-xr-x. 2 root root 6 Nov  3 14:33 config
```

3-
```command
[root@imagemol7 mongo_data]# mv admin/index/ /mongo_index/admin/
[root@imagemol7 mongo_data]# mv local/index/ /mongo_index/local/
[root@imagemol7 mongo_data]# mv config/index/ /mongo_index/config/
[root@imagemol7 mongo_data]# ls -ltr /mongo_index/*
/mongo_index/admin:
total 0
drwx------. 2 mongod mongod 39 Nov  3 14:23 index

/mongo_index/local:
total 0
drwx------. 2 mongod mongod 39 Nov  3 14:23 index

/mongo_index/config:
total 0
drwx------. 2 mongod mongod 72 Nov  3 14:23 index
[root@imagemol7 mongo_data]# 
```

4-
```command
[root@imagemol7 mongo_data]# ln -s /mongo_index/admin/index/ /mongo_data/admin/index
[root@imagemol7 mongo_data]# ln -s /mongo_index/local/index/ /mongo_data/local/index
[root@imagemol7 mongo_data]# ln -s /mongo_index/config/index/ /mongo_data/config/index

/mongo_data/admin:
total 0
drwx------. 2 mongod mongod 39 Nov  3 14:23 collection
lrwxrwxrwx. 1 root   root   25 Nov  3 14:36 index -> /mongo_index/admin/index/

/mongo_data/local:
total 0
drwx------. 2 mongod mongod 39 Nov  3 14:23 collection
lrwxrwxrwx. 1 root   root   25 Nov  3 14:36 index -> /mongo_index/local/index/

/mongo_data/config:
total 0
drwx------. 2 mongod mongod 39 Nov  3 14:23 collection
lrwxrwxrwx. 1 root   root   26 Nov  3 14:36 index -> /mongo_index/config/index/
```

5- 
```command
[root@imagemol7 ~]# service mongod start
Redirecting to /bin/systemctl start mongod.service
```