# HR 데이터베이스에서 필요한 SQL 작업 처리 모듈
import pymysql
import pymysql.cursors

class HRDao:
    SELECT_STATEMENT = "SELECT e.emp_id, e.emp_name, d.dept_name, j.job_title, e.hire_date, concat('$',format(e.salary, 0)) as salary"
    def __init__(self, host:str, port:int, user:str, password:str, db:str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db=db
        self.join_sql = """"""

    def get_connection(self) -> pymysql.Connection:
        return pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db)
    
    def select_job(self):
        """
        업무 조회 메소드
        return tuple[job_id, job_name]
        """
        sql = "SELECT job_id, job_title FROM job ORDER BY job_title"
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()

    def select_dept(self):
        """
        부서조회 메소드
        return tuple[dept_id, dept_name, loc]
        """
        sql = "SELECT dept_id, dept_name, loc FROM dept ORDER BY dept_name"
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
            
    def select_emp_by_job(self, job_id:str):
        """
        업무명을 조건으로 직원 조회
        return list[dict{column명:value}]
        """
        # job_id가 없는 직원은 나오면 안된다. 그래서 inner join. 소속 부서가 없더라도 대상 job_id를 담당 직원은 나와야 하므로 dept와는 left outer join
        sql = f"""
        {HRDao.SELECT_STATEMENT}
        FROM emp e JOIN job j ON e.job_id = j.job_id LEFT JOIN dept d ON e.dept_id = d.dept_id 
        WHERE e.job_id = %s ORDER BY e.emp_id
        """
        with self.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor: # DataFrame 생성 하기 위해 DictCursor 사용
                cursor.execute(sql, [job_id])
                return cursor.fetchall()

    def select_emp_by_dept(self, dept_id:str):
        """
        부서명을 조건으로 직원 조회
        return list[dict{column명:value}]
        """
        # dept_id가 없는 직원은 나오면 안된다. 그래서 inner join. job_id가 없더라도 대상 dept_id의 직원은 나와야 하므로 dept와는 left outer join
        sql = f"""
        {HRDao.SELECT_STATEMENT}
        FROM emp e JOIN dept d ON e.dept_id = d.dept_id LEFT JOIN job j ON e.job_id = j.job_id
        WHERE e.dept_id = %s ORDER BY e.emp_id
        """
        with self.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, [dept_id])
                return cursor.fetchall()

    def select_all_emp(self):
        """
        모든 직원 조회
        return list[dict{column명:value}]
        """
        sql = f"""
        {HRDao.SELECT_STATEMENT}
        FROM emp e left JOIN dept d ON e.dept_id = d.dept_id LEFT JOIN job j ON e.job_id = j.job_id
        ORDER BY e.emp_id
        """
        with self.get_connection() as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
            

if __name__ == "__main__":
    from pprint import pprint
    import pandas as pd

    dao = HRDao("127.0.0.1", 3306, "scott", "tiger", "hr")
    print(dao.select_job())
    # print(dao.select_dept())
    # print(pd.DataFrame(dao.select_emp_by_job('FI_ACCOUNT')))
    # print(pd.DataFrame(dao.select_emp_by_dept('10')))
    # df = pd.DataFrame(dao.select_all_emp())
    # print(df.shape)
