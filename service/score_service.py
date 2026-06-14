"""
ScoreService - 成绩业务服务
实现成绩录入、验证、计算等业务逻辑
"""

from dao.score_dao import ScoreDAO
from dao.user_dao import UserDAO
from typing import Optional, Dict, Any, List


class ScoreService:
    """
    成绩业务服务

    职责:
    - 成绩录入（含验证）
    - 成绩计算（总评、绩点）
    - 成绩修改
    - 成绩查询
    - 成绩统计
    """

    def __init__(self):
        """初始化成绩服务"""
        self.score_dao = ScoreDAO()
        self.user_dao = UserDAO()

    def add_score(
        self,
        student_id: int,
        subject_id: int,
        daily_score: Optional[float] = None,
        midterm_score: Optional[float] = None,
        final_score: Optional[float] = None,
        input_by: int = 0
    ) -> Dict[str, Any]:
        """
        成绩录入

        包含验证:
        - 成绩范围 0-100
        - 学生ID存在性
        - 科目ID存在性
        - 自动计算总评成绩和绩点

        Args:
            student_id: 学生ID
            subject_id: 科目ID
            daily_score: 平时成绩（0-100）
            midterm_score: 期中成绩（0-100）
            final_score: 期末成绩（0-100）
            input_by: 录入人ID

        Returns:
            Dict: 操作结果
                - success: bool 是否成功
                - message: str 提示信息
                - data: dict 成绩信息（成功时）
        """
        # 1. 验证成绩范围
        scores = [
            ('平时成绩', daily_score),
            ('期中成绩', midterm_score),
            ('期末成绩', final_score)
        ]

        for name, score in scores:
            if score is not None and (score < 0 or score > 100):
                return {
                    'success': False,
                    'message': f'{name}必须在0-100之间，当前值: {score}',
                    'data': None
                }

        # 2. 验证学生和科目是否存在
        student = self.user_dao.find_by_id(student_id)
        if not student:
            return {
                'success': False,
                'message': f'学生ID {student_id} 不存在',
                'data': None
            }

        # 3. 计算总评成绩（权重: 平时30% + 期中20% + 期末50%）
        total_score = self._calculate_total_score(daily_score, midterm_score, final_score)

        # 4. 计算绩点
        gpa_point = self._calculate_gpa(total_score)

        # 5. 插入数据库
        rows = self.score_dao.insert_score(
            student_id=student_id,
            subject_id=subject_id,
            daily_score=daily_score,
            midterm_score=midterm_score,
            final_score=final_score,
            total_score=total_score,
            gpa_point=gpa_point,
            input_by=input_by
        )

        if rows > 0:
            return {
                'success': True,
                'message': '成绩录入成功',
                'data': {
                    'student_id': student_id,
                    'subject_id': subject_id,
                    'total_score': total_score,
                    'gpa_point': gpa_point
                }
            }
        else:
            return {
                'success': False,
                'message': '成绩录入失败，可能已存在该记录',
                'data': None
            }

    def update_score(
        self,
        score_id: int,
        daily_score: Optional[float] = None,
        midterm_score: Optional[float] = None,
        final_score: Optional[float] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        修改成绩

        Args:
            score_id: 成绩ID
            daily_score: 平时成绩
            midterm_score: 期中成绩
            final_score: 期末成绩
            status: 状态

        Returns:
            Dict: 操作结果
        """
        # 验证成绩范围
        scores = [
            ('平时成绩', daily_score),
            ('期中成绩', midterm_score),
            ('期末成绩', final_score)
        ]

        for name, score in scores:
            if score is not None and (score < 0 or score > 100):
                return {
                    'success': False,
                    'message': f'{name}必须在0-100之间',
                    'data': None
                }

        # 重新计算总评和绩点
        total_score = None
        gpa_point = None

        if any(s is not None for s in [daily_score, midterm_score, final_score]):
            # 获取现有成绩
            existing = self.score_dao.query_by_id(score_id)
            if existing:
                d = daily_score if daily_score is not None else existing.get('daily_score')
                m = midterm_score if midterm_score is not None else existing.get('midterm_score')
                f = final_score if final_score is not None else existing.get('final_score')
                total_score = self._calculate_total_score(d, m, f)
                gpa_point = self._calculate_gpa(total_score)

        rows = self.score_dao.update_score(
            score_id=score_id,
            daily_score=daily_score,
            midterm_score=midterm_score,
            final_score=final_score,
            total_score=total_score,
            gpa_point=gpa_point,
            status=status
        )

        if rows > 0:
            return {
                'success': True,
                'message': '成绩修改成功',
                'data': {'score_id': score_id}
            }
        else:
            return {
                'success': False,
                'message': '成绩修改失败',
                'data': None
            }

    def delete_score(self, score_id: int) -> Dict[str, Any]:
        """
        删除成绩

        Args:
            score_id: 成绩ID

        Returns:
            Dict: 操作结果
        """
        rows = self.score_dao.delete_score(score_id)

        if rows > 0:
            return {
                'success': True,
                'message': '成绩删除成功',
                'data': None
            }
        else:
            return {
                'success': False,
                'message': '成绩删除失败，记录不存在',
                'data': None
            }

    def get_student_scores(self, student_id: int) -> List[Dict[str, Any]]:
        """
        查询学生成绩

        Args:
            student_id: 学生ID

        Returns:
            List[Dict]: 成绩列表
        """
        return self.score_dao.query_by_student(student_id)

    def get_all_scores(self) -> List[Dict[str, Any]]:
        """
        查询所有成绩

        Returns:
            List[Dict]: 成绩列表
        """
        return self.score_dao.query_all()

    def get_subject_statistics(self, subject_id: int) -> Optional[Dict[str, Any]]:
        """
        获取科目统计信息

        Args:
            subject_id: 科目ID

        Returns:
            Dict: 统计信息
        """
        return self.score_dao.get_statistics_by_subject(subject_id)

    @staticmethod
    def _calculate_total_score(
        daily: Optional[float] = None,
        midterm: Optional[float] = None,
        final: Optional[float] = None
    ) -> float:
        """
        计算总评成绩

        权重:
        - 平时成绩: 30%
        - 期中成绩: 20%
        - 期末成绩: 50%

        Args:
            daily: 平时成绩
            midterm: 期中成绩
            final: 期末成绩

        Returns:
            float: 总评成绩
        """
        d = daily or 0
        m = midterm or 0
        f = final or 0

        # 如果某项未录入，权重重新分配
        weights = []
        values = []

        if daily is not None:
            weights.append(0.3)
            values.append(d)
        if midterm is not None:
            weights.append(0.2)
            values.append(m)
        if final is not None:
            weights.append(0.5)
            values.append(f)

        if not weights:
            return 0.0

        # 归一化权重
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]

        total = sum(v * w for v, w in zip(values, normalized_weights))
        return round(total, 2)

    @staticmethod
    def _calculate_gpa(total_score: float) -> float:
        """
        根据总评成绩计算绩点

        绩点换算表:
        - 90-100: 4.0
        - 85-89: 3.7
        - 82-84: 3.3
        - 78-81: 3.0
        - 75-77: 2.7
        - 72-74: 2.3
        - 68-71: 2.0
        - 64-67: 1.5
        - 60-63: 1.0
        - <60: 0.0

        Args:
            total_score: 总评成绩

        Returns:
            float: 绩点
        """
        if total_score >= 90:
            return 4.0
        elif total_score >= 85:
            return 3.7
        elif total_score >= 82:
            return 3.3
        elif total_score >= 78:
            return 3.0
        elif total_score >= 75:
            return 2.7
        elif total_score >= 72:
            return 2.3
        elif total_score >= 68:
            return 2.0
        elif total_score >= 64:
            return 1.5
        elif total_score >= 60:
            return 1.0
        else:
            return 0.0
