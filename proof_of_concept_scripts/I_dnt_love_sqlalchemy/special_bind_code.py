# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:59:32 2015

@author: bethanygarcia
"""

from flask_sqlalchemy import SQLAlchemy

class MySQLAlchemy(SQLAlchemy):
    def _execute_for_all_tables(self, app, bind, operation, **kwargs):
        app = self.get_app(app)

        if bind == '__all__':
            binds = [None] + list(app.config.get('SQLALCHEMY_BINDS') or ())
        elif isinstance(bind, basestring) or bind is None:
            binds = [bind]
        else:
            binds = bind

        for bind in binds:
            tables = self.get_tables_for_bind(bind)
            op = getattr(self.Model.metadata, operation)
            op(bind=self.get_engine(app, bind), tables=tables, **kwargs)

    def reflect(self, bind='__all__', app=None, **kwargs):
        self._execute_for_all_tables(app, bind, 'reflect', **kwargs)