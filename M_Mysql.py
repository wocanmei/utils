#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql.cursors


class W_Mysql:
    def __init__(self, host,port,user,pw,db,charset='utf8'):
        try:
            self.__conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                passwd=pw,
                db=db,
                charset=charset,
                cursorclass=pymysql.cursors.DictCursor)
            self.connected = True

            self._select_one_offset=0
            self._select_one_inquery=''
            
            self._select_more_inquery=''
            self._select_more_offset=0

        except pymysql.Error as e:
            print('mysql connection error :{}'.format(e), end='')

    def insert(self, table:str, values:dict):
        sql_top = 'insert into ' + table + ' ('
        sql_tail = ') values ('
        try:
            for key, val in values.items():
                sql_top += key + ','
                sql_tail += '"'+val+'"' + ','
            sql = sql_top[:-1] + sql_tail[:-1] + ')'
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return self.__conn.insert_id()
        except pymysql.Error as e:
            print('insert error:{}'.format(e))
            self.__conn.rollback()
            return False

    def update(self, table:str, values:dict, condition:str):
        sql = 'update ' + table + ' set '
        try:
            for key, val in values.items():
                sql += key + '="' + val + '",'
            sql = sql[:-1] + ' where ' + condition
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.rowcount
        except pymysql.Error as e:
            print('update error:{}'.format(e))
            self.__conn.rollback()
            return False

    def delete(self, table:str, condition:str):
        sql = 'delete from ' + table + ' where ' + condition
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.rowcount
        except pymysql.Error as e:
            print('delete data error:{}'.format(e))
            self.__conn.rollback()
            return False

    def select_one(self, table:str, condition:str, offset:int=0,field:str='*',reset=False):
        if(reset):
            self._select_one_offset=offset
        
        inquey_hash='{}_{}_{}'.format(table,condition,offset)
        if(inquey_hash!=self._select_one_inquery):
            self._select_one_offset=offset
            self._select_one_inquery=inquey_hash

        sql = 'select ' + field + ' from ' + table + ' where ' + condition +' limit 1 '+' offset '+ str(self._select_one_offset)
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            self._select_one_offset+=1
            return cursor.fetchall()[0]
        except pymysql.Error as e:
            print('selct error:{}'.format(e))
            return False

    def select_more(self, table:str, condition:str,limit:int, offset:int=0,field:str='*',reset=False):
        if(reset):
            self._select_more_offset=offset
        
        inquey_hash='{}_{}_{}'.format(table,condition,offset)
        if(inquey_hash!=self._select_more_inquery):
            self._select_more_offset=offset
            self._select_more_inquery=inquey_hash

        sql = 'select ' + field + ' from ' + table + ' where ' + condition+' limit '+str(limit)+' offset '+ str(self._select_more_offset)
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            self._select_more_offset+=limit
            return cursor.fetchall()
        except pymysql.Error as e:
            print('selct error:{}'.format(e))
            return False

    def select_all(self, table:str, condition:str,field:str='*'):
        sql = 'select ' + field + ' from ' + table + ' where ' + condition
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()
        except pymysql.Error as e:
            print('selct all error:{}'.format(e))
            return False

    def count(self, table:str, condition:str='1'):
        sql = 'SELECT count(*)res FROM ' + table + ' WHERE ' + condition
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()[0]['res']
        except pymysql.Error as e:
            print('count error:{}'.format(e))
            return False

    def sum(self, table:str, field:str, condition:str='1'):
        sql = 'SELECT SUM(' + field + ') AS res FROM ' + table + ' WHERE ' + condition
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()[0]['res']
        except pymysql.Error as e:
            print('count error:{}'.format(e))
            return False


    def execute(self,sql:str):
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()
        except pymysql.Error as e:
            print('execute mysql error:{}'.format(e))
            return False


    def __del__(self):
        try:
            self.__conn.close()
        except pymysql.Error as e:
            print('close mysql error:{}'.format(e))

    def close(self):
        self.__del__()