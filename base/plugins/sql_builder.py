class SqlBuilder():

    def __init__(self):
        self._queryBuild = []


    def select(self, selectWhat):
        '''
        SqlBuilder().select('*')
        select('pid, user_id, user_name')
        '''

        self._queryBuild.append('SELECT {}'.format(selectWhat))
        return self


    def selectDistinct(self, selectWhat):
        '''
        SqlBuilder().select('*')
        select('pid, user_id, user_name')
        '''

        self._queryBuild.append('SELECT DISTINCT {}'.format(selectWhat))
        return self


    def fromTable(self, table):
        '''
        sql = SqlBuilder()
        sql.select('*').fromTable('category')
        => SELECT * FROM users

        sql.SqlBuilder().select('pid, user_id, user_name').fromTable('users').create()
        => SELECT pid, user_id, user_name FROM users
        '''

        self._queryBuild.append('FROM {}'.format(table))
        return self


    def create(self):
        '''
        sql = SqlBuilder()
        sql.select('*').fromTable('users').create()
        => SELECT * FROM users
        will return sql string and will flush and clear the sqlbuilder object
        '''

        query = ' '.join(self._queryBuild)
        self._queryBuild.clear()
        return query


    def where(self, where):
        '''
        sql = SqlBuilder()
        sql.select('*').fromTable('users').where('users.pid=1').crate()
        => SELECT * FROM users WHERE users.id=1
        '''

        self._queryBuild.append('WHERE {}'.format(where))
        return self


    def aNd(self, andWhere):
        '''
        sql = SqlBuilder()
        sql.select('*').fromTable('users').where('users.pid=1').aNd('users.name=\'{}\'.format('amru'))
        => SELECT * FROM users WHERE users.id=1 AND name='amru'
        '''

        self._queryBuild.append('AND {}'.format(andWhere))
        return self


    def oR(self, orWhere):
        '''
        sql = SqlBuilder()
        sql.select('*').fromTable('users').where('users.pid=1').oR('users.name=\'{}\''.format('amru'))
        => SELECT * FROM users WHERE users.id=1 OR name='amru'
        '''

        self._queryBuild.append('OR {}'.format(orWhere))
        return self


    def inSelect(self, inSelect):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.id=1').create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.id=1)
        '''

        self._queryBuild.append('IN ({})'.format(inSelect))
        return self


    def like(self, like):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.name').like('\'{}\''.format('ngetik')).create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.name LIKE 'ngetik')
        '''

        self._queryBuild.append('LIKE {}'.format(like))
        return self


    def notLike(self, notLike):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.name').notLike('\'{}\''.format('ngetik')).create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.name NOT LIKE 'ngetik')
        '''

        self._queryBuild.append('NOT LIKE {}'.format(notLike))
        return self


    def orderByDesc(self, orderBy):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.name').notLike('\'{}\''.format('ngetik')).create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).orderByDesc('users.name, users.id').create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.name NOT LIKE 'ngetik') ORDER BY sers.name, users.id DESC
        '''

        self._queryBuild.append('ORDER BY {} DESC'.format(orderBy))
        return self

    
    def orderByAsc(self, orderBy):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.name').notLike('\'{}\''.format('ngetik')).create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).orderByAsc('users.name, users.id').create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.name NOT LIKE 'ngetik') ORDER BY sers.name, users.id ASC
        '''

        self._queryBuild.append('ORDER BY {} ASC'.format(orderBy))
        return self


    def limit(self, limit):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.name').notLike('\'{}\''.format('ngetik')).create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).orderByAsc('users.name, users.id').limit(1).create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.name NOT LIKE 'ngetik') ORDER BY sers.name, users.id ASC LIMIT 1
        '''

        self._queryBuild.append('LIMIT {}'.format(limit))
        return self


    def limitWithOffset(self, limit, offset):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.name').notLike('\'{}\''.format('ngetik')).create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).orderByAsc('users.name, users.id').limitWithOffset(1, 0).create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.name NOT LIKE 'ngetik') ORDER BY sers.name, users.id ASC LIMIT 1 OFFSET 0
        '''

        self._queryBuild.append('LIMIT {} OFFSET {}'.format(limit, offset))
        return self


    def groupBy(self, groupBy):
        '''
        sql = SqlBuilder()
        sql.select('COUNT(job.uid) AS total_job, job.uid').fromTable('job').groupBy('job.uid').create()
        => SELECT COUNT(job.uid) AS total_job FROM job GROUP BY job.uid
        '''

        self._queryBuild.append('GROUP BY {}'.format(groupBy))
        return self


    def innerJoin(self, table, innerJoinOn):
        '''
        sql = SqlBuilder()
        sql.select('users.name, job.name, users.id').fromTable('job').innerJoin('users', 'users.id=job.uid').create()
        => SELECT users.name, job.name, users.id FROM job INNER JOIN users ON users.id=job.uid
        '''

        self._queryBuild.append('INNER JOIN {} ON {}'.format(table, innerJoinOn))
        return self


    def join(self, table, joinOn):
        '''
        sql = SqlBuilder()
        sql.select('users.name, job.name, users.id').fromTable('job').Join('users', 'users.id=job.uid').create()
        => SELECT users.name, job.name, users.id FROM job JOIN users ON users.id=job.uid
        '''

        self._queryBuild.append('JOIN {} ON {}'.format(table, joinOn))
        return self


    def leftJoin(self, table, leftJoinOn):
        '''
        sql = SqlBuilder()
        sql.select('users.name, job.name, users.id').fromTable('job').leftJoin('users', 'users.id=job.uid').create()
        => SELECT users.name, job.name, users.id FROM job LEFT JOIN users ON users.id=job.uid
        '''

        self._queryBuild.append('LEFT JOIN {} ON {}'.format(table, leftJoinOn))
        return self


    def rightJoin(self, table, rightJoinOn):
        '''
        sql = SqlBuilder()
        sql.select('users.name, job.name, users.id').fromTable('job').rightJoin('users', 'users.id=job.uid').create()
        => SELECT users.name, job.name, users.id FROM job RIGHT JOIN users ON users.id=job.uid
        '''

        self._queryBuild.append('RIGHT JOIN {} ON {}'.format(table, rightJoinOn))
        return self
        