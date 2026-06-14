"""
ScoreDAO - 成绩数据访问对象
实现成绩的增删改查功能
"""

from dao.db import DBConnection, DB_CONFIG
from typing import Optional, Dict, Any, List


class ScoreDAO:
    """
    成绩数据访问对象

    职责:
    - 成绩录入（插入）
    - 成绩修改（更新）
    - 成绩删除
    - 按学生查询成绩
    - 查询所有成绩
    - 成绩统计
    """

    def __init__(self, db_config: Optional[Dict[str, Any]] = None):
        """
        初始化ScoreDAO

        Args:
            db_config: 数据库配置字典
        """
        self.db_config = db_config or DB_CONFIG

    def insert_score(
        self,
        student_id: int,
        subject_id: int,
        daily_score: Optional[float] = None,
        midterm_score: Optional[float] = None,
        final_score: Optional[float] = None,
        total_score: float = 0.0,
        gpa_point: Optional[float] = None,
        input_by: int = 0
    ) -> int:
        """
        插入成绩记录

        Args:
            student_id: 学生ID
            subject_id: 科目ID
            daily_score: 平时成绩
            midterm_score: 期中成绩
            final_score: 期末成绩
            total_score: 总评成绩
            gpa_point: 绩点
            input_by: 录入人ID

        Returns:
            int: 影响行数
        """
        with DBConnection(**self.db_config) as db:
            sql = """
                INSERT INTO score 
                (student_id, subject_id, daily_score, midterm_score, final_score, 
                 total_score, gpa_point, status, input_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                student_id, subject_id, daily_score, midterm_score, final_score,
                total_score, gpa_point, 'submitted', input_by
            )
            return db.execute_update(sql, params)

    def update_score(
        self,
        score_id: int,
        daily_score: Optional[float] = None,
        midterm_score: Optional[float] = None,
        final_score: Optional[float] = None,
        total_score: Optional[float] = None,
        gpa_point: Optional[float] = None,
        status: Optional[str] = None
    ) -> int:
        """
        更新成绩记录

        Args:
            score_id: 成绩ID
            daily_score: 平时成绩
            midterm_score: 期中成绩
            final_score: 期末成绩
            total_score: 总评成绩
            gpa_point: 绩点
            status: 状态

        Returns:
            int: 影响行数
        """
        with DBConnection(**self.db_config) as db:
            # 构建动态SQL
            fields = []
            params = []

            if daily_score is not None:
                fields.append("daily_score = %s")
                params.append(daily_score)
            if midterm_score is not None:
                fields.append("midterm_score = %s")
                params.append(midterm_score)
            if final_score is not None:
                fields.append("final_score = %s")
                params.append(final_score)
            if total_score is not None:
                fields.append("total_score = %s")
                params.append(total_score)
            if gpa_point is not None:
                fields.append("gpa_point = %s")
                params.append(gpa_point)
            if status is not None:
                fields.append("status = %s")
                params.append(status)

            if not fields:
                return 0

            sql = f"UPDATE score SET {', '.join(fields)} WHERE score_id = %s"
            params.append(score_id)

            return db.execute_update(sql, tuple(params))

    def delete_score(self, score_id: int) -> int:
        """
        删除成绩记录

        Args:
            score_id: 成绩ID

        Returns:
            int: 影响行数
        """
        with DBConnection(**self.db_config) as db:
            sql = "DELETE FROM score WHERE score_id = %s"
            return db.execute_update(sql, (score_id,))

    def query_by_student(self, student_id: int) -> List[Dict[str, Any]]:
        """
        按学生ID查询成绩（含科目名称）

        Args:
            student_id: 学生ID

        Returns:
            List[Dict]: 成绩列表
        """
        with DBConnection(**self.db_config) as db:
            sql = """
                SELECT 
                    sc.score_id,
                    sc.student_id,
                    st.name as student_name,
                    sc.subject_id,
                    sub.name as subject_name,
                    sub.credit,
                    sc.daily_score,
                    sc.midterm_score,
                    sc.final_score,
                    sc.total_score,
                    sc.gpa_point,
                    sc.status,
                    sc.input_time
                FROM score sc
                JOIN student st ON sc.student_id = st.student_id
                JOIN subject sub ON sc.subject_id = sub.subject_id
                WHERE sc.student_id = %s
                ORDER BY sub.subject_id
            """
            return db.execute_query(sql, (student_id,))

    def query_by_subject(self, subject_id: int) -> List[Dict[str, Any]]:
        """
        按科目ID查询成绩（含学生姓名）

        Args:
            subject_id: 科目ID

        Returns:
            List[Dict]: 成绩列表
        """
        with DBConnection(**self.db_config) as db:
            sql = """
                SELECT 
                    sc.score_id,
                    sc.student_id,
                    st.name as student_name,
                    st.class_name,
                    sc.subject_id,
                    sub.name as subject_name,
                    sc.daily_score,
                    sc.midterm_score,
                    sc.final_score,
                    sc.total_score,
                    sc.gpa_point,
                    sc.status
                FROM score sc
                JOIN student st ON sc.student_id = st.student_id
                JOIN subject sub ON sc.subject_id = sub.subject_id
                WHERE sc.subject_id = %s
                ORDER BY sc.total_score DESC
            """
            return db.execute_query(sql, (subject_id,))

    def query_all(self) -> List[Dict[str, Any]]:
        """
        查询所有成绩记录（含学生和科目信息）

        Returns:
            List[Dict]: 成绩列表
        """
        with DBConnection(**self.db_config) as db:
            sql = """
                SELECT 
                    sc.score_id,
                    sc.student_id,
                    st.name as student_name,
                    st.class_name,
                    sc.subject_id,
                    sub.name as subject_name,
                    sub.credit,
                    sc.daily_score,
                    sc.midterm_score,
                    sc.final_score,
                    sc.total_score,
                    sc.gpa_point,
                    sc.status,
                    sc.input_time
                FROM score sc
                JOIN student st ON sc.student_id = st.student_id
                JOIN subject sub ON sc.subject_id = sub.subject_id
                ORDER BY st.name, sub.name
            """
            return db.execute_query(sql)

    def query_by_id(self, score_id: int) -> Optional[Dict[str, Any]]:
        """
        按成绩ID查询单条记录

        Args:
            score_id: 成绩ID

        Returns:
            Dict: 成绩信息，None表示不存在
        """
        with DBConnection(**self.db_config) as db:
            sql = """
                SELECT 
                    sc.*,
                    st.name as student_name,
                    sub.name as subject_name
                FROM score sc
                JOIN student st ON sc.student_id = st.student_id
                JOIN subject sub ON sc.subject_id = sub.subject_id
                WHERE sc.score_id = %s
            """
            result = db.execute_query(sql, (score_id,))
            return result[0] if result else None

    def get_statistics_by_subject(self, subject_id: int) -> Optional[Dict[str, Any]]:
        """
        获取某科目的成绩统计信息

        Args:
            subject_id: 科目ID

        Returns:
            Dict: 统计信息（平均分、最高分、最低分、及格率等）
        """
        with DBConnection(**self.db_config) as db:
            sql = """
                SELECT 
                    COUNT(*) as total_count,
                    ROUND(AVG(total_score), 2) as avg_score,
                    MAX(total_score) as max_score,
                    MIN(total_score) as min_score,
                    SUM(CASE WHEN total_score >= 60 THEN 1 ELSE 0 END) as pass_count,
                    ROUND(SUM(CASE WHEN total_score >= 60 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pass_rate
                FROM score
                WHERE subject_id = %s AND status = 'approved'
            """
            result = db.execute_query(sql, (subject_id,))
            return result[0] if result else None

    def get_student_gpa(self, student_id: int) -> Optional[float]:
        """
        计算学生的平均绩点GPA

        Args:
            student_id: 学生ID

        Returns:
            float: 平均绩点
        """
        with DBConnection(**self.db_config) as db:
            sql = """
                SELECT ROUND(AVG(gpa_point), 2) as avg_gpa
                FROM score
                WHERE student_id = %s AND status = 'approved'
            """
            result = db.execute_query(sql, (student_id,))
            return result[0]['avg_gpa'] if result and result[0]['avg_gpa'] else 0.0
