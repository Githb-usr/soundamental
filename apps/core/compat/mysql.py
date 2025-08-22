# apps/core/compat/mysql.py
# Permet d'utiliser PyMySQL là où Django attend MySQLdb (mysqlclient).
try:
    import MySQLdb  # mysqlclient présent ? On ne fait rien.
except Exception:
    import pymysql
    pymysql.install_as_MySQLdb()
