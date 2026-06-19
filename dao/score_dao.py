"""
ScoreDAO - 成绩数据访问对象
实现成绩的增删改查功能
"""

from dao.db import DBConnection
from config import Config
from constants import ScoreStatus, ValidationRules, ScoreCalculation, ErrorMessage
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


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
            db_config: 数据库配置字典，若不提供则使用默认配置
        """
        self.db_config = db_config or Config.get_db_config()

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
            int: 影响行数，0表示插入失败
        """
        # 输入验证
        if not self._validate_score_inputs(daily_score, midterm_score, final_score):
            logger.error(f"成绩数据验证失败: daily={daily_score}, midterm={midterm_score}, final={final_score}")
            return 0

        if student_id <= 0 or subject_id <= 0:
            logger.error(f"无效的学生ID或科目ID: student_id={student_id}, subject_id={subject_id}")
            return 0

        with DBConnection(**self.db_config) as db:
            sql = """
                INSERT INTO score 
                (student_id, subject_id, daily_score, midterm_score, final_score, 
                 total_score, gpa_point, status, input_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                student_id, subject_id, daily_score, midterm_score, final_score,
                total_score, gpa_point, ScoreStatus.SUBMITTED, input_by
            )
            affected_rows = db.execute_update(sql, params)
            if affected_rows > 0:
                logger.info(f"成绩已录入: student_id={student_id}, subject_id={subject_id}")
            else:
                logger.error(f"成绩录入失败: student_id={student_id}, subject_id={subject_id}")
            return affected_rows

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
            status: 状态（使用 ScoreStatus 中定义的常量）

        Returns:
            int: 影响行数，0表示无更新或失败
        """
        # 输入验证
        if score_id <= 0:
            logger.error(f"无效的成绩ID: {score_id}")
            return 0

        if not self._validate_score_inputs(daily_score, midterm_score, final_score):
            logger.error(f"成绩数据验证失败: daily={daily_score}, midterm={midterm_score}, final={final_score}")
            return 0

        if status and status not in ScoreStatus.ALL_STATUSES:
            logger.error(f"无效的成绩状态: {status}")
            return 0

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
                logger.warning(f"没有要更新的字段: score_id={score_id}")
                return 0

            sql = f"UPDATE score SET {', '.join(fields)} WHERE score_id = %s"
            params.append(score_id)

            affected_rows = db.execute_update(sql, tuple(params))
            if affected_rows > 0:
                logger.info(f"成绩已更新: score_id={score_id}")
            else:
                logger.warning(f"成绩更新失败或无记录: score_id={score_id}")
            return affected_rows

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
        if subject_id <= 0:
            logger.error(f"无效的科目ID: {subject_id}")
            return None

        with DBConnection(**self.db_config) as db:
            sql = f"""
                SELECT 
                    COUNT(*) as total_count,
                    ROUND(AVG(total_score), 2) as avg_score,
                    MAX(total_score) as max_score,
                    MIN(total_score) as min_score,
                    SUM(CASE WHEN total_score >= {ScoreCalculation.PASS_SCORE} THEN 1 ELSE 0 END) as pass_count,
                    ROUND(SUM(CASE WHEN total_score >= {ScoreCalculation.PASS_SCORE} THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pass_rate
                FROM score
                WHERE subject_id = %s AND status = %s
            """
            result = db.execute_query(sql, (subject_id, ScoreStatus.APPROVED))
            if result:
                logger.info(f"获取科目统计信息: subject_id={subject_id}")
                return result[0]
            else:
                logger.warning(f"未获取到科目统计信息: subject_id={subject_id}")
                return None

    def get_student_gpa(self, student_id: int) -> Optional[float]:
        """
        计算学生的平均绩点GPA

        Args:
            student_id: 学生ID

        Returns:
            float: 平均绩点
        """
        if student_id <= 0:
            logger.error(f"无效的学生ID: {student_id}")
            return 0.0

        with DBConnection(**self.db_config) as db:
            sql = f"""
                SELECT ROUND(AVG(gpa_point), 2) as avg_gpa
                FROM score
                WHERE student_id = %s AND status = %s
            """
            result = db.execute_query(sql, (student_id, ScoreStatus.APPROVED))
            if result and result[0]['avg_gpa']:
                logger.info(f"获取学生GPA: student_id={student_id}")
                return result[0]['avg_gpa']
            else:
                logger.warning(f"未获取到学生GPA数据: student_id={student_id}")
                return 0.0

    @staticmethod
    def _validate_score_inputs(
        daily_score: Optional[float] = None,
        midterm_score: Optional[float] = None,
        final_score: Optional[float] = None
    ) -> bool:
        """
        验证成绩输入的合法性

        Args:
            daily_score: 平时成绩
            midterm_score: 期中成绩
            final_score: 期末成绩

        Returns:
            bool: 验证通过返回True，否则False
        """
        scores = [daily_score, midterm_score, final_score]

        for score in scores:
            if score is None:
                continue
            
            # 检查类型
            if not isinstance(score, (int, float)):
                logger.error(f"{ErrorMessage.INVALID_SCORE_TYPE}: {score}")
                return False
            
            # 检查范围
            if score < ScoreCalculation.MIN_SCORE or score > ScoreCalculation.MAX_SCORE:
                logger.error(f"{ErrorMessage.INVALID_SCORE_RANGE}: {score}")
                return False

        return True
